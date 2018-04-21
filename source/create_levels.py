import arcade
import random

from constants import *
from level import Level
from level_1 import get_level_1_array
from level_1 import add_level_1_creatures
from level_2 import get_level_2_array
from level_2 import add_level_2_creatures
from level_3 import get_level_3_array
from level_3 import add_level_3_creatures
from stairs import Stairs


def create_stairs(level_list):

    for level in level_list:
        level.stair_list = arcade.SpriteList()

    # Place the stairs from 0 to 1
    placed = False
    while not placed:
        row = random.randrange(GRID_HEIGHT)
        column = random.randrange(GRID_WIDTH)
        value_0 = level_list[0].grid[row][column]
        value_1 = level_list[1].grid[row][column]
        if value_0 == 0 and value_1 == 0:
            placed = True
            stairs = Stairs("images/stairs_down.png", WALL_SPRITE_SCALING)
            stairs.center_x = column * WALL_SPRITE_SIZE + WALL_SPRITE_SIZE / 2
            stairs.center_y = row * WALL_SPRITE_SIZE + WALL_SPRITE_SIZE / 2
            stairs.tag = "Down"
            level_list[0].stair_list.append(stairs)

            stairs = Stairs("images/stairs_up.png", WALL_SPRITE_SCALING)
            stairs.center_x = column * WALL_SPRITE_SIZE + WALL_SPRITE_SIZE / 2
            stairs.center_y = row * WALL_SPRITE_SIZE + WALL_SPRITE_SIZE / 2
            stairs.tag = "Up"
            level_list[1].stair_list.append(stairs)

    # Place the stairs from 1 to 2
    placed = False
    while not placed:
        row = random.randrange(GRID_HEIGHT)
        column = random.randrange(GRID_WIDTH)
        value_0 = level_list[1].grid[row][column]
        value_1 = level_list[2].grid[row][column]
        if value_0 == 0 and value_1 == 0:
            placed = True
            stairs = Stairs("images/stairs_down.png", WALL_SPRITE_SCALING)
            stairs.center_x = column * WALL_SPRITE_SIZE + WALL_SPRITE_SIZE / 2
            stairs.center_y = row * WALL_SPRITE_SIZE + WALL_SPRITE_SIZE / 2
            stairs.tag = "Down"
            level_list[1].stair_list.append(stairs)

            stairs = Stairs("images/stairs_up.png", WALL_SPRITE_SCALING)
            stairs.center_x = column * WALL_SPRITE_SIZE + WALL_SPRITE_SIZE / 2
            stairs.center_y = row * WALL_SPRITE_SIZE + WALL_SPRITE_SIZE / 2
            stairs.tag = "Up"
            level_list[2].stair_list.append(stairs)


def create_walls(level_list):

    for index, level in enumerate(level_list):
        i = index+1
        wall_filename = f"images/wall-{i:02}.png"
        level.wall_list = arcade.SpriteList()

        for row in range(GRID_HEIGHT):
            column = 0
            while column < GRID_WIDTH:
                while column < GRID_WIDTH and level.grid[row][column] == 0:
                    column += 1
                start_column = column
                while column < GRID_WIDTH and level.grid[row][column] == 1:
                    column += 1
                end_column = column - 1

                column_count = end_column - start_column + 1
                column_mid = (start_column + end_column) / 2

                wall = arcade.Sprite(wall_filename, WALL_SPRITE_SCALING,
                                     repeat_count_x=column_count)
                wall.center_x = column_mid * WALL_SPRITE_SIZE + WALL_SPRITE_SIZE / 2
                wall.center_y = row * WALL_SPRITE_SIZE + WALL_SPRITE_SIZE / 2
                wall.width = WALL_SPRITE_SIZE * column_count

                level.wall_list.append(wall)


def create_levels(player_sprite):
    level_list = []

    level = Level()
    level.grid = get_level_1_array()
    level_list.append(level)
    level.background_color = arcade.color.BISTRE

    level = Level()
    level.grid = get_level_2_array()
    level_list.append(level)
    level.background_color = arcade.color.BLACK_OLIVE

    level = Level()
    level.grid = get_level_3_array()
    level_list.append(level)
    level.background_color = arcade.color.EERIE_BLACK

    create_walls(level_list)

    add_level_1_creatures(level_list[0])
    add_level_2_creatures(level_list[1])
    add_level_3_creatures(level_list[2], player_sprite)

    create_stairs(level_list)

    return level_list
