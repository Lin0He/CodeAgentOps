Implement `detect_anomaly_window(values, threshold, window_size)` in `monitoring.py`.

The function should return the start index of the first rolling window whose average is strictly greater than `threshold`.

Rules:
- Return `-1` if no anomalous window exists.
- If `window_size` is larger than the number of values, return `-1`.
- If `window_size <= 0`, raise `ValueError`.
- The comparison must be strictly greater than threshold, not greater-or-equal.
- Do not modify tests.
