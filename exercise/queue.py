from typing import Any, List, Tuple

class PriorityQueue:
    def __init__(self):
        self.items: List[Tuple[Any, int]] = []

    def push(self, item: Any, priority: int):
        for i, (_, p) in enumerate(self.items):
            if priority > p:  # Lower numeric value = lower priority
                self.items.insert(i, (item, priority))
                return
        self.items.append((item, priority))

    def pop(self):
        if not self.items:
            return None
        return self.items.pop(0)[0]  # Remove and return the item from the start of the list

