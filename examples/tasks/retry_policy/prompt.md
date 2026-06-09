Implement retry policy helpers in `retry_policy.py`.

Functions:

1. `should_retry(error_type: str, attempt: int, max_attempts: int) -> bool`

Rules:
- Retry transient errors: `"timeout"`, `"rate_limit"`, `"server_error"`.
- Do not retry permanent errors: `"validation_error"`, `"auth_error"`, `"not_found"`.
- Retry only if `attempt < max_attempts`.
- Attempt is 1-indexed.
- Unknown error types should not be retried.

2. `backoff_seconds(attempt: int, base: float = 0.5, cap: float = 8.0) -> float`

Rules:
- Return exponential backoff: `base * 2 ** (attempt - 1)`.
- Delay must not exceed `cap`.
- If `attempt < 1`, raise `ValueError`.

Do not modify tests.