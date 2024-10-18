import random

from cost import Cost
from roman import RomanNumeral

def test_back_to_front():
    n=40
    divisiors = [random.randint(1, 100) for _ in range(n)]
    dividends = [random.randint(400, 1000) for _ in range(n)]

    for x, y in zip(dividends, divisiors):
        xr = RomanNumeral(x)
        yr = RomanNumeral(y)

        strout, result, remainder = xr.division_algorithm(yr, Cost())
        print(strout)
        true_result = x // y
        true_remainder = x % y
        assert true_remainder == remainder.val() and true_result == result.val()

def test_add():
    l = RomanNumeral(27)
    r = RomanNumeral(3)

    c = Cost()
    s = l.sum(r, c)
    s.simplify(c)

    print(s.pretty())
    assert s.val() == 30

def test_table():
    l1 = RomanNumeral(random.randint(50, 300))
    l2 = RomanNumeral.from_str(RomanNumeral.place_letters[random.randint(3, len(RomanNumeral.place_letters) -1)])
    res = l1.table_mul(RomanNumeral.multiplication_table(), l2, Cost())

    print(l1.pretty(), l2.pretty(), res.pretty())
    assert res.val() == l1.val() * l2.val()

for i in range(50): test_table()