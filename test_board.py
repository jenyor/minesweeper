from itertools import chain

from board import Board
import config
from cell import Cell


def test_generate_random():
    MAGIC_NUM = 10
    board1 = Board.generate_random(config.Config((MAGIC_NUM, MAGIC_NUM), MAGIC_NUM, (1, 1), "custom"))

    num_of_mines = 0
    for piece in chain.from_iterable(board1.get_all_cells()):
        num_of_mines += piece.is_mine()

    assert num_of_mines == board1.num_of_mines


def test_find_adjacent_cells():
    size = (4, 6)
    board = Board.generate_random(config.Config(size, size[1], (1, 1), "custom"))

    assert board.get_cell_in_pos((0, 1)).adjacent_cells == [
        board.cells[0][0],
        board.cells[0][2],
        board.cells[1][0],
        board.cells[1][1],
        board.cells[1][2],
    ]
    assert board.get_cell_in_pos((0, 0)).adjacent_cells == [board.cells[0][1], board.cells[1][0], board.cells[1][1]]
    assert board.get_cell_in_pos((2, 2)).adjacent_cells == [
        board.cells[1][1],
        board.cells[1][2],
        board.cells[1][3],
        board.cells[2][1],
        board.cells[2][3],
        board.cells[3][1],
        board.cells[3][2],
        board.cells[3][3],
    ]


def test_process_adjacent_cells():
    # .**
    # .*.
    # *..
    # Answer
    # 222
    # 333
    # 121
    board = Board(
        (3, 3),
        4,
        [
            [Cell.new_pure(), Cell.new_mine(), Cell.new_mine()],
            [Cell.new_pure(), Cell.new_mine(), Cell.new_pure()],
            [Cell.new_mine(), Cell.new_pure(), Cell.new_pure()],
        ],
    )
    board.process_adjacent_cells()
    answer = [[2, 2, 2], [3, 3, 3], [1, 2, 1]]
    mines = []
    [mines.append([item.adjacent_mines for item in row]) for row in board.cells]
    assert answer == mines


def test_click_cell():
    board = Board(
        (3, 5),
        5,
        [
            [Cell.new_pure(), Cell.new_mine(), Cell.new_mine(), Cell.new_pure(), Cell.new_pure()],
            [Cell.new_pure(), Cell.new_mine(), Cell.new_pure(), Cell.new_pure(), Cell.new_pure()],
            [Cell.new_mine(), Cell.new_pure(), Cell.new_pure(), Cell.new_pure(), Cell.new_pure()],
        ],
    )
    board.process_adjacent_cells()
    board.click_cell(board.cells[2][3], False)
    closed = [[1, 1, 1, 0, 0], [1, 1, 0, 0, 0], [1, 1, 0, 0, 0]]
    found = []
    [found.append([1 if item.is_closed() else 0 for item in row]) for row in board.cells]
    assert found == closed
