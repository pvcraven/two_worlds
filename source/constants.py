# Sprite scaling. Make this larger, like 0.5 to zoom in and add
# 'mystery' to what you can see. Make it smaller, like 0.1 to see
# more of the map.
WALL_SPRITE_SCALING = 0.6
PLAYER_SPRITE_SCALING = 0.4

WALL_SPRITE_SIZE = 32 * WALL_SPRITE_SCALING

# How big the grid is
GRID_WIDTH = 50
GRID_HEIGHT = 50

AREA_WIDTH = GRID_WIDTH * WALL_SPRITE_SIZE
AREA_HEIGHT = GRID_HEIGHT * WALL_SPRITE_SIZE

# How fast the player moves
MOVEMENT_SPEED = 5

# How close the player can get to the edge before we scroll.
VIEWPORT_MARGIN = 300

# How big the window is
WINDOW_WIDTH = 1600
WINDOW_HEIGHT = 1000

MERGE_SPRITES = True
