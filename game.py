import pygame
import sys
from player import Player
from enemy import Enemy
from bullet import Bullet
from explosion import Explosion
from screen_size import *

class Game:
    def __init__(self):
        pygame.init()
        self.score = 0
        self.screen = pygame.display.set_mode((Screen_width, Screen_height))
        self.clock = pygame.time.Clock()
        pygame.display.set_caption('Battle Ships Score')
        self.bullets = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.explosions = pygame.sprite.Group()
        self.player = Player(self, self.bullets)
        self.game_over = False
        self.background_image = pygame.image.load("sprites/star_bg/bg_03.png").convert()
        self.background_y = 0
    
    def run_game(self):
        self.start_screen()
        while not self.game_over:
            self.handle_events()
            self.update_screen()
            self.clock.tick(60)
        self.game_over_screen()
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self.handle_keydown_event(event)
            elif event.type == pygame.KEYUP:
                self.handle_keyup_event(event)
    
    def handle_keydown_event(self, event):
        if event.key == pygame.K_RIGHT:
            self.player.move_right = True
        elif event.key == pygame.K_LEFT:
            self.player.move_left = True
        elif event.key == pygame.K_UP:
            self.player.move_up = True
        elif event.key == pygame.K_DOWN:
            self.player.move_down = True
        elif event.key == pygame.K_SPACE:
            self.player.shoot()
    
    def handle_keyup_event(self, event):
        if event.key == pygame.K_RIGHT:
            self.player.move_right = False
        elif event.key == pygame.K_LEFT:
            self.player.move_left = False
        elif event.key == pygame.K_UP:
            self.player.move_up = False
        elif event.key == pygame.K_DOWN:
            self.player.move_down = False
    
    def update_screen(self):
        self.animate_background()
        self.draw_background()
        self.draw_score()
        self.player.move()
        self.player.run_Player()
        self.spawn_enemies()
        self.update_and_draw_bullets()
        self.update_and_draw_enemies()
        self.update_and_draw_explosions()
        self.detect_collisions()
        pygame.display.flip()
    
    def animate_background(self):
        self.background_y += 1
        if self.background_y >= self.background_image.get_height():
            self.background_y = 0

    def draw_background(self):
        self.screen.blit(self.background_image, (0, self.background_y))
        if self.background_y > 0:
            self.screen.blit(self.background_image, (0, self.background_y - self.background_image.get_height()))

    
    def draw_score(self):
        font = pygame.font.Font(None, 36)
        score_text = font.render("Score: " + str(self.score), True, (255, 255, 255))
        score_rect = score_text.get_rect()
        score_rect.topleft = (10, 10)
        self.screen.blit(score_text, score_rect)
    
    def spawn_enemies(self):
        if len(self.enemies) < 20:
            enemy = Enemy(Screen_width, Screen_height)
            self.enemies.add(enemy)
    
    def update_and_draw_bullets(self):
        self.bullets.update()
        for bullet in self.bullets.sprites():
            bullet.draw()
    
    def update_and_draw_enemies(self):
        self.enemies.update()
        self.enemies.draw(self.screen)
    
    def update_and_draw_explosions(self):
        self.explosions.update()
        self.explosions.draw(self.screen)
    
    def detect_collisions(self):
        collisions = pygame.sprite.groupcollide(self.bullets, self.enemies, True, True)
        for bullet, enemy_list in collisions.items():
            for enemy in enemy_list:
                explosion = Explosion(enemy.rect.centerx, enemy.rect.centery)
                self.explosions.add(explosion)
                bullet.kill()
                enemy.kill()
                self.score += 50
        
        if pygame.sprite.spritecollideany(self.player, self.enemies):
            self.game_over = True
        
        if pygame.sprite.spritecollideany(self.player, self.explosions):
            self.game_over = True
    
    def start_screen(self):
        start_image = pygame.image.load("sprites/star_bg/bg_03.png").convert()
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

            self.screen.blit(start_image, (0, 0))
            self.screen.blit(text1, text1_rect)
            self.screen.blit(text2, text2_rect)
            self.screen.blit(text3, text3_rect)

            pygame.display.flip()
            self.clock.tick(60)
    
    def game_over_screen(self):
        font = pygame.font.Font(None, 64)
        text1 = font.render("Game Over", True, (255, 255, 255))
        text_rect1 = text1.get_rect()
        text_rect1.center = (Screen_width // 2, Screen_height // 2)
        text2 = font.render("Press ENTER to play again", True, (255, 255, 255))
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
                    
            self.screen.blit(text1, text_rect1)
            self.screen.blit(text2, text_rect2)
    
            pygame.display.flip()
            self.clock.tick(60)

if __name__ == "__main__":
    game = Game()
    game.run_game()
