import pygame
from global_var import *
from player import Player

class Asteroid(pygame.sprite.Sprite):
    def __init__(self, game, pos, x_const, y_const):
        pygame.sprite.Sprite.__init__(self)
        self.game = game
        if rpi:
            self.image = pygame.image.load("Images/as2.png").convert_alpha()
        else:
            self.image = pygame.image.load("Space-side-scroller/Images/as2.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (64, 81))
        self.rect = self.image.get_rect(center=pos)
        self.max_x_const = x_const
        self.max_y_const = y_const
        self.ship_speed = 1

    #Function to move the ship
    def move_ship(self):
        self.rect.x -= self.ship_speed
    
    #Function to check ship constraints
    def constraint(self):
        if self.rect.left <= -150:
            self.kill()
        
    def update(self):
        self.move_ship()
        self.constraint()