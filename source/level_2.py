"""
Parts of this code from:
http://arcade.academy/examples/maze_depth_first.html#depth-first-maze

"""
import random
import arcade

from constants import *
from randomly_place_sprite import randomly_place_sprite
from wander_sprite import WanderSprite

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

    # Randomly open some extra passages

    count = 0
    while count < 10:
        x = random.randrange(5, GRID_WIDTH - 5)
        y = random.randrange(5, GRID_HEIGHT - 5)
        if maze[y][x] != 0 and maze[y-1][x] != 0 and maze[y+1][x]:
            maze[y][x] = 0
            count += 1
        elif maze[y][x] != 0 and maze[y][x-1] != 0 and maze[y][x+1]:
            maze[y][x] = 0
            count += 1

    return maze

def add_level_2_creatures(level):

    level.creature_list = arcade.SpriteList()

    key = arcade.Sprite("images/key-02.png", OBJECT_SPRITE_SCALING)
    key.tag = "key-02"
    randomly_place_sprite(key, level.wall_list)
    level.objects_list.append(key)

    for i in range(3):
        skull = WanderSprite("images/skull.png", CREATURE_SPRITE_SCALING)
        skull.tag = "skull"
        skull.dialog_list = ["Woooo!"]
        skull.physics_engine = arcade.PhysicsEngineSimple(skull, level.all_obstacles)
        randomly_place_sprite(skull, level.wall_list)
        level.creature_list.append(skull)
