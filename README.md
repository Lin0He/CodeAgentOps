# CodeAgentOps

**Evaluation and observability for autonomous coding agents as production systems.**

CodeAgentOps is a lightweight Python MVP for evaluating autonomous coding agents beyond final test pass rate. It treats a coding agent as a production system and records not only whether the generated code eventually passes tests, but also how the agent behaved during the repair process: latency, token usage, estimated cost, retry behavior, context growth, patch churn, tool overhead, public-vs-hidden test behavior, and failure modes.

The current version uses a DeepSeek-backed single-agent repair loop. It reads a task prompt and starter code, asks the model to generate full-file updates, applies the update in an isolated workspace, runs public pytest tests during repair, runs hidden tests for final scoring, and generates markdown/JSON evaluation reports.

This project is intentionally small and engineering-focused. It is not trying to be a full coding-agent framework. The goal is to build a clean, runnable evaluation harness that can be extended toward more advanced autonomous coding-system evaluation.

---

## Why this project exists

Most coding-agent demos answer only one question:

> Did the final generated code pass the tests?

That is not enough for production-oriented autonomous coding systems.

In real systems, we also care about:

* How many attempts did the agent need?
* Did the agent pass hidden tests or only visible public tests?
* How much latency did the repair loop add?
* How much did the run cost?
* Did retries amplify token usage and cost?
* Did the agent make a small targeted fix or rewrite the whole file?
* Did the agent modify forbidden files such as tests?
* Did the failure come from the model, the patch protocol, the test runner, the workspace, or the execution environment?
* Can we inspect the raw LLM response and pytest output after the run?

CodeAgentOps is built around this production-systems view of coding-agent evaluation.

---

## Current status

The current v0.4 benchmark contains seven small Python tasks. In the latest sample run, the DeepSeek-backed single-agent repair loop solved all seven tasks on the first attempt.

| Metric                             |     Value |
| ---------------------------------- | --------: |
| Tasks                              |         7 |
| Final success rate                 |       7/7 |
| First-attempt success rate         |       7/7 |
| Estimated total cost               | $0.002768 |
| Estimated cost per successful task | $0.000395 |

This confirms that the harness is stable end to end:

* DeepSeek API calls work.
* Full-file update parsing works.
* Isolated workspace execution works.
* Public pytest evaluation works.
* Hidden pytest evaluation works.
* Metrics collection works.
* Markdown report generation works.

However, the benchmark is currently still under-calibrated for deeper coding-agent evaluation. Since all tasks passed on the first attempt, this run did not expose retry amplification, repair-after-failure behavior, public-vs-hidden test gaps, or failure-mode diversity.

The current version should therefore be interpreted as a stable low-cost baseline, not as a complete benchmark of coding-agent capability.

---

## In scope

CodeAgentOps currently focuses on:

* Single-agent coding repair loops.
* Python coding tasks.
* DeepSeek API as the real LLM provider.
* Public tests as visible repair feedback.
* Hidden tests as final scoring.
* Full-file update protocol instead of arbitrary diffs.
* Isolated task workspaces.
* Pytest-based evaluation.
* Per-task and per-iteration metrics.
* Markdown and JSON reports.
* Raw trace artifacts such as LLM responses and pytest outputs.
* Small production-oriented benchmark tasks.

---

## Out of scope

The current MVP intentionally does not include:

* Multi-agent orchestration.
* Planner/executor/reviewer agent roles.
* Multi-provider comparison.
* Browser UI or dashboard.
* Distributed execution.
* Sandboxed container security.
* Large SWE-bench-style repositories.
* Long-context repository-level tasks.
* Real-time tracing backend.
* Human-in-the-loop review UI.
* Complex patch formats such as arbitrary unified diffs.
* Automatic benchmark leaderboard generation.

These are useful future extensions, but they are intentionally excluded from the MVP to keep the project runnable and easy to inspect.

---

## How the agent workflow works

The current workflow is a simple repair loop:

```text
Load task prompt and starter code
        ↓
Create isolated workspace under runs/
        ↓
Copy public tests into workspace
        ↓
Read current workspace files
        ↓
Build DeepSeek prompt
        ↓
Call DeepSeek API
        ↓
Parse full-file update
        ↓
Apply update to workspace
        ↓
Run public pytest tests
        ↓
If public tests fail:
    feed pytest output back to agent
    retry up to max_iterations
        ↓
If public tests pass:
    copy and run hidden tests
        ↓
Collect metrics and artifacts
        ↓
Generate markdown and JSON reports
```

