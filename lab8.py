# # Racer
# import pygame, sys
# from pygame.locals import *
# import random, time

# pygame.init()

# FPS = 60
# FramePerSec = pygame.time.Clock()

# BLUE  = (0, 0, 255)
# RED   = (255, 0, 0)
# GREEN = (0, 255, 0)
# BLACK = (0, 0, 0)
# WHITE = (255, 255, 255)
# YELLOW = (255, 215, 0)

# SCREEN_WIDTH = 400
# SCREEN_HEIGHT = 600
# SPEED = 5
# SCORE = 0
# COINS_COLLECTED = 0

# DISPLAYSURF = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
# pygame.display.set_caption("Racer Game")

# font = pygame.font.SysFont("Verdana", 60)
# font_small = pygame.font.SysFont("Verdana", 20)
# game_over = font.render("Game Over", True, BLACK)

# background = pygame.image.load("images/street.png").convert()
# background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))

# class Enemy(pygame.sprite.Sprite):
#     def __init__(self):
#         super().__init__()
#         self.image = pygame.image.load("images/enemy.png").convert_alpha()
#         self.image = pygame.transform.scale(self.image, (45, 90))
#         self.rect = self.image.get_rect()
#         self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)

#     def move(self):
#         global SCORE
#         self.rect.move_ip(0, SPEED)
#         if self.rect.top > SCREEN_HEIGHT:
#             SCORE += 1
#             self.rect.top = 0
#             self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)

# class Player(pygame.sprite.Sprite):
#     def __init__(self):
#         super().__init__()
#         self.image = pygame.image.load("images/player.png").convert_alpha()
#         self.image = pygame.transform.scale(self.image, (45, 90))
#         self.rect = self.image.get_rect()
#         self.rect.center = (160, 520)

#     def move(self):
#         pressed_keys = pygame.key.get_pressed()
#         if self.rect.left > 0:
#             if pressed_keys[K_LEFT]:
#                 self.rect.move_ip(-5, 0)
#         if self.rect.right < SCREEN_WIDTH:
#             if pressed_keys[K_RIGHT]:
#                 self.rect.move_ip(5, 0)

# class Coin(pygame.sprite.Sprite):
#     def __init__(self):
#         super().__init__()
#         self.radius = 12
#         self.image = pygame.Surface((self.radius * 2, self.radius * 2), pygame.SRCALPHA)
#         pygame.draw.circle(self.image, YELLOW, (self.radius, self.radius), self.radius)
#         pygame.draw.circle(self.image, (255, 255, 150), (self.radius, self.radius), self.radius - 4)
#         self.rect = self.image.get_rect()
#         self.reset_pos()

#     def reset_pos(self):
#         self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), random.randint(-300, -50))

#     def move(self):
#         self.rect.move_ip(0, SPEED)
#         if self.rect.top > SCREEN_HEIGHT:
#             self.reset_pos()

# P1 = Player()
# E1 = Enemy()
# C1 = Coin()

# enemies = pygame.sprite.Group()
# enemies.add(E1)
# coins = pygame.sprite.Group()
# coins.add(C1)
# all_sprites = pygame.sprite.Group()
# all_sprites.add(P1, E1, C1)

# INC_SPEED = pygame.USEREVENT + 1
# pygame.time.set_timer(INC_SPEED, 1000)

# while True:
#     for event in pygame.event.get():
#         if event.type == INC_SPEED:
#             SPEED += 0.5
#         if event.type == QUIT:
#             pygame.quit()
#             sys.exit()

#     DISPLAYSURF.blit(background, (0, 0))

#     scores = font_small.render(f"Score: {SCORE}", True, BLACK)
#     coins_text = font_small.render(f"Coins: {COINS_COLLECTED}", True, BLACK)
#     DISPLAYSURF.blit(scores, (10, 10))
#     DISPLAYSURF.blit(coins_text, (SCREEN_WIDTH - 120, 10))

#     for entity in all_sprites:
#         DISPLAYSURF.blit(entity.image, entity.rect)
#         entity.move()

#     if pygame.sprite.spritecollideany(P1, enemies):
#         pygame.mixer.Sound('crash.mp3').play()
#         time.sleep(0.5)
#         DISPLAYSURF.fill(RED)
#         DISPLAYSURF.blit(game_over, (30, 250))
#         pygame.display.update()
#         for entity in all_sprites:
#             entity.kill()
#         time.sleep(2)
#         pygame.quit()
#         sys.exit()

#     if pygame.sprite.spritecollideany(P1, coins):
#         COINS_COLLECTED += 1
#         for coin in coins:
#             coin.reset_pos()

#     pygame.display.update()
#     FramePerSec.tick(FPS)
# # Snake
# import pygame
# import random
# import sys

# pygame.init()

# WIDTH = 600
# HEIGHT = 400
# CELL_SIZE = 20
# screen = pygame.display.set_mode((WIDTH, HEIGHT))
# pygame.display.set_caption("Snake Game")

# BLACK = (0, 0, 0)
# GREEN = (0, 255, 0)
# RED = (255, 0, 0)
# WHITE = (255, 255, 255)

# font = pygame.font.SysFont(None, 36)

# def draw_text(text, color, x, y):
#     img = font.render(text, True, color)
#     screen.blit(img, (x, y))

# def random_food_position(snake):
#     while True:
#         x = random.randrange(0, WIDTH // CELL_SIZE) * CELL_SIZE
#         y = random.randrange(0, HEIGHT // CELL_SIZE) * CELL_SIZE
#         if (x, y) not in snake:
#             return (x, y)

# def main():
#     clock = pygame.time.Clock()

