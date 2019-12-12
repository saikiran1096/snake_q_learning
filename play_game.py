"""
snake.py

author:         Stephen Radley
date:           2018/07/05
package:        snake
version:        0.0.1
x"""

from snake.snake_game.game import SnakeGame

"""
main ...
"""


def main():
    g = SnakeGame()

    try:
        g.run()
    finally:
        g.quit_game()


if __name__ == '__main__':
    main()