The agent sees the task prompt, the current source files, and previous public pytest feedback. It does not see hidden tests. Hidden tests are only used for final scoring.

---

## Evaluation design

CodeAgentOps separates visible repair feedback from final scoring.

### Public tests

Public tests are copied into the workspace before the repair loop starts. They are used after each model-generated patch. If public tests fail, the pytest output is sent back to the model in the next iteration.

This simulates a coding-agent workflow where the agent can observe local test failures and repair the code.

### Hidden tests

Hidden tests are copied into the workspace only after public tests pass or the repair loop ends. Hidden tests are not sent back to the model.

This allows the harness to detect cases where an agent passes visible tests but fails hidden requirements.

### Full-file update protocol

The model is asked to return complete file updates using this format:

````text
### FILE: relative/path.py
```python
# full updated file content
````

````

The MVP uses full-file updates instead of arbitrary diffs because they are simpler to parse, easier to debug, and more reliable for a one-day MVP.

### Forbidden file edits

Tasks can define forbidden paths such as:

```yaml
forbidden_paths:
  - public_tests/
  - hidden_tests/
````

If the model attempts to modify tests or other forbidden files, the run records a `modified_forbidden_file` failure mode.

---

## Metrics collected

### Correctness

* public test pass
* hidden test pass
* final success
* first-attempt success
* regression preservation

### Agent loop behavior

* iterations to success
* API calls per task
* retry amplification
* repair success after initial failure

### Latency

* end-to-end task latency
* per-iteration LLM latency
* patch apply time
* pytest runtime
* tool/runtime overhead ratio

### Tokens and cost

* prompt tokens
* completion tokens
* total tokens
* estimated cost
* cost per task
* cost per successful task
* output tokens per second

### Context growth

* context size per iteration
* prompt growth after feedback injection

### Patch stability

* files changed
* lines added
* lines deleted
* patch churn
* final patch size
* churn-to-final ratio
* forbidden file edits

### Failure modes

* `syntax_error`
* `test_failure`
* `hidden_test_failure`
* `invalid_patch`
* `timeout`
* `no_code_change`
* `modified_forbidden_file`
* `max_iterations_reached`
* `runtime_error`

---

## Benchmark tasks

The current benchmark contains seven small Python tasks. They are intentionally compact so the full benchmark can run quickly, but each task targets a different class of production-relevant coding behavior.

### 1. `fix_calculator_bug`

**Focus:** baseline bug fixing and regression preservation.

The agent receives a small calculator module with basic arithmetic utilities. The task checks whether the model can make a minimal fix while preserving existing behavior.

Why it is useful:

* Establishes a simple baseline.
* Tests whether the full-file update protocol works.
* Verifies that public and hidden tests can both run inside the workspace.
* Produces a low-complexity reference point for latency and cost.

---

### 2. `implement_slugify`

**Focus:** text normalization and edge-case handling.

The agent implements a `slugify` utility. This task is simple but tends to produce larger file rewrites because the model often implements normalization, separator handling, lowercase conversion, and cleanup logic together.

Why it is useful:

* Tests feature implementation rather than pure bug fixing.
* Creates measurable patch churn.
* Checks whether hidden tests catch edge cases.
* Helps distinguish localized repair from broader rewrite-style implementation.

In the v0.4 sample run, this task had a high churn-to-final ratio, suggesting that the model rewrote most of the final solution rather than making a tiny targeted edit.

---

### 3. `fix_lru_cache`

**Focus:** stateful behavior.

The agent fixes an LRU cache implementation. This task tests whether the model can reason about mutable state, cache capacity, and access-order updates.

Why it is useful:

* Tests stateful logic.
* Represents a common production systems component.
* Checks whether the model can preserve existing cache behavior while fixing eviction semantics.
* Produces a contrast with broader implementation tasks because the patch can be more localized.

In the v0.4 sample run, this task had a relatively low churn-to-final ratio, suggesting a more targeted repair.

---

### 4. `parse_duration`

**Focus:** config/time parsing.

The agent implements a compact duration parser such as:

```text
45s     -> 45
2m10s   -> 130
1h30m   -> 5400
```

Why it is useful:

* Production systems often parse timeout, retry, cache, and scheduling configs.
* Tests string parsing.
* Tests invalid input handling.
* Provides hidden-test opportunities around empty strings, missing units, zero components, and invalid formats.

---

### 5. `detect_anomaly_window`

**Focus:** monitoring-style rolling window logic.

