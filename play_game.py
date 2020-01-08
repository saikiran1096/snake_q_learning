import traceback

from snake.snake_game.console_game import SnakeGame, quit_game


def main():
    g = SnakeGame((32, 32))

    try:
        g.run()
        quit_game()
    except:
        quit_game()
        traceback.print_exc()

    print(f'Game ended with score {g.score}')


if __name__ == '__main__':
    main()
