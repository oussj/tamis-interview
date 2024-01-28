from exercise.queue import PriorityQueue
import unittest

class TestPriorityQueue(unittest.TestCase):

    def test_push_and_pop(self):
        pq = PriorityQueue()
        pq.push('low priority', 1)
        pq.push('high priority', 2)
        pq.push('medium priority', 1.5)

        # The item with the highest priority should be popped first
        self.assertEqual(pq.pop(), 'high priority')
        self.assertEqual(pq.pop(), 'medium priority')
        self.assertEqual(pq.pop(), 'low priority')

    def test_pop_empty_queue(self):
        pq = PriorityQueue()
        
        # Popping from an empty queue should return None (or raise an exception, depending on your implementation)
        self.assertIsNone(pq.pop())

    def test_order_of_same_priority(self):
        pq = PriorityQueue()
        pq.push('first', 1)
        pq.push('second', 1)

        # Items with the same priority should be popped in the order they were pushed
        self.assertEqual(pq.pop(), 'first')
        self.assertEqual(pq.pop(), 'second')
        
    def test_fifo_order_same_priority(self):
        pq = PriorityQueue()
        pq.push('first', 1)
        pq.push('second', 1)
        pq.push('third', 1)

        self.assertEqual(pq.pop(), 'first')
        self.assertEqual(pq.pop(), 'second')
        self.assertEqual(pq.pop(), 'third')

    def test_mixed_priorities(self):
        pq = PriorityQueue()
        pq.push('first', 2)
        pq.push('second', 1)
        pq.push('third', 2)

        # 'first' and 'third' have the same higher priority, so 'first' should come out first as it was pushed first
        self.assertEqual(pq.pop(), 'first')
        self.assertEqual(pq.pop(), 'third')
        self.assertEqual(pq.pop(), 'second')  # 'second' has lower priority


if __name__ == '__main__':
    unittest.main()
