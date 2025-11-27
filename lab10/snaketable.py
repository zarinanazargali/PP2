import pygame
import random
import sys
import json
import psycopg2
from typing import List, Tuple, Optional

DB_NAME = "postgres"
DB_USER = "postgres"
DB_PASSWORD = "Hope2007@"
DB_HOST = "localhost"
DB_PORT = "5432"

pygame.init()
WIDTH = 600
HEIGHT = 400
CELL_SIZE = 20
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game (PostgreSQL)")
FONT = pygame.font.SysFont(None, 28)
BIG_FONT = pygame.font.SysFont(None, 48)

BG = (255, 182, 193)  
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
HEAD_COLOR = (0, 200, 0)
BODY_COLOR = (0, 150, 0)
FOOD_COLOR = (200, 50, 50)
WALL_COLOR = (100, 100, 100)
BUTTON_COLOR = (50, 120, 200)
BUTTON_HOVER = (70, 140, 220)
TEXTBOX_BG = (230, 230, 230)
PAUSE_OVERLAY = (255, 255, 0)

GRID_W = WIDTH // CELL_SIZE
GRID_H = HEIGHT // CELL_SIZE

class DB:
    def __init__(self):
        self.conn = psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT
        )
        self.cur = self.conn.cursor()
        self._init_tables()

    def _init_tables(self):
        self.cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            username VARCHAR(50) UNIQUE NOT NULL,
            current_level INT DEFAULT 1
        );
        """)
        self.cur.execute("""
        CREATE TABLE IF NOT EXISTS user_score (
            id SERIAL PRIMARY KEY,
            user_id INT NOT NULL REFERENCES users(id),
            score INT DEFAULT 0,
            snake_body TEXT NOT NULL,
            direction VARCHAR(10) NOT NULL,
            food_position TEXT NOT NULL,
            level INT NOT NULL
        );
        """)
        self.conn.commit()

    def get_or_create_user(self, username: str) -> Tuple[int,int]:
        self.cur.execute("SELECT id, current_level FROM users WHERE username=%s", (username,))
        row = self.cur.fetchone()
        if row:
            return row[0], row[1]
        self.cur.execute("INSERT INTO users (username) VALUES (%s) RETURNING id", (username,))
        user_id = self.cur.fetchone()[0]
        self.conn.commit()
        return user_id, 1

    def update_user_level(self, user_id: int, level: int):
        self.cur.execute("UPDATE users SET current_level=%s WHERE id=%s", (level, user_id))
        self.conn.commit()

    def save_state(self, user_id: int, score: int, snake: List[Tuple[int,int]], direction: str, food: Tuple[int,int], level: int):
        snake_json = json.dumps(snake)
        food_json = json.dumps(food)
        self.cur.execute("DELETE FROM user_score WHERE user_id=%s", (user_id,))
        self.cur.execute("""
        INSERT INTO user_score (user_id, score, snake_body, direction, food_position, level)
        VALUES (%s, %s, %s, %s, %s, %s)
        """, (user_id, score, snake_json, direction, food_json, level))
        self.conn.commit()

    def load_state(self, user_id: int) -> Optional[dict]:
        self.cur.execute("SELECT score, snake_body, direction, food_position, level FROM user_score WHERE user_id=%s", (user_id,))
        row = self.cur.fetchone()
        if not row:
            return None
        return {
            "score": row[0],
            "snake": json.loads(row[1]),
            "direction": row[2],
            "food": tuple(json.loads(row[3])),
            "level": row[4]
        }
LEVELS = {
    1: {"speed": 8,  "walls": []},
    2: {"speed": 10, "walls": lambda: [(GRID_W//2*CELL_SIZE, y*CELL_SIZE) for y in range(3, GRID_H-3)]},
    3: {"speed": 12, "walls": lambda: [(x*CELL_SIZE, GRID_H//2*CELL_SIZE) for x in range(3, GRID_W-3)]},
    4: {"speed": 14, "walls": lambda: [((GRID_W//4 + i)*CELL_SIZE, (GRID_H//4)*CELL_SIZE) for i in range(6)] + [((GRID_W//4 + i)*CELL_SIZE, (GRID_H//4+6)*CELL_SIZE) for i in range(6)]},
    5: {"speed": 18, "walls": lambda: [((5+i)*CELL_SIZE, (5 + (i%6))*CELL_SIZE) for i in range(18)]},
}
MAX_LEVEL = max(LEVELS.keys())

def get_walls(level: int) -> List[Tuple[int,int]]:
    w = LEVELS.get(level, LEVELS[1])["walls"]
    return w() if callable(w) else w

def get_speed(level: int) -> int:
    return LEVELS.get(level, LEVELS[1])["speed"]

def draw_text(surf, text, color, x, y, font=FONT):
    surf.blit(font.render(text, True, color), (x, y))

def random_food(snake: List[Tuple[int,int]], walls: List[Tuple[int,int]]) -> Tuple[int,int]:
    attempts = 0
    while True:
        x = random.randrange(0, GRID_W) * CELL_SIZE
        y = random.randrange(0, GRID_H) * CELL_SIZE
        p = (x,y)
        if p in snake or p in walls:
            attempts += 1
            if attempts>1000:
                for yy in range(GRID_H):
                    for xx in range(GRID_W):
                        q = (xx*CELL_SIZE, yy*CELL_SIZE)
                        if q not in snake and q not in walls:
                            return q
            continue
        return p
class Button:
    def __init__(self, rect, label):
        self.rect = rect
        self.label = label
    def draw(self, surf):
        mx,my = pygame.mouse.get_pos()
        hovered = self.rect.collidepoint((mx,my))
        color = BUTTON_HOVER if hovered else BUTTON_COLOR
        pygame.draw.rect(surf, color, self.rect)
        draw_text(surf, self.label, WHITE, self.rect.x+10, self.rect.y+8)
    def clicked(self,pos):
        return self.rect.collidepoint(pos)

def login_screen(db: DB):
    clock = pygame.time.Clock()
    input_box = pygame.Rect(WIDTH//2 - 150, HEIGHT//2 - 90, 300, 40)
    username = ""
    active = True
    info_text = ""
    saved_exists = False
    saved_state = None
    user_id = None
    saved_level = 1

    btn_continue = Button(pygame.Rect(WIDTH//2 - 140, HEIGHT//2 + 10, 120, 40), "Continue")
    btn_new = Button(pygame.Rect(WIDTH//2 + 20, HEIGHT//2 + 10, 120, 40), "New Game")

    while True:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type==pygame.KEYDOWN and active:
                if event.key==pygame.K_BACKSPACE:
                    username = username[:-1]
                elif event.key==pygame.K_RETURN:
                    if username.strip():
                        user_id, saved_level = db.get_or_create_user(username.strip())
                        saved_state = db.load_state(user_id)
                        saved_exists = saved_state is not None
                        if saved_exists:
                            info_text = f"User found. Saved level: {saved_level}. Choose Continue or New Game."
                        else:
                            info_text = f"No saved game. Press Continue to start new game at level {saved_level}."
                        active = False
                else:
                    if len(username)<20 and event.unicode.isprintable():
                        username += event.unicode
            if event.type==pygame.MOUSEBUTTONDOWN and not active:
                mx,my = event.pos
                if btn_continue.clicked((mx,my)):
                    return username.strip(), user_id, saved_state, "CONTINUE"
                elif btn_new.clicked((mx,my)):
                    return username.strip(), user_id, None, "NEW"

        SCREEN.fill(BG)
        draw_text(SCREEN,"Enter username:",BLACK,WIDTH//2 - 110, HEIGHT//2 - 140)
        pygame.draw.rect(SCREEN,TEXTBOX_BG,input_box)
        draw_text(SCREEN, username or "type name and press Enter", BLACK if username else (120,120,120), input_box.x+8,input_box.y+6)
        if info_text:
            draw_text(SCREEN, info_text, BLACK, WIDTH//2 - 260, HEIGHT//2 - 40)
        if not active:
            btn_continue.draw(SCREEN)
            btn_new.draw(SCREEN)
            draw_text(SCREEN, "Continue loads saved game. New Game starts fresh (same level).", BLACK, WIDTH//2 - 260, HEIGHT//2 + 60, font=pygame.font.SysFont(None,20))
        pygame.display.flip()
        clock.tick(30)

def run_game(db: DB, username, user_id, saved_state, start_mode):
    if saved_state and start_mode=="CONTINUE":
        snake = [tuple(p) for p in saved_state["snake"]]
        direction = saved_state["direction"]
        food = tuple(saved_state["food"])
        score = saved_state["score"]
        level = saved_state["level"]
    else:
        _, saved_level = db.get_or_create_user(username)
        level = saved_state["level"] if (saved_state and start_mode=="NEW") else saved_level
        mid_x = (GRID_W//2)*CELL_SIZE
        mid_y = (GRID_H//2)*CELL_SIZE
        snake = [(mid_x,mid_y),(mid_x-CELL_SIZE,mid_y),(mid_x-2*CELL_SIZE,mid_y)]
        direction="RIGHT"
        walls = get_walls(level)
        food = random_food(snake,walls)
        score = 0

    paused=False
    clock=pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                db.save_state(user_id,score,snake,direction,food,level)
                pygame.quit()
                sys.exit()
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_ESCAPE:
                    db.save_state(user_id,score,snake,direction,food,level)
                    pygame.quit()
                    sys.exit()
                elif event.key==pygame.K_p:
                    paused = not paused
                    db.save_state(user_id,score,snake,direction,food,level)
                    if paused:
                        print(f"[PAUSED] Saved user {username} score={score} level={level}")
                    else:
                        print("[RESUMED]")
                elif not paused:
                    if event.key==pygame.K_UP and direction!="DOWN": direction="UP"
                    elif event.key==pygame.K_DOWN and direction!="UP": direction="DOWN"
                    elif event.key==pygame.K_LEFT and direction!="RIGHT": direction="LEFT"
                    elif event.key==pygame.K_RIGHT and direction!="LEFT": direction="RIGHT"

        if not paused:
            head_x,head_y = snake[0]
            if direction=="UP": head_y-=CELL_SIZE
            elif direction=="DOWN": head_y+=CELL_SIZE
            elif direction=="LEFT": head_x-=CELL_SIZE
            elif direction=="RIGHT": head_x+=CELL_SIZE
            new_head=(head_x,head_y)
            walls=get_walls(level)
            if head_x<0 or head_x>=WIDTH or head_y<0 or head_y>=HEIGHT or new_head in snake or new_head in walls:
                db.save_state(user_id,score,snake,direction,food,level)
                print("Game Over")
                pygame.quit()
                sys.exit()
            snake.insert(0,new_head)
            if new_head==food:
                score+=1
                new_level = min(1+score//3, MAX_LEVEL)
                if new_level!=level:
                    level=new_level
                    db.update_user_level(user_id,level)
                    walls=get_walls(level)
                    food=random_food(snake,walls)
                else:
                    food=random_food(snake,walls)
            else:
                snake.pop()

        SCREEN.fill(BG)
        for wx,wy in get_walls(level):
            pygame.draw.rect(SCREEN,WALL_COLOR,(wx,wy,CELL_SIZE,CELL_SIZE))
        pygame.draw.rect(SCREEN,FOOD_COLOR,(food[0],food[1],CELL_SIZE,CELL_SIZE))
        for i,seg in enumerate(snake):
            color = HEAD_COLOR if i==0 else BODY_COLOR
            pygame.draw.rect(SCREEN,color,(seg[0],seg[1],CELL_SIZE,CELL_SIZE))
        draw_text(SCREEN,f"User: {username}",BLACK,10,6)
        draw_text(SCREEN,f"Score: {score}",BLACK,10,30)
        draw_text(SCREEN,f"Level: {level}",BLACK,10,54)
        draw_text(SCREEN,"P = Pause & Save",BLACK,10,78)
        if paused:
            overlay=BIG_FONT.render("PAUSED",True,PAUSE_OVERLAY)
            rect=overlay.get_rect(center=(WIDTH//2,HEIGHT//2))
            SCREEN.blit(overlay,rect)
        pygame.display.flip()
        clock.tick(get_speed(level))

def main():
    db = DB()
    username, user_id, saved_state, mode = login_screen(db)
    run_game(db, username, user_id, saved_state, mode)

if __name__=="__main__":
    main()