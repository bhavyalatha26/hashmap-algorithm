import unittest

from src.main import HashMap


class TestHashMap(unittest.TestCase):

    def setUp(self):
        self.hashmap = HashMap()

    def test_put_and_get(self):
        self.hashmap.put("apple", 1)
        self.assertEqual(self.hashmap.get("apple"), 1)
        self.hashmap.put("apple", 2)  # test update
        self.assertEqual(self.hashmap.get("apple"), 2)

    def test_get_default(self):
        self.assertEqual(self.hashmap.get("banana"), None)
        self.assertEqual(self.hashmap.get("banana", 0), 0)

    def test_len(self):
        self.assertEqual(len(self.hashmap), 0)
        self.hashmap.put("apple", 1)
        self.assertEqual(len(self.hashmap), 1)
        self.hashmap.put("banana", 2)
        self.assertEqual(len(self.hashmap), 2)

    def test_contains(self):
        self.assertFalse("apple" in self.hashmap)
        self.hashmap.put("apple", 1)
        self.assertTrue("apple" in self.hashmap)

    def test_remove(self):
        self.hashmap.put("apple", 1)
        self.hashmap.put("banana", 2)
        self.hashmap.remove("apple")
        self.assertIsNone(self.hashmap.get("apple"))
        self.assertEqual(len(self.hashmap), 1)
        self.assertTrue("banana" in self.hashmap)
        self.hashmap.remove("banana")
        self.assertEqual(len(self.hashmap), 0)
        self.assertFalse("banana" in self.hashmap)

    def test_resize(self):
        for i in range(20):  # force resize
            self.hashmap.put(str(i), i)
        self.assertTrue(self.hashmap.capacity > 16)
        self.assertEqual(len(self.hashmap), 20)
        for i in range(20):
            self.assertEqual(self.hashmap.get(str(i)), i)


if __name__ == '__main__':
    unittest.main()
