import math
import random
from grid import Point, Grid
from roman import Roman

def test_roman_sum():
    g = Grid()
    g.push()
    g.write_s("DLX DLX")
    g.pop()

    r = Roman(g)
    r.sum(Point(4, 0))

    for log in r.logs:
        print(log)
    print(g.pretty())
    print(g.pretty_logs())
    assert g.get_s(Point(0, 1), 6) == "DDLLXX"
def test_origin():
    g = Grid()
    g.write_s("ORIGIN")
    g.drag(Point(3,4))

    g.move_pencil(Point(0, 0))
    g.push()
    g.write_s("CCLXXVV")
    g.pop()

    r = Roman(g)
    r.simplify()
    print(g.pretty_logs())
    print(g.pretty())
    print(r.logs)
    assert(g.get_s(Point(0, 2), 6) == "CCLXXX")

def test_simplify():
    g = Grid()

    g.push()
    g.write_s("MLLLLVVV")
    g.pop()

    r = Roman(g)

    r.simplify()
    print(g.pretty_logs())
    print(g.pretty())
    print(r.logs)
    assert g.get_s(Point(0, 2), 20).strip(" ") == "MCCXV"

def test_table():
    g = Grid()
    g.push()
    g.write_s("L XXVI")
    g.pop()
    g.drag(Point(2, 0))
    print(g.pretty())

    r = Roman(g)
    r.table_multiply(Point(-2, 0))
    print(g.pretty_logs())
    print(g.pretty())
    print(r.logs)
    assert g.get_s(Point(0, 1), 6) == "DDCCLL"

def test_greater():
    g = Grid()
    g.push()
    g.write_s("MM MDXVI")
    g.pop()

    r = Roman(g)
    out = r.greater(Point(3, 0))
    print(g.pretty_logs())
    print(g.pretty())
    print(r.logs)
    assert out

def test_write_from_decimal():
    g = Grid()
    g.push()
    r = Roman(g)
    r.write_from_decimal(1234)
    print(g.pretty_logs())  
    print(g.pretty())
    assert g.get_s(Point(0, 0), 10) == "MCCXXXIIII"

def test_divide():
    g = Grid()
    g.push()
    r = Roman(g)
    r.write_from_decimal(3996)
    g.move_pencil(Point(0, 1))

    g.push()
    g.write_s("  III")
    g.pop()

    g.drag(Point(2, 1))

    r.divide(Point(0, 0))

    print(g.pretty_logs())  
    print(g.pretty())   
    print(r.logs)
    assert g.get_s(Point(5, 0), 9) == "MCCCXXXII"

def divide_numbers(n, divisor):
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

    # print(g.pretty_logs())  
    print(g.pretty())   
    # print(r.logs)
    return g.get_s(Point(0, 0), 20).strip(" ")

def test_divide_numbers():
    for i in range(1, 500):
        n = random.randint(100, 4000)
        divisor = random.randint(1, 100)
        n, divisor = 1663, 43
        print(n, divisor)
        out_r = divide_numbers(n, divisor)

        out_correct = n // divisor
        g = Grid()
        r = Roman(g)
        r.write_from_decimal(out_correct)
        correct_r = g.get_s(Point(0, 0), 20).strip(" ")
        print("true " + correct_r, "returned " + out_r)
        assert 0 == 1
        assert correct_r == out_r

def test_ungroup_letters():
    g = Grid()
    g.push()
    r = Roman(g)
    r.write_from_decimal(16)
    g.pop()
    g.move_pencil(Point(0,1))
    print(g.pretty())
    r.ungroup_letter()

    print(g.pretty())

    assert g.get_s(Point(0,1), 20).strip(" ") == "VV"

def test_fully_ungroup_letter():
    g = Grid()
    g.push()
    r = Roman(g)
    r.write_from_decimal(15)
    g.pop()
    g.move_pencil(Point(0,1))
    print(g.pretty())
    r.fully_ungroup()

    print(g.pretty())

    assert g.get_s(Point(0,0), 20).strip(" ") == "I" * 15

def test_divide_macbeth():
    n = 672
    divisor = 45
    
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
    print(g.pretty())
    out_r = g.get_s(Point(0,1), 20).strip(" ")
    g.pop()

    out_correct = n // divisor
    g = Grid()
    r = Roman(g)
    r.write_from_decimal(out_correct)
    correct_r = g.get_s(Point(0, 0), 20).strip(" ")
    assert 0 == 1
    assert out_r == correct_r


   