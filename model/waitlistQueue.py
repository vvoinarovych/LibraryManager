from collections import deque


class WaitlistQueue:
    def __init__(self):
        self.queue = deque()

    def enqueue(self, user_id):
        self.queue.append(user_id)

    def dequeue(self):
        if self.queue:
            return self.queue.popleft()
        return None

    def is_empty(self):
        return len(self.queue) == 0
