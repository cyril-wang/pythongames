import pygame
from pygame.sprite import Sprite

class Bullet(Sprite):
    # class to manage bullets fired from ship

    def __init__(self, ai_game):
        # create bullet object at ship's position
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.color = self.settings.bullet_color

        # create bullet rect at (0,0) and set correct postion
        self.rect = pygame.Rect(0,0, self.settings.bullet_width,
                                self.settings.bullet_height)
        self.rect.midtop = ai_game.ship.rect.midtop

        # store bullet's position as a decimal value
        self.y = float(self.rect.y)

    def update(self):
        # move bullet up screen
        # update decimal position of bullet
        self.y -= self.settings.bullet_speed
        self.rect.y = self.y

    def draw_bullet(self):
        # draw bullet to screen
        pygame.draw.rect(self.screen, self.color, self.rect)
