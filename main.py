import pygame
import random
import heapq
from collections import deque
from config import *
from player import Player
from grid import draw_grid

pygame.init()
pygame.font.init()
FONT = pygame.font.SysFont('Arial', 20)  # Smaller font for numbers

def generate_walls():
    walls = [[True for _ in range(GRID_HEIGHT)] for _ in range(GRID_WIDTH)]
    stack = []
    start_x, start_y = 0, 0
    walls[start_x][start_y] = False
    stack.append((start_x, start_y))
    directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]
    direction_weights = {(1, 0): 0.2, (0, 1): 0.2, (-1, 0): 0.3, (0, -1): 0.3}

    while stack:
        x, y = stack[-1]
        neighbors = []
        for dx, dy in directions:
            nx, ny = x + dx * 2, y + dy * 2
            if 0 <= nx < GRID_WIDTH and 0 <= ny < GRID_HEIGHT and walls[nx][ny]:
                neighbors.append((nx, ny, dx, dy))

        if neighbors:
            weights = [direction_weights[(dx, dy)] for _, _, dx, dy in neighbors]
            nx, ny, dx, dy = random.choices(neighbors, weights=weights, k=1)[0]
            walls[nx][ny] = False
            walls[x + dx][y + dy] = False
            stack.append((nx, ny))
        else:
            stack.pop()

    for i in range(GRID_WIDTH):
        for j in range(GRID_HEIGHT):
            if walls[i][j] and random.random() < 0.15:
                for dx, dy in directions:
                    ni, nj = i + dx, j + dy
                    if 0 <= ni < GRID_WIDTH and 0 <= nj < GRID_HEIGHT and not walls[ni][nj]:
                        walls[i][j] = False
                        break

    walls[0][0] = False
    walls[GRID_WIDTH - 1][GRID_HEIGHT - 1] = False

    return walls

def generate_numbers(walls):
    numbers = [[-1 for _ in range(GRID_HEIGHT)] for _ in range(GRID_WIDTH)]
    for i in range(GRID_WIDTH):
        for j in range(GRID_HEIGHT):
            if not walls[i][j]:
                numbers[i][j] = random.randint(0, 9)
    return numbers

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

def draw_numbers(screen, numbers, walls):
    for i in range(GRID_WIDTH):
        for j in range(GRID_HEIGHT):
            if not walls[i][j]:
                num = numbers[i][j]
                text = FONT.render(str(num), True, (200, 200, 200))
                text_rect = text.get_rect(center=((i * TILE_SIZE) + TILE_SIZE//2, (j * TILE_SIZE) + TILE_SIZE//2))
                screen.blit(text, text_rect)

def is_valid_move(x, y, walls):
    return 0 <= x < GRID_WIDTH and 0 <= y < GRID_HEIGHT and not walls[x][y]

def dijkstra(walls, numbers, start, end):
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
                # Edge weight is abs difference of numbers on adjacent cells
                weight = abs(numbers[x][y] - numbers[nx][ny])
                nd = cur_dist + weight
                if nd < dist[nx][ny]:
                    dist[nx][ny] = nd
                    prev[nx][ny] = (x, y)
                    heapq.heappush(heap, (nd, (nx, ny)))

    path = []
    cur = end
    if dist[end[0]][end[1]] == float('inf'):
        return []
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
    numbers = generate_numbers(walls)
    player = Player()
    steps = 0
    show_delta = False
    best_value = 0
    best_path = []

    button_rect = pygame.Rect(SCREEN_WIDTH // 2 - 60, 700 + 20, 120, 40)

    running = True
    while running:
        screen.fill(BACKGROUND_COLOR)
        draw_grid(screen)
        draw_walls(screen, walls)
        draw_numbers(screen, numbers, walls)

        # Draw end point in red
        end_rect = pygame.Rect((GRID_WIDTH - 1) * TILE_SIZE, (GRID_HEIGHT - 1) * TILE_SIZE, TILE_SIZE, TILE_SIZE)
        pygame.draw.rect(screen, (255, 0, 0), end_rect)

        if show_delta and best_path:
            draw_best_path(screen, best_path)
            # Draw numbers on best path in black for visibility
            for (x, y) in best_path:
                num = numbers[x][y]
                text = FONT.render(str(num), True, (0, 0, 0))  # Black numbers
                text_rect = text.get_rect(center=((x * TILE_SIZE) + TILE_SIZE // 2, (y * TILE_SIZE) + TILE_SIZE // 2))
                screen.blit(text, text_rect)

        player.draw(screen, numbers, FONT)
        draw_panel(screen, steps, button_rect, best_value, show_delta)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if button_rect.collidepoint(event.pos):
                    if show_delta:
                        walls = generate_walls()
                        numbers = generate_numbers(walls)
                        show_delta = False
                        best_value = 0
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
            n1 = numbers[player.x][player.y]
            n2 = numbers[new_x][new_y]
            player.x, player.y = new_x, new_y
            steps += abs(n1 - n2)  # <-- Changed to abs difference sum

        if player.x == GRID_WIDTH - 1 and player.y == GRID_HEIGHT - 1 and not show_delta:
            start = (0, 0)
            end = (GRID_WIDTH - 1, GRID_HEIGHT - 1)
            best_path = dijkstra(walls, numbers, start, end)
            if not best_path:
                best_path = [(0, 0), (GRID_WIDTH - 1, GRID_HEIGHT - 1)]
            # Calculate total best weight as sum of abs diffs along path
            best_value = sum(
                abs(numbers[best_path[i][0]][best_path[i][1]] - numbers[best_path[i + 1][0]][best_path[i + 1][1]])
                for i in range(len(best_path) - 1)
            )
            show_delta = True

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

def draw_panel(screen, steps, button_rect, best_value, show_delta):
    panel_rect = pygame.Rect(0, 700, SCREEN_WIDTH, PANEL_HEIGHT)
    pygame.draw.rect(screen, PANEL_BG_COLOR, panel_rect)

    step_text = FONT.render(f"Steps: {steps}", True, TEXT_COLOR)
    screen.blit(step_text, (20, 700 + 30))

    best_text = FONT.render(f"Best: {'?' if not show_delta else best_value}", True, TEXT_COLOR)  # Renamed "Delta" to "Best"
    screen.blit(best_text, (SCREEN_WIDTH - 150, 700 + 30))

    mouse_pos = pygame.mouse.get_pos()
    color = BUTTON_HOVER_COLOR if button_rect.collidepoint(mouse_pos) else BUTTON_COLOR
    pygame.draw.rect(screen, color, button_rect)
    button_label = "Next"  # Changed button text to "Best"
    button_text = FONT.render(button_label, True, (255, 255, 255))
    text_rect = button_text.get_rect(center=button_rect.center)
    screen.blit(button_text, text_rect)


if __name__ == "__main__":
    main()
