import pygame

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, scale):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load("Space-side-scroller/Images/player.png")
        self.image = pygame.transform.scale(img, (img.get_width() / scale, img.get_height() / scale))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)