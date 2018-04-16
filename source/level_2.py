"""
Parts of this code from:
http://arcade.academy/examples/maze_depth_first.html#depth-first-maze

"""
import random
import arcade

from constants import *

def _create_grid_with_cells(width, height):
    """ Create a grid with empty cells on odd row/column combinations. """
    grid = []
    for row in range(height):
        grid.append([])
        for column in range(width):
            if column % 2 == 1 and row % 2 == 1:
                grid[row].append(0)
            elif column == 0 or row == 0 or column == width - 1 or row == height - 1:
                grid[row].append(1)
            else:
                grid[row].append(1)
    return grid


def get_level_2_array():
    maze = _create_grid_with_cells(GRID_WIDTH, GRID_HEIGHT)

    w = (len(maze[0]) - 1) // 2
    h = (len(maze) - 1) // 2
    vis = [[0] * w + [1] for _ in range(h)] + [[1] * (w + 1)]

    def walk(x, y):
        vis[y][x] = 1

        d = [(x - 1, y), (x, y + 1), (x + 1, y), (x, y - 1)]
        random.shuffle(d)
        for (xx, yy) in d:
            if vis[yy][xx]:
                continue
            if xx == x:
                maze[max(y, yy) * 2][x * 2 + 1] = 0
            if yy == y:
                maze[y * 2 + 1][max(x, xx) * 2] = 0

            walk(xx, yy)

    walk(random.randrange(w), random.randrange(h))

    return maze

def add_level_2_creatures(level):

    level.creature_list = arcade.SpriteList()
