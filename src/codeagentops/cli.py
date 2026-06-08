from __future__ import annotations

from pathlib import Path

import click

from codeagentops.config import RunConfig, load_settings
from codeagentops.report import generate_markdown_report
from codeagentops.runner import run_task
from codeagentops.workspace import list_tasks, load_task


@click.group()
def main() -> None:
    """CodeAgentOps: eval + observability for autonomous coding agents."""


@main.command("list-tasks")
@click.option("--tasks-dir", type=click.Path(path_type=Path), default=Path("examples/tasks"))
def list_tasks_cmd(tasks_dir: Path) -> None:
    for task_path in list_tasks(tasks_dir):
        click.echo(task_path.name)


@main.command("run")
@click.option("--task", "task_name", type=str, default=None, help="Task folder name. Omit to run all tasks.")
@click.option("--tasks-dir", type=click.Path(path_type=Path), default=Path("examples/tasks"))
@click.option("--runs-dir", type=click.Path(path_type=Path), default=Path("runs"))
@click.option("--max-iterations", type=int, default=3)
@click.option("--pytest-timeout-s", type=float, default=20.0)
@click.option("--report-path", type=click.Path(path_type=Path), default=Path("runs/report.md"))
def run_cmd(task_name: str | None, tasks_dir: Path, runs_dir: Path, max_iterations: int, pytest_timeout_s: float, report_path: Path) -> None:
    settings = load_settings()
    config = RunConfig(tasks_dir=tasks_dir, runs_dir=runs_dir, max_iterations=max_iterations, pytest_timeout_s=pytest_timeout_s)
    task_paths = list_tasks(tasks_dir)
    if task_name:
        task_paths = [p for p in task_paths if p.name == task_name]
        if not task_paths:
            raise click.ClickException(f"Task not found: {task_name}")

    results = []
    for task_path in task_paths:
        task = load_task(task_path)
        click.echo(f"Running task: {task.name}")
        result = run_task(task, config, settings)
        results.append(result)
        click.echo(f"  success={result.success} public={result.public_passed} hidden={result.hidden_passed} iterations={result.iterations_to_success}")

    report = generate_markdown_report(results, report_path)
    click.echo(f"Report written to: {report}")


if __name__ == "__main__":
    main()
