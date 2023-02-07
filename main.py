import board
import config


def hello_world():
    return "Hello World"


def main():
    game_config = config.Config((9, 9), 5, (800, 800))
    print(hello_world())

    game_board = board.Board().generate_random(game_config)
    print(repr(game_board))


if __name__ == "__main__":
    main()
