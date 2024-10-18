class Cost:
    def __init__(self):
        self.ops = []
    def op(self, operation, left, right, ans):
        self.ops.append([operation, left, right, ans])

    def get_every(self, operation):
        return filter(lambda x: x[0] == operation, self.ops)