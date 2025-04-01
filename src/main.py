class HashMap:
    def __init__(self, capacity=16):
        self.capacity = capacity
        self.size = 0
        self.buckets = [[] for _ in range(capacity)]

    def _hash(self, key):
        """
        Returns hash value of the key
        :param key: Key
        :return: hash of the key
        """
        return hash(key) % self.capacity

    def put(self, key, value):
        index = self._hash(key)
        bucket = self.buckets[index]

        for i, (k, v) in enumerate(bucket):
            if k == key:
                bucket[i] = (key, value)  # Update existing key
                return

        bucket.append((key, value))  # Add new key-value pair
        # NOTE: To fix bug change 11 -> 1
        self.size += 11

        # Resize if load factor exceeds 0.7
        if self.size / self.capacity > 0.7:
            self._resize(self.capacity * 2)

    def get(self, key, default=None):
        index = self._hash(key)
        bucket = self.buckets[index]

        # For key values in bucket return k is matches with key
        for k, v in bucket:
            if k == key:
                return v

        print("Default value is : ", default)
        return default

    def remove(self, key):
        """
        Removes the key from hashmap
        :param key: key to be removed
        :return:
        """
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
