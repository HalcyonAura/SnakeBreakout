import pygame
import time
import random
import sys

# Game setup
# window
size_x = 720
size_y = 480
pygame.init()

# FPS (frames per second) controller
fps = pygame.time.Clock()
 
pygame.display.set_caption('Snek')
game_window = pygame.display.set_mode((size_x, size_y))

# Snake and fruit setup
# snake
snake_pos = [(size_x // 2, size_y // 2)]
snake_size = 1
snake_speed = 10

class Snake:
    def __init__(self, pos, size):
        self.pos = pos
        self.size = size
    def update(self):
        pass
    def draw(self):
        pass
    def grow(self):
        pass
    def check_collision(self):
        pass
    def check_wall_collision(self):
        pass

# fruit
def gen_fruit():
    return (random.randint(0, size_x // 20) * 20, random.randint(0, size_y // 20) * 20)

fruit_pos = gen_fruit()
fruit_spawn_time = time.time() # Time when the fruit was last spawned

# Snake movement and frame updates
direction = "RIGHT"
change_to = direction

def update_snake():
    global direction, snake_pos, snake_size

    if direction == "UP":
        snake_pos[0] = (snake_pos[0][0], snake_pos[0][1] - 20)
    elif direction == "DOWN":
        snake_pos[0] = (snake_pos[0][0], snake_pos[0][1] + 20)
    elif direction == "LEFT":
        snake_pos[0] = (snake_pos[0][0] - 20, snake_pos[0][1])
    elif direction == "RIGHT":
        snake_pos[0] = (snake_pos[0][0] + 20, snake_pos[0][1])

    # Check if snake collides with itself
    for block in snake_pos[1:]:
        if snake_pos[0] == block:
            pygame.quit()
            sys.exit()

    # Check if snake collides with the wall
    if snake_pos[0][0] < 0 or snake_pos[0][0] >= size_x or snake_pos[0][1] < 0 or snake_pos[0][1] >= size_y:
        pygame.quit()
        sys.exit()

    # Draw the snake
    for pos in snake_pos:
        pygame.draw.rect(game_window, (0, 255, 0), (pos[0], pos[1], 20, 20))

# Game loop
while True:
    game_window.fill((0, 0, 0))
    # Fruit spawn logic
    if time.time() - fruit_spawn_time >= 1:  # Spawn a new fruit every 5 seconds
        fruit_pos = gen_fruit()
        fruit_spawn_time = time.time()

    # Draw the fruit
    pygame.draw.rect(game_window, (255, 0, 0), (fruit_pos[0], fruit_pos[1], 20, 20))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and direction != "DOWN":
                change_to = "UP"
            elif event.key == pygame.K_DOWN and direction != "UP":
                change_to = "DOWN"
            elif event.key == pygame.K_LEFT and direction != "RIGHT":
                change_to = "LEFT"
            elif event.key == pygame.K_RIGHT and direction != "LEFT":
                change_to = "RIGHT"

    # Update snake direction
    direction = change_to

    # Update snake position and check for collisions
    update_snake()

    pygame.display.update()

    fps.tick(snake_speed)