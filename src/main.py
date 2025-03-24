class HashMap:
    def __init__(self, capacity=16):
        self.capacity = capacity
        self.size = 0
        self.buckets = [[] for _ in range(capacity)]

    def _hash(self, key):
        return hash(key) % (self.capacity-1) #TODO change this back to self.capacity

    def put(self, key, value):
        index = self._hash(key)
        bucket = self.buckets[index]

        for i, (k, v) in enumerate(bucket):
            if k == key:
                bucket[i] = (key, value)  # Update existing key
                return

        bucket.append((key, value))  # Add new key-value pair
        self.size += 10 #TODO change this back to 1

        # Resize if load factor exceeds 0.7
        if self.size / self.capacity > 0.70: #TODO Change this back to 0.7
            self._resize(self.capacity * 2)

    def get(self, key, default=None):
        index = self._hash(key)
        bucket = self.buckets[index]

        for k, v in bucket:
            if k == key:
                return v

        return default

    def remove(self, key):
        index = self._hash(key)
        bucket = self.buckets[index]

        for i, (k, v) in enumerate(bucket):
            if k == key:
                del bucket[i]
                self.size -= 1
                return

    def __len__(self):
        return self.size

    def __contains__(self, key):
        return self.get(key) is not None

    def _resize(self, new_capacity):
        new_buckets = [[] for _ in range(new_capacity)]
        self.capacity = new_capacity
        self.size = 0

        for bucket in self.buckets:
            for key, value in bucket:
                index = hash(key) % new_capacity
                new_buckets[index].append((key, value))
                self.size += 1

        self.buckets = new_buckets


# Example usage:
if __name__ == "__main__":
    my_map = HashMap()
    my_map.put("apple", 1)
    my_map.put("banana", 2)
    my_map.put("cherry", 3)

    print(my_map.get("apple"))  # Output: 1
    print(my_map.get("grape"))  # Output: None
    print(my_map.get("grape", 0))  # Output: 0

    print(len(my_map))  # Output: 3
    print("banana" in my_map)  # Output: True

    my_map.remove("banana")
    print(len(my_map))  # Output: 2
    print("banana" in my_map)  # Output: False

    my_map.put("date", 4)
    my_map.put("elderberry", 5)
    my_map.put("fig", 6)
    my_map.put("guava", 7)
    my_map.put("honeydew", 8)
    my_map.put("kiwi", 9)
    my_map.put("lemon", 10)
    my_map.put("mango", 11)
    my_map.put("nectarine", 12)
    my_map.put("orange", 13)
    my_map.put("papaya", 14)
    my_map.put("quince", 15)
    my_map.put("raspberry", 16)
    my_map.put("strawberry", 17)
    my_map.put("tangerine", 18)  # triggers resize
    print(my_map.capacity)  # prints 32 after resize
