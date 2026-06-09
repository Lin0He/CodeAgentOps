Implement `aggregate_eval_results(results: list[dict]) -> dict` in `eval_summary.py`.

The input is a list of task result dictionaries. Each item may contain:

- `success`: bool
- `public_passed`: bool
- `hidden_passed`: bool
- `iterations`: int
- `cost_usd`: float
- `latency_s`: float

Return a dictionary with:

- `tasks`: total number of tasks
- `successes`: number of tasks where `success` is True
- `success_rate`: successes / tasks, or 0.0 if there are no tasks
- `public_pass_rate`: number of public-passed tasks / tasks
- `hidden_pass_rate`: number of hidden-passed tasks / tasks
- `avg_iterations`: average iterations, or 0.0 if there are no tasks
- `total_cost_usd`: sum of costs
- `avg_latency_s`: average latency, or 0.0 if there are no tasks

Missing boolean fields should be treated as False.
Missing numeric fields should be treated as 0.

Do not modify tests.