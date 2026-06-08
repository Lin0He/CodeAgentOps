from __future__ import annotations

import os
import subprocess
import time
import shutil
from dataclasses import dataclass
from pathlib import Path


@dataclass
class PytestResult:
    passed: bool
    exit_code: int
    runtime_s: float
    stdout: str
    stderr: str
    failure_mode: str | None = None


def copy_tests_into_workspace(
    source_tests_dir: Path,
    workspace: Path,
    target_name: str,
) -> Path:
    """
    Copy public or hidden tests into the isolated task workspace.

    Example:
        examples/tasks/foo/public_tests
        -> runs/foo/<timestamp>/workspace/public_tests
    """
    source_tests_dir = source_tests_dir.resolve()
    workspace = workspace.resolve()
    target_dir = workspace / target_name

    if target_dir.exists():
        shutil.rmtree(target_dir)

    shutil.copytree(source_tests_dir, target_dir)
    return target_dir


def classify_pytest_failure(
    stdout: str,
    stderr: str,
    timed_out: bool = False,
) -> str:
    output = f"{stdout}\n{stderr}"

    if timed_out:
        return "timeout"

    if "SyntaxError" in output:
        return "syntax_error"

    if (
        "ModuleNotFoundError" in output
        or "ImportError" in output
        or "NameError" in output
        or "TypeError" in output
        or "AttributeError" in output
    ):
        return "runtime_error"

    if (
        "FAILED" in output
        or "AssertionError" in output
        or "E       assert" in output
        or "assert " in output
    ):
        return "test_failure"

    return "runtime_error"


def run_pytest(
    workspace: Path,
    tests_path: Path,
    timeout_s: int = 20,
) -> PytestResult:
    workspace = workspace.resolve()
    tests_path = tests_path.resolve()

    if not tests_path.exists():
        return PytestResult(
            passed=False,
            exit_code=1,
            runtime_s=0.0,
            stdout="",
            stderr=f"Tests path does not exist: {tests_path}",
            failure_mode="runtime_error",
        )

    # Important:
    # Run pytest from inside the task workspace so imports like
    # `from calculator import add` resolve against workspace/calculator.py.
    try:
        relative_tests_path = tests_path.relative_to(workspace)
    except ValueError:
        relative_tests_path = tests_path

    env = os.environ.copy()
    existing_pythonpath = env.get("PYTHONPATH", "")
    env["PYTHONPATH"] = (
        str(workspace)
        if not existing_pythonpath
        else f"{workspace}{os.pathsep}{existing_pythonpath}"
    )

    start = time.perf_counter()

    try:
        completed = subprocess.run(
            [
                "python",
                "-m",
                "pytest",
                str(relative_tests_path),
                "-q",
                "-vv",
            ],
            cwd=str(workspace),
            env=env,
            capture_output=True,
            text=True,
            timeout=timeout_s,
        )
        runtime_s = time.perf_counter() - start

        passed = completed.returncode == 0
        failure_mode = None
        if not passed:
            failure_mode = classify_pytest_failure(
                completed.stdout,
                completed.stderr,
                timed_out=False,
            )

        return PytestResult(
            passed=passed,
            exit_code=completed.returncode,
            runtime_s=runtime_s,
            stdout=completed.stdout,
            stderr=completed.stderr,
            failure_mode=failure_mode,
        )

    except subprocess.TimeoutExpired as exc:
        runtime_s = time.perf_counter() - start
        stdout = exc.stdout or ""
        stderr = exc.stderr or ""

        return PytestResult(
            passed=False,
            exit_code=124,
            runtime_s=runtime_s,
            stdout=stdout,
            stderr=stderr,
            failure_mode="timeout",
        )
