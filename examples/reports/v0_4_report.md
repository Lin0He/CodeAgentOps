# CodeAgentOps Run Report

## Summary

- Tasks: **7**
- Final success rate: **7/7**
- First-attempt success rate: **7/7**
- Estimated total cost: **$0.002748**
- Estimated cost per successful task: **$0.000393**

## Task Results

| Task | Success | Public | Hidden | Iterations | API calls | E2E latency | LLM latency | Pytest runtime | Tokens | Cost | Failure modes |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| Aggregate Eval Results | True | True | True | 1 | 1 | 3.60s | 2.95s | 0.65s | 1161 | $0.000634 | - |
| Detect Anomaly Window | True | True | True | 1 | 1 | 2.39s | 1.78s | 0.61s | 594 | $0.000277 | - |
| fix_calculator_bug | True | True | True | 1 | 1 | 2.45s | 1.84s | 0.60s | 649 | $0.000343 | - |
| fix_lru_cache | True | True | True | 1 | 1 | 2.35s | 1.74s | 0.60s | 694 | $0.000331 | - |
| implement_slugify | True | True | True | 1 | 1 | 2.87s | 2.26s | 0.61s | 600 | $0.000370 | - |
| Parse Duration | True | True | True | 1 | 1 | 3.05s | 2.45s | 0.60s | 650 | $0.000389 | - |
| Retry Policy | True | True | True | 1 | 1 | 2.76s | 2.16s | 0.60s | 854 | $0.000405 | - |

## Observability Metrics

### Aggregate Eval Results

- Retry amplification: **1.00x**
- Tool/runtime overhead ratio: **18.28%**
- Patch churn: **42** lines changed across iterations
- Final patch size: **45** lines
- Churn-to-final ratio: **0.93**
- Files changed: **eval_summary.py**

| Iter | Public pass | LLM latency | Prompt tok | Completion tok | Output tok/s | Patch apply | Pytest | Context chars | Failure |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| 1 | True | 2.95s | 775 | 386 | 131.04 | 0.001s | 0.35s | 2909 | - |

### Detect Anomaly Window

- Retry amplification: **1.00x**
- Tool/runtime overhead ratio: **25.59%**
- Patch churn: **12** lines changed across iterations
- Final patch size: **20** lines
- Churn-to-final ratio: **0.60**
- Files changed: **monitoring.py**

| Iter | Public pass | LLM latency | Prompt tok | Completion tok | Output tok/s | Patch apply | Pytest | Context chars | Failure |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| 1 | True | 1.78s | 454 | 140 | 78.68 | 0.001s | 0.31s | 1769 | - |

### fix_calculator_bug

- Retry amplification: **1.00x**
- Tool/runtime overhead ratio: **24.85%**
- Patch churn: **18** lines changed across iterations
- Final patch size: **30** lines
- Churn-to-final ratio: **0.60**
- Files changed: **calculator.py**

| Iter | Public pass | LLM latency | Prompt tok | Completion tok | Output tok/s | Patch apply | Pytest | Context chars | Failure |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| 1 | True | 1.84s | 447 | 202 | 109.72 | 0.001s | 0.31s | 1703 | - |

### fix_lru_cache

- Retry amplification: **1.00x**
- Tool/runtime overhead ratio: **25.79%**
- Patch churn: **10** lines changed across iterations
- Final patch size: **26** lines
- Churn-to-final ratio: **0.38**
- Files changed: **lru_cache.py**

| Iter | Public pass | LLM latency | Prompt tok | Completion tok | Output tok/s | Patch apply | Pytest | Context chars | Failure |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| 1 | True | 1.74s | 521 | 173 | 99.16 | 0.001s | 0.30s | 1990 | - |

### implement_slugify

- Retry amplification: **1.00x**
- Tool/runtime overhead ratio: **21.45%**
- Patch churn: **32** lines changed across iterations
- Final patch size: **33** lines
- Churn-to-final ratio: **0.97**
- Files changed: **text_utils.py**

| Iter | Public pass | LLM latency | Prompt tok | Completion tok | Output tok/s | Patch apply | Pytest | Context chars | Failure |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| 1 | True | 2.26s | 349 | 251 | 111.14 | 0.001s | 0.31s | 1445 | - |

### Parse Duration

- Retry amplification: **1.00x**
- Tool/runtime overhead ratio: **19.68%**
- Patch churn: **26** lines changed across iterations
- Final patch size: **39** lines
- Churn-to-final ratio: **0.67**
- Files changed: **duration.py**

| Iter | Public pass | LLM latency | Prompt tok | Completion tok | Output tok/s | Patch apply | Pytest | Context chars | Failure |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| 1 | True | 2.45s | 393 | 257 | 104.78 | 0.001s | 0.30s | 1453 | - |

### Retry Policy

- Retry amplification: **1.00x**
- Tool/runtime overhead ratio: **21.93%**
- Patch churn: **14** lines changed across iterations
- Final patch size: **22** lines
- Churn-to-final ratio: **0.64**
- Files changed: **retry_policy.py**

| Iter | Public pass | LLM latency | Prompt tok | Completion tok | Output tok/s | Patch apply | Pytest | Context chars | Failure |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| 1 | True | 2.16s | 644 | 210 | 97.42 | 0.001s | 0.31s | 2230 | - |
