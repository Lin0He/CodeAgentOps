from __future__ import annotations

import time
from pathlib import Path

from codeagentops.config import RunConfig, Settings
from codeagentops.evaluators.pytest_runner import copy_tests_into_workspace, run_pytest
from codeagentops.metrics import add_usage, merge_patch_stats
from codeagentops.models import IterationTrace, LLMUsage, PatchStats, TaskRunResult, TaskSpec
from codeagentops.patching.apply_patch import apply_file_updates
from codeagentops.providers.deepseek import DeepSeekProvider
from codeagentops.workspace import create_workspace, read_workspace_files
from codeagentops.artifacts import (
    write_iteration_messages,
    write_llm_response,
    write_pytest_output,
    write_trace,
)


SYSTEM_PROMPT = """You are a coding repair agent.
Return only full-file updates using this exact format:

### FILE: relative/path.py
```python
# full file content here
```

Rules:
- Modify only source files in the workspace.
- Do not modify tests.
- Prefer the smallest correct change.
- Preserve existing behavior unless the task explicitly asks for a change.
"""


def build_messages( task: TaskSpec,
                    workspace_text: str,
                    previous_feedback: str | None) -> list[dict[str, str]]:
    feedback_block = f"\nPrevious test feedback:\n```text\n{previous_feedback}\n```\n" if previous_feedback else ""
    user_prompt = f"""
        Task:
        {task.prompt}

        Current workspace files:
        {workspace_text}
        {feedback_block}
        Return the full updated source file(s) only.
    """.strip()
    return [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_prompt},
    ]


def classify_patch_failure(message: str) -> str:
    lowered = message.lower()
    if "forbidden" in lowered:
        return "modified_forbidden_file"
    if "no file updates" in lowered or "no code change" in lowered:
        return "no_code_change"
    return "invalid_patch"


def run_task(task: TaskSpec, run_config: RunConfig, settings: Settings) -> TaskRunResult:
    provider = DeepSeekProvider(settings)
    workspace = create_workspace(task, run_config.runs_dir)
    task_run_dir = workspace.parent
    start_task = time.perf_counter()

    total_usage = LLMUsage()
    total_patch_stats = PatchStats()
    traces: list[IterationTrace] = []
    failure_modes: list[str] = []
    previous_feedback: str | None = None
    public_passed = False
    hidden_passed = False
    iterations_to_success: int | None = None
    total_llm_latency = 0.0
    total_pytest_runtime = 0.0

    public_tests_path = copy_tests_into_workspace(task.public_tests_dir, workspace, "public_tests")

    for iteration in range(1, run_config.max_iterations + 1):
        workspace_text = read_workspace_files(workspace)
        messages = build_messages(task, workspace_text, previous_feedback)
        context_chars = sum(len(m["content"]) for m in messages)
        write_iteration_messages(task_run_dir, iteration, messages)

        try:
            llm_result = provider.complete(messages)
        except Exception as exc:
            failure_modes.append("runtime_error")
            previous_feedback = f"LLM provider error: {exc}"
            break

        write_llm_response(task_run_dir, iteration, llm_result.content)

        total_llm_latency += llm_result.latency_s
        total_usage = add_usage(total_usage, llm_result.usage)
        output_tps = llm_result.usage.completion_tokens / llm_result.latency_s if llm_result.latency_s > 0 else 0.0

        patch_result = apply_file_updates(workspace, llm_result.content, task.forbidden_paths)
        total_patch_stats = merge_patch_stats(total_patch_stats, patch_result.patch_stats)

        if not patch_result.ok:
            failure_mode = classify_patch_failure(patch_result.message)
            failure_modes.append(failure_mode)
            traces.append(IterationTrace(
                iteration=iteration,
                llm_latency_s=llm_result.latency_s,
                prompt_tokens=llm_result.usage.prompt_tokens,
                completion_tokens=llm_result.usage.completion_tokens,
                total_tokens=llm_result.usage.total_tokens,
                output_tokens_per_s=output_tps,
                estimated_cost_usd=llm_result.usage.estimated_cost_usd,
                patch_apply_time_s=patch_result.apply_time_s,
                pytest_runtime_s=0.0,
                public_tests_passed=False,
                failure_mode=failure_mode,
                context_chars=context_chars,
                modified_files=patch_result.patch_stats.modified_files,
                lines_added=patch_result.patch_stats.lines_added,
                lines_deleted=patch_result.patch_stats.lines_deleted,
            ))
            previous_feedback = patch_result.message
            continue

        public_result = run_pytest(workspace, public_tests_path, run_config.pytest_timeout_s)
        write_pytest_output(
            task_run_dir,
            f"iteration_{iteration}_public",
            public_result.stdout,
            public_result.stderr,
        )

        total_pytest_runtime += public_result.runtime_s
        public_passed = public_result.passed
        failure_mode = None if public_result.passed else public_result.failure_mode
        if failure_mode:
            failure_modes.append(failure_mode)

        traces.append(IterationTrace(
            iteration=iteration,
            llm_latency_s=llm_result.latency_s,
            prompt_tokens=llm_result.usage.prompt_tokens,
            completion_tokens=llm_result.usage.completion_tokens,
            total_tokens=llm_result.usage.total_tokens,
            output_tokens_per_s=output_tps,
            estimated_cost_usd=llm_result.usage.estimated_cost_usd,
            patch_apply_time_s=patch_result.apply_time_s,
            pytest_runtime_s=public_result.runtime_s,
            public_tests_passed=public_result.passed,
            failure_mode=failure_mode,
            context_chars=context_chars,
            modified_files=patch_result.patch_stats.modified_files,
            lines_added=patch_result.patch_stats.lines_added,
            lines_deleted=patch_result.patch_stats.lines_deleted,
        ))

        if public_result.passed:
            iterations_to_success = iteration
            break

        previous_feedback = f"pytest stdout:\n{public_result.stdout}\n\npytest stderr:\n{public_result.stderr}"

    if public_passed:
        hidden_tests_path = copy_tests_into_workspace(task.hidden_tests_dir, workspace, "hidden_tests")
        hidden_result = run_pytest(workspace, hidden_tests_path, run_config.pytest_timeout_s)
        total_pytest_runtime += hidden_result.runtime_s
        hidden_passed = hidden_result.passed
        if not hidden_passed:
            failure_modes.append("hidden_test_failure")
            write_pytest_output(
                task_run_dir,
                "final_hidden",
                hidden_result.stdout,
                hidden_result.stderr,
            )
    else:
        failure_modes.append("max_iterations_reached")

    end_to_end = time.perf_counter() - start_task
    tool_time = max(end_to_end - total_llm_latency, 0.0)
    retry_amplification = len(traces) / max(iterations_to_success or 1, 1)
    result = TaskRunResult(
        task_name=task.name,
        success=public_passed and hidden_passed,
        public_passed=public_passed,
        hidden_passed=hidden_passed,
        first_attempt_success=public_passed and hidden_passed and iterations_to_success == 1,
        iterations_to_success=iterations_to_success,
        api_calls=len(traces),
        retry_amplification=retry_amplification,
        end_to_end_latency_s=end_to_end,
        total_llm_latency_s=total_llm_latency,
        total_pytest_runtime_s=total_pytest_runtime,
        tool_overhead_ratio=tool_time / end_to_end if end_to_end > 0 else 0.0,
        usage=total_usage,
        patch_stats=total_patch_stats,
        failure_modes=sorted(set(failure_modes)),
        iterations=traces,
        run_dir=str(task_run_dir),
    )
    write_trace(task_run_dir, result.to_dict())
    return result
