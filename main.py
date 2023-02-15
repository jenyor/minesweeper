import config
import game
import argparse


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-m","--mines", type=int, help="Number of mines on the field", default=5)
    parser.add_argument("-b" ,"--blocks", nargs='+', type=int, help="Size of the field (width x height in blocks)", default=(9, 9))
    parser.add_argument("-d", "--difficulty", type=int, help="Presets of difficulty", default=0)
    parser.add_argument("-scr", "--screensize", nargs='+', type=int, help="Size of the window (width x height in pixels)", default=(800, 800))

    args = parser.parse_args()
    game_config = config.Config(tuple(args.blocks), args.mines, tuple(args.screensize))

    game.Game(game_config).run()


if __name__ == "__main__":
    main()
