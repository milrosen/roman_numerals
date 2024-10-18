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

        strout, result, remainder = xr.division_algorithm(yr)

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

test_add()
