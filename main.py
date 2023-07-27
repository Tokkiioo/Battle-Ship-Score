# delete import asyncio
import pygame
import sys
from player import Player
from enemy import Enemy
from bullet import Bullet
from explosion import Explosion
from screen_size import *

class Game():
    def __init__(self):
        # pygame start setup
        pygame.init()
        
        # Game score
        self.score = 0
        
        # window setup 
        self.screen = pygame.display.set_mode((Screen_width, Screen_height)) # Width, Hight

        # Load Background
        self.image = pygame.image.load("sprites/star_bg/bg_03.png").convert()
        
        # Timer
        self.clock = pygame.time.Clock()

        # Game title
        pygame.display.set_caption('Battle Ships Score')

        # Group for bullets
        self.bullets = pygame.sprite.Group()
        
        # Group for enemies
        self.enemies = pygame.sprite.Group()
        
        # Group for explosions
        self.explosions = pygame.sprite.Group()

        # Call to class Player from player.py
        self.player = Player(self, self.bullets)
        
        # Variable de estado para controlar si el juego ha terminado
        self.game_over = False  

    def run_game(self):
        self.start_screen()  # Llamada al método start_screen() para mostrar la pantalla de inicio
        # Loop game
        y = 0
        running = True
        while running:
            # poll for events
            # pygame.QUIT event means the user clicked X to close your window
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

                # Conditions to run the movement player continually to right, left, up or donw
                elif event.type == pygame.KEYDOWN: # If you press the button...
                    if event.key == pygame.K_RIGHT: # What button? The key button right
                        self.player.move_right = True # Then do the movement to the right... And so on, so on
                    if event.key == pygame.K_LEFT:
                        self.player.move_left = True
                    if event.key == pygame.K_UP:
                        self.player.move_up = True
                    if event.key == pygame.K_DOWN:
                        self.player.move_down = True
                    if event.key == pygame.K_SPACE: # Check for bullet firing
                        self.player.shoot()
                elif event.type == pygame.KEYUP: # But when leave to press buton...
                    if event.key == pygame.K_RIGHT: # What button? The key button right
                        self.player.move_right = False # Then stop the movement to the right... And so on, so on
                    if event.key == pygame.K_LEFT:
                        self.player.move_left = False
                    if event.key == pygame.K_UP:
                        self.player.move_up = False
                    if event.key == pygame.K_DOWN:
                        self.player.move_down = False
            
            # This animate background downwards
            y_relative = y % self.image.get_rect().height
            self.screen.blit(self.image, (0,y_relative - self.image.get_rect().height))
            if y_relative < Screen_height:
                self.screen.blit(self.image, (0,y_relative))
            y += 1
            
            # Show score on screen
            def showScore (screen, font, text, color, size, x, y):
                word_type = pygame.font.Font(font, size)
                surface = word_type.render(text, True, color)
                score_rect = surface.get_rect()
                score_rect.center = (x, y)
                screen.blit(surface, score_rect)
            
            # Draw score on screen
            showScore(self.screen, None, str(self.score), (255, 255, 255), 40, 50, 50)             

            # Call the function "move" in player.py to execute the movements
            self.player.move() 

            # Call the function run_Player from player.py to run the image player
            self.player.run_Player()
            
            if len(self.enemies) < 20:  # Control number of enemies in the screen
                enemy = Enemy(Screen_width, Screen_height)
                self.enemies.add(enemy)

            # Update and draw bullets
            self.bullets.update()
            for bullet in self.bullets.sprites():
                bullet.draw()
            
            # Update and draw enemies    
            self.enemies.update()
            self.enemies.draw(self.screen)
            
            # Update and draw explosions  
            self.explosions.update()
            self.explosions.draw(self.screen)
            
            # Detect colide between bullets and enemies
            collisions = pygame.sprite.groupcollide(self.bullets, self.enemies, True, True)
            
            # Create explosion in the position of collision 
            for bullet, enemy_list in collisions.items():
                for enemy in enemy_list:
                    explosion = Explosion(enemy.rect.centerx, enemy.rect.centery)
                    self.explosions.add(explosion)
                    bullet.kill() # Eliminate the bullet after collision
                    enemy.kill() # Eliminate the enemy after collision
            
            # Condition to sum score        
            if collisions:
                self.score += 50
            
            # Condition to check if the enemy colide with the player. If is true, game over
            if pygame.sprite.spritecollideany(self.player, self.enemies):
                running = False
                
            # Condition to check if the explosion colide with the player. If is true, game over
            if pygame.sprite.spritecollideany(self.player, self.explosions):
                running = False
            
            pygame.display.flip()  # Update the screen
            self.clock.tick(60)  # Limit FPS to 60
                    
        self.game_over_screen()
    
    # Creating the start menu
    def start_screen(self):
        start_image = pygame.image.load("sprites/star_bg/bg_03.png").convert()  # Carga la imagen de la pantalla de inicio
        font = pygame.font.Font(None, 64)
        text1 = font.render("Press ENTER to play!", True, (255, 255, 255))
        text1_rect = text1.get_rect(center=(Screen_width // 2, Screen_height // 2))
        text2 = font.render("Controls: Arrows to move", True, (255, 255, 255))
        text2_rect = text2.get_rect(center=(Screen_width // 2, Screen_height // 2 + 50))
        text3 = font.render("SPACE: Shoot", True, (255, 255, 255))
        text3_rect = text3.get_rect(center=(Screen_width // 2, Screen_height // 2 + 100))

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        return

            self.screen.blit(start_image, (0, 0))  # Mostrar la imagen de fondo
            self.screen.blit(text1, text1_rect)  # Mostrar el primer texto
            self.screen.blit(text2, text2_rect)  # Mostrar el segundo texto
            self.screen.blit(text3, text3_rect)  # Mostrar el tercer texto

            pygame.display.flip()
            self.clock.tick(60)
    
    def game_over_screen(self):
        font = pygame.font.Font(None, 64)  # Crea una fuente con tamaño 64
        text1 = font.render("Game Over", True, (255, 255, 255))  # Renderiza el texto "Game Over" con color blanco
        text_rect1 = text1.get_rect()
        text_rect1.center = (Screen_width // 2, Screen_height // 2)  # Centra el texto en la pantalla
        text2 = font.render("Press ENTER to play again", True, (255, 255, 255))  # Renderiza el texto "Game Over" con color blanco
        text_rect2 = text2.get_rect()
        text_rect2.center = (Screen_width // 2, Screen_height // 2 + 50)
        
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        self.game_over = False
                        self.score = 0
                        self.player = Player(self, self.bullets)
                        self.bullets.empty()
                        self.enemies.empty()
                        self.explosions.empty()
                        self.run_game()
                        
                    
            self.screen.blit(text1, text_rect1)  # Show game over on screen
            self.screen.blit(text2, text_rect2)  # Show ENTER to play again
    
            # flip() the display to put your work on screen
            pygame.display.flip()
            self.clock.tick(60)  # limits FPS to 60
            
if __name__  == "__main__":
    game = Game()
    game.run_game()