# player.py

from config import TILE_SIZE, PLAYER_COLOR, GRID_WIDTH, GRID_HEIGHT
import pygame

class Player:
    def __init__(self):
        # Start in the top-left corner
        self.x = 0
        self.y = 0

    def move(self, dx, dy):
        new_x = self.x + dx
        new_y = self.y + dy

        # Keep player within bounds
        if 0 <= new_x < GRID_WIDTH:
            self.x = new_x
        if 0 <= new_y < GRID_HEIGHT:
            self.y = new_y

    def draw(self, screen):
        rect = pygame.Rect(self.x * TILE_SIZE, self.y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
        pygame.draw.rect(screen, PLAYER_COLOR, rect)
