"""Chase-Lev Work-Stealing Deque Scheduler Engine.
100% Python Standard Library.
"""

class ChaseLevDeque:
    """Chase-Lev Work-Stealing Deque: Local LIFO push/pop, remote FIFO steal."""
    def __init__(self, initial_capacity=32):
        self.buffer = [None] * initial_capacity
        self.capacity = initial_capacity
        self.top = 0
        self.bottom = 0

    def push(self, task):
        b = self.bottom
        if b - self.top >= self.capacity:
            new_cap = self.capacity * 2
            new_buf = [None] * new_cap
            for i in range(self.top, b):
                new_buf[i % new_cap] = self.buffer[i % self.capacity]
            self.buffer = new_buf
            self.capacity = new_cap
        self.buffer[b % self.capacity] = task
        self.bottom = b + 1

    def pop(self):
        b = self.bottom - 1
        self.bottom = b
        t = self.top
        size = b - t
        if size < 0:
            self.bottom = t
            return None
        task = self.buffer[b % self.capacity]
        if size > 0:
            return task
        if self.top != t:
            task = None
        self.bottom = t + 1
        self.top = t + 1
        return task

    def steal(self):
        t = self.top
        b = self.bottom
        if b - t <= 0:
            return None
        task = self.buffer[t % self.capacity]
        self.top = t + 1
        return task
