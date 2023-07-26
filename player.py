import pygame
from bullet import Bullet


# Creating the class containing the groups
class Player:
    def __init__(self, a_game, bullets):
        # Acces to the screen
        self.screen = a_game.screen
        # Put the player in any ubication and "get_rect" create a rectangle in all surface
        self.screen_rect = a_game.screen.get_rect()
        # Load the player image
        self.image = pygame.image.load("sprites/Ships/ship_0003.png").convert()
        # Put an rectangle in the player image
        self.rect = self.image.get_rect()
        # Put the player in the middle of the screen
        self.rect.midbottom = self.screen_rect.midbottom
        # Creating the condition to Move the player continually to he right
        self.move_right = False
        # Creating the condition to Move the player continually to he left
        self.move_left = False
        # Creating the condition to Move the player continually to he left
        self.move_up = False
        # Creating the condition to Move the player continually to he left
        self.move_down = False
        # Creating the variable bullets
        self.bullets = bullets

    def move(self):
        if self.move_right and self.rect.right < self.screen_rect.right: # The "and self.rect.right < self.screen_rect.right" that means the movement to the right is minor then right side of the edge screen. With is we put limits to we character
            self.rect.x += 5
        if self.move_left and self.rect.left > 0:
            self.rect.x -= 5
        if self.move_up and self.rect.top > 0:
            self.rect.y -= 5
        if self.move_down and self.rect.bottom < self.screen_rect.bottom:
            self.rect.y += 5

    def run_Player(self):
        # Draw the image player in the screen
        self.screen.blit(self.image, self.rect)

    def shoot(self):
        bullet = Bullet(self.screen, self.rect.midtop)  # Create an instance of the Bullet class
        self.bullets.add(bullet)  # Add the bullet to a bullet group
        

