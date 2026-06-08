from __future__ import annotations

import difflib
import re
import time
from dataclasses import dataclass
from pathlib import Path

from codeagentops.models import PatchStats


@dataclass
class PatchApplyResult:
    ok: bool
    message: str
    apply_time_s: float
    patch_stats: PatchStats


_CODE_BLOCK_RE = re.compile(r"```(?:python|py|text)?\s*(.*?)```", re.DOTALL | re.IGNORECASE)
_FILE_HEADER_RE = re.compile(r"^###\s+FILE:\s*(?P<path>.+?)\s*$", re.MULTILINE)


def extract_file_updates(llm_text: str) -> dict[str, str]:
    """Extract file updates from a strict but easy LLM format.

    Expected format:
        ### FILE: calculator.py
        ```python
        ... full file content ...
        ```

    Multiple file blocks are allowed. For MVP, full-file replacement is much
    simpler and more reliable than arbitrary unified diff application.
    """
    updates: dict[str, str] = {}
    matches = list(_FILE_HEADER_RE.finditer(llm_text))
    for i, match in enumerate(matches):
        path = match.group("path").strip()
        start = match.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(llm_text)
        block = llm_text[start:end].strip()
        code_match = _CODE_BLOCK_RE.search(block)
        content = code_match.group(1) if code_match else block
        updates[path] = content.strip() + "\n"
    return updates


def _safe_target(root: Path, relative_path: str) -> Path:
    target = (root / relative_path).resolve()
    root_resolved = root.resolve()
    if root_resolved not in target.parents and target != root_resolved:
        raise ValueError(f"Unsafe path outside workspace: {relative_path}")
    return target


def apply_file_updates(workspace: Path, llm_text: str, forbidden_paths: list[str]) -> PatchApplyResult:
    start = time.perf_counter()
    stats = PatchStats()
    try:
        updates = extract_file_updates(llm_text)
        if not updates:
            return PatchApplyResult(False, "No file updates found in LLM response.", time.perf_counter() - start, stats)

        for rel_path, new_content in updates.items():
            if any(rel_path.startswith(prefix.rstrip("/") + "/") or rel_path == prefix.rstrip("/") for prefix in forbidden_paths):
                stats.forbidden_file_edits.append(rel_path)
                continue

            target = _safe_target(workspace, rel_path)
            target.parent.mkdir(parents=True, exist_ok=True)
            old_content = target.read_text(encoding="utf-8") if target.exists() else ""
            diff = list(difflib.unified_diff(
                old_content.splitlines(),
                new_content.splitlines(),
                fromfile=f"a/{rel_path}",
                tofile=f"b/{rel_path}",
                lineterm="",
            ))
            added = sum(1 for line in diff if line.startswith("+") and not line.startswith("+++"))
            deleted = sum(1 for line in diff if line.startswith("-") and not line.startswith("---"))
            if old_content != new_content:
                target.write_text(new_content, encoding="utf-8")
                stats.modified_files.append(rel_path)
                stats.files_changed += 1
                stats.lines_added += added
                stats.lines_deleted += deleted
                stats.patch_churn += added + deleted
                stats.final_patch_size += len(new_content.splitlines())

        if stats.forbidden_file_edits:
            return PatchApplyResult(False, f"Forbidden file edits: {stats.forbidden_file_edits}", time.perf_counter() - start, stats)
        if not stats.modified_files:
            return PatchApplyResult(False, "No code change was applied.", time.perf_counter() - start, stats)
        stats.churn_to_final_ratio = stats.patch_churn / max(stats.final_patch_size, 1)
        return PatchApplyResult(True, "Patch applied.", time.perf_counter() - start, stats)
    except Exception as exc:
        return PatchApplyResult(False, f"Invalid patch/update: {exc}", time.perf_counter() - start, stats)
