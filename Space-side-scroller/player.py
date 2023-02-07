import pygame
from global_var import *

class Player(pygame.sprite.Sprite):
    def __init__(self, game):
        pygame.sprite.Sprite.__init__(self)
        self.game = game
        if rpi:
            self.image = "Images/player.png"
        else:
            self.image = "Space-side-scroller/Images/player.png"
        self.ship_x, self.ship_y = 0, self.game.DISPLAY_H / 2 - 40
        self.ship = pygame.image.load(self.image)
        self.ship = pygame.transform.scale(self.ship, (64, 81))
        self.max_left, self.max_right = 3, (self.game.DISPLAY_W - 65)
        self.max_up, self.max_down = 9, 390
        self.ship_speed = 10
        self.rect = self.ship.get_rect()

    def get_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_DOWN]:
                if self.ship_y <= self.max_down:
                    self.ship_y += self.ship_speed
        if keys[pygame.K_UP]:
            if self.ship_y >= self.max_up:
                self.ship_y -= self.ship_speed
        if keys[pygame.K_LEFT]:
            if self.ship_x >= self.max_left:
                self.ship_x -= self.ship_speed
        if keys[pygame.K_RIGHT]:
            if self.ship_x <= self.max_right:
                self.ship_x += self.ship_speed
        if rpi:
            if ((self.chanY.value * 480) < 220):
                if self.ship_y <= self.max_down:
                    self.ship_y += self.ship_speed
            if ((self.chanY.value * 480) > 260):
                if self.ship_y >= self.max_up:
                    self.ship_y -= self.ship_speed
            if ((self.chanX.value * 800) < 380):
                if self.ship_x >= self.max_left:
                    self.ship_x -= self.ship_speed
            if ((self.chanX.value * 800) > 420):
                if self.ship_x <= self.max_right:
                    self.ship_x += self.ship_speed
    def update(self):
        self.game.display.blit(self.ship, (self.ship_x, self.ship_y))