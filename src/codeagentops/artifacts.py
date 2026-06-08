from __future__ import annotations

import json
from pathlib import Path


def write_json(path: Path, data: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")


def write_text_artifact(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def write_iteration_messages(
    run_dir: Path,
    iteration: int,
    messages: list[dict[str, str]],
) -> None:
    write_json(run_dir / f"iteration_{iteration}_messages.json", messages)


def write_llm_response(
    run_dir: Path,
    iteration: int,
    content: str,
) -> None:
    write_text_artifact(run_dir / f"iteration_{iteration}_llm_response.txt", content)


def write_pytest_output(
    run_dir: Path,
    name: str,
    stdout: str,
    stderr: str,
) -> None:
    write_text_artifact(
        run_dir / f"{name}_pytest_output.txt",
        f"STDOUT:\n{stdout}\n\nSTDERR:\n{stderr}",
    )


def write_trace(
    run_dir: Path,
    result_dict: dict,
) -> None:
    write_json(run_dir / "trace.json", result_dict)
