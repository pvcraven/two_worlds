import arcade
import random

class WanderSprite(arcade.Sprite):

    def __init__(self, filename, sprite_scaling):

        super().__init__(filename, sprite_scaling)

        self.tag = None
        self.wall_list = None
        self.direction = 0
        self.physics_engine = None

    def update(self):
        self.physics_engine.update()

        if random.randrange(60) == 0:
            self.change_x = random.randrange(-2, 3)
            self.change_y = random.randrange(-2, 3)