import arcade
import random

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
