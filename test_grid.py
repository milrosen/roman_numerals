from grid import Grid, Point

def test_grid_loggs():
    g = Grid()
    g.get(Point(30, 1))
    g.get(Point(1, 30))

    for pt in g.eye_history:
        print(list(pt))

    assert g.eye_history == [Point(0, 0), Point(30, 1), Point(1, 30)]

def test_grid_write():
    g = Grid()
    g.write("a")

    print(g.pretty())
    assert g.get() == "a"
