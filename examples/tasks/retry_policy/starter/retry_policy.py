def should_retry(error_type: str, attempt: int, max_attempts: int) -> bool:
    """
    Decide whether an operation should be retried.
    """
    return False


def backoff_seconds(attempt: int, base: float = 0.5, cap: float = 8.0) -> float:
    """
    Return exponential backoff delay for a retry attempt.
    """
    return base