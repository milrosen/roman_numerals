class Cost:
    def __init__(self):
        self.steps = []
    def op(self, operation, left, right, ans):
        self.steps.append([operation, left, right, ans])

    def begin_phase(self, phase):
        self.steps.append(["begin phase", phase, "", ""])