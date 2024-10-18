from typing import List 


class Rewrite:
    def __init__(self, from_string: str, to_string: str, action):
        self.left = from_string
        self.right = to_string
        self.action = action
        self.delta = abs(len(from_string) - len(to_string))
    
    def from_chunk(from_string: str, to_string: str, action, size):
        r = Rewrite(from_string, to_string, action)
        r.delta = size
        
        return r

    def __str__(self):
        return f'From: {self.left}, To: {self.right}, Performed During: {self.action}'

class Cost:
    def __init__(self) -> None:
        self.eye_movements: list[tuple[int, int]] = []
        self.number_of_symbols: int = 0
        self.actions_history: list[Rewrite] = []
        self.recalls_multiplication: list[tuple[str, str, str]] = []
        self.recalls_grouping: list[str] = []
        self.actions_stack: list[str] = []
        self.pencil_movements: list[tuple[int, int]] = [(0,0)]
        self.recalls_ordering: list[tuple[str, str]] = []

    def start_action(self, action, **kwargs):
        self.actions_stack.append(f"{action}")
        return len(self.actions_history)
    
    def finish_action(self, action, id):
        pass

    def shift_pencil(self, x, y):
        cx, cy = self.pencil_movements[-1]

        self.move_pencil(cx + x, cy + y)

    def __getitem__(self, item):
        return getattr(self, item)

    def recall_grouping_fact(self, letter, group_size):
        self.recalls_grouping.append(letter)

    def recall_multiplication_fact(self, l1, l2, result):
        self.recalls_multiplication.append((l1, l2, result))
    
    def recall_ordering_fact(self, l1, l2):
        self.recalls_ordering.append((l1, l2))

    def rewrite(self, from_string, to_string):
        self.shift_pencil(len(to_string), 1)
        r = Rewrite(from_string, to_string, self.actions_stack[-1])
        self.actions_history.append(r)

    def move_eye(self, x, y):
        self.eye_movements.append((x,y))

    def move_pencil(self, x, y):
        self.pencil_movements.append((x,y))

    def pretty(self):
        out = ''
        for key in self.__dict__:
            if key != "observers" and key != "number_of_symbols":
                out += f"{key}: {list(map(str, self[key]))}\n"
        out += f"number_of_symbols: {self.number_of_symbols}"
        return out