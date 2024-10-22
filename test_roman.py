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
    g.write_s("CCLXXVV")
    g.pop()

    r = Roman(g)

    r.simplify()
    print(g.pretty_logs())
    print(g.pretty())
    print(r.logs)
    assert g.get_s(Point(0, 2), 6) == "CCLXXX"

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
    assert g.get_s(Point(0, 1), 6) == "LVI"