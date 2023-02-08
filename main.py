import config
import game


def hello_world():
    return "Hello World"


def main():
    game_config = config.Config((4, 4), 5, (1000, 800))
    print(hello_world())

    game.Game(game_config).run()


if __name__ == "__main__":
    main()
