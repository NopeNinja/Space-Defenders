import pygame
import random
import sys
import time
from pygame import QUIT
from pygame import image

DODGETIME = 1
running = True
pygame.init()
screen = pygame.display.set_mode((600, 600))
background = pygame.Surface((600, 600))
clock = pygame.time.Clock()
engine = pygame.image.load('engine.png')
engine = pygame.transform.scale(engine, (25, 38))
engineRect = engine.get_rect()


class Player:

  def __init__(self, x, y):
    self.image = pygame.Surface((100, 100))
    self.image = pygame.image.load("jet picture.png").convert_alpha()
    self.image.set_alpha(100)
    self.image = pygame.transform.scale(self.image, (100, 100))
    self.rect = self.image.get_rect()
    self.rect.x = x
    self.rect.y = y
    self.health = 3
    self.dodge = 0
    self.hitbox = pygame.Rect(0, 0, 40, 80)

  def update(self):
    self.hitbox.x = self.rect.x + 30
    self.hitbox.y = self.rect.y + 10


class Engine:

  def __init__(self, x, y, image):
    self.image = image
    self.rect = self.image.get_rect()
    self.rect.x = x
    self.rect.y = y


# Enemy Laser
class Lazar:

  def __init__(self, x, y):
    self.image = pygame.Surface((10, 20))
    self.image.fill("pink")
    self.rect = self.image.get_rect()
    self.rect.x = x + 45
    self.rect.y = y
    self.speed = random.randint(3, 5)

  def collision(self, player):
    if self.rect.colliderect(player.hitbox):
      current = time.time()
      if not (current - player.dodge <= DODGETIME):
        print(player)
        player.health -= 1
        list.remove(self)
        print(player.health)
        if player.health == 0:
          pygame.quit()

  def update(self):
    screen.blit(self.image, self.rect)
    self.rect.y += 4
    self.collision(player)


list = []


class Enemy:

  def __init__(self, x, y, health, size):
    self.image = pygame.Surface((50, 50))
    self.image = pygame.image.load("enemy ship.png.png")
    self.image = pygame.transform.scale(self.image, size)
    self.rect = self.image.get_rect()
    self.rect.x = x
    self.rect.y = y
    self.start = time.time()
    self.health = health
    self.direction = True
    self.speed = (random.randint(2, 10))
    self.lazar_cooldown = 0
    self.isboss = False

  def attack(self):
    if self.current - self.lazar_cooldown > 0.5:
      if player.rect.x - 5 <= self.rect.x <= player.rect.x + 5:
        if self.isboss == True:
          list.append(Lazar(self.rect.x, self.rect.y + self.rect.height))
          list.append(Lazar(self.rect.x + 50, self.rect.y + self.rect.height))
        else:
          list.append(Lazar(self.rect.x, self.rect.y + self.rect.height))
        self.lazar_cooldown = self.current

  def update(self):
    self.current = time.time()
    for laser in list:
      laser.update()
    self.attack()
    if self.isboss == True:
      pygame.draw.rect(screen, "red",
                       pygame.Rect(25, 25, 550 * self.health / 5, 25))
    screen.blit(self.image, self.rect)
    if self.direction:

      self.rect.x += self.speed
    else:
      self.rect.x -= self.speed

    if self.rect.x >= 600:
      self.direction = False
    if self.rect.x <= 0:
      self.direction = True


# Player Laser
class laser:

  def __init__(self):
    self.image = pygame.Surface((10, 20))
    self.image.fill("red")
    self.rect = self.image.get_rect()
    self.rect.x = player.rect.x + 45
    self.rect.y = player.rect.y

  def collision(self, enemy):
    if self.rect.colliderect(enemy):
      enemy.health -= 1
      if enemy.health <= 0:
        enemies.remove(enemy)
      laser3.remove(self)

  def update(self):
    screen.blit(self.image, self.rect)
    self.rect.y -= 5
    for enemy in enemies:
      self.collision(enemy)


laser3 = []
start = time.time()
start2 = time.time()

player = Player(300, 500)
e = Engine(0, 600 - 38, engine)
wave_counter = 1
enemies = []
win = False
font = pygame.font.SysFont('Comic Sans MS', 30)
text = font.render("VICTORY", True, (255, 0, 0))


def wave():

  global wave_counter, win

  current = time.time()
  if win == False and len(enemies) == 0:
    wave_counter += 1
    print(wave_counter)
    if wave_counter == 5:
      boss = Enemy(random.randint(0, 600), -10, 5, (200, 200))
      boss.isboss = True
      enemies.append(boss)
    elif wave_counter == 6:
      win = True

    else:
      for _ in range(wave_counter):
        fighter = Enemy(random.randint(0, 600), -10, 1, (100, 100))
        enemies.append(fighter)


while running == True:
  wave()
  screen.fill((13, 13, 13))
  current = time.time()

  e = Engine(0, 600 - 38, engine)
  for event in pygame.event.get():

    if event.type == QUIT:
      pygame.quit()
      sys.exit()
  key = pygame.key.get_pressed()

  if key[pygame.K_w]:
    player.rect.y -= 5
  if key[pygame.K_s]:
    player.rect.y += 5
  if key[pygame.K_a]:
    player.rect.x -= 5
  if key[pygame.K_d]:
    player.rect.x += 5
  if key[pygame.K_e]:
    player.dodge = current
  if current - start >= 0.5:
    if key[pygame.K_SPACE]:
      laser3.append(laser())
      start = current
  player.update()
  for enemy in range(len(enemies)):
    enemies[enemy].update()

  for lazer in laser3:
    lazer.update()

  #delete lasers that are out of range
  for lazer in laser3:
    if lazer.rect.y < 0:
      laser3.remove(lazer)

  if current - player.dodge <= DODGETIME:
    player.image.set_alpha(75)
  else:
    player.image.set_alpha(255)
  screen.blit(player.image, player.rect)

  for i in range(player.health):
    e = Engine(i * 30, 600 - 38, engine)
    screen.blit(e.image, e.rect)
  if win == True:
    screen.blit(text, (300, 300))
  pygame.display.update()

  clock.tick(45)
