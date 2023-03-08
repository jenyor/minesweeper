import config
import game
import argparse
import sys


def main():
    """
    Creates a argparse.ArgumentParser class.
    It parses values, written to console and sets some configuration of the game
    """
    parser = argparse.ArgumentParser()

    parser.add_argument("-m", "--mines", type=int, help="Number of mines on the field", default=5)

    parser.add_argument(
        "-b", "--blocks", nargs="+", type=int, help="Size of the field (height and width in blocks)", default=(9, 9)
    )

    parser.add_argument(
        "-d", "--difficulty", type=str, help="Presets of difficulty (easy, medium, hard) or custom", default="custom"
    )

    parser.add_argument(
        "--screensize", nargs="+", type=int, help="Size of the window (width and height in pixels)", default=()
    )

    args = parser.parse_args()

    # Trying to check values of the config, to avoid too big amount of mines or negative screen size, fields or mines
    try:
        game_config = config.Config(tuple(args.blocks), args.mines, tuple(args.screensize), args.difficulty)
    except Exception as err:
        print(f"\n\033[31m ERROR: {err.args[0]} \n\033[0m")
        sys.exit(1)
    # If some Exception occured, it will tell user what's the problem in program and exit from the game
    start = True
    # Returns true if Space key pressed. Space is used for restart game with the same configuration and board
    while start:
        start = game.Game(game_config).run()
    # If Space key wasn't pressed, the game will start only once


if __name__ == "__main__":
    main()
