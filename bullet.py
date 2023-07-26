import pygame

class Bullet(pygame.sprite.Sprite):
    def __init__(self, screen, pos):
        super().__init__()
        self.screen = screen
        self.image = pygame.image.load("sprites/Tiles/tile_0000.png")
        self.rect = self.image.get_rect()
        self.rect.midbottom = pos
        self.speed = 5

    def update(self):
        self.rect.y -= self.speed
        if self.rect.bottom < 0:
            self.kill()

    def draw(self):
        self.screen.blit(self.image, self.rect)

