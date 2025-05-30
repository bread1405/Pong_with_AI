# Python Pong Game !
import pygame
import sys
import os

# Initializing Pygame
pygame.init()

# Configurable parameters
frame_rate = 75

# Setting game window
width, height = 800, 600
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Pong Game")

# Upload saved sounds
base_path = os.path.dirname(__file__)
collision_sound = pygame.mixer.Sound(os.path.join(base_path, "event.mp3"))
collision_sound2 = pygame.mixer.Sound(os.path.join(base_path, "event2.mp3"))

# Colors
white = (255, 255, 255)
black = (0, 0, 0)

# Size and placement of players and ball
player_width, player_height = 15, 100
ball_size = 20

# X stands for left player (AI)
# Y stands for right player (human)
player1_x, player1_y = 50, height // 2 - player_height // 2 
player2_x, player2_y = width - 50 - player_width, height // 2 - player_height // 2

# Ball position
ball_x, ball_y = width // 2 - ball_size // 2, height // 2 - ball_size // 2
ball_speed_x, ball_speed_y = 7, 7

# Scores
player1_score, player2_score = 0, 0

# Font for displaying the score
font = pygame.font.Font(None, 74)

# Simple function for AI
def ai_move(ball_y, player1_y):
    if ball_y < player1_y + player_height // 2 and player1_y > 0:
        return -6
    elif ball_y > player1_y + player_height // 2 and player1_y < height - player_height:
        return 6
    return 0

# Game loop
clock = pygame.time.Clock()

# Event handling for closing the window
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()

    # Player keyboard control
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP] and player2_y > 0:
        player2_y -= 7
    if keys[pygame.K_DOWN] and player2_y < height - player_height:
        player2_y += 7

    # AI stands for first player (left player)
    ai_movement = ai_move(ball_y, player1_y)
    player1_y += ai_movement
    
    # Ball movement
    ball_x += ball_speed_x
    ball_y += ball_speed_y

    # Ball and paddle collision
    player1_rect = pygame.Rect(player1_x, player1_y, player_width, player_height)
    player2_rect = pygame.Rect(player2_x, player2_y, player_width, player_height)
    ball_rect = pygame.Rect(ball_x, ball_y, ball_size, ball_size)

    if player1_rect.colliderect(ball_rect):
        ball_speed_x = abs(ball_speed_x) * 1.05
        ball_speed_y *= 1.05
        collision_sound.play()
    
    if player2_rect.colliderect(ball_rect):
        ball_speed_x = -abs(ball_speed_x) * 1.05
        ball_speed_y *= 1.05
        collision_sound.play()

    max_speed = 20
    ball_speed_x = max(-max_speed, min(ball_speed_x, max_speed))
    ball_speed_y = max(-max_speed, min(ball_speed_y, max_speed))

    # Ball and wall collision
    if ball_y <= 0 or ball_y >= height - ball_size:
        ball_speed_y *= -1
        collision_sound2.play()

    # Scoring system: reset ball and update score
    if ball_x <= 0:
        player2_score += 1
        ball_x = width // 2 + 80
        ball_y = height // 2 - ball_size // 2
        ball_speed_x = -4
        ball_speed_y = 4

    if ball_x >= width:
        player1_score += 1
        ball_x = width // 2 - 80 - ball_size
        ball_y = height // 2 - ball_size // 2
        ball_speed_x = 4
        ball_speed_y = 4
    
    # Reset scores when either player reaches 10 points
    if player1_score >= 10 or player2_score >= 10:
        winner_text = "AI WINS!" if player1_score >= 10 else "PLAYER WINS!"
        winner_surface = font.render(winner_text, True, white)
        winner_rect = winner_surface.get_rect(center=(width//2, height//2))
        win.blit(winner_surface, winner_rect)
        pygame.display.flip()
        pygame.time.wait(3000)
        player1_score = 0
        player2_score = 0
        ball_x = width // 2 - ball_size // 2
        ball_y = height // 2 - ball_size // 2
        ball_speed_x = 4
        ball_speed_y = 4
        player1_y = height // 2 - player_height // 2
        player2_y = height // 2 - player_height // 2
    
    # Game zone rendering
    win.fill(black)
    pygame.draw.rect(win, white, player1_rect)
    pygame.draw.rect(win, white, player2_rect)
    pygame.draw.ellipse(win, white, ball_rect)

    # Render the scores
    player1_text = font.render(str(player1_score), True, white)
    win.blit(player1_text, (width // 4, 20))
    player2_text = font.render(str(player2_score), True, white)
    win.blit(player2_text, (width * 3 // 4, 20))

    pygame.display.flip()
    clock.tick(frame_rate)
