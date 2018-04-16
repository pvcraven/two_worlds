

def create_grid(width, height):
    """ Create a two-dimensional grid of specified size. """
    return [[0 for x in range(width)] for y in range(height)]

class Level():
    def __init__(self):
        self.grid = None
        self.wall_list = None
        self.stair_list = None
        self.creature_list = None

def print_grid(grid):
    for row in grid:
        for cell in row:
            print(cell, end="")
        print()