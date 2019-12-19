"""
snake.py

author:         Stephen Radley
date:           2018/07/05
package:        snake
version:        0.0.1
x"""
import traceback

from snake.snake_game.game import SnakeGame, quit_game

"""
main ...
"""


def main():
    g = SnakeGame((40, 20))

    try:
        g.run()
        quit_game()
    except:
        quit_game()
        traceback.print_exc()

    print(f'Game ended with score {g.score}')


if __name__ == '__main__':
    main()
