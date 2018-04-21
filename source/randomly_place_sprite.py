import random
import arcade

from constants import *


def randomly_place_sprite(sprite, wall_list):
    # Randomly place the player. If we are in a wall, repeat until we aren't.
    placed = False
    while not placed:

        # Randomly position
        sprite.center_x = random.randrange(AREA_WIDTH)
        sprite.center_y = random.randrange(AREA_HEIGHT)

        # Are we in a wall?
        walls_hit = arcade.check_for_collision_with_list(sprite, wall_list)
        if len(walls_hit) == 0:
            # Not in a wall! Success!
            placed = True
