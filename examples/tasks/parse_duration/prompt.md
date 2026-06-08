Implement `parse_duration(text: str) -> int` in `duration.py`.

The function should parse compact duration strings into seconds.

Supported units:
- `h` for hours
- `m` for minutes
- `s` for seconds

Examples:
- `"45s"` -> `45`
- `"2m10s"` -> `130`
- `"1h30m"` -> `5400`

Invalid input should raise `ValueError`.

Keep the implementation simple and do not modify tests.
