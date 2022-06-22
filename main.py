import pygame
import random
import math
from pygame import mixer    # handle music


# initialize the pygame
pygame.init()

# create the screen
screen = pygame.display.set_mode((800, 600))

# background image
background = pygame.image.load('background.jpg')

# background music
#mixer.music.load('background.wav')
#mixer.music.play(-1)    # by adding -1, the music will play in loop, otherwise music will only play once


# Title and Icon
pygame.display.set_caption("Game Title Here")
icon = pygame.image.load('image_name.png')
pygame.display.set_icon(icon)


# add player
playerImg = pygame.image.load('player.png')
playerX = 370       # place playerImg at 370 from left
playerY = 480       # place playerImg at 480 from top
playerX_Move = 0
playerY_Move = 0

# add enemies
enemyImg = []
enemyX = []
enemyY = []
enemyX_Move = []
enemyY_Move = []
num_of_enemies = 6
for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('enemy.png'))
    enemyX.append(random.randint(0, 735))
    enemyY.append(random.randint(50, 150))
    enemyX_Move.append(0.3)
    enemyY_Move.append(40)

# add bullet
bulletImg = pygame.image.load('bullet.png')
bulletX = 0
bulletY = playerY
bulletX_Move = 0
bulletY_Move = 0.5
bullet_state = "ready"  # "ready" means bullet is not fired yet
                        # "fire" means bullet is fired

score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)     # freesansbold.ttf is free font in pygame module
textX = 10
textY = 10

# game over text
over_font = pygame.font.Font('freesansbold.ttf', 64)


def show_score(x, y):
    score = font.render("Score: " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))


def game_over_text():
    over_text = over_font.render("Game Over", True, (255, 255, 255))
    screen.blit(over_text, (200, 250))


def player(x, y):
    # draw the image on the screen at X Y coordinate
    screen.blit(playerImg, (x, y))


def enemy(x, y, i):
    # draw the image on the screen at X Y coordinate
    screen.blit(enemyImg[i], (x, y))

def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))    # by x+16 and y+10 is to set bullet fire from the top of the space ship


def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt(math.pow(enemyX - bulletX, 2) + math.pow(enemyY - bulletY, 2))
    if distance < 36:
        return True
    else:
        return False


def spaceShipCollision(enemyX, enemyY, playerX, playerY):
    distance1 = math.sqrt(math.pow(enemyX - playerX, 2) + math.pow(enemyY - playerY, 2))
    if distance1 < 36:
        return True
    else:
        return False



    # game loop, quit when click close
running = True
while running:

    # set screen background color in RGB format
    screen.fill((0, 0, 0))
    # add background image
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # move left right up down based on what arrow key are pressed
        if event.type == pygame.KEYDOWN:        # KEYDOWN means key are pressed down
            if event.key == pygame.K_LEFT:
                playerX_Move = -0.5
            if event.key == pygame.K_RIGHT:
                playerX_Move = 0.5
            if event.key == pygame.K_UP:
                playerY_Move = -0.5
            if event.key == pygame.K_DOWN:
                playerY_Move = 0.5
            if event.key == pygame.K_SPACE and bullet_state == "ready":
              # bullet_sound = mixer.Sound('name.wav')      # add bullet shooting sound
              # bullet_sound.play()
                bulletX = playerX
                bulletY = playerY
                fire_bullet(bulletX, bulletY)

        # stop moving when detect key released
        if event.type == pygame.KEYUP:          # KEYUP means key are released
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT \
                    or event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                playerY_Move = 0
                playerX_Move = 0

# player movement
    playerX += playerX_Move
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:    # 736 = 800- player image width which is 64 px
        playerX = 736
    playerY += playerY_Move
    if playerY <= 0:
        playerY = 0
    elif playerY >= 536:    # 736 = 800- player image width which is 64 px
        playerY = 536

# enemy movement
    for i in range(num_of_enemies):

        # Game over
        if spaceShipCollision(enemyX[i], enemyY[i], playerX, playerY):
            for j in range(num_of_enemies):
                enemyX_Move = 0
                enemyY_Move = 0
            game_over_text()
            break

        enemyX[i] += enemyX_Move[i]
        if enemyX[i] <= 0:
            enemyX_Move[i] = 0.3
            enemyY[i] += enemyY_Move[i]
        elif enemyX[i] >= 736:  # 736 = 800- player image width which is 64 px
            enemyX_Move[i] = -0.3
            enemyY[i] += enemyY_Move[i]

        if enemyY[i] > 536:
            enemyY[i] = random.randint(50,150)

        # check enemy collision
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
          # explosion_sound = mixer.Sound('name.wav')      # add enemy explosion sound
          # explosion_sound.play()
            bulletY = playerY
            bullet_state = "ready"
            score_value += 1
            enemyX[i] = random.randint(0, 735)
            enemyY[i] = random.randint(50, 150)

        enemy(enemyX[i], enemyY[i], i)

    # bullet movement
    if bulletY <= 0:                    # when bullet is out of screen
        bulletY = playerY               # reset bullet position to top of space ship
        bullet_state = "ready"          # set bullet_state to ready to shoot another bullet
    if bullet_state == "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_Move



    player(playerX, playerY)
    show_score(textX, textY)
    pygame.display.update()



