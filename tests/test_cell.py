from cell import Cell


def test_toogle_flag():
    cell1 = Cell.new_mine()
    cell1.toogle_flag()
    assert cell1.is_marked()
    cell1.toogle_flag()
    assert not cell1.is_marked()