The agent implements a function that returns the first rolling window whose average is strictly above a threshold.

Why it is useful:

* Connects the benchmark to monitoring and ML systems evaluation.
* Tests boundary conditions such as window size larger than input.
* Tests strict threshold behavior.
* Represents a small but realistic observability/data-quality utility.

---

### 6. `aggregate_eval_results`

**Focus:** evaluation metrics aggregation.

The agent implements an aggregation function over task-level evaluation records. It computes success count, pass rates, average iterations, total cost, and average latency.

Why it is useful:

* Directly relates to the CodeAgentOps project itself.
* Tests missing-field handling.
* Tests metric aggregation correctness.
* Represents the type of logic needed in evaluation dashboards or benchmark reports.

In the v0.4 sample run, this task used the most tokens and had the highest estimated cost, making it a useful task for comparing cost and prompt complexity.

---

### 7. `retry_policy`

**Focus:** API reliability logic.

The agent implements retry helpers for transient and permanent error types, including exponential backoff with a cap.

Why it is useful:

* Production LLM systems need retry and backoff behavior.
* Tests edge cases such as max attempts, unknown errors, invalid attempts, and capped backoff.
* Connects directly to real agent infrastructure concerns such as rate limits, timeouts, and server errors.

---

## Example v0.4 report summary

The latest v0.4 sample run produced:

| Task                   | Success | Public | Hidden | Iterations |      Cost |
| ---------------------- | ------: | -----: | -----: | ---------: | --------: |
| Aggregate Eval Results |    True |   True |   True |          1 | $0.000640 |
| Detect Anomaly Window  |    True |   True |   True |          1 | $0.000277 |
| fix_calculator_bug     |    True |   True |   True |          1 | $0.000343 |
| fix_lru_cache          |    True |   True |   True |          1 | $0.000331 |
| implement_slugify      |    True |   True |   True |          1 | $0.000384 |
| Parse Duration         |    True |   True |   True |          1 | $0.000389 |
| Retry Policy           |    True |   True |   True |          1 | $0.000405 |

Full report:

```text
examples/reports/v0_4_report.md
```

---

## Initial observations from v0.4

The v0.4 run confirms that the current harness is stable and cheap to run.

Key observations:

1. **All tasks passed on the first attempt.**
   This confirms the basic agent loop is reliable on small Python tasks, but it also means the benchmark is not yet hard enough to stress repair behavior.

2. **No failure modes appeared.**
   Failure-mode taxonomy exists in the harness, but the current benchmark did not trigger it.

3. **No public-vs-hidden gap appeared.**
   Public and hidden tests both passed for all tasks. Future tasks should include more adversarial hidden cases.

4. **Patch churn already provides useful signal.**
   Some tasks produce localized repairs, while others produce broader rewrites. For example, `implement_slugify` had a high churn-to-final ratio, while `fix_lru_cache` had a lower ratio.

5. **Cost and latency are measurable even for small tasks.**
   The benchmark provides a low-cost baseline for future comparison with harder tasks, multi-step repair loops, and alternative agent designs.

---

## Project architecture

```text
codeagentops/
├── README.md
├── pyproject.toml
├── .env.example
├── src/
│   └── codeagentops/
│       ├── cli.py
│       ├── config.py
│       ├── models.py
│       ├── runner.py
│       ├── workspace.py
│       ├── metrics.py
│       ├── report.py
│       ├── artifacts.py
│       ├── providers/
│       │   └── deepseek.py
│       ├── evaluators/
│       │   └── pytest_runner.py
│       └── patching/
│           └── apply_patch.py
├── examples/
│   ├── tasks/
│   └── reports/
└── runs/
```

### `cli.py`

Defines the command-line interface.

Main commands:

```bash
codeagentops list-tasks
codeagentops run --max-iterations 3
```

The CLI loads settings, discovers tasks, runs the benchmark, and writes reports.

### `config.py`

Loads runtime settings such as:

* DeepSeek API key
* DeepSeek model
* runs directory
* task directory
* pytest timeout
* max iterations

The API key is read from:

```text
DEEPSEEK_API_KEY
```

### `models.py`

Defines core data models such as:

* `TaskSpec`
* `LLMUsage`
* `IterationTrace`
* `PatchStats`
* `TaskRunResult`

These models make the runner output structured and easy to serialize into JSON.

### `runner.py`

Contains the main single-agent repair loop.

It orchestrates:

* workspace creation
* prompt construction
* DeepSeek calls
* patch application
* public pytest evaluation
* feedback injection
* hidden pytest evaluation
* metric aggregation
* trace writing

