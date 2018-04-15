import arcade
import random
import timeit

from constants import *
from create_levels import create_levels


class MyGame(arcade.Window):
    """
    Main application class.
    """

    def __init__(self, width, height):
        super().__init__(width, height)

        self.grid = None
        self.level_list = None
        self.current_level = None
        self.current_level_no = 0
        self.player_list = None
        self.player_sprite = None
        self.view_bottom = 0
        self.view_left = 0
        self.physics_engine = None

        self.processing_time = 0
        self.draw_time = 0

        arcade.set_background_color(arcade.color.BLACK)

    def setup(self):
        self.level_list = create_levels()

        self.player_list = arcade.SpriteList()

        # Start on level 1
        self.current_level = self.level_list[self.current_level_no]

        # Set up the player
        self.player_sprite = arcade.Sprite("images/character.png", PLAYER_SPRITE_SCALING)
        self.player_list.append(self.player_sprite)

        # Randomly place the player. If we are in a wall, repeat until we aren't.
        placed = False
        while not placed:

            # Randomly position
            self.player_sprite.center_x = random.randrange(AREA_WIDTH)
            self.player_sprite.center_y = random.randrange(AREA_HEIGHT)

            # Are we in a wall?
            walls_hit = arcade.check_for_collision_with_list(self.player_sprite, self.current_level.wall_list)
            if len(walls_hit) == 0:
                # Not in a wall! Success!
                placed = True

        self.physics_engine = arcade.PhysicsEngineSimple(self.player_sprite,
                                                         self.current_level.wall_list)

    def on_draw(self):
        """ Render the screen. """

        # Start timing how long this takes
        draw_start_time = timeit.default_timer()

        # This command should happen before we start drawing. It will clear
        # the screen to the background color, and erase what we drew last frame.
        arcade.start_render()

        # Draw the sprites
        self.current_level.wall_list.draw()
        self.current_level.stair_list.draw()
        self.player_list.draw()

        # Draw info on the screen
        sprite_count = len(self.current_level.wall_list)

        output = f"Sprite Count: {sprite_count}"
        arcade.draw_text(output,
                         self.view_left + 20,
                         WINDOW_HEIGHT - 20 + self.view_bottom,
                         arcade.color.WHITE, 16)

        output = f"Drawing time: {self.draw_time:.3f}"
        arcade.draw_text(output,
                         self.view_left + 20,
                         WINDOW_HEIGHT - 40 + self.view_bottom,
                         arcade.color.WHITE, 16)

        output = f"Processing time: {self.processing_time:.3f}"
        arcade.draw_text(output,
                         self.view_left + 20,
                         WINDOW_HEIGHT - 60 + self.view_bottom,
                         arcade.color.WHITE, 16)

        self.draw_time = timeit.default_timer() - draw_start_time

    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed. """

        if key == arcade.key.W:
            self.player_sprite.change_y = MOVEMENT_SPEED
        elif key == arcade.key.S:
            self.player_sprite.change_y = -MOVEMENT_SPEED
        elif key == arcade.key.A:
            self.player_sprite.change_x = -MOVEMENT_SPEED
        elif key == arcade.key.D:
            self.player_sprite.change_x = MOVEMENT_SPEED
        elif key == arcade.key.DOWN:
            stair_hit_list = arcade.check_for_collision_with_list(self.player_sprite, self.current_level.stair_list)
            if len(stair_hit_list) == 0:
                print("There are no stairs down here.")
            elif stair_hit_list[0].tag == "Up":
                print("These are UP stairs, not down stairs.")
            else:
                self.current_level_no += 1
                self.current_level = self.level_list[self.current_level_no]
        elif key == arcade.key.UP:
            stair_hit_list = arcade.check_for_collision_with_list(self.player_sprite, self.current_level.stair_list)
            if len(stair_hit_list) == 0:
                print("There are no stairs down here.")
            elif stair_hit_list[0].tag == "Down":
                print("These are DOWN stairs, not up stairs.")
            else:
                self.current_level_no -= 1
                self.current_level = self.level_list[self.current_level_no]

    def on_key_release(self, key, modifiers):
        """Called when the user releases a key. """

        if key == arcade.key.W or key == arcade.key.S:
            self.player_sprite.change_y = 0
        elif key == arcade.key.A or key == arcade.key.D:
            self.player_sprite.change_x = 0

    def update(self, delta_time):
        """ Movement and game logic """

        start_time = timeit.default_timer()

        # print(f"{self.player_sprite.center_x:.0f}, {self.player_sprite.center_y:.0f} - {self.stair_list[0].center_x:.0f}, {self.stair_list[0].center_y:.0f}")

        # Call update on all sprites (The sprites don't do much in this
        # example though.)
        self.physics_engine.update()

        # --- Manage Scrolling ---

        # Track if we need to change the viewport

        changed = False

        # Scroll left
        left_bndry = self.view_left + VIEWPORT_MARGIN
        if self.player_sprite.left < left_bndry:
            self.view_left -= left_bndry - self.player_sprite.left
            changed = True

        # Scroll right
        right_bndry = self.view_left + WINDOW_WIDTH - VIEWPORT_MARGIN
        if self.player_sprite.right > right_bndry:
            self.view_left += self.player_sprite.right - right_bndry
            changed = True

        # Scroll up
        top_bndry = self.view_bottom + WINDOW_HEIGHT - VIEWPORT_MARGIN
        if self.player_sprite.top > top_bndry:
            self.view_bottom += self.player_sprite.top - top_bndry
            changed = True

        # Scroll down
        bottom_bndry = self.view_bottom + VIEWPORT_MARGIN
        if self.player_sprite.bottom < bottom_bndry:
            self.view_bottom -= bottom_bndry - self.player_sprite.bottom
            changed = True

        if changed:
            arcade.set_viewport(self.view_left,
                                WINDOW_WIDTH + self.view_left,
                                self.view_bottom,
                                WINDOW_HEIGHT + self.view_bottom)

        # Save the time it took to do this.
        self.processing_time = timeit.default_timer() - start_time


