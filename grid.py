
from functools import wraps
from typing import Self


class Point():
    def __init__(self, x, y):
       self.x = x
       self.y = y
    
    def __iter__(self):
        return iter([self.x, self.y])
    
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y
    
    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)


class Grid():
    def __init__(self):
        self.grid = [[" "] * 50 for _ in range(50)]
        self.pencil = Point(0, 0)
        self.eye = Point(0, 0)
        self.origin = Point(0,0)
        self.eye_stack = []
        self.eye_history = [Point(0, 0)]
        self.writes = []
    
    def logger(names: list):
        def logging_wrapper(f):
            @wraps(f)
            def logging(self: Self, *args):
                out = f(self, *args)
                if "eye" in names:
                    self.eye_history.append(self.eye + Point(0, 0))
                if "write" in names:
                    self.writes.append(args[0] + " " + str(list(self.pencil + Point(0, 0))))
                return out
            return logging
        return logging_wrapper
    
    def shift_one(self):
        self.eye.x += 1
    
    def shift_back(self):
        self.eye.x -= 1
    
    @logger("eye")
    def get(self, loc: Point = None):
        
        if loc is None:
            loc = self.eye + Point(0, 0)
        else: loc += self.origin
        self.eye = loc + Point(0, 0)

        x, y = loc
        return self.grid[y][x] 

    def push(self):
        self.eye_stack.append(self.eye + Point(0, 0))
    
    def drag(self, loc: Point):
        self.origin += loc
        self.eye = loc
        self.pencil += loc
    
    def pop(self):
        self.eye = self.eye_stack.pop() + Point(0, 0)

    def nudge_pencil(self, dir: Point):
        self.move_pencil(self.pencil + dir)
    
    @logger("pencil eye write")
    def write(self, char: str, loc: Point = None):
        if loc is None:
            loc = self.pencil
        else: loc += self.origin
        self.eye = self.pencil + Point(0, 0)
        x, y = loc
        
        self.grid[y][x] = char
        self.pencil.x += 1
    
    # @logger(["pencil", "eye"])
    def move_pencil(self, loc: Point=None):
        if loc is None: loc = self.eye + Point(0, 0)
        self.pencil = loc + self.origin

    def write_s(self, string: str):
        for char in string:
            self.write(char)
    def pretty(self):
        out = ""
        for row in self.grid:
            out += "".join(row) + "|\n"
        out += f"Pencil: {list(self.pencil + Point(0, 0))}, Origin: {list(self.origin + Point(0, 0))}, Eye: {list(self.eye + Point(0, 0))}"
        return out
    
    
    def nudge_eye(self, dir: Point):
        self.eye = (self.eye + dir)

    @logger("eye")
    def get_absolute(self, loc: Point):
        return self.grid[loc.y][loc.x]

    def get_s(self, start: Point, length: int):
        result = ""
        for _ in range(length):
            result += self.get(start)
            start.x += 1
        return result
    
    def pretty_logs(self):
        out = "Eye History: "
        out += ', '.join([str(list(pt)) for pt in self.eye_history])
        out += "\nWrites: "
        out += ', '.join(self.writes)
        return out
    