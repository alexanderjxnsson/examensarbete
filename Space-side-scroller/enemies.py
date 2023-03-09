import pygame
from global_var import *

class Enemies(pygame.sprite.Sprite):
    def __init__(self, game, pos, x_const, y_const, speed):
        pygame.sprite.Sprite.__init__(self)
        self.game = game
        if rpi:
            self.image = pygame.image.load("Images/enemy1_new_crop.png").convert_alpha()
        else:
            self.image = pygame.image.load("Space-side-scroller/Images/enemy1_new_crop.png").convert_alpha()
        self.rect = self.image.get_rect(center=pos)
        self.max_x_const = x_const
        self.max_y_const = y_const
        self.ship_speed = speed
        self.bullet_time = 0
        self.bullet_cooldown = 1750
        self.ready = True
        
        
    #Function to move the ship
    def move_ship(self):
        self.rect.x -= self.ship_speed
    
    #Function to check ship constraints
    def constraint(self):
        if self.rect.left <= -150:
            self.kill()

    def return_pos(self):
        val = self.rect.x
        return val

    def update(self):
        self.move_ship()
        self.constraint()
        self.recharge()
    
    def create_bullet(self):
        return Enemy_bullet(self.rect.x + 40, self.rect.y + 50)    

    def recharge(self):
        if not self.ready:
            current_time = pygame.time.get_ticks()
            if current_time - self.bullet_time >= self.bullet_cooldown:
                self.ready = True
        if self.ready:
            self.ready = False
            self.bullet_time = pygame.time.get_ticks()
            self.game.enemy_bullet.add(self.create_bullet())

class Enemy_bullet(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__()
        if rpi:
            self.image = pygame.image.load("Images/bullet_blue.png").convert_alpha()
        else:
            self.image = pygame.image.load("Space-side-scroller/Images/bullet_blue.png").convert_alpha()
        #self.image.fill((255,0,0))
        self.rect = self.image.get_rect(center = (pos_x, pos_y))
    
    def update(self):
        self.rect.x -= 10
        if self.rect.x <= -150:
            self.kill()
        