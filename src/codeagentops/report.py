from __future__ import annotations

import json
from pathlib import Path

from codeagentops.models import TaskRunResult


def _fmt_money(value: float) -> str:
    return f"${value:.6f}"


def generate_markdown_report(results: list[TaskRunResult], output_path: Path) -> Path:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    total_tasks = len(results)
    successes = sum(r.success for r in results)
    first_attempt = sum(r.first_attempt_success for r in results)
    total_cost = sum(r.usage.estimated_cost_usd for r in results)
    successful_cost = sum(r.usage.estimated_cost_usd for r in results if r.success)
    cost_per_success = successful_cost / max(successes, 1)

    lines: list[str] = []
    lines.append("# CodeAgentOps Run Report")
    lines.append("")
    lines.append("## Summary")
    lines.append("")
    lines.append(f"- Tasks: **{total_tasks}**")
    lines.append(f"- Final success rate: **{successes}/{total_tasks}**")
    lines.append(f"- First-attempt success rate: **{first_attempt}/{total_tasks}**")
    lines.append(f"- Estimated total cost: **{_fmt_money(total_cost)}**")
    lines.append(f"- Estimated cost per successful task: **{_fmt_money(cost_per_success)}**")
    lines.append("")

    lines.append("## Task Results")
    lines.append("")
    lines.append("| Task | Success | Public | Hidden | Iterations | API calls | E2E latency | LLM latency | Pytest runtime | Tokens | Cost | Failure modes |")
    lines.append("|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|")
    for r in results:
        lines.append(
            f"| {r.task_name} | {r.success} | {r.public_passed} | {r.hidden_passed} | "
            f"{r.iterations_to_success or '-'} | {r.api_calls} | {r.end_to_end_latency_s:.2f}s | "
            f"{r.total_llm_latency_s:.2f}s | {r.total_pytest_runtime_s:.2f}s | {r.usage.total_tokens} | "
            f"{_fmt_money(r.usage.estimated_cost_usd)} | {', '.join(r.failure_modes) or '-'} |"
        )
    lines.append("")

    lines.append("## Observability Metrics")
    lines.append("")
    for r in results:
        lines.append(f"### {r.task_name}")
        lines.append("")
        lines.append(f"- Retry amplification: **{r.retry_amplification:.2f}x**")
        lines.append(f"- Tool/runtime overhead ratio: **{r.tool_overhead_ratio:.2%}**")
        lines.append(f"- Patch churn: **{r.patch_stats.patch_churn}** lines changed across iterations")
        lines.append(f"- Final patch size: **{r.patch_stats.final_patch_size}** lines")
        lines.append(f"- Churn-to-final ratio: **{r.patch_stats.churn_to_final_ratio:.2f}**")
        lines.append(f"- Files changed: **{', '.join(r.patch_stats.modified_files) or '-'}**")
        lines.append("")
        lines.append("| Iter | Public pass | LLM latency | Prompt tok | Completion tok | Output tok/s | Patch apply | Pytest | Context chars | Failure |")
        lines.append("|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|")
        for it in r.iterations:
            lines.append(
                f"| {it.iteration} | {it.public_tests_passed} | {it.llm_latency_s:.2f}s | {it.prompt_tokens} | "
                f"{it.completion_tokens} | {it.output_tokens_per_s:.2f} | {it.patch_apply_time_s:.3f}s | "
                f"{it.pytest_runtime_s:.2f}s | {it.context_chars} | {it.failure_mode or '-'} |"
            )
        lines.append("")

    output_path.write_text("\n".join(lines), encoding="utf-8")
    json_path = output_path.with_suffix(".json")
    json_path.write_text(json.dumps([r.to_dict() for r in results], indent=2), encoding="utf-8")
    return output_path
