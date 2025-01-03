class UndoStack:
    def __init__(self):
        self.stack = []

    def push(self, operation):
        self.stack.append(operation)

    def pop(self):
        if self.stack:
            return self.stack.pop()
        return None
