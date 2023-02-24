import pytest

from config import Config

# TODO test: set_difficulty, calculate_screen


@pytest.mark.constructor
@pytest.mark.parametrize("num_mines, cells_in_board", [(0, (10, 10)), (20, (4, 5)), (200, (5, 5))])
def test_init_incorrect_mines_and_cells_in_board(num_mines, cells_in_board):
    with pytest.raises(Exception):
        Config(cells_in_board, num_mines, (1, 1), "custom")


@pytest.mark.constructor
@pytest.mark.parametrize("screen_size", [(-10, 10), (0, 10)])
def test_init_incorrect_screen_size(screen_size):
    with pytest.raises(Exception):
        Config((10, 10), 1, screen_size, "custom")


@pytest.mark.constructor
@pytest.mark.parametrize("difficulty", ["lol", "", "eas"])
def test_init_incorrect_difficulty(difficulty):
    with pytest.raises(Exception):
        Config((10, 10), 1, (1, 1), difficulty)


@pytest.mark.constructor
@pytest.mark.parametrize("screen_size, difficulty", [((1, 2), "custom")])
@pytest.mark.parametrize("cells_in_board, num_of_mines", [((1, 4), 3)])
def test_init_correct_arguments(cells_in_board, num_of_mines, screen_size, difficulty):
    Config(cells_in_board, num_of_mines, screen_size, difficulty)
