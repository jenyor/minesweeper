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