### `workspace.py`

Creates isolated task workspaces under `runs/` and reads current workspace files into the prompt.

This keeps generated code separate from benchmark source files.

### `providers/deepseek.py`

Implements the DeepSeek API client.

The provider returns:

* model response text
* prompt token count
* completion token count
* total token count
* estimated cost
* LLM latency

### `patching/apply_patch.py`

Parses full-file updates from the model and applies them to the workspace.

It also computes patch statistics:

* modified files
* lines added
* lines deleted
* final patch size
* patch churn

### `evaluators/pytest_runner.py`

Runs pytest inside the isolated workspace.

Important design detail: pytest runs with the workspace as the current working directory and import root. This avoids import errors such as `ModuleNotFoundError` when tests import local starter files.

### `metrics.py`

Aggregates usage and patch statistics across iterations.

### `report.py`

Generates markdown and JSON reports from structured run results.

### `artifacts.py`

Writes raw trace artifacts such as:

* LLM messages
* raw LLM responses
* public pytest output
* hidden pytest output
* trace JSON

These artifacts make failures inspectable after the run.

---

## Quickstart

### 1. Clone the repository

```bash
git clone <repo-url>
cd CodeAgentOps
```

### 2. Create a virtual environment

```bash
python -m venv .venv
source .venv/bin/activate
```

### 3. Install the package

```bash
pip install -e .
```

### 4. Configure DeepSeek

```bash
cp .env.example .env
```

Edit `.env`:

```bash
DEEPSEEK_API_KEY=your_deepseek_api_key_here
DEEPSEEK_MODEL=deepseek-chat
```

### 5. List available tasks

```bash
codeagentops list-tasks
```

### 6. Run the benchmark

```bash
codeagentops run --max-iterations 3
```

### 7. Read the generated report

```bash
cat runs/report.md
```

---

## Example output files

After a run, CodeAgentOps creates files such as:

```text
runs/
├── report.md
├── report.json
└── <task-name>/
    └── <timestamp>/
        ├── trace.json
        ├── iteration_1_messages.json
        ├── iteration_1_llm_response.txt
        ├── iteration_1_public_pytest_output.txt
        ├── final_hidden_pytest_output.txt
        └── workspace/
```

The `runs/` directory is ignored by git. Curated sample reports are stored under:

```text
examples/reports/
```

---

## Design choices

### DeepSeek-only MVP

The MVP intentionally supports only DeepSeek as the real LLM provider. Multi-provider abstraction is useful later, but it would add unnecessary complexity to the one-day MVP.

### Single-agent repair loop

The current version uses one coding agent rather than a planner/executor/reviewer setup. This keeps the system easier to debug and makes the evaluation loop transparent.

### Full-file update protocol

Full-file updates are easier to parse and audit than arbitrary diffs. This reduces patching complexity and makes the MVP more robust.

### Public tests for repair, hidden tests for scoring

Public tests are used as repair feedback. Hidden tests are used only for final scoring. This separation is important for detecting future public-test overfitting.

### Isolated workspace execution

Each task run uses a copied workspace. This prevents the model from modifying the original benchmark tasks and makes runs reproducible.

### Raw artifacts

The harness stores raw LLM responses and pytest outputs so that failures can be debugged after the run.

---

## Limitations

The current benchmark is intentionally small. It is useful as a stable baseline, but it is not yet hard enough to fully stress autonomous coding agents.

Current limitations:

* all current tasks are single-file Python tasks
* no multi-file repair tasks
* no long-context repository tasks
* no multi-agent comparison
* no provider comparison
* no simulated API failures
* no flaky tests
* no adversarial hidden-test suite
* no benchmark leaderboard
* no web UI
* no secure sandbox beyond local workspace isolation

---

## Roadmap

### v0.5

* improve documentation
* add clearer in-scope and out-of-scope sections
* document workflow and project architecture
* improve benchmark task descriptions
* add narrative interpretation to reports
* prepare the repository for hackathon submission

### v0.6

* add harder diagnostic tasks
* add tasks that require multiple repair iterations
* add public-pass / hidden-fail cases
* add multi-file tasks
* improve report-level benchmark conclusions

### v0.7

* simulate transient API and tool failures
* evaluate retry behavior under failure
* add flaky test detection
* improve failure-mode classification
* compare multiple runs over time

### Later

* add optional reviewer-agent loop
* add provider comparison
* add benchmark result comparison
* add trace visualization
* add support for larger repository-level tasks

---
