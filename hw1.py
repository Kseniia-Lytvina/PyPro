class HashTable:
    def __init__(self, initial_capacity=8, load_factor=0.7):
        self.capacity = initial_capacity
        self.size = 0
        self.load_factor = load_factor
        self.table = [None] * self.capacity

    def _hash(self, key):
        return hash(key) % self.capacity

    def _probe(self, index):
        while self.table[index] is not None and self.table[index][0] != "<DELETED>":
            index = (index + 1) % self.capacity
        return index

    def _resize(self):
        old_table = self.table
        self.capacity *= 2
        self.table = [None] * self.capacity
        self.size = 0

        for item in old_table:
            if item and item[0] != "<DELETED>":
                self.add(item[0], item[1])

    def add(self, key, value):
        if self.size + 1 > self.capacity * self.load_factor:
            self._resize()

        index = self._hash(key)

        while self.table[index] is not None:
            k, v = self.table[index]
            if k == key:
                self.table[index] = (key, value)
                return
            index = (index + 1) % self.capacity

        self.table[index] = (key, value)
        self.size += 1

    def get(self, key):
        index = self._hash(key)

        while self.table[index] is not None:
            k, v = self.table[index]
            if k == key:
                return v
            index = (index + 1) % self.capacity
        raise KeyError(f"Ключ '{key}' не знайдено")

    def __repr__(self):
        items = []
        for pair in self.table:
            if pair is not None and pair[0] != "<DELETED>":
                k, v = pair
                items.append(f"{k}: {v}")
        return "{" + ", ".join(items) + "}"

ht = HashTable()
ht.add("apple", 1)
ht.add("banana", 2)
ht.add("orange", 3)

print(ht.get("banana"))     # >> 2
print(ht)                   # >> {apple: 1, banana: 2, orange: 3}