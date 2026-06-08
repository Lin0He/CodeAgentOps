Fix the small LRU cache implementation.

Requirements:
- `get(key)` returns the value for an existing key and marks it as most recently used.
- `get(key)` returns `None` for a missing key.
- `put(key, value)` inserts or updates a key and marks it as most recently used.
- When capacity is exceeded, evict the least recently used item.
- Capacity must be positive; constructing with capacity <= 0 should raise `ValueError`.
- Preserve the simple public API: class `LRUCache` with `get`, `put`, and `items`.
