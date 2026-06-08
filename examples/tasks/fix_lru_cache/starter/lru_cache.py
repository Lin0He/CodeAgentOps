class LRUCache:
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.data = {}
        self.order = []

    def get(self, key):
        return self.data.get(key)

    def put(self, key, value):
        self.data[key] = value
        self.order.append(key)
        if len(self.data) > self.capacity:
            oldest = self.order.pop(0)
            del self.data[oldest]

    def items(self):
        return list(self.data.items())
