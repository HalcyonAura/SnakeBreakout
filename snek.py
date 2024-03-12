import pygame
import time
import random
from enum import Enum

#some taken from replit, some from geeksforgeeks, otherwise adapted such as multiple fruits

class Direction(Enum):
  UP = 0
  DOWN = 1
  LEFT = 2
  RIGHT = 3

class Food:
    block_size = None
    color = (0,255,0)
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

class Snake:
  length = None
  direction = None
  body = None
  block_size = None
  color = (0,0,255)
  bounds = None

  def __init__(self, block_size, bounds):
    self.block_size = block_size
    self.bounds = bounds
    self.respawn()

  def respawn(self):
    self.length = 3
    self.body = [(20,20),(20,40),(20,60)]
    self.direction = Direction.DOWN

  def draw(self, game, window):
    for segment in self.body:
      game.draw.rect(window, self.color, (segment[0],segment[1],self.block_size, self.block_size))

  def move(self):
    curr_head = self.body[-1]
    if self.direction == Direction.DOWN:
      next_head = (curr_head[0], curr_head[1] + self.block_size)
      self.body.append(next_head)
    elif self.direction == Direction.UP:
      next_head = (curr_head[0], curr_head[1] - self.block_size)
      self.body.append(next_head)
    elif self.direction == Direction.RIGHT:
      next_head = (curr_head[0] + self.block_size, curr_head[1])
      self.body.append(next_head)
    elif self.direction == Direction.LEFT:
      next_head = (curr_head[0] - self.block_size, curr_head[1])
      self.body.append(next_head)

    if self.length < len(self.body):
      self.body.pop(0)

  def steer(self, direction):
    if self.direction == Direction.DOWN and direction != Direction.UP:
      self.direction = direction
    elif self.direction == Direction.UP and direction != Direction.DOWN:
      self.direction = direction
    elif self.direction == Direction.LEFT and direction != Direction.RIGHT:
      self.direction = direction
    elif self.direction == Direction.RIGHT and direction != Direction.LEFT:
      self.direction = direction

  def eat(self):
    self.length += 1

  def check_for_food(self, food):
    head = self.body[-1]
    if head[0] == food.x and head[1] == food.y:
      self.eat()
      return True

  def check_tail_collision(self):
    head = self.body[-1]
    has_eaten_tail = False

    for i in range(len(self.body) - 1):
      segment = self.body[i]
      if head[0] == segment[0] and head[1] == segment[1]:
        has_eaten_tail = True

    return has_eaten_tail

  def check_bounds(self):
    head = self.body[-1]
    if head[0] >= self.bounds[0]:
      return True
    if head[1] >= self.bounds[1]:
      return True

    if head[0] < 0:
        return True
    if head[1] < 0:
        return True

    return False

pygame.init()
bounds = (720, 480)
window = pygame.display.set_mode(bounds)
pygame.display.set_caption("Snek")

block_size = 20
snake = Snake(block_size, bounds)
foods = [Food(block_size,bounds)]
fruit_spawn_time = time.time() # Time when the fruit was last spawned

run = True
while run:
  pygame.time.delay(100)
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      run = False

  keys = pygame.key.get_pressed()
  if keys[pygame.K_LEFT]:
    snake.steer(Direction.LEFT)
  elif keys[pygame.K_RIGHT]:
    snake.steer(Direction.RIGHT)
  elif keys[pygame.K_UP]:
    snake.steer(Direction.UP)
  elif keys[pygame.K_DOWN]:
    snake.steer(Direction.DOWN)
  # make eventual pause menu via ESCAPE
    
  # Fruit spawn logic
  if time.time() - fruit_spawn_time >= 5:  # Spawn a new fruit every 5 seconds
      food = Food(block_size,bounds)
      food.respawn()
      foods.append(food)
      fruit_spawn_time = time.time()
      
  snake.move()
  for f in foods:
    if(snake.check_for_food(f)):
      foods.pop(foods.index(f))

  if snake.check_bounds() == True or snake.check_tail_collision() == True:
    pygame.display.update()
    pygame.time.delay(1000)
    snake.respawn()
    #make a better way to clean up food regen
    foods.clear()
    food = Food(block_size, bounds)
    food.respawn()
    foods.append(food)
    fruit_spawn_time = time.time()

  window.fill((0,0,0))
  snake.draw(pygame, window)
  for f in foods:
    f.draw(pygame, window)
  pygame.display.update()