#     snake = [(100, 100), (80, 100), (60, 100)]
#     direction = "RIGHT"
#     food = random_food_position(snake)
#     score = 0
#     level = 1
#     speed = 10  

#     while True:
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 pygame.quit()
#                 sys.exit()

#             if event.type == pygame.KEYDOWN:
#                 if event.key == pygame.K_UP and direction != "DOWN":
#                     direction = "UP"
#                 elif event.key == pygame.K_DOWN and direction != "UP":
#                     direction = "DOWN"
#                 elif event.key == pygame.K_LEFT and direction != "RIGHT":
#                     direction = "LEFT"
#                 elif event.key == pygame.K_RIGHT and direction != "LEFT":
#                     direction = "RIGHT"

#         x, y = snake[0]
#         if direction == "UP":
#             y -= CELL_SIZE
#         elif direction == "DOWN":
#             y += CELL_SIZE
#         elif direction == "LEFT":
#             x -= CELL_SIZE
#         elif direction == "RIGHT":
#             x += CELL_SIZE

#         new_head = (x, y)

#         if x < 0 or x >= WIDTH or y < 0 or y >= HEIGHT:
#             pygame.quit()
#             sys.exit()

#         if new_head in snake:
#             pygame.quit()
#             sys.exit()

#         snake.insert(0, new_head)

#         if new_head == food:
#             score += 1
#             if score % 3 == 0:
#                 level += 1
#                 speed += 3  
#             food = random_food_position(snake)
#         else:
#             snake.pop()

#         screen.fill(BLACK)
#         for block in snake:
#             pygame.draw.rect(screen, GREEN, (block[0], block[1], CELL_SIZE, CELL_SIZE))
#         pygame.draw.rect(screen, RED, (food[0], food[1], CELL_SIZE, CELL_SIZE))

#         draw_text(f"Score: {score}", WHITE, 10, 10)
#         draw_text(f"Level: {level}", WHITE, 10, 40)

#         pygame.display.flip()
#         clock.tick(speed)

# if __name__ == "__main__":
#     main()
# # Paint
# import pygame

# def main():
#     pygame.init()
#     screen = pygame.display.set_mode((800, 600))
#     clock = pygame.time.Clock()
#     pygame.display.set_caption("Drawing App")

#     radius = 15
#     x = 0
#     y = 0
#     mode = 'pen'  
#     color = (0, 0, 255)  
#     drawing = False
#     start_pos = None
#     points = []

#     def drawLineBetween(screen, index, start, end, width, color):
#         dx = start[0] - end[0]
#         dy = start[1] - end[1]
#         iterations = max(abs(dx), abs(dy))
#         for i in range(iterations):
#             progress = 1.0 * i / iterations
#             aprogress = 1 - progress
#             x = int(aprogress * start[0] + progress * end[0])
#             y = int(aprogress * start[1] + progress * end[1])
#             pygame.draw.circle(screen, color, (x, y), width)

#     while True:
#         pressed = pygame.key.get_pressed()
#         alt_held = pressed[pygame.K_LALT] or pressed[pygame.K_RALT]
#         ctrl_held = pressed[pygame.K_LCTRL] or pressed[pygame.K_RCTRL]

#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 return
#             if event.type == pygame.KEYDOWN:
#                 if event.key == pygame.K_w and ctrl_held:
#                     return
#                 if event.key == pygame.K_F4 and alt_held:
#                     return
#                 if event.key == pygame.K_ESCAPE:
#                     return

#                 if event.key == pygame.K_p:
#                     mode = 'pen'
#                 elif event.key == pygame.K_r:
#                     mode = 'rect'
#                 elif event.key == pygame.K_c:
#                     mode = 'circle'
#                 elif event.key == pygame.K_e:
#                     mode = 'eraser'

#                 elif event.key == pygame.K_1:
#                     color = (255, 0, 0)   
#                 elif event.key == pygame.K_2:
#                     color = (0, 255, 0)   
#                 elif event.key == pygame.K_3:
#                     color = (0, 0, 255)   
#                 elif event.key == pygame.K_4:
#                     color = (255, 255, 0) 

#             if event.type == pygame.MOUSEBUTTONDOWN:
#                 if event.button == 1:  
#                     drawing = True
#                     start_pos = event.pos
#                     points = [event.pos]
#                 elif event.button == 3:  
#                     radius = max(1, radius - 1)
#                 elif event.button == 2:  
#                     radius = min(200, radius + 1)

#             if event.type == pygame.MOUSEBUTTONUP:
#                 if event.button == 1:
#                     drawing = False
#                     if mode == 'rect':
#                         end_pos = event.pos
#                         rect = pygame.Rect(start_pos, (end_pos[0] - start_pos[0],
#                                                        end_pos[1] - start_pos[1]))
#                         pygame.draw.rect(screen, color, rect, 2)
#                     elif mode == 'circle':
#                         end_pos = event.pos
#                         radius_circle = int(((end_pos[0]-start_pos[0])**2 + (end_pos[1]-start_pos[1])**2)**0.5)
#                         pygame.draw.circle(screen, color, start_pos, radius_circle, 2)
#                     start_pos = None

#             if event.type == pygame.MOUSEMOTION and drawing:
#                 position = event.pos
#                 if mode == 'pen':
#                     drawLineBetween(screen, 0, points[-1], position, radius, color)
#                     points.append(position)
#                 elif mode == 'eraser':
#                     pygame.draw.circle(screen, (0, 0, 0), position, radius)

#         pygame.display.flip()
#         clock.tick(60)

# if __name__ == "__main__":
#     main()
