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
    
    def val(self) -> int:
        out = 0
        for val, amt in zip(RomanNumeral.place_values, self.values):
            out += val * amt
        return out
    
    def pretty(self) -> str:
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
    def simplify(self, cost=Cost()):
        p = self.pretty()
        for i in range(len(self.values) -1, 0, -1):
            grouping = self.values[i] // RomanNumeral.group_letters[i]
            self.values[i-1] += grouping
            self.values[i]   %= RomanNumeral.group_letters[i]
        if p != self.pretty(): cost.op("simplify", p, "", self.pretty())
            

    def sum(self, o: Self, cost=Cost()) -> Self:
        out = RomanNumeral(0)
        out.values = [i + j for i,j in zip(self.values, o.values)]
        if out.val() != 0 and self.val() != 0: 
            cost.op("sum", self.pretty(), o.pretty(), out.pretty())
        return out
    

    def naieve_mul(self, n, cost=Cost()) -> Self:
        r = RomanNumeral(0)
        r.values = [x * n for x in self.values]
        if n != 1: cost.op("naieve_mul", self.pretty(), str(n), r.pretty())
        return r
    
    def table_mul(self, table, o: Self, cost=Cost()) -> Self:
        out = ''
        for i, v1 in enumerate(self.values):
            for j, v2 in enumerate(o.values):
                t = table[i][j].pretty() * v1 * v2
                out += t
        outr = RomanNumeral.from_str(out)
        if o.val() != 1: cost.op("table_mul", self.pretty(), o.pretty(), out)
        return outr
    
    def less(self, r, cost=Cost() )-> bool:
        cost.op("less", self.pretty(), r.pretty(), "left" if self.val() < r.val() else "right")
        return self.val() < r.val()
    
    def __compose__(f, g):
        def h(r, cost):
            r1 = g(r, cost)
            r1.simplify(cost)
            r2 = f(r1, cost)
            return r2
        return h
    
    def less_add(self, r1, r2, cost=Cost()) -> Self:
        return RomanNumeral.__compose__(p(RomanNumeral.less, self), p(RomanNumeral.sum, r1))(r2, cost)

    def division_algorithm(self, divisor: Self, cost):
        table = RomanNumeral.multiplication_table()
        out_string = ''

        out_string += '----------------\n'
        out_string += f'{self.pretty()} ÷ {divisor.pretty()}\n'
        out_string += '---------------\n'

        primitives = list(map(RomanNumeral.from_str, RomanNumeral.place_letters))
        stack = []

        for letter in reversed(primitives):
            if letter.val() * divisor.val() > self.val():
                self.less(RomanNumeral(letter.val() * divisor.val()), cost)
                break
            right_base = divisor.table_mul(table, letter, cost)
            right_base.simplify(cost)
            self.less(right_base, cost)
            out_string += '{0} -- {1}'.format(letter.pretty(), right_base.pretty()) + "\n"
            stack.insert(0, (letter, right_base))
        
        out_string += '----------------\n' 
        out_string += f'{self.pretty()} ÷ {divisor.pretty()}\n'
        out_string += '----------------\n'

        cost.begin_phase("division")
        accl, accr = RomanNumeral(0), RomanNumeral(0)
        for l, divisor in stack:
            count = 0
            while not self.less_add(accr, divisor):
                count += 1
                
                _r = divisor.naieve_mul(count)
                _r.simplify()
                accr = accr.sum(divisor, cost)
                accr.simplify(cost)
                accl = accl.sum(l, cost)
                accl.simplify(cost)

                a, b, c, d = list(map(RomanNumeral.pretty, [l, _r, accl, accr]))
                out_string += '\033[92mUNDER {0: <5} {1: <10} --- {2: <10} {3}\033[0m\n'.format(a * count, b, c, d)
            else:
                if count == 0: continue

                self.less(accr.sum(divisor), cost)

                _r = divisor.naieve_mul(count+1)
                amt = RomanNumeral.group_letters[RomanNumeral.place_letters.index(l.pretty())]

                if amt-1 == count: continue
                _r.simplify()
                accr_over = accr.sum(divisor)
                accr_over.simplify()
                accl_over = accl.sum(l)
                accl_over.simplify()

                a, b, c, d = list(map(RomanNumeral.pretty, [l, _r, accl_over, accr_over]))
                out_string += '\033[91mOVER  {0: <5} {1: <10} --- {2: <10} {3}\033[0m\n'.format(a * (count+1), b, c, d)
        out_string += f'{self.pretty()} ÷ {divisor.pretty()} = {accl.pretty()} R {RomanNumeral(self.val() - accr.val()).pretty()}\n'
        out_string += f'{self.val()} ÷ {divisor.val()} = {accl.val()} R{self.val() - accr.val()}\n'
        # out_string += f'{self.val()} ÷ {r.val()} = {math.floor(self.val() / r.val())} R{self.val() % r.val()}\n'

        return out_string, accl, RomanNumeral(self.val()-accr.val())