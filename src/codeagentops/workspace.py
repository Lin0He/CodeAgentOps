from __future__ import annotations

import shutil
import time
from pathlib import Path

import yaml

from codeagentops.models import TaskSpec


def load_task(task_path: Path) -> TaskSpec:
    meta_path = task_path / "metadata.yaml"
    metadata = yaml.safe_load(meta_path.read_text(encoding="utf-8")) if meta_path.exists() else {}
    return TaskSpec(
        name=metadata.get("name", task_path.name),
        path=task_path,
        prompt=(task_path / "prompt.md").read_text(encoding="utf-8"),
        entrypoint=metadata.get("entrypoint", "main.py"),
        public_tests_dir=task_path / "public_tests",
        hidden_tests_dir=task_path / "hidden_tests",
        forbidden_paths=metadata.get("forbidden_paths", ["public_tests", "hidden_tests"]),
    )


def list_tasks(tasks_dir: Path) -> list[Path]:
    return sorted([p for p in tasks_dir.iterdir() if p.is_dir() and (p / "prompt.md").exists()])


def create_workspace(task: TaskSpec, run_root: Path) -> Path:
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    workspace = run_root / task.name / timestamp / "workspace"
    workspace.parent.mkdir(parents=True, exist_ok=True)
    shutil.copytree(task.path / "starter", workspace)
    return workspace


def read_workspace_files(workspace: Path, max_chars_per_file: int = 16_000) -> str:
    chunks: list[str] = []
    for path in sorted(workspace.rglob("*.py")):
        rel = path.relative_to(workspace)
        if any(part in {".venv", "__pycache__", ".pytest_cache"} for part in rel.parts):
            continue
        text = path.read_text(encoding="utf-8")
        if len(text) > max_chars_per_file:
            text = text[:max_chars_per_file] + "\n# ... truncated ...\n"
        chunks.append(f"### FILE: {rel}\n```python\n{text}\n```")
    return "\n\n".join(chunks)
