import pygame
import random
import sys

WIDTH, HEIGHT = 600, 600
TILE = 20
FPS_START = 10
FOOD_DESPAWN_TIME = 3000  

pygame.init()
win = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 24)

bg_images = [
    pygame.transform.scale(pygame.image.load("images/level1.png"), (WIDTH, HEIGHT)),
    pygame.transform.scale(pygame.image.load("images/level2.png"), (WIDTH, HEIGHT)),
    pygame.transform.scale(pygame.image.load("images/level3.png"), (WIDTH, HEIGHT)),
    pygame.transform.scale(pygame.image.load("images/level4.png"), (WIDTH, HEIGHT))
]

snake = [(10, 10), (9, 10), (8, 10)]
direction = (1, 0)
score = 0
level = 1
speed = FPS_START

walls = set()
for x in range(WIDTH // TILE):
    walls.add((x, 0))
    walls.add((x, HEIGHT // TILE - 1))
for y in range(HEIGHT // TILE):
    walls.add((0, y))
    walls.add((WIDTH // TILE - 1, y))

food = None
food_weight = 1
food_spawn_time = 0

def generate_food():
    global food, food_weight, food_spawn_time
    grid_w = WIDTH // TILE
    grid_h = HEIGHT // TILE
    while True:
        pos = (random.randint(1, grid_w - 2), random.randint(1, grid_h - 2))
        if pos not in snake and pos not in walls:
            food = pos
            food_weight = random.choice([1, 2, 3])
            food_spawn_time = pygame.time.get_ticks()
            return

def draw():
    bg_index = min(level - 1, len(bg_images) - 1)
    win.blit(bg_images[bg_index], (0, 0))

    for wx, wy in walls:
        pygame.draw.rect(win, (100, 100, 100), (wx*TILE, wy*TILE, TILE, TILE))

    for x, y in snake:
        pygame.draw.rect(win, (167, 105, 255), (x*TILE, y*TILE, TILE, TILE))

    if food:
        color = (
            (255, 0, 0) if food_weight == 1
            else (255, 165, 0) if food_weight == 2
            else (255, 255, 0)
        )
        pygame.draw.rect(win, color, (food[0]*TILE, food[1]*TILE, TILE, TILE))

    text = font.render(f"Score: {score}   Level: {level}", True, (255, 255, 255))
    win.blit(text, (10, 10))

    pygame.display.update()

generate_food()

while True:
    clock.tick(speed)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and direction != (0, 1): direction = (0, -1)
            if event.key == pygame.K_DOWN and direction != (0, -1): direction = (0, 1)
            if event.key == pygame.K_LEFT and direction != (1, 0): direction = (-1, 0)
            if event.key == pygame.K_RIGHT and direction != (-1, 0): direction = (1, 0)

    head = snake[0]
    new_head = (head[0] + direction[0], head[1] + direction[1])

    if new_head in walls:
        pygame.quit()
        sys.exit()

    if new_head in snake:
        pygame.quit()
        sys.exit()

    snake.insert(0, new_head)

    if pygame.time.get_ticks() - food_spawn_time > FOOD_DESPAWN_TIME:
        generate_food()

    if new_head == food:
        score += food_weight

        if score % 2 == 0:
            level += 1
            speed += 1

        generate_food()
    else:
        snake.pop()

    draw()