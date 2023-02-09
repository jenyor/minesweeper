import config
import game


def hello_world():
    return "Hello World"


def main():
    game_config = config.Config((9, 9), 5, (800, 800))
    print(hello_world())

    game.Game(game_config).run()


if __name__ == "__main__":
    main()
