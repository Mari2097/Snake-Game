import pygame
import random
import os
import json

#-------init-------
pygame.init()
WIDTH ,HEIGHT = 600 ,400
BLOCK_SIZE =20
screen =pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Snake Game")
clock =pygame.time.Clock()
font =pygame.font.SysFont("Arial" ,24)

#-------color-------
WHITE =(255,255,255)
GREEN =(0,200,0)
RED =(255,0,0)
BLACK=(0,0,0)
YELLOW =(255,255,0)

#--------paths------
SCORE_FILE ="high_score.json"

def load_high_score():
    if os.path.exists(SCORE_FILE):
        try:
            with open(SCORE_FILE ,"r") as f:
                return json.load(f).get("high_score" ,0)
        except json.JSONDecodeError:
            return 0
    return 0

def save_high_score(score):
    with open(SCORE_FILE ,"w") as f:
        json.dump({"high_score" : score} ,f)

#------draw--------
def draw_snake(snake):
    for segment in snake :
        pygame.draw.rect(screen , GREEN ,(segment[0] , segment[1], BLOCK_SIZE, BLOCK_SIZE))

def draw_text_center(text ,color ,y):
    renered =font.render(text ,True ,color )
    rect =renered.get_rect(center =(WIDTH//2 ,y))
    screen.blit(renered ,rect)


#------main menu----
def show_menu():
    while True:
        screen.fill(BLACK)
        draw_text_center("Press ENTER to start" ,YELLOW, HEIGHT//2 -30)
        draw_text_center("Press ESC to exit" ,RED ,HEIGHT//2 +10)
        pygame.display.update()

        for e in pygame.event.get():
            if e.type ==pygame.QUIT:
                pygame.quit(); exit()
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_RETURN:
                    return
                elif e.key ==pygame.K_ESCAPE:
                    pygame.quit(); exit()

#------game loop-----
def game():
    print("start game")
    x, y =WIDTH // 2 ,HEIGHT // 2 
    dx, dy = 0,0
    snake = [(x,y)]
    length = 1
    score = 0 
    high_score = load_high_score()

    food_x = random.randrange(0 ,WIDTH - BLOCK_SIZE ,BLOCK_SIZE)
    food_y = random.randrange(0 ,HEIGHT - BLOCK_SIZE ,BLOCK_SIZE)
    food = [food_x, food_y]

    running =True
    while running:
        screen.fill(BLACK)

        for event in pygame.event.get():
           if event.type ==pygame.QUIT:
               running =False
           elif event.type ==pygame.KEYDOWN:
              if event.key == pygame.K_UP and dy == 0:
                  dx, dy = 0, -BLOCK_SIZE
              elif event.key == pygame.K_DOWN and dy == 0:
                  dx, dy = 0, BLOCK_SIZE
              elif event.key == pygame.K_LEFT and dx == 0:
                  dx, dy = -BLOCK_SIZE, 0
              elif event.key == pygame.K_RIGHT and dx == 0:
                  dx, dy = BLOCK_SIZE, 0

        # --- موقعیت جدید سر مار ---
        x += dx
        y += dy

        # --- عبور از دیوار ---
        if x < 0:
            x = WIDTH - BLOCK_SIZE
        elif x >= WIDTH:
            x = 0
        if y < 0:
            y = HEIGHT - BLOCK_SIZE
        elif y >= HEIGHT:
            y = 0

        head = (x,y)

        # --- برخورد با بدن ---
        if head in snake[:-1]:
            if score > high_score:
                save_high_score(score)
            running = False

        snake.append(head)
        if len(snake) > length:
            snake.pop(0)

        # --- خوردن غذا ---
        if x == food [0] and y == food [1]:
            score += 1
            length += 1
            while True:
                new_food_x = random.randrange(0 ,WIDTH - BLOCK_SIZE ,BLOCK_SIZE)
                new_food_y = random.randrange(0, HEIGHT - BLOCK_SIZE ,BLOCK_SIZE)
                if (new_food_x, new_food_y) not in snake:
                    food = [new_food_x, new_food_y]
                    break

        # --- رسم عناصر ---
        draw_snake(snake)
        pygame.draw.rect(screen ,RED ,(*food , BLOCK_SIZE ,BLOCK_SIZE))

        screen.blit(font.render(f"Score : {score}",True ,WHITE) ,(10, 10))
        screen.blit(font.render(f"High Score : {high_score}" ,True ,WHITE) ,(10 ,40))
        pygame.display.update()
        clock.tick(12)

    # --- صفحه Game Over با گزینه بازی مجدد ---
    screen.fill(BLACK)
    draw_text_center(f"Game Over! Final Score: {score}" ,RED ,HEIGHT//2 -40)
    draw_text_center("Press ENTER to play again" ,YELLOW ,HEIGHT//2)
    draw_text_center("Press ESC to exit" ,WHITE ,HEIGHT//2 +40)
    pygame.display.update()
    
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    waiting = False
                    game()  # بازی مجدد
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit(); exit()

#------run game----
while True:
    show_menu()
    game()
