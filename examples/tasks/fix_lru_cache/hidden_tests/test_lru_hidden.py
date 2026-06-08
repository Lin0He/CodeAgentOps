import pytest
from lru_cache import LRUCache


def test_update_existing_does_not_duplicate_capacity():
    cache = LRUCache(2)
    cache.put("a", 1)
    cache.put("a", 10)
    cache.put("b", 2)
    assert cache.get("a") == 10
    assert cache.get("b") == 2


def test_update_marks_recent():
    cache = LRUCache(2)
    cache.put("a", 1)
    cache.put("b", 2)
    cache.put("a", 10)
    cache.put("c", 3)
    assert cache.get("b") is None
    assert cache.get("a") == 10


def test_invalid_capacity():
    with pytest.raises(ValueError):
        LRUCache(0)
