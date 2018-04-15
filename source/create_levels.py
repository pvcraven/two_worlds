import arcade

from constants import  *
from level import Level
from level_1 import get_level_1_array


def create_stairs(level_list):

    for level in level_list:
        level.stair_list = arcade.SpriteList()
    # # Place the down stairs
    # placed = False
    # while not placed:
    #     row = random.randrange(dg.height)
    #     column = random.randrange(dg.width)
    #     value = dg.dungeon[row][column]
    #     if value != '#':
    #         placed = True
    #         stairs = Stairs("images/stairs_down.png", WALL_SPRITE_SCALING)
    #         stairs.center_x = column * WALL_SPRITE_SIZE + WALL_SPRITE_SIZE / 2
    #         stairs.center_y = row * WALL_SPRITE_SIZE + WALL_SPRITE_SIZE / 2
    #         stairs.tag = "Down"
    #         stair_list.append(stairs)
    #



def create_walls(level_list):

    for level in level_list:
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

                wall = arcade.Sprite("images/wall-01.png", WALL_SPRITE_SCALING,
                                     repeat_count_x=column_count)
                wall.center_x = column_mid * WALL_SPRITE_SIZE + WALL_SPRITE_SIZE / 2
                wall.center_y = row * WALL_SPRITE_SIZE + WALL_SPRITE_SIZE / 2
                wall.width = WALL_SPRITE_SIZE * column_count
                print(f"({wall.center_x}, {wall.center_y}) - {wall.width}")

                level.wall_list.append(wall)

def create_levels():
    level_list = []

    level = Level()
    level.grid = get_level_1_array()
    level_list.append(level)

    create_walls(level_list)
    create_stairs(level_list)

    return level_list