import arcade


class PlayerSprite(arcade.Sprite):

    def __init__(self, filename, sprite_scaling):

        super().__init__(filename, sprite_scaling)

        self.inventory = []
