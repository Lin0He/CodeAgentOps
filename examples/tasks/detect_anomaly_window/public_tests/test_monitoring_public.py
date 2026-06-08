from monitoring import detect_anomaly_window


def test_detects_first_anomalous_window():
    values = [1, 2, 10, 12, 11]
    assert detect_anomaly_window(values, threshold=9, window_size=3) == 2


def test_returns_minus_one_when_no_anomaly():
    values = [1, 2, 3, 4]
    assert detect_anomaly_window(values, threshold=10, window_size=2) == -1


def test_detects_window_at_start():
    values = [10, 10, 1, 1]
    assert detect_anomaly_window(values, threshold=9, window_size=2) == 0
