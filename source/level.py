import arcade


def create_grid(width, height):
    """ Create a two-dimensional grid of specified size. """
    return [[0 for x in range(width)] for y in range(height)]


def print_grid(grid):
    for row in grid:
        for cell in row:
            print(cell, end="")
        print()


class Level:
    def __init__(self):
        self.grid = None
        self.wall_list = arcade.SpriteList()
        self.all_obstacles = arcade.SpriteList()
        self.stair_list = arcade.SpriteList()
        self.creature_list = arcade.SpriteList()
        self.objects_list = arcade.SpriteList()
        self.missile_list = arcade.SpriteList()
        self.background_color = arcade.color.BLACK
