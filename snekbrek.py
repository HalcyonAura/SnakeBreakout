import pygame
import time
import random
from enum import Enum
# Constants
screen_width = 600
screen_height = 600

pygame.init()
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("The Epic Adventures of Sir Slithersworth the Snake-Smashing, Block-Breaking, Pythonic Pursuer of Pixelated Peril: A Tale of Code, Chaos, and Comedic Catastrophe in the Virtual Realm of VsCode!?")

# but has snake functionality

class Paddle:
    length = 1
    body = None
    block_size = 10
    def __init__(self):
        self.respawn()
    def move(self):
        # reset movement direction
        self.direction_x = 0
        self.direction_y = 0
        curr_head = self.body[-1]
        key = pygame.key.get_pressed()
        if key[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
            self.direction_x = -1
            next_head = (curr_head[0] - self.block_size, curr_head[1])
            rect = pygame.Rect(next_head[0], next_head[1], self.block_size, self.block_size)
            self.body.append(rect)
        elif key[pygame.K_RIGHT] and self.rect.right < screen_width:
            self.rect.x += self.speed
            self.direction_x = 1
            next_head = (curr_head[0] + self.block_size, curr_head[1])
            rect = pygame.Rect(next_head[0], next_head[1], self.block_size, self.block_size)
            self.body.append(rect)
        elif key[pygame.K_UP] and self.rect.top > 0:
            self.rect.y -= self.speed
            self.direction_y = -1
            next_head = (curr_head[0], curr_head[1] - self.block_size)
            rect = pygame.Rect(next_head[0], next_head[1], self.block_size, self.block_size)
            self.body.append(rect)
        elif key[pygame.K_DOWN] and self.rect.bottom < screen_height:
            self.rect.y += self.speed
            self.direction_y = 1
            next_head = (curr_head[0], curr_head[1] + self.block_size)
            rect = pygame.Rect(next_head[0], next_head[1], self.block_size, self.block_size)
            self.body.append(rect)
        
        if self.length < len(self.body):
          self.body.pop(0)
    
    def draw(self):
        pygame.draw.rect(screen, (0,255,0), self.rect)
        # how draw rest of body?
        for segment in self.body[:-1]:
            pygame.draw.rect(screen, (0,255,0), segment)
    def respawn(self):
        self.rect = pygame.Rect(100, 400, self.block_size, self.block_size)
        self.body = [self.rect]
        self.direction_x = 0
        self.direction_y = 0
        self.speed = 2
    def check_for_food(self, food):
        if self.rect.x >= food.x - self.block_size and self.rect.x <= food.x + self.block_size and self.rect.y >= food.y - self.block_size and self.rect.y <= food.y + self.block_size:
            self.eat()
            return True
    def eat(self):
        self.length += 1
        
class Ball:
    def __init__(self):
        self.respawn()
    def move(self):
        self.pos = (self.pos[0] + self.vel[0], self.pos[1] + self.vel[1])
        if self.pos[0] <= 0 or self.pos[0] >= screen_width:
            self.vel = (-self.vel[0], self.vel[1])
        if self.pos[1] <= 0 or self.pos[1] >= screen_height:
            self.vel = (self.vel[0], -self.vel[1])
        self.check_collision()
    def draw(self):
         pygame.draw.circle(screen, (255,)*3, self.pos, self.rad, 0)
    def check_collision(self):
        # check for collision with paddle
        if self.pos[1] + self.rad >= paddle.rect.top and self.pos[1] - self.rad <= paddle.rect.bottom and self.pos[0] >= paddle.rect.left and self.pos[0] <= paddle.rect.right:
            self.vel = (self.vel[0], -self.vel[1])
        # fix corner collisions
        # check for collision with bricks
        for b in bricks.bricks:
            if self.pos[1] + self.rad >= b.top and self.pos[1] - self.rad <= b.bottom and self.pos[0] >= b.left and self.pos[0] <= b.right:
                self.vel = (self.vel[0], -self.vel[1])
                bricks.bricks.remove(b)
    def respawn(self):
        self.pos = (300, 300)
        self.rad = 5
        self.vel = (1, 1)

class Brick:    
    def __init__(self):
        self.respawn()
    def draw(self):
        for b in self.bricks:
            pygame.draw.rect(screen, (0,0,255), b)
    def check_collision(self):
        pass
    def respawn(self):
        self.cols = 5
        self.rows = 3
        self.width = (screen_width-100) // self.cols
        self.height = (screen_height/4) // self.rows
        self.padding = 10
        self.offset = 30
        self.bricks = []
        for i in range(self.cols):
            for j in range(self.rows):
                self.bricks.append(pygame.Rect(i*(self.width+self.padding)+self.offset, j*(self.height+self.padding)+self.offset, self.width, self.height))

class Direction(Enum):
  DOWN = 0
  LEFT = 1
  RIGHT = 2
  UP = 3

class Food:
    block_size = None
    color = (255,0,0)
    x = 0;
    y = 0;
    bounds = None

    def __init__(self, block_size, bounds):
        self.block_size = block_size
        self.bounds = bounds

    def draw(self, game, window):
        game.draw.rect(window, self.color, (self.x, self.y, self.block_size, self.block_size))

    def respawn(self):
        blocks_in_x = (self.bounds[0])//self.block_size
        blocks_in_y = (self.bounds[1])//self.block_size
        self.x = random.randint(0, blocks_in_x - 1) * self.block_size
        self.y = random.randint(0, blocks_in_y - 1) * self.block_size


if __name__ == "__main__":  
    paddle = Paddle()
    ball = Ball()
    bricks = Brick()

    foods = [Food(10,(screen_width, screen_height))]
    fruit_spawn_time = time.time() # Time when the fruit was last spawned

    run = True
    pause = False
    while run or pause:
        while pause:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pause = False
                    run = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pause = False
                        run = True
        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pause = True
                        run = False
            # keys = pygame.key.get_pressed()
            # if keys[pygame.K_LEFT]:
            #     snake.steer(Direction.LEFT)
            # elif keys[pygame.K_RIGHT]:
            #     snake.steer(Direction.RIGHT)
            # elif keys[pygame.K_UP]:
            #     snake.steer(Direction.UP)
            # elif keys[pygame.K_DOWN]:
            #     snake.steer(Direction.DOWN)
            # # make eventual pause menu via ESCAPE
                
            # Fruit spawn logic
            if time.time() - fruit_spawn_time >= 5:  # Spawn a new fruit every 5 seconds
                food = Food(10,(screen_width, screen_height))
                food.respawn()
                foods.append(food)
                fruit_spawn_time = time.time()
                
            # snake.move()
            for f in foods:
                if(paddle.check_for_food(f)):
                    foods.pop(foods.index(f))

            # if snake.check_bounds() == True or snake.check_tail_collision() == True:
            #     pygame.display.update()
            #     pygame.time.delay(1000)
            #     snake.respawn()
            #     #make a better way to clean up food regen
            #     foods.clear()
            #     food = Food(block_size, bounds)
            #     food.respawn()
            #     foods.append(food)
            #     fruit_spawn_time = time.time()
            screen.fill((0,0,0))
            paddle.draw()
            paddle.move()
            for f in foods:
                f.draw(pygame, screen)
            ball.draw()
            ball.move()
            bricks.draw()
            pygame.time.delay(5)
            pygame.display.update()

    pygame.quit()