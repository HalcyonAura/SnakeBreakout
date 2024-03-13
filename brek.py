import pygame
from enum import Enum

class Direction(Enum):
  LEFT = -1
  RIGHT = 1

pygame.init()

screen_width = 600
screen_height = 600

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Brekout')

class Paddle:
    def __init__(self):
        self.respawn()
    def move(self):
        # reset movement direction
        self.direction = 0
        key = pygame.key.get_pressed()
        if key[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
            self.direction = -1
        if key[pygame.K_RIGHT] and self.rect.right < screen_width:
            self.rect.x += self.speed
            self.direction = 1
    def draw(self):
        pygame.draw.rect(screen, (0,255,0), self.rect)
    def respawn(self):
        self.rect = pygame.Rect(100, 400, 100, 10)
        self.direction = 0
        self.speed = 2
        
    
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


paddle = Paddle()
ball = Ball()
bricks = Brick()

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

        screen.fill((0,0,0))
        paddle.draw()
        paddle.move()
        ball.draw()
        ball.move()
        bricks.draw()
        pygame.time.delay(5)
        pygame.display.update()

pygame.quit()