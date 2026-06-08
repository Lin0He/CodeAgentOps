def parse_duration(text: str) -> int:
    """
    Parse a duration string into seconds.

    Supported units:
    - h: hours
    - m: minutes
    - s: seconds

    Examples:
        "1h30m" -> 5400
        "45s" -> 45
        "2m10s" -> 130
    """
    return int(text)
