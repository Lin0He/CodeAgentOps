from __future__ import annotations

from codeagentops.models import LLMUsage, PatchStats


def add_usage(a: LLMUsage, b: LLMUsage) -> LLMUsage:
    return LLMUsage(
        prompt_tokens=a.prompt_tokens + b.prompt_tokens,
        completion_tokens=a.completion_tokens + b.completion_tokens,
        total_tokens=a.total_tokens + b.total_tokens,
        estimated_cost_usd=a.estimated_cost_usd + b.estimated_cost_usd,
    )


def merge_patch_stats(total: PatchStats, current: PatchStats) -> PatchStats:
    total.files_changed += current.files_changed
    total.lines_added += current.lines_added
    total.lines_deleted += current.lines_deleted
    total.final_patch_size = current.final_patch_size or total.final_patch_size
    total.patch_churn += current.patch_churn
    total.modified_files.extend(current.modified_files)
    total.forbidden_file_edits.extend(current.forbidden_file_edits)
    total.churn_to_final_ratio = total.patch_churn / max(total.final_patch_size, 1)
    # Stable unique file list for readability.
    total.modified_files = sorted(set(total.modified_files))
    total.forbidden_file_edits = sorted(set(total.forbidden_file_edits))
    return total
