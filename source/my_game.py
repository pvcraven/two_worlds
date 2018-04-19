import arcade
import random
import timeit
import os

from constants import *
from create_levels import create_levels
from randomly_place_sprite import randomly_place_sprite
from player_sprite import PlayerSprite
from utility import get_closest_sprite


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
        self.message_queue = None

        # Start 'state' will be showing the first page of instructions.
        self.current_state = INSTRUCTIONS_PAGE_0

        self.instructions = []
        texture = arcade.load_texture("images/instructions-01.png")
        self.instructions.append(texture)

        arcade.set_background_color(arcade.color.BLACK)

    def setup(self):
        self.current_state = INSTRUCTIONS_PAGE_0
        self.message_queue = []

        self.level_list = create_levels()

        self.player_list = arcade.SpriteList()

        # Start on level 1
        self.current_level = self.level_list[self.current_level_no]

        # Set up the player
        self.player_sprite = PlayerSprite("images/character.png", PLAYER_SPRITE_SCALING)
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
        self.current_level.objects_list.draw()
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

        # Draw inventory
        arcade.draw_lrtb_rectangle_filled(self.view_left,
                                          self.view_left + WINDOW_WIDTH - 1,
                                          self.view_bottom + PLAYER_SPRITE_SIZE * 2,
                                          self.view_bottom, arcade.color.BLACK)

        x_position = self.view_left
        for item in self.player_sprite.inventory:
            item.bottom = self.view_bottom
            item.left = x_position
            x_position += item.width
            item.draw()

        # Draw messages
        if len(self.message_queue) > 0:
            center_x = WINDOW_WIDTH // 2 + self.view_left
            center_y = WINDOW_HEIGHT // 2 + self.view_bottom
            width = 400
            arcade.draw_rectangle_filled(center_x, center_y,
                                         width, 200, arcade.color.BLACK)
            arcade.draw_rectangle_outline(center_x, center_y,
                                          width, 200, arcade.color.WHITE, 2)
            arcade.draw_text(self.message_queue[0],
                             center_x, center_y, arcade.color.WHITE, 14, width=width, align="center",
                             anchor_x="center", anchor_y="center")

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

    def talk(self):
        nearest_sprite, distance = get_closest_sprite(self.player_sprite, self.current_level.creature_list)

        if distance < PLAYER_SPRITE_SIZE * 3:
            dialog = nearest_sprite.get_dialog(self.player_sprite)
            if dialog is not None:
                self.message_queue.append(dialog)
            else:
                self.message_queue.append("What?")
        else:
            self.message_queue.append("No one near by")




    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed. """

        if self.current_state == INSTRUCTIONS_PAGE_0:
            if key == arcade.key.SPACE:
                self.current_state = GAME_RUNNING

        elif self.current_state == GAME_RUNNING:
            if key == arcade.key.SPACE and len(self.message_queue) > 0:
                self.message_queue.pop(0)
            elif len(self.message_queue) > 0:
                return
            elif key == arcade.key.SPACE:
                self.talk()
            elif key == arcade.key.W:
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
                    has_key = False
                    for inventory_item in self.player_sprite.inventory:
                        new_level = self.current_level_no + 1
                        if inventory_item.tag == f"key-{new_level:02}":
                            has_key = True
                    if not has_key:
                        self.message_queue.append("You don't have the key for the stairway door.")
                        return
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
        """ Movement and game logic """

        if not self.current_state == GAME_RUNNING:
            return

        if len(self.message_queue) > 0:
            return


        start_time = timeit.default_timer()

        # Move player
        self.physics_engine.update()
        self.player_sprite.center_x = int(self.player_sprite.center_x)
        self.player_sprite.center_y = int(self.player_sprite.center_y)

        # Move creatures
        for creature in self.current_level.creature_list:
            creature.update()
            creature.center_x = int(creature.center_x)
            creature.center_y = int(creature.center_y)

        # Pick up items
        objects_hit_list = arcade.check_for_collision_with_list(self.player_sprite, self.current_level.objects_list)
        for my_object in objects_hit_list:
            self.current_level.objects_list.remove(my_object)
            self.player_sprite.inventory.append(my_object)

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
