import unittest
from heap.heap import Heap

class TestHeap(unittest.TestCase):

    def test_max_heap_push_pop(self):
        heap = Heap(length=5, is_max=True)
        heap.push(10)
        heap.push(20)
        heap.push(5)
        heap.push(15)
        heap.push(30)
        self.assertEqual(heap.pop(), 30)
        self.assertEqual(heap.pop(), 20)
        self.assertEqual(heap.pop(), 15)
        self.assertEqual(heap.pop(), 10)
        self.assertEqual(heap.pop(), 5)
        self.assertTrue(heap.is_empty())

    def test_min_heap_push_pop(self):
        heap = Heap(length=5, is_max=False)
        heap.push(10)
        heap.push(20)
        heap.push(5)
        heap.push(15)
        heap.push(30)
        self.assertEqual(heap.pop(), 5)
        self.assertEqual(heap.pop(), 10)
        self.assertEqual(heap.pop(), 15)
        self.assertEqual(heap.pop(), 20)
        self.assertEqual(heap.pop(), 30)
        self.assertTrue(heap.is_empty())

    def test_empty_heap_pop(self):
        heap = Heap(length=3)
        with self.assertRaises(Exception) as context:
            heap.pop()
        self.assertEqual(str(context.exception), "EMPTY_HEAP")

    def test_full_heap_push(self):
        heap = Heap(length=2)
        heap.push(1)
        heap.push(2)
        heap.push(3)
        self.assertTrue(heap.is_full())
        with self.assertRaises(Exception) as context:
            heap.push(3)
        self.assertEqual(str(context.exception), "FULL_HEAP")

    def test_heap_capacity_and_height(self):
        heap = Heap(length=10)
        self.assertGreaterEqual(heap.weight, 10)
        self.assertEqual(heap.length, 0)
        self.assertTrue(heap.is_empty())

if __name__ == "__main__":
    unittest.main()