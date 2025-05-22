# config.py

# Screen settings
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 800  # increased from 700 to 800 to add panel below
FPS = 10  # Movement speed

# Grid settings
TILE_SIZE = 30
GRID_WIDTH = SCREEN_WIDTH // TILE_SIZE  # 33 tiles wide
GRID_HEIGHT = 700 // TILE_SIZE  # Keep grid height same as before (700 px for grid), so 23 tiles

PANEL_HEIGHT = SCREEN_HEIGHT - 700  # 100 px panel height

# Colors (R, G, B)
BACKGROUND_COLOR = (30, 30, 30)
GRID_COLOR = (50, 50, 50)
PLAYER_COLOR = (255, 165, 0)

PANEL_BG_COLOR = (40, 40, 40)
TEXT_COLOR = (200, 200, 200)
BUTTON_COLOR = (70, 130, 180)
BUTTON_HOVER_COLOR = (100, 160, 210)
