import unittest
from itertools import chain

from board import *
import config


class BoardUnitTests(unittest.TestCase):
    def test_generate_random(self):
        MAGIC_NUM = 10
        board = Board.generate_random(config.Config((MAGIC_NUM, MAGIC_NUM), MAGIC_NUM, (1, 1)))

        num_of_mines = 0
        for piece in chain.from_iterable(board.get_all_cells()):
            num_of_mines += piece.is_mine()

        self.assertEqual(num_of_mines, board.num_of_mines)

    def test_find_adjacent_cells(self):
        size = (4, 6)
        board = Board.generate_random(config.Config(size, size[1], (1, 1)))

        self.assertEqual(
            board.get_cell_in_pos((0, 1)).adjacent_cells,
            [board.cells[0][0], board.cells[0][2], board.cells[1][0], board.cells[1][1], board.cells[1][2]],
        )
        self.assertEqual(
            board.get_cell_in_pos((0, 0)).adjacent_cells,
            [board.cells[0][1], board.cells[1][0], board.cells[1][1]],
        )
        self.assertEqual(
            board.get_cell_in_pos((2, 2)).adjacent_cells,
            [
                board.cells[1][1],
                board.cells[1][2],
                board.cells[1][3],
                board.cells[2][1],
                board.cells[2][3],
                board.cells[3][1],
                board.cells[3][2],
                board.cells[3][3],
            ],
        )
