# CodeAgentOps Run Report

## Summary

- Tasks: **5**
- Final success rate: **5/5**
- First-attempt success rate: **5/5**
- Estimated total cost: **$0.001726**
- Estimated cost per successful task: **$0.000345**

## Task Results

| Task | Success | Public | Hidden | Iterations | API calls | E2E latency | LLM latency | Pytest runtime | Tokens | Cost | Failure modes |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| Detect Anomaly Window | True | True | True | 1 | 1 | 2.97s | 2.15s | 0.81s | 594 | $0.000277 | - |
| fix_calculator_bug | True | True | True | 1 | 1 | 3.35s | 2.76s | 0.58s | 664 | $0.000359 | - |
| fix_lru_cache | True | True | True | 1 | 1 | 2.81s | 2.18s | 0.62s | 694 | $0.000331 | - |
| implement_slugify | True | True | True | 1 | 1 | 3.34s | 2.73s | 0.60s | 600 | $0.000370 | - |
| Parse Duration | True | True | True | 1 | 1 | 3.22s | 2.58s | 0.63s | 650 | $0.000389 | - |

## Observability Metrics

### Detect Anomaly Window

- Retry amplification: **1.00x**
- Tool/runtime overhead ratio: **27.64%**
- Patch churn: **12** lines changed across iterations
- Final patch size: **20** lines
- Churn-to-final ratio: **0.60**
- Files changed: **monitoring.py**

| Iter | Public pass | LLM latency | Prompt tok | Completion tok | Output tok/s | Patch apply | Pytest | Context chars | Failure |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| 1 | True | 2.15s | 454 | 140 | 65.22 | 0.001s | 0.50s | 1769 | - |

### fix_calculator_bug

- Retry amplification: **1.00x**
- Tool/runtime overhead ratio: **17.45%**
- Patch churn: **18** lines changed across iterations
- Final patch size: **30** lines
- Churn-to-final ratio: **0.60**
- Files changed: **calculator.py**

| Iter | Public pass | LLM latency | Prompt tok | Completion tok | Output tok/s | Patch apply | Pytest | Context chars | Failure |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| 1 | True | 2.76s | 447 | 217 | 78.56 | 0.002s | 0.32s | 1703 | - |

### fix_lru_cache

- Retry amplification: **1.00x**
- Tool/runtime overhead ratio: **22.41%**
- Patch churn: **10** lines changed across iterations
- Final patch size: **26** lines
- Churn-to-final ratio: **0.38**
- Files changed: **lru_cache.py**

| Iter | Public pass | LLM latency | Prompt tok | Completion tok | Output tok/s | Patch apply | Pytest | Context chars | Failure |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| 1 | True | 2.18s | 521 | 173 | 79.40 | 0.002s | 0.33s | 1990 | - |

### implement_slugify

- Retry amplification: **1.00x**
- Tool/runtime overhead ratio: **18.07%**
- Patch churn: **32** lines changed across iterations
- Final patch size: **33** lines
- Churn-to-final ratio: **0.97**
- Files changed: **text_utils.py**

| Iter | Public pass | LLM latency | Prompt tok | Completion tok | Output tok/s | Patch apply | Pytest | Context chars | Failure |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| 1 | True | 2.73s | 349 | 251 | 91.80 | 0.002s | 0.32s | 1445 | - |

### Parse Duration

- Retry amplification: **1.00x**
- Tool/runtime overhead ratio: **19.78%**
- Patch churn: **26** lines changed across iterations
- Final patch size: **39** lines
- Churn-to-final ratio: **0.67**
- Files changed: **duration.py**

| Iter | Public pass | LLM latency | Prompt tok | Completion tok | Output tok/s | Patch apply | Pytest | Context chars | Failure |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| 1 | True | 2.58s | 393 | 257 | 99.55 | 0.002s | 0.36s | 1453 | - |
