def create_grid(width, height):
    """ Create a two-dimensional grid of specified size. """
    return [[0 for x in range(width)] for y in range(height)]

class Level():
    def __init__(self):
        self.wall_list = None
        self.stair_list = None
