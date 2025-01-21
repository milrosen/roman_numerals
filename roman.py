from grid import Grid, Point



class Roman():

    def __init__(self, grid: Grid) -> None:
        self.grid = grid
    
        self.logs = []

    vals = [(1000, "M"), (500, "D"), (100, "C"), (50, "L"), (10, "X"), (5, "V"), (1, "I")]
    letters = ["I", "V", "X", "L", "C", "D", "M"]    

    def divide_macbeth_fair(self, absolute_dividend_loc :Point):
        # this version should intermix checking if we have enough letters and writing whatever
        self.grid.look(Point(0,0))
        self.grid.move_pencil(Point(0,1))
        self.fully_ungroup()
        num_ones = self.size_of_letter_run()
        copying = True
        left_steps = 0

        self.grid.look(self.grid.to_relative(absolute_dividend_loc))
        current_letter = self.grid.get()
        while self.grid.get() != " ":
            self.grid.shift_one()
        
        self.grid.push()
        self.grid.shift_back()

        full_lines = []

        while self.grid.get() != " ":
            self.grid.push()
            self.grid.shift_back()
        
        while True:
            self.grid.pop()
            l = self.grid.get()
            self.compare_lengths(absolute_dividend_loc)

            if l == " ": 
                if current_letter != "I" and (left_steps % num_ones) != 0:
                    self.grid.nudge_pencil(Point(-left_steps, 1))
                    left_steps = 0
                    current_letter = self.recall_ungroup_letter(current_letter)
                    copying = False
                    
                    self.grid.push()
                    self.grid.write(" ")
                    self.grid.nudge_pencil(Point(-1, 0))
                    self.grid.nudge_eye(Point(0, -1))
                    while self.grid.get() != " ":
                        self.grid.push()
                        self.grid.shift_one()
                    continue
                else:
                    break

            if copying:
                if l == current_letter:
                    self.grid.push()
                    self.grid.write(l)
                    self.grid.pop()
                    left_steps += 1
                    if left_steps >= num_ones:
                        self.grid.push()
                        self.grid.write_s(" ✓")
                        self.grid.pop()
                        full_lines.append(self.grid.pencil.y)
                        self.grid.nudge_pencil(Point(-left_steps-2, 1))
                        left_steps = 0
                else:
                    self.grid.push()
                    current_letter = self.recall_ungroup_letter(current_letter)
                    self.grid.write(" ")
                    self.grid.shift_back()
                    while self.grid.get() != " ":
                        self.grid.push()
                        self.grid.shift_back()
                    self.grid.shift_one()
                    self.grid.move_pencil()
                    self.grid.nudge_pencil(Point(0,1))
                    left_steps = 0
                    copying = False
            else:
                ordering = self.recall_ordering_fact(current_letter, l)

                if ordering < 0:
                    
                    ammount = self.recall_grouping_fact(current_letter)
                    self.grid.push()
                    self.grid.write_s(current_letter * ammount)
                    self.grid.pop()
                    left_steps += ammount
                    while left_steps >= num_ones:
                        self.grid.push()
                        self.grid.write_s(" ✓")
                        full_lines.append(self.grid.pencil.y)
                        self.grid.pop()
                        self.grid.nudge_pencil(Point(-left_steps-2, 1))
                        left_steps -= num_ones
                        if left_steps > 0:
                            self.grid.push()
                            self.grid.write_s(current_letter * (left_steps))
                            self.grid.pop()

                if ordering > 0:
                    
                    self.grid.push()
                    self.grid.write(" ")
                    self.grid.shift_back()
                    current_letter = self.recall_ungroup_letter(current_letter)
                    while self.grid.get() != " ":
                        self.grid.push()
                        self.grid.shift_back()
                    self.grid.nudge_pencil(Point(-left_steps-1, 1))
                    left_steps = 0
                if ordering == 0:
                    self.grid.push()
                    copying = True
                    
        if left_steps == 0:
            self.grid.nudge_pencil(Point(0, -1))
        self.grid.nudge_pencil(Point(-left_steps, 2))
        for y in full_lines:
            l = self.grid.get_absolute(Point(0, y))
            self.grid.push()
            self.grid.write(l)
            self.grid.pop()
        self.grid.write(" ")
        self.grid.shift_back()
        while self.grid.get() != " ":
            self.grid.shift_back()
        self.grid.shift_one()
        self.grid.origin = self.grid.eye + Point(0,0)


    def divide_macbeth(self, absolute_dividend_loc :Point):
        # we want the input to look like DIVISOR   DIVIDEND
        #                                          IIIIIIVIDEND -- break down number untill it's all ones

        # step one, ungroup the divisor untill it is all I's
        self.grid.look(Point(0,0))
        self.grid.move_pencil(Point(0,1))
        self.fully_ungroup()
        num_ones = self.size_of_letter_run()

        self.grid.look(self.grid.to_relative(absolute_dividend_loc))

        full_lines = []

        while True:
            self.grid.move_pencil(Point(0,1))

            self.grid.push()
            need_to_skip = self.is_improper_form()
            self.grid.pop()

            if not need_to_skip and self.grid.get() == "I" or self.grid.get() == " ": 
                break

            if need_to_skip: 
                self.copy_letter_below()
                self.ungroup_once()
                self.grid.shift_one()
            else:
                l = self.grid.get()
                if self.recall_grouping_fact(self.recall_ungroup_letter(l)) == 2 and not need_to_skip :
                    self.ungroup_letter()
                else:
                    self.ungroup_once()
                    self.grid.shift_one()
            self.copy_below()

            self.grid.newline()
            self.grid.push()
            s = self.size_of_letter_run()
            while s >= num_ones:
                full_lines.append(self.grid.get_absolute_point(Point(0,0)))
                
                self.grid.write(" ")
                self.grid.write("✓")

                self.grid.look(Point(num_ones, 0))
                self.grid.move_pencil(Point(0,1))
                self.copy_below()
                self.grid.newline()
                self.grid.push()
                s = self.size_of_letter_run()


            self.grid.pop()
            self.grid.move_pencil()
            self.grid.nudge_pencil(Point(0,1))

        self.grid.newline()
        # self.grid.move_pencil(Point(0,1))
        for pt in full_lines:
            self.grid.write(self.grid.get_absolute(pt))

    def compare_lengths(self,loc):
        self.grid.push()
        while self.grid.get() != " ":
            self.grid.shift_back()
        self.grid.shift_one()
        
        count = 0
        l1 = "A"
        l2 = "A"

        while l1 != " " and l2 != " ":
            self.grid.push()
            p = self.grid.to_relative(Point(count, loc.x))
            self.grid.get(Point(p.x, count))
            self.grid.pop()
            l2 = self.grid.get()
            self.grid.shift_one()
            count += 1

        self.grid.pop()

    def is_improper_form(self):
        l = self.grid.get()
        if l == " ": return False
        while self.grid.get() == l: self.grid.shift_one()
        return self.recall_ordering_fact(self.grid.get(), l) > 0

    def copy_letter_below(self):
        l = self.grid.get()
        while self.grid.get() == l:
            self.grid.push()
            self.grid.write(l)
            self.grid.pop()
            self.grid.shift_one()

    def copy_below(self):
        # whatever the rest of the line is, this fn copies it to wherever the pencil is
        while (l := self.grid.get()) != " ":
                self.grid.push()
                self.grid.write(l)
                self.grid.pop()
                self.grid.shift_one()

    def size_of_letter_run(self, p=None):
        if p is None: p = Point(0,0)

        out = 0

        l = self.grid.get(p)

        if l == ' ': return 0

        while self.grid.get() == l: 
            out += 1
            self.grid.shift_one()

        return out


    def fully_ungroup(self):
        self.grid.look(Point(0,0))
        while (l := self.grid.get()) != "I":
            while self.grid.get() != 'I' and self.grid.get() != ' ':
                self.ungroup_letter()
            while self.grid.get() == "I":
                self.grid.push()
                self.grid.write("I")
                self.grid.pop()
                self.grid.shift_one()
            self.grid.newline()
            self.grid.move_pencil()
            self.grid.nudge_pencil(Point(0,1))

    def ungroup_letter(self):
        # assume that the pencil is where we want to write, and the eye is where we want to look
        letter = self.grid.get()
        while (l := self.grid.get()) == letter:
            self.ungroup_once()
            self.grid.shift_one()

    def ungroup_once(self):
        ungroup_l = self.recall_ungroup_letter(self.grid.get())
        amt = self.recall_grouping_fact(ungroup_l)
        self.grid.push()
        self.grid.write_s(ungroup_l * amt)
        self.grid.pop()

    def divide(self, abosolute_dividend_loc: Point) -> None:
        letter_idx = 1
        self.grid.push()
        self.grid.move_pencil(Point(-2, 0))
        self.grid.write("I")
        self.grid.pop()
        s = [self.grid.get_absolute_point(Point(0, 0))]

        while not self.greater(self.grid.to_relative(abosolute_dividend_loc)) and letter_idx < len(self.letters):
            self.grid.look(Point(0, 0))
            self.grid.newline()
            self.sum(self.grid.to_relative(s[0]))
            self.grid.newline()
            self.grid.push()
            self.grid.move_pencil(Point(-2, 3))
            self.grid.write(self.letters[letter_idx])
            self.grid.pop()
            self.table_multiply(Point(-2, 3))
            self.grid.newline()
            self.simplify()
            self.grid.pan(Point(0, 2))
            s.append(self.grid.get_absolute_point(Point(0, 0)))
            
            letter_idx += 1
        if len(s) != len(self.letters): s.pop()
        self.grid.pan(Point(-2, 1))
        for loc in reversed(s):
            count = 1
            while not self.greater(self.grid.to_relative(abosolute_dividend_loc)):
                l = self.grid.get(self.grid.to_relative(loc) + Point(-2, 0))
                if count >= self.recall_grouping_fact(l): break
                self.grid.look(Point(0, 0))
                self.sum(self.grid.to_relative(loc))
                self.grid.newline()
                self.simplify()
                self.grid.pan(Point(25, -1))
                self.sum(self.grid.to_relative(loc) + Point(-2, 0))
                self.grid.newline()
                self.simplify()
                self.grid.pan(Point(-25, 2))
                self.grid.move_pencil(Point(0, 0))
                count += 1
            else:
                self.grid.newline()
                self.grid.look(Point(0, 0))
                self.sum(Point(0, -4))
                self.grid.pan(Point(25, 0))
                self.sum(Point(0, -4))
                self.grid.pan(Point(-25, 0))
                self.grid.newline()
        self.grid.pan(Point(20, 0))

    def write_from_decimal(self, number: int) -> None:
        for (val, letter) in self.vals:
            self.grid.write_s(letter * (number // val))
            number %= val

    def greater(self, loc: Point) -> bool:
        while True:
            l1 = self.grid.get()
            self.grid.push()
            l2 = self.grid.get(loc)
            if l1 == " " and l2 == " ": return False
            loc += Point(1, 0)
            self.grid.pop()
            self.grid.shift_one()
            o = self.recall_ordering_fact(l2, l1)

            if o == 0: continue
            return o <= 0


        
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
        
        while (l := self.grid.get()) != " ":
            self.grid.shift_one()

        self.grid.shift_back()
        prev_letter = self.grid.get()

        while True:
            l = self.grid.get()
            self.grid.shift_back()

            if l == prev_letter:
                count_letter += 1
                continue

            self.grid.push()
            self.grid.nudge_eye(Point(2, 0))
            group_letter = self.grid.get()
            grouping = self.recall_grouping_fact(group_letter)
            grouped_letter = self.recall_group_letter(group_letter)
            
            groups = count_letter // grouping

            for _ in range(groups):
                self.grid.push()
                self.grid.move_pencil() 
                self.grid.nudge_pencil(Point(0, 1))
                self.grid.write(grouped_letter)
                self.grid.pop()
                self.grid.nudge_eye(Point(grouping, 0))

            if l == " ": break
            
            count_letter = 1
            if l == grouped_letter: 
                count_letter += groups
            self.grid.pop()
            prev_letter = l

        count_out = 0
        count_letter = 0
        while (l := self.grid.get(Point(count_letter, 0))) != " ":  
            grouped_letter = self.grid.get(Point(count_letter, 1))
            if grouped_letter == " ":
                self.grid.write(l, Point(count_out, 2))
            else:
                grouping = self.recall_grouping_fact(l)
                chain_grouped_letter = self.grid.get(Point(count_letter + grouping - 1, 1))
                while chain_grouped_letter != " ":
                    chained_letter = self.grid.get(Point(count_letter + grouping - 1, 0))
                    grouping += self.recall_grouping_fact(chained_letter) - 1
                    chain_grouped_letter = self.grid.get(Point(count_letter + grouping - 1, 1))
                else:
                    self.grid.write(grouped_letter, Point(count_out, 2))
                    count_letter += grouping - 1
                    

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
        group = {"v": "i", "x": "v", "l": "x", "c": "l", "d": "c", "m": "d"}

        return group[l1].upper()

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
    

def helper_divide_macbeth(n, divisor):
    g = Grid()
    g.push()
    r = Roman(g)
    g.push()
    r.write_from_decimal(n)
    g.pop()
    g.newline()
    g.move_pencil()
    r.write_from_decimal(divisor)
    g.move_pencil(Point(0,1))
    r.divide_macbeth(Point(0,0))

    return r

def helper_divide_macbeth_fair(n, divisor):
    g = Grid()
    g.push()
    r = Roman(g)
    g.push()
    r.write_from_decimal(n)
    g.pop()
    g.newline()
    g.move_pencil()
    r.write_from_decimal(divisor)
    g.move_pencil(Point(0,1))
    r.divide_macbeth_fair(Point(0,0))

    return r

def helper_divide(n, divisor):
    g = Grid()
    g.push()
    r = Roman(g)
    r.write_from_decimal(n)
    g.move_pencil(Point(0, 1))

    g.push()
    g.write_s("  ")
    r.write_from_decimal(divisor)
    g.pop()

    g.drag(Point(2, 1))

    r.divide(Point(0, 0))
    return r

def add_entry(roman: Roman, object, divisor: int, dividend: int):
    total_pen_movement = 0
    length = 0
    width = 0

    # prev = Point(0,0)
    # for p in roman.grid.eye_history:
    #     if p.y >= length: length = p.y
    #     if p.x >= width: width = p.x

    #     d = prev - p
    #     total_eye_movement += abs(d.x) + abs(d.y)
    #     prev = p
    
    # prev = Point(0,0)
    # for _, p in roman.grid.writes:
    #     d = prev - p
    #     total_pen_movement += abs(d.x) + abs(d.y)
    #     prev = p

    for i, row in enumerate(roman.grid.grid):
        row_len = len(''.join(row[:-1]).strip())
        if row_len == 0: continue
        length = i
        width = max(row_len, width)
    
    object["num_rows"].append(length)
    object["total_eye_movement"].append(roman.grid.eye_movement)
    object["total_pen_movement"].append(roman.grid.pencil_movement)
    object["total_symbols_written"].append(roman.grid.writes)
    object["facts_recalled"].append(len(roman.logs))
    object["divisor"].append(divisor)
    object["dividend"].append(dividend)
    object["width"].append(width-1)
    object["gets"].append(roman.grid.gets)
    object["max_stack"].append(roman.grid.max_stack)

if __name__ == "__main__":
    import pandas as pd
    import tqdm

    res_milton =  {"num_rows": [], "width": [], "total_eye_movement": [], "total_pen_movement": [], "total_symbols_written": [], "facts_recalled": [], "divisor": [], "dividend": [], "max_stack": [], "gets": []}
    # res_macbeth =  {"num_rows": [], "width": [], "total_eye_movement": [], "total_pen_movement": [], "total_symbols_written": [], "facts_recalled": [], "divisor": [], "dividend": [], "max_stack": [], "gets": []}
    res_macbeth_fair =  {"num_rows": [], "width": [], "total_eye_movement": [], "total_pen_movement": [], "total_symbols_written": [], "facts_recalled": [], "divisor": [], "dividend": [], "max_stack": [], "gets": []}

    n = 3901
    d = 13

    r_milton = helper_divide(n, d)
    # r_macbeth = helper_divide_macbeth(n, d)
    r_macbeth_fair = helper_divide_macbeth_fair(n, d)

    # print(r_macbeth.grid.pretty())
    print(r_milton.grid.pretty())
    print(r_macbeth_fair.grid.pretty())

    add_entry(r_milton, res_milton, n, d)
    # add_entry(r_macbeth, res_macbeth, n, d)
    add_entry(r_macbeth_fair, res_macbeth_fair, n, d)

    print(res_milton, res_macbeth_fair)
    for n in tqdm.tqdm(range(500, 4000)):
        for divisor in range(2, 100):
            # out_correct = n // divisor
            # g = Grid()
            # r = Roman(g)
            # r.write_from_decimal(out_correct)
            # correct_r = g.get_s(Point(0, 0), 20).strip(" ")

            # r_macbeth = helper_divide_macbeth(n, divisor)
            # add_entry(r_macbeth, res_macbeth, n, divisor)
           
            r_milton  = helper_divide(n, divisor)
            add_entry(r_milton, res_milton, n, divisor)

            r_macbeth_fair = helper_divide_macbeth_fair(n, divisor)
            add_entry(r_macbeth_fair, res_macbeth_fair, n, divisor)



    df_milton = pd.DataFrame(res_milton)
    # df_macbeth = pd.DataFrame(res_macbeth)
    df_macbeth_fair = pd.DataFrame(res_macbeth_fair)

    df_milton.to_csv("./data/milton_again.csv")
    # df_macbeth.to_csv("./data/macbeth_full_gets.csv")
    df_macbeth_fair.to_csv("./data/macbeth_again.csv")

