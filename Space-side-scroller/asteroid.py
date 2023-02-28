import pygame
from global_var import *
from player import Player

class Asteroid(pygame.sprite.Sprite):
    def __init__(self, game, pos, x_const, y_const, asteroid_choice, speed):
        pygame.sprite.Sprite.__init__(self)
        self.game = game
        if rpi:
            self.image1 = pygame.image.load("Images/as2.png").convert_alpha()
            self.image2 = pygame.image.load("Images/as3.png").convert_alpha()
        else:
            self.image1 = pygame.image.load("Space-side-scroller/Images/as2.png").convert_alpha()
            self.image2 = pygame.image.load("Space-side-scroller/Images/as3.png").convert_alpha()
        

        
        if asteroid_choice == 1:
            self.image = pygame.transform.scale(self.image1, (82, 80))
            self.rect = self.image.get_rect(center=pos)
        elif asteroid_choice == 2:
            self.image = pygame.transform.scale(self.image2, (80, 60))
            self.rect = self.image.get_rect(center=pos)
        self.max_x_const = x_const
        self.max_y_const = y_const
        self.ship_speed = speed

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