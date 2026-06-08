# CodeAgentOps

**Evaluation and observability for autonomous coding agents as production systems.**

CodeAgentOps is a lightweight one-day MVP harness for evaluating autonomous coding agents beyond final test pass/fail. It treats a coding agent like a production system: every task run produces traces, latency metrics, token/cost estimates, retry behavior, context growth, patch churn, tool overhead, and failure modes.

This MVP intentionally uses a single-agent repair loop and one real provider: **DeepSeek API**.

## Why this project exists

Most coding-agent demos stop at: "did the generated code pass tests?"

That is necessary, but not enough for production agentic coding systems. A useful evaluation harness should also ask:

- How many repair iterations were needed?
- How much latency came from the LLM versus local tools?
- Did retries amplify cost?
- Did the context grow over time?
- Was the patch stable or did the agent churn the codebase?
- Did the agent modify forbidden files such as tests?
- Did it pass hidden tests, not just visible public tests?
- What failure mode occurred when it failed?

CodeAgentOps gives a minimal, runnable answer to those questions.

## MVP features

### Correctness

- Public pytest pass/fail
- Hidden pytest pass/fail
- Final success
- First-attempt success
- Regression preservation through public and hidden tests

### Agent loop behavior

- Single-agent repair loop
- Iterations to success
- API calls per task
- Retry amplification
- Repair success after initial failure

### Latency

- End-to-end task latency
- Per-iteration LLM latency
- Patch apply time
- Pytest runtime
- Tool/runtime overhead ratio

### Tokens and cost

- Prompt tokens
- Completion tokens
- Total tokens
- Estimated cost
- Cost per task
- Cost per successful task
- Output tokens per second when usage metadata is available

### Context growth

- Prompt/context size by iteration
- Context growth proxy through prompt tokens and context characters

### Patch stability

- Files changed
- Lines added
- Lines deleted
- Patch churn
- Final patch size
- Churn-to-final ratio
- Forbidden file edit detection

### Failure modes

- `syntax_error`
- `test_failure`
- `hidden_test_failure`
- `invalid_patch`
- `timeout`
- `no_code_change`
- `modified_forbidden_file`
- `max_iterations_reached`
- `runtime_error`

## Architecture

```text
codeagentops/
├── README.md
├── pyproject.toml
├── .env.example
├── src/
│   └── codeagentops/
│       ├── cli.py
│       ├── config.py
│       ├── metrics.py
│       ├── models.py
│       ├── report.py
│       ├── runner.py
│       ├── workspace.py
│       ├── providers/
│       │   └── deepseek.py
│       ├── evaluators/
│       │   └── pytest_runner.py
│       └── patching/
│           └── apply_patch.py
├── examples/
│   └── tasks/
│       ├── fix_calculator_bug/
│       ├── implement_slugify/
│       └── fix_lru_cache/
└── runs/
```

## Agent loop

For each task:

1. Copy starter code into an isolated run workspace.
2. Copy public tests into the workspace.
3. Send task prompt, current source files, and previous feedback to DeepSeek.
4. Ask the model to return full-file updates in a strict format.
5. Apply file updates.
6. Reject forbidden edits, especially test edits.
7. Run public pytest tests.
8. If public tests fail, feed pytest output back into the next iteration.
9. Retry until success or `max_iterations` is reached.
10. Run hidden tests once public tests pass.
11. Save `trace.json` and generate a markdown report.

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
cp .env.example .env
```

Edit `.env`:

```bash
DEEPSEEK_API_KEY=your_deepseek_api_key_here
DEEPSEEK_MODEL=deepseek-chat
```

The cost numbers in `.env.example` are rough configurable assumptions. Update them to match your model/account pricing.

## Run

List available tasks:

```bash
codeagentops list-tasks
```

Run all demo tasks:

```bash
codeagentops run --max-iterations 3
```

Run one task:

```bash
codeagentops run --task fix_calculator_bug --max-iterations 3
```

Generate report at a custom path:

```bash
codeagentops run --report-path runs/demo_report.md
```

## Expected LLM response format

The MVP uses full-file replacement instead of complex patch parsing. This is more robust for a one-day project.

The model must respond like this:

````text
### FILE: calculator.py
```python
def add(a, b):
    return a + b
```
````

Multiple files are supported by returning multiple `### FILE:` blocks.

## Demo tasks

### 1. `fix_calculator_bug`

Type: bug fixing + security edge case

The agent must fix true division and replace unsafe `eval` with a restricted arithmetic evaluator. Hidden tests check unsafe syntax rejection.

### 2. `implement_slugify`

Type: feature implementation + edge cases

The agent must implement URL slug generation, separator normalization, accent normalization, max-length truncation, and empty fallback behavior.

### 3. `fix_lru_cache`

Type: data structure bug fix + regression preservation

The agent must fix LRU recency behavior, updates, eviction, and invalid capacity handling.

## Output artifacts

Each task run creates:

```text
runs/<task>/<timestamp>/
├── trace.json
├── hidden_test_output.txt   # only if hidden tests fail
└── workspace/
```

The aggregate report is written to:

```text
runs/report.md
runs/report.json
```

## Example report sections

- Summary success rate
- First-attempt success rate
- Estimated total cost
- Cost per successful task
- Per-task latency and token table
- Per-iteration observability table
- Patch churn and stability metrics
- Failure mode summary

## One-day implementation philosophy

This project deliberately avoids:

- Web UI
- Multi-provider abstraction
- Complex multi-agent orchestration
- Distributed execution
- Sandboxed containers
- Full benchmark-suite complexity

The goal is a clean, selection-ready MVP that demonstrates strong engineering judgment: evaluating autonomous coding agents as observable production systems.

## Extension ideas

After the hackathon MVP, useful extensions include:

- Add vLLM/OpenAI/Anthropic providers
- Add Docker sandboxing per task
- Add real unified-diff patch support
- Add repository-scale tasks
- Add multi-agent planner/implementer/reviewer loops
- Add Fiberplane/OpenTelemetry-style traces
- Add latency/cost Pareto plots
- Add task difficulty tags and leaderboard export
