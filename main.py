import pygame
import random

# Define constants for screen width and height
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Initialize the game
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Super Star Wars Game")

clock = pygame.time.Clock()

# Define colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
GOLD = (255, 215, 0)
BLACK = (0, 0, 0)

# Load images
player_image = pygame.image.load('mario.png')
enemy_image = pygame.image.load('goomba.png')
background_image = pygame.image.load('background.jpg')
coin_image = pygame.image.load('coin.png')
powerup_image = pygame.image.load('powerup.png')

# Resize images
player_image = pygame.transform.scale(player_image, (40, 60))
enemy_image = pygame.transform.scale(enemy_image, (40, 40))
coin_image = pygame.transform.scale(coin_image, (30, 30))
powerup_image = pygame.transform.scale(powerup_image, (30, 30))

# Define player properties
player_width = 40
player_height = 60
player_x = 400
player_y = SCREEN_HEIGHT - player_height - 10
player_speed = 5

# Define enemy properties
enemies = []
enemy_width = 40
enemy_height = 40
enemy_speed = 3
num_enemies = 3

for i in range(num_enemies):
    enemy_x = random.randint(0, SCREEN_WIDTH - enemy_width)
    enemy_y = random.randint(50, 150)
    enemies.append([enemy_x, enemy_y])

# Define coin properties
coins = []
coin_width = 30
coin_height = 30
num_coins = 5

for i in range(num_coins):
    coin_x = random.randint(0, SCREEN_WIDTH - coin_width)
    coin_y = random.randint(50, 150)
    coins.append([coin_x, coin_y])

# Define power-up properties
powerup_width = 30
powerup_height = 30
powerup_x = random.randint(0, SCREEN_WIDTH - powerup_width)
powerup_y = random.randint(50, 150)
powerup_speed = 2

# Define level and scoring properties
current_level = 1
max_levels = 12
lives = 3
coins_collected = 0

# Load sounds
coin_sound = pygame.mixer.Sound('coin.wav')
powerup_sound = pygame.mixer.Sound('powerup.wav')
jump_sound = pygame.mixer.Sound('jump.wav')
lose_life_sound = pygame.mixer.Sound('lose_life.wav')

# Load background music
pygame.mixer.music.load('star_wars_theme.mp3')
pygame.mixer.music.play(-1)

font = pygame.font.Font('freesansbold.ttf', 16)
score_font = pygame.font.Font('freesansbold.ttf', 24)

def show_level():
    level_text = font.render(f"Level: {current_level}/{max_levels}", True, WHITE)
    screen.blit(level_text, (10, 10))


def show_score():
    score_text = score_font.render(f"Coins: {coins_collected}", True, WHITE)
    screen.blit(score_text, (10, 40))


def show_lives():
    lives_text = score_font.render(f"Lives: {lives}", True, WHITE)
    screen.blit(lives_text, (SCREEN_WIDTH - 120, 10))


def render_powerup():
    screen.blit(powerup_image, (powerup_x, powerup_y))


# Function to reset game properties
def reset_game():
    global player_x, player_y, player_speed, enemies, coins, powerup_x, powerup_y, current_level, lives, coins_collected, enemy_speed, powerup_speed

    player_x = 400
    player_y = SCREEN_HEIGHT - player_height - 10
    player_speed = 5

    enemies = []
    for i in range(num_enemies):
        enemy_x = random.randint(0, SCREEN_WIDTH - enemy_width)
        enemy_y = random.randint(50, 150)
        enemies.append([enemy_x, enemy_y])

    coins = []
    for i in range(num_coins):
        coin_x = random.randint(0, SCREEN_WIDTH - coin_width)
        coin_y = random.randint(50, 150)
        coins.append([coin_x, coin_y])

    powerup_x = random.randint(0, SCREEN_WIDTH - powerup_width)
    powerup_y = random.randint(50, 150)
    current_level = 1
    coins_collected = 0
    lives = 3
    enemy_speed = 3
    powerup_speed = 2


# Set up game loop
running = True
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_x > 0:
        player_x -= player_speed
    if keys[pygame.K_RIGHT] and player_x < SCREEN_WIDTH - player_width:
        player_x += player_speed
    if keys[pygame.K_r]:
        reset_game()

    if keys[pygame.K_SPACE] and player_y == SCREEN_HEIGHT - player_height - 10:
        jump_sound.play()
        player_y -= 15

    # Apply gravity
    if player_y < SCREEN_HEIGHT - player_height - 10:
        player_y += 5

    # Move the enemies
    for enemy in enemies:
        enemy[1] += enemy_speed
        if enemy[1] > SCREEN_HEIGHT:
            enemy[0] = random.randint(0, SCREEN_WIDTH - enemy_width)
            enemy[1] = random.randint(50, 150)
            lose_life_sound.play()
            lives -= 1  # decrease lives if enemy reaches bottom

        if (player_x + player_width > enemy[0]) and (player_x < enemy[0] + enemy_width) and (
                player_y + player_height > enemy[1]) and (player_y < enemy[1] + enemy_height):
            enemy[0] = random.randint(0, SCREEN_WIDTH - enemy_width)
            enemy[1] = random.randint(50, 150)
            lose_life_sound.play()
            lives -= 1

        screen.blit(enemy_image, (enemy[0], enemy[1]))

    # Move the power-up
    powerup_y += powerup_speed
    if powerup_y > SCREEN_HEIGHT:
        powerup_x = random.randint(0, SCREEN_WIDTH - powerup_width)
        powerup_y = random.randint(50, 150)

    if (player_x + player_width > powerup_x) and (player_x < powerup_x + powerup_width) and (
            player_y + player_height > powerup_y) and (player_y < powerup_y + powerup_height):
        powerup_x = random.randint(0, SCREEN_WIDTH - powerup_width)
        powerup_y = random.randint(50, 150)
        player_speed += 1
        powerup_sound.play()

    # Move the coins
    for coin in coins:
        if (player_x + player_width > coin[0]) and (player_x < coin[0] + coin_width) and (
                player_y + player_height > coin[1]) and (player_y < coin[1] + coin_height):
            coin[0] = random.randint(0, SCREEN_WIDTH - coin_width)
            coin[1] = random.randint(50, 150)
            coins_collected += 1
            coin_sound.play()

        screen.blit(coin_image, (coin[0], coin[1]))

    # Draw the player
    screen.blit(player_image, (player_x, player_y))

    screen.blit(background_image, (0, 0))
    pygame.draw.rect(screen, BLACK, (0, 0, SCREEN_WIDTH, 50))

    show_level()
    show_score()
    show_lives()
    render_powerup()

    # Check if the player has completed the level
    if coins_collected >= num_coins:
        current_level += 1
        if current_level > max_levels:
            running = False
            print("Congratulations! You won the game!")
        else:
            coins_collected = 0
            lives += 1
            enemy_speed += 1
            powerup_speed += 1
            player_speed = 5

    # Check if the player has lost all lives
    if lives <= 0:
        running = False
        print("Game Over")

    pygame.display.update()
    clock.tick(60)

pygame.quit()
