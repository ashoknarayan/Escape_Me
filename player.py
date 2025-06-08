import pygame
from config import TILE_SIZE, PLAYER_COLOR, GRID_WIDTH, GRID_HEIGHT

class Player:
    def __init__(self):
        self.x = 0
        self.y = 0

    def move(self, dx, dy):
        new_x = self.x + dx
        new_y = self.y + dy

        if 0 <= new_x < GRID_WIDTH:
            self.x = new_x
        if 0 <= new_y < GRID_HEIGHT:
            self.y = new_y

    def draw(self, screen, numbers, font):
        rect = pygame.Rect(self.x * TILE_SIZE, self.y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
        pygame.draw.rect(screen, PLAYER_COLOR, rect)

        num = numbers[self.x][self.y]
        text = font.render(str(num), True, (0, 0, 0))  # black text for contrast
        text_rect = text.get_rect(center=rect.center)
        screen.blit(text, text_rect)
