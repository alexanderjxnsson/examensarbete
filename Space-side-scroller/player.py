import pygame
from global_var import *

class Player(pygame.sprite.Sprite):
    def __init__(self, game, pos):
        pygame.sprite.Sprite.__init__(self)
        self.game = game
        if rpi:
            self.image = pygame.image.load("Images/player.png").convert_alpha()
        else:
            self.image = pygame.image.load("Space-side-scroller/Images/player.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (64, 81))
        self.rect = self.image.get_rect(center=pos)
        self.max_x_const = 800
        self.max_y_const = 480
        self.ship_speed = 5
        self.bullet_time = 0
        self.bullet_cooldown = 400
        self.ready = True

    #Function to move the ship
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
        if keys[pygame.K_RETURN] and self.ready:
            self.ready = False
            self.game.score += 100
            self.bullet_time = pygame.time.get_ticks()
            self.game.bullet_group.add(self.create_bullet())
        if rpi:
            if ((self.game.chanY.value * 480) < 220):
                self.rect.y += self.ship_speed
            if ((self.game.chanY.value * 480) > 260):
                self.rect.y -= self.ship_speed
            if ((self.game.chanX.value * 800) < 380):
                self.rect.x -= self.ship_speed
            if ((self.game.chanX.value * 800) > 420):
                self.rect.x += self.ship_speed
            if self.game.start_btn.is_pressed and self.ready:
                self.ready = False
                self.bullet_time = pygame.time.get_ticks()
                self.game.bullet_group.add(self.create_bullet())
    
    #Function to check ship constraints
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
        self.recharge()
        #self.game.display.blit(self.image, (self.rect.x, self.rect.y))
    
    def create_bullet(self):
        return Bullet(self.rect.x + 25, self.rect.y + 41)
    
    def recharge(self):
        if not self.ready:
            current_time = pygame.time.get_ticks()
            if current_time - self.bullet_time >= self.bullet_cooldown:
                self.ready = True

class Bullet(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__()
        if rpi:
            self.image = pygame.image.load("Images/bullet.png").convert_alpha()
        else:
            self.image = pygame.image.load("Space-side-scroller/Images/bullet.png").convert_alpha()
        #self.image.fill((255,0,0))
        self.rect = self.image.get_rect(center = (pos_x, pos_y))
    
    def update(self):
        self.rect.x += 10
        if self.rect.x >= 820:
            self.kill()