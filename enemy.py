import pygame
import random
from screen_size import *

class Enemy(pygame.sprite.Sprite):
    def __init__(self, screen_width, screen_height):
        super().__init__()
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.image = pygame.image.load("sprites/Ships/ship_0014.png").convert()
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(1, self.screen_width - self.rect.width) # The position of enemies in X axis
        self.rect.y = random.randint(-2 * self.screen_height, -self.rect.height) # Move the enemies down
        self.speed = random.randint(3, 10) # Speed of enemies between 3 to 10

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > self.screen_height:
            self.rect.x = random.randint(1, self.screen_width - self.rect.width)
            self.rect.y = random.randint(-1 * self.screen_height, -self.rect.height)
            self.speed = random.randint(3, 10)
