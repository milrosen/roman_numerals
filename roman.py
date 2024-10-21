from grid import Grid, Point

class Roman():

    def __init__(self, grid: Grid) -> None:
        self.grid = grid
        self.logs = []

    vals = [(1000, "M"), (500, "D"), (100, "C"), (50, "L"), (10, "X"), (5, "V"), (1, "I")]

    def write_from_decimal(self, number: int) -> None:
        for (val, letter) in self.vals:
            self.grid.write_s(letter * (number // val))
            number %= val

    def compare(self, loc: Point) -> bool:
        while True:
            l1 = self.grid.get()
            self.grid.push()
            l2 = self.grid.get(loc)
            loc += Point(1, 0)
            self.grid.pop()
            self.grid.shift_one()
            o = self.recall_ordering_fact(l1, l2)

            if o == 0: continue
            return o > 0


        
    def table_multiply(self, loc: Point):
        count_out = 0
        self.grid.push()
        letter = self.grid.get(loc)
        self.grid.pop()

        while (l := self.grid.get()) != " ":
            out = self.recall_multiply_fact(l, letter)
            self.grid.push()
            self.grid.move_pencil(Point(count_out, 1))
            self.grid.write_s(out)
            self.grid.pop()
            self.grid.shift_one()
            count_out += len(out)


    def simplify(self) -> None:
        self.grid.move_pencil(Point(0, 1))
        count_letter = 0
        prev_letter = ""
        
        while self.grid.get() != " ":
            self.grid.shift_one()
        
        self.grid.shift_back()
        prev_letter = self.grid.get()
        
        while (l := self.grid.get()) != " ":
            if l == prev_letter: 
                count_letter += 1
                self.grid.shift_back()
                continue
            
            grouping = self.recall_grouping_fact(prev_letter)
            groups = count_letter // grouping
            self.grid.move_pencil()
            self.grid.nudge_pencil(Point(1, 1))
            self.grid.push()
            grouped_letter = self.recall_group_letter(prev_letter)
            if (groups > 0): self.grid.write(grouped_letter)
            self.grid.pop()

            self.grid.shift_back()
            if grouped_letter == l: 
                count_letter = 1 + groups
            else: 
                count_letter = 1

            prev_letter = l

        grouping = self.recall_grouping_fact(prev_letter)
        next_letter = self.recall_group_letter(prev_letter)
        print(next_letter[0])
        groups = count_letter // grouping
        self.grid.move_pencil()
        self.grid.nudge_pencil(Point(1, 1))
        self.grid.push()
        if groups > 0: self.grid.write_s(next_letter + "")
        self.grid.pop()

        count_out = 0
        count_letter = 0
        while (l := self.grid.get(Point(count_letter, 0))) != " ":  
            grouped_letter = self.grid.get(Point(count_letter, 1))
            print(grouped_letter)
            if grouped_letter == " ":
                self.grid.write(l, Point(count_out, 2))
            else:
                self.grid.write(grouped_letter, Point(count_out, 2))
                count_letter += self.recall_grouping_fact(l) -1

            count_letter += 1
            count_out += 1


        
    def sum(self, other_start: Point) -> None:
        l1 = ""
        l2 = ""
        self.grid.move_pencil(Point(0, 1))
        while l1 != " " or l2 != " ":
            l1 = self.grid.get()
            self.grid.push()

            l2 = self.grid.get(other_start)
            print(l1, l2, list(self.grid.eye))
            ord = self.recall_ordering_fact(l1, l2)
            if ord > 0:
                self.grid.write(l1)
                self.grid.pop()
                self.grid.shift_one()
            if ord < 0:
                self.grid.push()
                self.grid.write(l2)
                self.grid.pop()
                self.grid.pop()
                other_start.x += 1
            if ord == 0:
                self.grid.write_s(l1 + l2)
                self.grid.pop()
                self.grid.shift_one()
                other_start.x += 1

    def recall_ordering_fact(self, l1, l2):
        l1, l2 = l1.lower(), l2.lower()
        if l1 != " " and l2 != " ": 
            self.logs.append(("recalls ordering fact", l1, l2))

        ordering = [" ", "i", "v", "x", "l", "c", "d", "m"]
        return ordering.index(l1) - ordering.index(l2)
    
    def recall_grouping_fact(self, l1):
        l1 = l1.lower()
        self.logs.append(("recalls grouping fact", l1))
        grouping = {"i": 5, "v": 2, "x": 5, "l": 2, "c": 5, "d": 2, "m": 20}

        return grouping[l1]
    
    def recall_group_letter(self, l1):
        l1 = l1.lower()
        self.logs.append(("recalls group letter", l1))
        group = {"i": "v", "v": "x", "x": "l", "l": "c", "c": "d", "d": "m", "m": "m"}
        
        return group[l1].upper()
    
    def recall_ungroup_letter(self, l1):
        l1 = l1.lower()
        self.logs.append(("recalls ungroup letter", l1))

    def index(l):
        return [" ", "i", "v", "x", "l", "c", "d", "m"].index(l) - 1

    def recall_multiply_fact(self, l1, l2):
        
        l1, l2 = l1.lower(), l2.lower()

        self.logs.append(("recalls multiply fact", l1, l2))

        table = [
            ["i", "v",   "x",    "l",     "c",    "d",    "m"],
            ["v", "xxv", "l",    "ccl",   "d",    "mmd",  "m"*5],
            ["x", "l",   "c",    "d",     "m",    "m"*5,  "m"*10],
            ["l", "ccl", "d",    "mmd",   "m"*5,  "m"*25, "m"],
            ["c", "d",   "m",    "m"*5,   "m"*10, "m",    "m"],
            ["d", "mmd", "m"*5,  "m"*25,  "m",    "m",    "m"],
            ["m", "m"*5, "m"*10, "m",     "m",    "m",    "m"],  
        ]

        return table[Roman.index(l1)][Roman.index(l2)].upper()