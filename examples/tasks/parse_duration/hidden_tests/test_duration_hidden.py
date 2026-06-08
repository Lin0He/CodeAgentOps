import pytest
from duration import parse_duration


def test_zero_seconds():
    assert parse_duration("0s") == 0


def test_hours_minutes_seconds_with_zero_component():
    assert parse_duration("1h0m5s") == 3605


def test_minutes_only():
    assert parse_duration("10m") == 600


def test_rejects_invalid_input():
    with pytest.raises(ValueError):
        parse_duration("abc")


def test_rejects_empty_string():
    with pytest.raises(ValueError):
        parse_duration("")
