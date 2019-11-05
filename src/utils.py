import bisect


class Queue:
    """
    Abstract class for queue.
    2 types of queue:
        - Stack which is Last in First out queue
        - FIFO queue which is First in First out queue
    """

    def extend(self, items):
        for item in items:
            self.append(item)


def stack():
    """Last in first out queue. Match the list structure in python"""
    return []


class FIFOQueue(Queue):
    """First in first out queue"""

    def __init__(self):
        self.q = []

    def append(self, item):
        self.q.append(item)

    def __len__(self):
        return len(self.q)

    def pop(self):
        try:
            item = self.q[0]
            self.q = self.q[1:]
            return item
        except IndexError:
            return None


class PriorityQueueElem:
    def __init__(self, val, e):
        self.val = val
        self.e = e

    def __lt__(self, other):
        return self.val < other.val

    def value(self):
        return self.val

    def elem(self):
        return self.e


class PriorityQueue(Queue):
    def __init__(self, f, order=min):
        self.q = []
        self.order = order
        self.f = f

    def append(self, item):
        queue_elem = PriorityQueueElem(self.f(item), item)
        bisect.insort(self.q, queue_elem)

    def pop(self):
        if self.order == min:
            return self.q.pop(0).elem()
        else:
            return self.q.pop().elem()
