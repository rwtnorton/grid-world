from gridworld.positions import neighborhood, neighbors


def test_neighors():
    pos = (2, 3)
    assert neighbors(pos) == {(1, 3), (3, 3), (2, 2), (2, 4)}


def test_neighborhood():
    assert neighborhood(dimensions=(2, 2), position=(0, 0)) == {
        (0, 1),
        (1, 0),
    }
    assert neighborhood(dimensions=(1, 1), position=(0, 0)) == set()
    assert neighborhood(dimensions=(3, 3), position=(1, 1)) == {
        (0, 1),
        (1, 0),
        (1, 2),
        (2, 1),
    }
    assert neighborhood(dimensions=(2, 2), position=(1, 1)) == {
        (0, 1),
        (1, 0),
    }
