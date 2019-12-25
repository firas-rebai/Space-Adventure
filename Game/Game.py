import pygame
import math
import random

pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.font.init()
# ___________________________________________________________________________________________________________________#
# game title and icon
font = pygame.font.Font('electroharmonix.ttf', 32)
font1 = pygame.font.Font('electroharmonix.ttf', 80)
text = font.render("Score", True, (255, 255, 255), (64, 64, 64))
scoreRect = text.get_rect()
win_textRect = text.get_rect()
scoreRect.center = (50, 15)
win_textRect.center = (300, 200)
pygame.display.set_caption("Space Adventure")
win_text = font1.render("You Win", True, (0, 0, 0), (64, 64, 64))
lost_text = font1.render("GAME OVER", True, (0, 0, 0), (64, 64, 64))
# ___________________________________________________________________________________________________________________#
# health
full_heart = pygame.image.load('full heart.png')
empty_heart = pygame.image.load('empty heart.png')
# player
PlayerImg = pygame.image.load('ufo.png')
PlayerX = 500
PlayerY = 540
PlayerX_change = 0
PlayerY_change = 0
health = 3
HX1 = 725
HX2 = 750
HX3 = 775
HY = 5
# enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
num_enemies = 3
pos = 60
for i in range(num_enemies):
    enemyImg.append(pygame.image.load('monster.png'))
    enemyX.append(pos)
    enemyY.append(pos)
    enemyX_change.append(0.3)
    pos += 60
enemyY_change = 40
# bullet
bulletImg = pygame.image.load('laser.png')
bullet_state = "ready"
eb_state = "ready"
bullet_change = 1
bulletY = 0
bulletX = 0
score_value = 0
counter = 0
ebY = 0
ebX = 0


def bullet(x, y):
    global bullet_state
    screen.blit(bulletImg, (x + 16, y + 10))
    bullet_state = "fire"


def enemy_bullet(x, y):
    global eb_state
    screen.blit(bulletImg, (x, y))
    eb_state = "fire"


def hit(x, y):
    screen.blit(pygame.image.load('explosion.png'), (x, y))


def player(x, y):
    screen.blit(PlayerImg, (x, y))


def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))


def distance(x1, y1, x2, y2):
    d = math.sqrt(pow(x1 - x2, 2) + pow(y1 - y2, 2))
    return d


# game loop
exit_time = 0
running = True
while running:
    screen.fill((64, 64, 64))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                PlayerX_change = 0.5
            if event.key == pygame.K_LEFT:
                PlayerX_change = -0.5
            if event.key == pygame.K_DOWN:
                PlayerY_change = 0.4
            if event.key == pygame.K_UP:
                PlayerY_change = -0.4
            if event.key == pygame.K_SPACE:
                bulletY = PlayerY
                bulletX = PlayerX
                bullet(bulletX, bulletY)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT:
                PlayerX_change = 0
            if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                PlayerY_change = 0
    if PlayerX < 0:
        PlayerX = 0
    elif PlayerX > 734:
        PlayerX = 734
    if PlayerY < 0:
        PlayerY = 0
    elif PlayerY > 534:
        PlayerY = 534

    # ___enemy_movement______________________________#
    for i in range(num_enemies):
        if enemyX[i] < 100:
            enemyX_change[i] = 0.3
            enemyY[i] += enemyY_change
        elif enemyX[i] > 700:
            enemyX_change[i] = -0.3
            enemyY[i] -= enemyY_change

        enemyX[i] += enemyX_change[i]
        enemy(enemyX[i], enemyY[i], i)
        # collision
        if distance(bulletX, bulletY, enemyX[i], enemyY[i]) <= 35:
            hit(enemyX[i] - 20, enemyY[i] - 20)
            score_value += 1
            bullet_state = "ready"
            enemyX[i] = 10000
            enemyY[i] = 10000
            enemyX_change[i] = 0
            enemyY_change = 0
    # ______bullet_____________________________#
    counter += 1
    print(counter)
    if counter % 1000 == 0:
        ebX = enemyX[1]
        ebY = enemyY[1]
        enemy_bullet(ebX, ebY)
    if eb_state is "fire":
        enemy_bullet(ebX, ebY)
        ebY += 0.5
    if bullet_state is "fire":
        bullet(bulletX, bulletY)
        bulletY -= bullet_change
    if bulletY <= 0:
        bullet_state = "ready"
    # ___score_______________________________#
    if pygame.font.get_init() is True:
        font = pygame.font.Font(pygame.font.get_default_font(), 50)
    # ____player_movement_______________________________#
    PlayerX += PlayerX_change
    PlayerY += PlayerY_change
    player(PlayerX, PlayerY)
    # ________score_______________________________#

    score = "score  " + str(score_value)
    text = font.render(score, True, (0, 0, 0), (64, 64, 64))
    screen.blit(text, scoreRect)
    if score_value == num_enemies - 1:
        screen.blit(win_text, win_textRect)
        exit_time += 1
        if exit_time == 1000:
            running = False
    # health
    if distance(PlayerX + 15, PlayerY - 15, ebX, ebY) <= 35:
        health -= 1
        PlayerX = 800
        PlayerY = 600
    if health == 3:
        screen.blit(full_heart, (HX1, HY))
        screen.blit(full_heart, (HX2, HY))
        screen.blit(full_heart, (HX3, HY))
    if health == 2:
        screen.blit(full_heart, (HX1, HY))
        screen.blit(full_heart, (HX2, HY))
        screen.blit(empty_heart, (HX3, HY))
    if health == 1:
        screen.blit(full_heart, (HX1, HY))
        screen.blit(empty_heart, (HX2, HY))
        screen.blit(empty_heart, (HX3, HY))
    if health == 0:
        screen.blit(empty_heart, (HX1, HY))
        screen.blit(empty_heart, (HX2, HY))
        screen.blit(empty_heart, (HX3, HY))
        screen.blit(lost_text, win_textRect)
        exit_time += 1
        PlayerY = 600
        PlayerX = 800
        if exit_time == 1000:
            running = False

    pygame.display.update()
