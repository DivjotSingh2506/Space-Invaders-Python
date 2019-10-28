import math
import random
import winsound
import os
import pygame
from pygame import mixer
import pygame, sys
from pygame.locals import *

# Intialize the pygame
pygame.init()
pygame.mixer.init()

os.environ['SDL_VIDEO_CENTERED'] = '1'

# create the screen
screen = pygame.display.set_mode((800, 600))

# Background
background = pygame.image.load('bg5.png')

# Sound
mixer.music.load("music.wav")
mixer.music.play(-1)

# Caption and Icon
pygame.display.set_caption("Space Invaders-v.1.1(beta)")
icon = pygame.image.load('invaderr.png')
pygame.display.set_icon(icon)

# Player
playerImg = pygame.image.load('ship1.gif')
playerX = 370
playerY = 480
playerX_change = 0
number_of_players = 1

# Enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('invade1.gif'))
    enemyX.append(random.randint(0, 736))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(4)
    enemyY_change.append(50)

# Bullet

# Ready - You can't see the bullet on the screen
# Fire - The bullet is currently moving

bulletImg = pygame.image.load('bullet7.gif')
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 10
bullet_state = "ready"

# Score

score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)

textX = 10
testY = 10

# Game Over
over_font = pygame.font.Font('freesansbold.ttf', 64)

def show_score(x, y):
    score = font.render("Score : " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))


def game_over_text():
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (200, 250))


def player(x, y):
    screen.blit(playerImg, (x, y))


def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))


def isCollision(enemyX, enemyY, bulletX, bulletY, playerX, playerY):
    distance = math.sqrt(math.pow(enemyX - bulletX, 2) + (math.pow(enemyY - bulletY, 2)))
    
    if distance < 27 and bulletY < 480:
        return True
    else:
        return False

def isCollision1(enemyX, enemyY, bulletX, bulletY, playerX, playerY):
    dist = math.sqrt(math.pow(enemyX - playerX, 2) + (math.pow(enemyY - playerY, 2)))
    if dist < 20 and bulletY == 480:
        return True
    else:
        return False

def stop_mixer():
    if pygame.mixer.music.stop() or pygame.mixer.stop() == True:
            pygame.mixer.stop()
            pygame.mixer.music.stop()
            pygame.mixer.quit()

# Game Loop
running = True
while running:

    # RGB = Red, Green, Blue
    screen.fill((0, 0, 0))
    # Background Image
    screen.blit(background, (0, 0))
    for event in pygame.event.get():
        if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
            
       

        # if keystroke is pressed check whether its right or left
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -5
            if event.key == pygame.K_RIGHT:
                playerX_change = 5
            if event.key == pygame.K_SPACE:
                if bullet_state is "ready":
                    bulletSound = mixer.Sound("shot.wav")
                    bulletSound.play()
                    # Get the current x cordinate of the spaceship
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)
                    

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0
    

                                
    # 5 = 5 + -0.1 -> 5 = 5 - 0.1
    # 5 = 5 + 0.1

    playerX += playerX_change
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736
    
        
    # Enemy Movement
    for i in range(num_of_enemies):

        # Game Over
        if enemyY[i] > 500:
            for j in range(num_of_enemies):
                enemyY[j] = 2000   
            game_over_text()
            stop_mixer()
            break

        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 4
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -4
            enemyY[i] += enemyY_change[i]

       

        
        # Collision b/w bullet and enemy
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY, playerX, playerY)
        if collision:
            explosionSound = mixer.Sound("explosion.wav")
            explosionSound.play()
            bulletY = 480
            bullet_state = "ready"
            score_value += 1
            enemyX[i] = random.randint(0, 736)
            enemyY[i] = random.randint(50, 150)

        enemy(enemyX[i], enemyY[i], i)

          
        #Collision b/w player and enemy
        collision2 = isCollision1(enemyX[i], enemyY[i], bulletX, bulletY, playerX, playerY)
        if collision2:
            winsound.PlaySound("explosive",winsound.SND_ASYNC)
            for j in range(num_of_enemies):
                    enemyY[j] = 2000
                    winsound.PlaySound("explosive",winsound.SND_ASYNC)
            game_over_text() 
            stop_mixer()
            

    # Bullet Movement
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"

    if bullet_state is "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    player(playerX, playerY)
    show_score(textX, testY)
    pygame.display.update()

           
           
        
