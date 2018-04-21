"""
Starting point for the game. Get is setup and running.
"""
import arcade

from constants import *
from my_game import MyGame


def main():
    game = MyGame(WINDOW_WIDTH, WINDOW_HEIGHT)
    game.setup()
    arcade.run()


if __name__ == "__main__":
    main()
