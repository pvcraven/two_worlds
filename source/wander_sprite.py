import arcade
import random
import math

from constants import *
from player_sprite import PlayerSprite
from randomly_place_sprite import randomly_place_sprite

class CreatureSprite(arcade.Sprite):

    def __init__(self, filename, sprite_scaling):

        super().__init__(filename, sprite_scaling)

        self.tag = None
        self.wall_list = None
        self.direction = 0
        self.physics_engine = None
        self.dialog_no = 0
        self.dialog_list = []

    def get_dialog(self, player_sprite):
        if self.dialog_no < len(self.dialog_list):
            self.dialog_no += 1
            return self.dialog_list[self.dialog_no - 1]


class WanderSprite(CreatureSprite):

    def update(self):
        self.physics_engine.update()

        if random.randrange(60) == 0:
            self.change_x = random.randrange(-2, 3)
            self.change_y = random.randrange(-2, 3)

class CustodianSprite(WanderSprite):

    def __init__(self, filename, sprite_scaling, level):

        super().__init__(filename, sprite_scaling)
        self.level = level
        self.give_key = False

    def get_dialog(self, player_sprite):
        if self.dialog_no == 0 and self.give_key:
            self.dialog_no += 1

            key = arcade.Sprite("images/key-01.png", OBJECT_SPRITE_SCALING)
            key.tag = "key-01"
            key.center_x = self.center_x
            key.center_y = self.center_y
            print(f"Placed key {key.center_x}, {key.center_y}")
            self.level.objects_list.append(key)

            return "Oh, you need a key?"
        elif self.dialog_no == 1 and self.give_key:
            return "Take care of that key."
        elif self.dialog_no == 0 and not self.give_key:
            self.dialog_no += 1
            return "Don't look at me, I'm just the janitor."
        elif self.dialog_no == 1 and not self.give_key:
            return "Don't spill anything."


class LibrarianSprite(WanderSprite):

    def __init__(self, filename, sprite_scaling, custodian_sprite):

        super().__init__(filename, sprite_scaling)
        self.custodian_sprite = custodian_sprite

    def get_dialog(self, player_sprite : PlayerSprite):
        self.change_x = 0
        self.change_y = 0

        has_scepter = False
        for item in player_sprite.inventory:
            print(item.tag)
            if item.tag == "scepter":
                has_scepter = True
        if has_scepter:
            return "Great job! The castle is saved!"
        elif self.dialog_no == 0:
            self.dialog_no += 1
            return "Sam! We've lost the scepter."
        elif self.dialog_no == 1:
            self.dialog_no += 1
            return "Please, find the scepter below the castle."
        elif self.dialog_no == 2:
            self.dialog_no += 1
            self.custodian_sprite.dialog_no = 0
            self.custodian_sprite.give_key = True
            return "Ask the janitor for the key."
        else:
            return "Please hurry."

class DragonSprite(WanderSprite):

    def __init__(self, filename, sprite_scaling, player_sprite):

        super().__init__(filename, sprite_scaling)
        self.player_sprite = player_sprite

    def get_dialog(self, player_sprite):
            return "Roar."

    def update(self):
        super().update()

        # First, calculate the angle to the player. We could do this
        # only when the bullet fires, but in this case we will rotate
        # the enemy to face the player each frame, so we'll do this
        # each frame.

        # Position the start at the enemy's current location
        start_x = self.center_x
        start_y = self.center_y

        # Get the destination location for the bullet
        dest_x = self.player_sprite.center_x
        dest_y = self.player_sprite.center_y

        # Do math to calculate how to get the bullet to the destination.
        # Calculation the angle in radians between the start points
        # and end points. This is the angle the bullet will travel.
        x_diff = dest_x - start_x
        y_diff = dest_y - start_y
        angle = math.atan2(y_diff, x_diff)

        # Set the enemy to face the player.
        # self.angle = math.degrees(angle)-90

