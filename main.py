import config
import game


def main():
    game_config = config.Config((9, 9), 5, (800, 800))

    game.Game(game_config).run()


if __name__ == "__main__":
    main()
