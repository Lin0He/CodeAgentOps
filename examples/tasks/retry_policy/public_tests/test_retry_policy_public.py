from retry_policy import backoff_seconds, should_retry


def test_retries_transient_errors_before_limit():
    assert should_retry("timeout", attempt=1, max_attempts=3) is True
    assert should_retry("rate_limit", attempt=2, max_attempts=3) is True
    assert should_retry("server_error", attempt=1, max_attempts=2) is True


def test_does_not_retry_permanent_errors():
    assert should_retry("validation_error", attempt=1, max_attempts=3) is False
    assert should_retry("auth_error", attempt=1, max_attempts=3) is False


def test_backoff_exponential():
    assert backoff_seconds(1) == 0.5
    assert backoff_seconds(2) == 1.0
    assert backoff_seconds(3) == 2.0