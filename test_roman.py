from grid import Point, Grid
from roman import Roman

def test_roman_sum():
    g = Grid()
    g.push()
    g.write_s("MDCVII CLXVI")
    g.pop()

    r = Roman(g)
    r.sum(Point(7, 0))

    for log in r.logs:
        print(log)
    print(g.pretty())
    print(g.pretty_logs())
    assert g.get_s(Point(0, 1), 11) == "MDCCLXVVIII"

def test_origin():
    g = Grid()
    g.write_s("ORIGIN")
    g.drag(Point(2,2))

    g.move_pencil(Point(0, 0))
    g.push()
    g.write_s("XX L")
    g.pop()

    assert g.get() == "X"

    r = Roman(g)
    r.sum(Point(3, 0))
    print(g.pretty())
    assert(g.get_s(Point(0, 1), 3) == "LXX")

def test_simplify():
    g = Grid()

    g.push()
    g.write_s("MDDCVIIIII")
    g.pop()

    r = Roman(g)

    r.simplify()
    print(g.pretty_logs())
    print(g.pretty())
    print(r.logs)
    assert g.get_s(Point(0, 2), 4) == "MMCX"

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

def test_compare():
    g = Grid()
    g.push()
    g.write_s("D MDXVI")
    g.pop()

    r = Roman(g)
    out = r.compare(Point(3, 0))
    print(g.pretty_logs())
    print(g.pretty())
    print(r.logs)
    assert not out

def test_write_from_decimal():
    g = Grid()
    g.push()
    r = Roman(g)
    r.write_from_decimal(1234)
    print(g.pretty_logs())  
    print(g.pretty())
    assert g.get_s(Point(0, 0), 10) == "MCCXXXIIII"