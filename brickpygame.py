#!/usr/bin/env python3
# BreakPygame

# Import modules
import pygame  # For pygame
import sys  # For handle system events such as close the game window
import time  # For pause some actions

# Define display width and height
width = 640
height = 480
background_color = (155, 188, 15)  # Gameboy display color
game = True


# Neccesary to use fonts in game
pygame.init()


# Ball
class Ball(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        # Load sprite
        self.image = pygame.image.load("assets/ball.png")
        # Obtain ball form for python
        self.rect = self.image.get_rect()
        # Init position for the ball
        self.rect.centerx = width / 2
        self.rect.centery = height / 2
        # Initial Speed in pixels (X, Y coords)
        self.speed = [5, 5]

    def update(self):
        # Avoid the ball runaway
        if self.rect.top <= 0:
            self.speed[1] = -self.speed[1]
        elif self.rect.right >= width or self.rect.left <= 0:
            self.speed[0] = -self.speed[0]
        # Move according to actual speed and position
        self.rect.move_ip(self.speed)


class Paddle(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        # Load sprite
        self.image = pygame.image.load("assets/paddle.png")
        # Obtain ball form for python
        self.rect = self.image.get_rect()
        # Init position for the paddle
        self.rect.midbottom = (width / 2, height - 20)
        # Initial Speed in pixels (X, Y coords)
        self.speed = [0, 0]

    def update(self, event):
        # Key Stroke left
        if event.key == pygame.K_LEFT and self.rect.left > 0:
            self.speed = [-10, 0]
        # Key stroke Right
        elif event.key == pygame.K_RIGHT and self.rect.right < width:
            self.speed = [10, 0]
        else:
            self.speed = [0, 0]
        # Move according to actual speed and position
        self.rect.move_ip(self.speed)


class Brick(pygame.sprite.Sprite):
    def __init__(self, position):
        pygame.sprite.Sprite.__init__(self)
        # Load sprite
        self.image = pygame.image.load("assets/brick.png")
        # Obtain ball form for python
        self.rect = self.image.get_rect()
        # Init position
        self.rect.topleft = position


class Wall(pygame.sprite.Group):
    def __init__(self, brickQuantity):
        pygame.sprite.Group.__init__(self)

        x_position = 20
        y_position = 50

        for i in range(brickQuantity):
            brick = Brick((x_position, y_position))
            self.add(brick)

            x_position += brick.rect.width
            if x_position >= width - 20:
                x_position = 20
                y_position += brick.rect.height


def game_over():
    while True:
        font = pygame.font.SysFont("Cave-Story", 72)
        text = font.render("Game Over ", True, (15, 56, 15))
        text_rect = text.get_rect()
        text_rect.center = [width / 2, height / 2]
        display.blit(text, text_rect)
        pygame.display.flip()

        # check if you press the quit icon
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # Close Game
                sys.exit()
                # Restart game


# Show Score
def show_score():
    font = pygame.font.SysFont("Cave-Story", 30)
    text = font.render(str(score).zfill(5), True, (15, 56, 15))
    text_rect = text.get_rect()
    text_rect.topleft = [20, 20]
    display.blit(text, text_rect)


# Show Lives
def show_lives():
    global lives
    font = pygame.font.SysFont("Cave-Story", 30)
    s_lives = "Lives: " + str(lives).zfill(2)
    text = font.render(s_lives, True, (15, 56, 15))
    text_rect = text.get_rect()
    text_rect.topright = [width - 20, 20]
    display.blit(text, text_rect)


# Start Display
display = pygame.display.set_mode((width, height))

# Title Game
pygame.display.set_caption("BrickPygame")

# Limit frames with clock
clock = pygame.time.Clock()

# Event keystroke repeat
pygame.key.set_repeat(30)

ball = Ball()
player = Paddle()
wall = Wall(30)
# Define Variables
score = 0
lives = 3
restart_ball = True

# Allow time to the player to get ready
def get_ready():

    # Fill Display
    display.fill(background_color)

    # Draw Score
    show_score()

    # Draw lives
    show_lives()

    # Draw Paddle
    display.blit(player.image, player.rect)

    # Draw wall
    wall.draw(display)

    font = pygame.font.SysFont("Cave-Story", 72)
    text = font.render("Get Ready", True, (15, 56, 15))
    text_rect = text.get_rect()
    text_rect.center = [width / 2, height / 2 - 40]
    display.blit(text, text_rect)

    font = pygame.font.SysFont("Cave-Story", 30)
    text = font.render("press spacebar to start ", True, (15, 56, 15))
    text_rect = text.get_rect()
    text_rect.center = [width / 2, height / 2 - (-70)]
    display.blit(text, text_rect)

    # Update elements in the display
    pygame.display.flip()

    # Get ready
    time.sleep(2)


get_ready()


# Infinte cicle to prevent the display to close when program execution
while game:
    # Check Events
    # Max FPS
    clock.tick(60)
    # check if you press te quit icon
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            # Close Game
            sys.exit()
        # Check the key downstrokes
        elif event.type == pygame.KEYDOWN:
            player.update(event)
            if restart_ball == True and event.key == pygame.K_SPACE:
                restart_ball = False
                if ball.rect.centerx < width / 2:
                    ball.speed = [5, -5]
                else:
                    ball.speed = [-5, -5]

    # Update ball position
    if restart_ball == False:
        ball.update()
    else:
        ball.rect.midbottom = player.rect.midtop

    # Fill Display
    display.fill(background_color)

    # Draw Score
    show_score()

    # Show Lives
    show_lives()

    # Ball and paddle collision
    if pygame.sprite.collide_rect(ball, player):
        ball.speed[1] = -ball.speed[1]

    # Ball and wall collision
    list = pygame.sprite.spritecollide(ball, wall, False)
    if list:
        brick = list[0]
        if ball.rect.centerx < brick.rect.left or ball.rect.centerx > brick.rect.right:
            ball.speed[0] = -ball.speed[0]
        else:
            ball.speed[1] = -ball.speed[1]
        wall.remove(brick)
        score += 10

    # Draw ball
    display.blit(ball.image, ball.rect)

    # Draw Paddle
    display.blit(player.image, player.rect)

    # Draw wall
    wall.draw(display)

    # Update elements in the display
    pygame.display.flip()

    # Check if the ball is below the paddle
    # Decrement life in one
    if ball.rect.top > height:
        lives -= 1
        restart_ball = True

    # No more lives
    if lives == 0:
        display.fill(background_color)
        game_over()
