import pygame
import random
import heapq
from collections import deque
from config import *
from player import Player
from grid import draw_grid

pygame.init()
pygame.font.init()
FONT = pygame.font.SysFont('Arial', 24)

def generate_walls():
    walls = [[False for _ in range(GRID_HEIGHT)] for _ in range(GRID_WIDTH)]

    # Step 1: Create a guaranteed path from start to end (zig-zag)
    path = []
    x, y = 0, 0
    path.append((x, y))
    while x < GRID_WIDTH - 1 or y < GRID_HEIGHT - 1:
        if x == GRID_WIDTH - 1:
            y += 1
        elif y == GRID_HEIGHT - 1:
            x += 1
        else:
            if random.random() < 0.5:
                x += 1
            else:
                y += 1
        path.append((x, y))

    # Step 2: Add random walls everywhere else but keep the path free
    for i in range(GRID_WIDTH):
        for j in range(GRID_HEIGHT):
            if (i, j) not in path:
                if random.random() < 0.3:  # 30% chance to place a wall
                    walls[i][j] = True

    return walls


def draw_walls(screen, walls):
    cross_color = (200, 50, 50)
    cross_thickness = 2
    for i in range(GRID_WIDTH):
        for j in range(GRID_HEIGHT):
            if walls[i][j]:
                rect = pygame.Rect(i * TILE_SIZE, j * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                pygame.draw.rect(screen, (70, 20, 20), rect)
                pygame.draw.line(screen, cross_color, rect.topleft, rect.bottomright, cross_thickness)
                pygame.draw.line(screen, cross_color, rect.topright, rect.bottomleft, cross_thickness)

def is_valid_move(x, y, walls):
    return 0 <= x < GRID_WIDTH and 0 <= y < GRID_HEIGHT and not walls[x][y]

def dijkstra(walls, start, end):
    # Returns shortest path as list of (x,y) from start to end or [] if no path
    dist = [[float('inf')] * GRID_HEIGHT for _ in range(GRID_WIDTH)]
    prev = [[None] * GRID_HEIGHT for _ in range(GRID_WIDTH)]
    dist[start[0]][start[1]] = 0
    heap = [(0, start)]

    while heap:
        cur_dist, (x, y) = heapq.heappop(heap)
        if (x, y) == end:
            break
        if cur_dist > dist[x][y]:
            continue
        for dx, dy in [(1,0), (-1,0), (0,1), (0,-1)]:
            nx, ny = x + dx, y + dy
            if is_valid_move(nx, ny, walls):
                nd = cur_dist + 1
                if nd < dist[nx][ny]:
                    dist[nx][ny] = nd
                    prev[nx][ny] = (x, y)
                    heapq.heappush(heap, (nd, (nx, ny)))

    # Reconstruct path
    path = []
    cur = end
    if dist[end[0]][end[1]] == float('inf'):
        return []  # no path
    while cur != start:
        path.append(cur)
        cur = prev[cur[0]][cur[1]]
    path.append(start)
    path.reverse()
    return path

def draw_best_path(screen, path):
    green = (0, 255, 0)
    for (x, y) in path:
        rect = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
        pygame.draw.rect(screen, green, rect)

def draw_panel(screen, steps, button_rect, delta, show_delta):
    panel_rect = pygame.Rect(0, 700, SCREEN_WIDTH, PANEL_HEIGHT)
    pygame.draw.rect(screen, PANEL_BG_COLOR, panel_rect)

    step_text = FONT.render(f"Steps: {steps}", True, TEXT_COLOR)
    screen.blit(step_text, (20, 700 + 30))

    delta_text = FONT.render(f"Delta: {'?' if not show_delta else delta}", True, TEXT_COLOR)
    screen.blit(delta_text, (SCREEN_WIDTH - 150, 700 + 30))

    mouse_pos = pygame.mouse.get_pos()
    color = BUTTON_HOVER_COLOR if button_rect.collidepoint(mouse_pos) else BUTTON_COLOR
    pygame.draw.rect(screen, color, button_rect)
    button_text = FONT.render("Restart", True, (255, 255, 255))
    text_rect = button_text.get_rect(center=button_rect.center)
    screen.blit(button_text, text_rect)

def main():
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Dungeon Game Simulator")
    clock = pygame.time.Clock()

    walls = generate_walls()
    player = Player()
    steps = 0
    show_delta = False
    delta = 0
    best_path = []

    button_rect = pygame.Rect(SCREEN_WIDTH // 2 - 60, 700 + 20, 120, 40)

    running = True
    while running:
        screen.fill(BACKGROUND_COLOR)
        draw_grid(screen)
        draw_walls(screen, walls)

        # Draw end point in red
        end_rect = pygame.Rect((GRID_WIDTH - 1) * TILE_SIZE, (GRID_HEIGHT - 1) * TILE_SIZE, TILE_SIZE, TILE_SIZE)
        pygame.draw.rect(screen, (255, 0, 0), end_rect)

        # If best_path known and show_delta True, draw best path in green
        if show_delta and best_path:
            draw_best_path(screen, best_path)

        player.draw(screen)
        draw_panel(screen, steps, button_rect, delta, show_delta)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if button_rect.collidepoint(event.pos):
                    # Restart button: reset player & steps and generate new walls & reset delta and path visibility
                    if show_delta:
                        walls = generate_walls()
                        show_delta = False
                        delta = 0
                        best_path = []
                    player.x, player.y = 0, 0
                    steps = 0

        keys = pygame.key.get_pressed()
        new_x, new_y = player.x, player.y
        if keys[pygame.K_UP]:
            new_x, new_y = player.x, player.y - 1
        elif keys[pygame.K_DOWN]:
            new_x, new_y = player.x, player.y + 1
        elif keys[pygame.K_LEFT]:
            new_x, new_y = player.x - 1, player.y
        elif keys[pygame.K_RIGHT]:
            new_x, new_y = player.x + 1, player.y

        if (new_x, new_y) != (player.x, player.y) and is_valid_move(new_x, new_y, walls):
            player.x, player.y = new_x, new_y
            steps += 1

        # When player reaches end
        if player.x == GRID_WIDTH - 1 and player.y == GRID_HEIGHT - 1 and not show_delta:
            # Find shortest path
            start = (0, 0)
            end = (GRID_WIDTH - 1, GRID_HEIGHT - 1)
            best_path = dijkstra(walls, start, end)
            if not best_path:
                # Should never happen since we generate guaranteed path but safe fallback
                best_path = [(0, 0), (GRID_WIDTH - 1, GRID_HEIGHT - 1)]
            # Calculate delta steps difference
            delta = steps - (len(best_path) - 1)
            show_delta = True

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main()
