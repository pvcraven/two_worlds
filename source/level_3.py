"""
Parts of this code from:
http://arcade.academy/examples/procedural_caves_cellular.html#procedural-caves-cellular

"""
import random
import arcade

from level import create_grid
from level import Level
from constants import *
from randomly_place_sprite import randomly_place_sprite
from wander_sprite import DragonSprite


# Parameters for cellular automata
CHANCE_TO_START_ALIVE = 0.4
DEATH_LIMIT = 3
BIRTH_LIMIT = 4
NUMBER_OF_STEPS = 4


def initialize_grid(grid):
    """ Randomly set grid locations to on/off based on chance. """
    for row in range(len(grid)):
        for column in range(len(grid[row])):
            if random.random() <= CHANCE_TO_START_ALIVE:
                grid[row][column] = 1


def count_alive_neighbors(grid, x, y):
    """ Count neighbors that are alive. """
    height = len(grid)
    width = len(grid[0])
    alive_count = 0
    for i in range(-1, 2):
        for j in range(-1, 2):
            neighbor_x = x + i
            neighbor_y = y + j
            if i == 0 and j == 0:
                continue
            elif neighbor_x < 0 or neighbor_y < 0 or neighbor_y >= height or neighbor_x >= width:
                # Edges are considered alive. Makes map more likely to appear naturally closed.
                alive_count += 1
            elif grid[neighbor_y][neighbor_x] == 1:
                alive_count += 1
    return alive_count


def do_simulation_step(old_grid):
    """ Run a step of the cellular automaton. """
    height = len(old_grid)
    width = len(old_grid[0])
    new_grid = create_grid(width, height)
    for x in range(width):
        for y in range(height):
            alive_neighbors = count_alive_neighbors(old_grid, x, y)
            if old_grid[y][x] == 1:
                if alive_neighbors < DEATH_LIMIT:
                    new_grid[y][x] = 0
                else:
                    new_grid[y][x] = 1
            else:
                if alive_neighbors > BIRTH_LIMIT:
                    new_grid[y][x] = 1
                else:
                    new_grid[y][x] = 0
    return new_grid


def get_level_3_array():
    # Create cave system using a 2D grid
    grid = create_grid(GRID_WIDTH, GRID_HEIGHT)
    initialize_grid(grid)
    for step in range(NUMBER_OF_STEPS):
        grid = do_simulation_step(grid)

    # Fill in the outside
    for x in range(GRID_WIDTH):
        grid[0][x] = 1
        grid[GRID_HEIGHT-1][x] = 1

    for y in range(GRID_HEIGHT):
        grid[y][0] = 1
        grid[y][GRID_WIDTH-1] = 1

    return grid


def add_level_3_creatures(level: Level, player_sprite: arcade.Sprite):

    level.creature_list = arcade.SpriteList()

    scepter = arcade.Sprite("images/scepter.png", OBJECT_SPRITE_SCALING)
    scepter.tag = "scepter"
    randomly_place_sprite(scepter, level.wall_list)
    print(f"Placed scepter {scepter.center_x}, {scepter.center_y}")
    level.objects_list.append(scepter)

    dragon = DragonSprite("images/dragon.png", CREATURE_SPRITE_SCALING, player_sprite)
    dragon.tag = "dragon"
    dragon.physics_engine = arcade.PhysicsEngineSimple(dragon, level.all_obstacles)
    randomly_place_sprite(dragon, level.wall_list)
    level.creature_list.append(dragon)
