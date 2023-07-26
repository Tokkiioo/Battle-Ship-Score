import pygame
from screen_size import *

class Explosion(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.fall_speed = 3
        self.images = pygame.image.load("sprites/Tiles/tile_0005.png").convert(),
        self.current_frame = 0  # frame actual de la animación
        self.image = None  # Current image to display
        self.rect = None  # Explosion collision rectangle
        self.image = self.images[self.current_frame]  # Set first image
        self.rect = self.image.get_rect()  # Get collision rectangle
        self.rect.centerx = x  # Set x position
        self.rect.centery = y  # set y position

    def update(self):
        self.rect.centery += self.fall_speed  # Move down the explosion
        if self.rect.centery >= Screen_height:  # Check if the explosion reach lower limit 
            self.kill()  # Eliminate explosion