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

@pytest.mark.constructor
@pytest.mark.parametrize("difficulty", ["easy", "medium", "hard", "custom"])
def test_set_difficulty(difficulty):
    test_config = Config((10, 10), 50, (500, 500), difficulty)
    test_config.set_difficulty()
    match(difficulty):
        case "easy":
            assert test_config.num_of_mines == 10 and test_config.cells_in_board == (9, 9)
        case "medium":
            assert test_config.num_of_mines == 40 and test_config.cells_in_board == (16, 16)
        case "hard":
            assert test_config.num_of_mines == 99 and test_config.cells_in_board == (22, 22)
        case "custom":
            assert test_config.num_of_mines == 50 and test_config.cells_in_board == (10, 10)

@pytest.mark.constructor
@pytest.mark.parametrize("cells_in_board", [(10, 10), (25, 10), (20, 20)])
def test_calculate_screen(cells_in_board):
    test_config = Config(cells_in_board, 5, (500, 500), "custom")
    test_config.calculate_screen(cells_in_board)
    if(cells_in_board[0] * cells_in_board[1] <= 144):
        assert test_config.screen_size[0] == cells_in_board[1] * 50 and test_config.screen_size[1] == cells_in_board[0] * 50
    else:
        assert test_config.screen_size[0] == cells_in_board[1] * 40 and test_config.screen_size[1] == cells_in_board[0] * 40
