from duration import parse_duration


def test_seconds_only():
    assert parse_duration("45s") == 45


def test_minutes_and_seconds():
    assert parse_duration("2m10s") == 130


def test_hours_and_minutes():
    assert parse_duration("1h30m") == 5400
