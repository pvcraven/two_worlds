import arcade
import random


class CreatureSprite(arcade.Sprite):\

    def __init__(self, filename, sprite_scaling):

        super().__init__(filename, sprite_scaling)

        self.tag = None
        self.wall_list = None
        self.direction = 0
        self.physics_engine = None
        self.dialog_no = 0
        self.dialog_list = []

    def get_dialog(self):
        if self.dialog_no < len(self.dialog_list):
            self.dialog_no += 1
            return self.dialog_list[self.dialog_no - 1]


class WanderSprite(CreatureSprite):

    def update(self):
        self.physics_engine.update()

        if random.randrange(60) == 0:
            self.change_x = random.randrange(-2, 3)
            self.change_y = random.randrange(-2, 3)
