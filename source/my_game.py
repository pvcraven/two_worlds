import arcade
import random
import timeit
import os

from constants import *
from create_levels import create_levels
from randomly_place_sprite import randomly_place_sprite

class MyGame(arcade.Window):
    """
    Main application class.
    """

    def __init__(self, width, height):
        super().__init__(width, height)

        # Set the working directory (where we expect to find files) to the same
        # directory this .py file is in. You can leave this out of your own
        # code, but it is needed to easily run the examples using "python -m"
        # as mentioned at the top of this program.
        file_path = os.path.dirname(os.path.abspath(__file__))
        os.chdir(file_path)

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

        # Start 'state' will be showing the first page of instructions.
        self.current_state = INSTRUCTIONS_PAGE_0

        self.instructions = []
        texture = arcade.load_texture("images/instructions-01.png")
        self.instructions.append(texture)

        arcade.set_background_color(arcade.color.BLACK)

    def setup(self):
        self.current_state = INSTRUCTIONS_PAGE_0

        self.level_list = create_levels()

        self.player_list = arcade.SpriteList()

        # Start on level 1
        self.current_level = self.level_list[self.current_level_no]

        # Set up the player
        self.player_sprite = arcade.Sprite("images/character.png", PLAYER_SPRITE_SCALING)
        self.player_list.append(self.player_sprite)

        for level in self.level_list:
            for wall in level.wall_list:
                level.all_obstacles.append(wall)
            for creature in level.creature_list:
                level.all_obstacles.append(creature)
            level.all_obstacles.append(self.player_sprite)

        randomly_place_sprite(self.player_sprite, self.current_level.all_obstacles)

        self.physics_engine = arcade.PhysicsEngineSimple(self.player_sprite,
                                                         self.current_level.all_obstacles)

        # self.level_list[0].wall_list.append(self.player_sprite)

    def draw_instructions_page(self, page_number):
        """
        Draw an instruction page. Load the page as an image.
        """
        page_texture = self.instructions[page_number]
        arcade.draw_texture_rectangle(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2,
                                      page_texture.width,
                                      page_texture.height, page_texture, 0)

    def draw_game(self):
        """ Render the screen. """

        # Start timing how long this takes
        draw_start_time = timeit.default_timer()

        # This command should happen before we start drawing. It will clear
        # the screen to the background color, and erase what we drew last frame.
        arcade.start_render()

        # Draw the sprites
        self.current_level.wall_list.draw()
        self.current_level.stair_list.draw()
        self.current_level.creature_list.draw()
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

    def on_draw(self):

        # This command has to happen before we start drawing
        arcade.start_render()

        if self.current_state == INSTRUCTIONS_PAGE_0:
            self.draw_instructions_page(0)

        elif self.current_state == INSTRUCTIONS_PAGE_1:
            self.draw_instructions_page(1)

        elif self.current_state == GAME_RUNNING:
            self.draw_game()

        else:
            self.draw_game()
            self.draw_game_over()

    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed. """

        if self.current_state == INSTRUCTIONS_PAGE_0:
            if key == arcade.key.SPACE:
                self.current_state = GAME_RUNNING

        elif self.current_state == GAME_RUNNING:
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
                    self.player_sprite.center_x = stair_hit_list[0].center_x
                    self.player_sprite.center_y = stair_hit_list[0].center_y
                    self.current_level_no += 1
                    self.current_level = self.level_list[self.current_level_no]
                    self.physics_engine = arcade.PhysicsEngineSimple(self.player_sprite,
                                                                     self.current_level.wall_list)
            elif key == arcade.key.UP:
                stair_hit_list = arcade.check_for_collision_with_list(self.player_sprite, self.current_level.stair_list)
                if len(stair_hit_list) == 0:
                    print("There are no stairs down here.")
                elif stair_hit_list[0].tag == "Down":
                    print("These are DOWN stairs, not up stairs.")
                else:
                    self.player_sprite.center_x = stair_hit_list[0].center_x
                    self.player_sprite.center_y = stair_hit_list[0].center_y
                    self.current_level_no -= 1
                    self.current_level = self.level_list[self.current_level_no]
                    self.physics_engine = arcade.PhysicsEngineSimple(self.player_sprite,
                                                                     self.current_level.wall_list)

    def on_key_release(self, key, modifiers):
        """Called when the user releases a key. """

        if key == arcade.key.W or key == arcade.key.S:
            self.player_sprite.change_y = 0
        elif key == arcade.key.A or key == arcade.key.D:
            self.player_sprite.change_x = 0

    def update(self, delta_time):

        if not self.current_state == GAME_RUNNING:
            return

        """ Movement and game logic """

        start_time = timeit.default_timer()

        # print(f"{self.player_sprite.center_x:.0f}, {self.player_sprite.center_y:.0f} - {self.stair_list[0].center_x:.0f}, {self.stair_list[0].center_y:.0f}")

        self.physics_engine.update()
        self.player_sprite.center_x = int(self.player_sprite.center_x)
        self.player_sprite.center_y = int(self.player_sprite.center_y)

        for creature in self.current_level.creature_list:
            creature.update()
            creature.center_x = int(creature.center_x)
            creature.center_y = int(creature.center_y)

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
