
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
    
    def __sub__(self, other):
        return Point(self.x - other.x, self.y - other.y)
    
    def __str__(self):
        return f"({self.x},{self.y})"


class Grid():
    def __init__(self):
        self.grid = [[" "] * 300 for _ in range(300)]
        self.pencil = Point(0, 0)
        self.eye = Point(0, 0)
        self.origin = Point(0,0)
        self.eye_stack = []
        self.eye_history = 0
        self.eye_movement = 0
        self.pencil_movement = 0
        self.gets = 0
        self.writes = 0
        self.max_stack = 0
        self.px = 0
        self.py = 0
        self.pout = ""
    
    def logger(names: list):
        def logging_wrapper(f):

            @wraps(f)
            def logging(self: Self, *args):
                prev_eye = self.eye + Point(0, 0)
                prev_pen = self.pencil + Point(0, 0)
                out = f(self, *args)
                if "eye" in names:
                    self.eye_history += 1
                    d = self.eye - prev_eye
                    self.eye_movement += abs(d.x) + abs(d.y)
                if "write" in names:
                    self.writes += 1
                if "pencil" in names:
                    d = self.pencil - prev_pen
                    self.pencil_movement += abs(d.x) + abs(d.y)
                if "get" in names:
                    self.gets += 1
                if "max_stack" in names:
                    self.max_stack = max(len(self.eye_stack), self.max_stack)
                return out
            return logging
        return logging_wrapper
    
    def shift_one(self):
        self.eye.x += 1
    
    def shift_back(self):
        self.eye.x -= 1
    
    @logger("eye get")
    def get(self, loc: Point = None):
        
        if loc is None:
            loc = self.eye + Point(0, 0)
        else: loc += self.origin
        self.eye = loc + Point(0, 0)

        x, y = loc
        return self.grid[y][x] 

    @logger("max_stack")
    def push(self):
        self.eye_stack.append(self.eye + Point(0, 0))
    
    def drag(self, loc: Point):
        self.origin += loc
        self.eye += loc
        self.pencil += loc
    
    def pop(self):
        self.eye = self.eye_stack.pop() + Point(0, 0)

    @logger("eye")
    def pan(self, loc: Point):
            self.origin += loc
            self.eye = self.origin + Point(0, 0)

    def newline(self):
        self.pan(Point(0, 1))  

    def get_absolute_point(self, loc: Point):
        return loc + self.origin

    @logger("pencil")
    def nudge_pencil(self, dir: Point):
        self.pencil = self.pencil + dir

    @logger("eye")
    def look(self, loc: Point):
        self.eye = loc + self.origin
    
    @logger("pencil eye write")
    def write(self, char: str, loc: Point = None):
        if loc is None:
            loc = self.pencil
        else: loc += self.origin
        self.eye = self.pencil + Point(0, 0)
        x, y = loc
        
        self.grid[y][x] = char
        self.pencil.x += 1
    
    @logger("pencil")
    def move_pencil(self, loc: Point=None):
        if loc is None: loc = self.eye - self.origin
        self.pencil = loc + self.origin

    def write_s(self, string: str):
        for char in string:
            self.write(char)
    
    def pretty(self):
        out = ""
        out += f"Pencil: {list(self.pencil + Point(0, 0))}, Origin: {list(self.origin + Point(0, 0))}, Eye: {list(self.eye + Point(0, 0))}\n"
        for row in self.grid:
            out += "".join(row).rstrip() + '\n'
        return out
    
    
    def nudge_eye(self, dir: Point):
        self.eye = (self.eye + dir)

    @logger("eye get")
    def get_absolute(self, loc: Point):
        return self.grid[loc.y][loc.x]
    
    def to_relative(self, loc: Point):
        return loc - self.origin

    def get_s(self, start: Point, length: int):
        result = ""
        for _ in range(length):
            result += self.get(start)
            start.x += 1
        return result
    
    def pretty_logs(self):
        out = "Eye History: "
        # out += ', '.join([str(list(pt)) for pt in self.eye_history])
        # out += "\nWrites: "
        # out += ', '.join(self.writes)
        return out
    