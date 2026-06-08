import pytest
from monitoring import detect_anomaly_window


def test_threshold_is_strictly_greater_not_greater_equal():
    values = [5, 5, 5]
    assert detect_anomaly_window(values, threshold=5, window_size=2) == -1


def test_window_size_larger_than_values():
    assert detect_anomaly_window([1, 2], threshold=1, window_size=3) == -1


def test_single_element_window():
    assert detect_anomaly_window([1, 9, 3], threshold=5, window_size=1) == 1


def test_invalid_window_size_zero():
    with pytest.raises(ValueError):
        detect_anomaly_window([1, 2, 3], threshold=1, window_size=0)


def test_invalid_window_size_negative():
    with pytest.raises(ValueError):
        detect_anomaly_window([1, 2, 3], threshold=1, window_size=-1)
