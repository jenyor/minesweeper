import config
import game
import argparse
import sys


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument("-m", "--mines", type=int,
                        help="Number of mines on the field", default=5)

    parser.add_argument("-b", "--blocks", nargs='+', type=int,
                        help="Size of the field (height and width in blocks)", default=(9, 9))

    parser.add_argument("-d", "--difficulty", type=str,
                        help="Presets of difficulty (easy, medium, hard) or custom", default="custom")

    parser.add_argument("--screensize", nargs='+', type=int,
                        help="Size of the window (width and height in pixels)", default=(800, 800))

    args = parser.parse_args()
    game_config = config.Config(tuple(args.blocks), args.mines, tuple(args.screensize), args.difficulty)
    try:
        game_config.check_values()
    except Exception as err:
        print(f"\n\033[31m ERROR: {err.args[0]} \n\033[0m")
        sys.exit(1)

    game_config.set_difficulty()
    game.Game(game_config).run()


if __name__ == "__main__":
    main()
