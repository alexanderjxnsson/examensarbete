import pygame
from global_var import *

class Player(pygame.sprite.Sprite):
    def __init__(self, game):
        pygame.sprite.Sprite.__init__(self)
        self.game = game
        if rpi:
            self.player_ship = "Images/player.png"
        else:
            self.player_ship = "Space-side-scroller/Images/player.png"
        self.ship_x, self.ship_y = 0, self.game.DISPLAY_H / 2 - 40
        self.ship = pygame.image.load(self.player_ship)
        self.ship = pygame.transform.scale(self.ship, (64, 81))
        self.max_left, self.max_right = 3, (self.game.DISPLAY_W - 65)
        self.max_up, self.max_down = 9, 390
        self.ship_speed = 10