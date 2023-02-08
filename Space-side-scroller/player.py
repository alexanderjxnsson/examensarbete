import pygame
from global_var import *

class Player(pygame.sprite.Sprite):
    def __init__(self, game, pos):
        pygame.sprite.Sprite.__init__(self)
        self.game = game
        if rpi:
            self.image = "Images/player.png"
        else:
            self.image = "Space-side-scroller/Images/player.png"
        self.ship = pygame.image.load(self.image).convert_alpha()
        self.ship = pygame.transform.scale(self.ship, (64, 81))
        self.rect = self.ship.get_rect(midleft=pos)
        self.max_x_const = 800
        self.max_y_const = 480
        self.ship_speed = 10

    def move_ship(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_DOWN]:
            self.rect.y += self.ship_speed
        if keys[pygame.K_UP]:
            self.rect.y -= self.ship_speed
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.ship_speed
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.ship_speed
        if rpi:
            if ((self.game.chanY.value * 480) < 220):
                self.rect.y += self.ship_speed
            if ((self.game.chanY.value * 480) > 260):
                self.rect.y -= self.ship_speed
            if ((self.game.chanX.value * 800) < 380):
                self.rect.x -= self.ship_speed
            if ((self.game.chanX.value * 800) > 420):
                self.rect.x += self.ship_speed
    
    def constraint(self):
        if self.rect.left <= 0:
            self.rect.left = 0
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.right >= self.max_x_const:
            self.rect.right = self.max_x_const
        if self.rect.bottom >= self.max_y_const:
            self.rect.bottom = self.max_y_const

    def update(self):
        self.move_ship()
        self.constraint()
        self.game.display.blit(self.ship, (self.rect.x, self.rect.y))