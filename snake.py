"""
snake.py

author:         Stephen Radley
date:           2018/07/05
package:        snake
version:        0.0.1
"""

from snake.snake_game_obj import SnakeGame


"""
main ...
"""
def main():
    g = SnakeGame()

    try:
        g.run()
    except KeyboardInterrupt:
        g.quit_game()
    finally:
        g.quit_game()



if __name__ == '__main__':
    main()