from __future__ import annotations

from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any


@dataclass
class TaskSpec:
    name: str
    path: Path
    prompt: str
    entrypoint: str
    public_tests_dir: Path
    hidden_tests_dir: Path
    forbidden_paths: list[str] = field(default_factory=lambda: ["public_tests", "hidden_tests"])


@dataclass
class LLMUsage:
    prompt_tokens: int = 0
    completion_tokens: int = 0
    total_tokens: int = 0
    estimated_cost_usd: float = 0.0


@dataclass
class LLMResult:
    content: str
    latency_s: float
    usage: LLMUsage
    model: str


@dataclass
class TestResult:
    passed: bool
    exit_code: int
    runtime_s: float
    stdout: str
    stderr: str
    failure_mode: str | None = None


@dataclass
class PatchStats:
    files_changed: int = 0
    lines_added: int = 0
    lines_deleted: int = 0
    final_patch_size: int = 0
    patch_churn: int = 0
    churn_to_final_ratio: float = 0.0
    modified_files: list[str] = field(default_factory=list)
    forbidden_file_edits: list[str] = field(default_factory=list)


@dataclass
class IterationTrace:
    iteration: int
    llm_latency_s: float
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int
    output_tokens_per_s: float
    estimated_cost_usd: float
    patch_apply_time_s: float
    pytest_runtime_s: float
    public_tests_passed: bool
    failure_mode: str | None
    context_chars: int
    modified_files: list[str]
    lines_added: int
    lines_deleted: int


@dataclass
class TaskRunResult:
    task_name: str
    success: bool
    public_passed: bool
    hidden_passed: bool
    first_attempt_success: bool
    iterations_to_success: int | None
    api_calls: int
    retry_amplification: float
    end_to_end_latency_s: float
    total_llm_latency_s: float
    total_pytest_runtime_s: float
    tool_overhead_ratio: float
    usage: LLMUsage
    patch_stats: PatchStats
    failure_modes: list[str]
    iterations: list[IterationTrace]
    run_dir: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)
