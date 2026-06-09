import pytest
from retry_policy import backoff_seconds, should_retry


def test_does_not_retry_at_max_attempts():
    assert should_retry("timeout", attempt=3, max_attempts=3) is False
    assert should_retry("rate_limit", attempt=5, max_attempts=5) is False


def test_unknown_errors_are_not_retried():
    assert should_retry("weird_error", attempt=1, max_attempts=3) is False


def test_not_found_is_permanent():
    assert should_retry("not_found", attempt=1, max_attempts=3) is False


def test_backoff_cap():
    assert backoff_seconds(10, base=0.5, cap=8.0) == 8.0


def test_invalid_attempt_raises():
    with pytest.raises(ValueError):
        backoff_seconds(0)