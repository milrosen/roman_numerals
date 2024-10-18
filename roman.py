import math
from cost import Cost
from typing import Self
import os
import random
from functools import partial as p

class RomanNumeral:
    place_values  = [1000, 500, 100, 50, 10, 5, 1]
    group_letters = [ 5,   2,   5,   2,   5,   2,   5]
    place_letters = ['M', 'D', 'C', 'L', 'X', 'V', 'I']
    '''
    each Roman Numeral is represented by an array containin the number of letters of that type
        [3, 1, 1, 1, 4, 0, 1] = MMMDCLXXXXI = 3691

    functions are not in-place unless specified

    operations return (cost, result) tuples
    '''
    def __init__(self, n: int) -> None:
        self.values = []
        for v in RomanNumeral.place_values:
            self.values.append(math.floor(n / v))
            n %= v

    def first_nonzero(self, i):
        for l, v in list(zip(RomanNumeral.place_letters, self.values))[i:]:
            if v != 0: return l

    def from_str(s: str) -> Self:
        r = RomanNumeral(0)
        for l in s:
            if RomanNumeral.place_letters.__contains__(l):
                i = RomanNumeral.place_letters.index(l)
                r.values[i] += 1
        return r
    
    def val(self):
        out = 0
        for val, amt in zip(RomanNumeral.place_values, self.values):
            out += val * amt
        return out
    
    def pretty(self):
        out = ''
        for l,v in zip(RomanNumeral.place_letters, self.values):
            out += l * v
        return out

    def multiplication_table():
        table = []
        for i in RomanNumeral.place_values:
            row = []
            for j in RomanNumeral.place_values:
                row.append(RomanNumeral(i * j))
            table.append(row)
        return table

    
    # in place
    def simplify(self, cost: Cost):
        id = cost.start_action("Simplify")
        processed_acc = len(self.pretty()) - self.values[-1]
        for i in range(len(self.values) -1, 0, -1):
            letter = RomanNumeral.place_letters[i] 
            grouping = self.values[i] // RomanNumeral.group_letters[i]
            if self.values[i] != 0: 
                cost.recall_grouping_fact(letter, RomanNumeral.group_letters[i])
            if grouping > 0:
                cost.move_pencil(processed_acc, 0)
                cost.rewrite(letter * self.values[i], letter * (RomanNumeral.group_letters[i] % self.values[i]))
                next_letter = RomanNumeral.place_letters[i-1]
                processed_acc -= self.values[i-1]
                cost.move_pencil(processed_acc, 1)
                cost.rewrite(next_letter * self.values[i-1], next_letter * (self.values[i-1]+grouping))
            self.values[i-1] += grouping
            self.values[i]   %= RomanNumeral.group_letters[i]
            
        cost.finish_action("Simplify", id)

    def sum(self, o: Self, cost: Cost) -> Self:
        id = cost.start_action("sum")

        s_len = len(self.pretty())

        self_considered, other_considered, result_len = [0, 0, 0]
        for i, (sv, ov, l) in enumerate(zip(self.values, o.values, RomanNumeral.place_letters)): 
            if sv == ov and sv == 0: continue
            if sv == 0: cost.recall_ordering_fact(l, self.first_nonzero(i))
            if ov == 0: cost.recall_ordering_fact(l, o.first_nonzero(i))
            
            self_considered += sv
            other_considered += ov
            result_len += sv + ov
            cost.move_eye(self_considered, 0)
            cost.move_eye(s_len, 0)
            cost.move_eye(s_len+other_considered, 0)
            cost.move_pencil(result_len, 1)

        cost.finish_action("sum", id)
        out = RomanNumeral(0)
        out.values = [i + j for i,j in zip(self.values, o.values)]
        return out
    

    def naieve_mul(self, n, cost: Cost):
        r = RomanNumeral(0)
        r.values = [x * n for x in self.values]
        id = cost.start_action("Naieve Mul")
        [cost.rewrite(l * v, l * v * n) for (l, v) in zip(RomanNumeral.place_letters, self.values) if v != 0]
        cost.finish_action("Naieve Mul", id)
        return r
    
    def table_mul(self, table, o: Self, cost: Cost) -> tuple[Self, int]:
        out = ''
        id = cost.start_action("Table Mul")
        for i, v1 in enumerate(self.values):
            for j, v2 in enumerate(o.values):
                t = table[i][j].pretty() * v1 * v2
                out += t
                if v1 != 0 and v2 != 0:
                    letters1 = v1 * RomanNumeral.place_letters[i]
                    letters2 = v2 * RomanNumeral.place_letters[j]
                    cost.recall_multiplication_fact(letters1, letters2, t)
                    cost.rewrite(letters1, t)
        outr = RomanNumeral.from_str(out)
        outr.simplify(cost)
        cost.finish_action("Table Mul", id)
        return outr
    
    def less(self, r, cost: Cost):
        id = cost.start_action("Compare")
        cost.finish_action("Compare", id)
        return self.val() < r.val()
    
    def __compose__(f, g):
        def h(r, cost):
            r1 = g(r, cost)
            r2 = f(r1, cost)
            return r2
        return h
    
    def less_add(self, r1, r2, cost: Cost):
        return RomanNumeral.__compose__(p(RomanNumeral.less, self), p(RomanNumeral.sum, r1))(r2, cost)

    def division_algorithm(self, divisor: Self):
        cost = Cost()
        id = cost.start_action("Division")
        table = RomanNumeral.multiplication_table()
        out_string = ''

        out_string += '----------------\n'
        out_string += f'{self.pretty()} ÷ {divisor.pretty()}\n'
        out_string += '---------------\n'

        primitives = list(map(RomanNumeral.from_str, RomanNumeral.place_letters))
        stack = []

        for letter in reversed(primitives):
            right_base = divisor.table_mul(table, letter, cost)
            out_string += '{0} -- {1}'.format(letter.pretty(), right_base.pretty()) + "\n"
            if self.less(right_base, cost): break
            stack.append((letter, right_base))
        
        out_string += '----------------\n' 
        out_string += f'{self.pretty()} ÷ {divisor.pretty()}\n'
        out_string += '----------------\n'

        accl, accr = RomanNumeral(0), RomanNumeral(0)
        for l, divisor in reversed(stack):
            count = 0
            while not self.less_add(accr, divisor, cost):
                count += 1
                r_ = divisor.naieve_mul(count, cost)
                r_.simplify(cost)
                accr = accr.sum(divisor, cost)
                accr.simplify(cost)
                accl = accl.sum(l, cost)
                accl.simplify(cost)

                a, b, c, d = list(map(RomanNumeral.pretty, [l, r_, accl, accr]))
                out_string += '\033[92mUNDER {0: <5} {1: <10} --- {2: <10} {3}\033[0m\n'.format(a * count, b, c, d)
            else:
                amt = RomanNumeral.group_letters[RomanNumeral.place_letters.index(l.pretty())]
                if amt-1 == count: continue

                r_ = divisor.naieve_mul(count+1, cost)
                r_.simplify(cost)
                accr_over = accr.sum(divisor, cost)
                accr_over.simplify(cost)
                accl_over = accl.sum(l, cost)
                accl_over.simplify(cost)

                a, b, c, d = list(map(RomanNumeral.pretty, [l, r_, accl_over, accr_over]))
                out_string += '\033[91mOVER  {0: <5} {1: <10} --- {2: <10} {3}\033[0m\n'.format(a * (count+1), b, c, d)
        cost.finish_action("Division", id)
        out_string += f'{self.pretty()} ÷ {divisor.pretty()} = {accl.pretty()} R {RomanNumeral(self.val() - accr.val()).pretty()}\n'
        out_string += f'{self.val()} ÷ {divisor.val()} = {accl.val()} R{self.val() - accr.val()}\n'
        # out_string += f'{self.val()} ÷ {r.val()} = {math.floor(self.val() / r.val())} R{self.val() % r.val()}\n'

        return out_string, accl, RomanNumeral(self.val()-accr.val())
            
table = RomanNumeral.multiplication_table()

x = RomanNumeral(random.randint(500,4000))
y = RomanNumeral(random.randint(0,100))

# x = RomanNumeral(3996)
# y = RomanNumeral(3)

os.system('color')
pretty, res, rem = x.division_algorithm(y)
print(pretty)

# things to consider: number of times we multiply with table
# scanning the numbers themselves
# writing a symbol
# how many symbols to keep in mind at the same time
# eye movements for naieve mul, remembering how many times you've copied
# counting backward, and also keeping track of the counting, grouping, and rewriting
# idea: do the same thing for arabic numbers
