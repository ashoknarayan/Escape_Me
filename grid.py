# grid.py

import pygame
from config import SCREEN_WIDTH, SCREEN_HEIGHT, TILE_SIZE, GRID_COLOR

def draw_grid(screen):
    # Draw vertical lines
    for x in range(0, SCREEN_WIDTH, TILE_SIZE):
        pygame.draw.line(screen, GRID_COLOR, (x, 0), (x, SCREEN_HEIGHT))
    # Draw horizontal lines
    for y in range(0, SCREEN_HEIGHT, TILE_SIZE):
        pygame.draw.line(screen, GRID_COLOR, (0, y), (SCREEN_WIDTH, y))
