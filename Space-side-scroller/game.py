import pygame
from player import Player

class Game():
    def __init__(self):
        pygame.init()
        self.running, self.playing = True, False
        self.UP_KEY, self.DOWN_KEY, self.START_KEY, self.BACK_KEY = False, False, False, False
        self.DISPLAY_W, self.DISPLAY_H = 800, 480
        self.display = pygame.Surface((self.DISPLAY_W, self.DISPLAY_H))
        self.window = pygame.display.set_mode(((self.DISPLAY_W, self.DISPLAY_H)))
        self.font_name = 'Space-side-scroller/Font/8-BIT_WONDER.TTF'
        self.BLACK, self.WHITE = (0, 0, 0), (255, 255, 255)

    def game_loop(self):
        while self.playing:
            self.check_events()
            if self.START_KEY:
                self.playing = False
            self.display.fill(self.BLACK)
            self.draw_text("Thanks for playing", 20, self.DISPLAY_W/2, self.DISPLAY_H/2)
            self.window.blit(self.display, (0,0))
            pygame.display.update()
            self.reset_keys()

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running, self.playing = False, False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.START_KEY = True
                if event.key == pygame.K_BACKSPACE:
                    self.BACK_KEY = True
                if event.key == pygame.K_DOWN:
                    self.DOWN_KEY = True
                if event.key == pygame.K_UP:
                    self.UP_KEY = True
    
    def reset_keys(self):
        self.UP_KEY, self.DOWN_KEY, self.START_KEY, self.BACK_KEY = False, False, False, False

    def draw_text(self, text, size, x, y):
        font = pygame.font.Font(self.font_name, size)
        text_surface = font.render(text, True, self.WHITE)
        text_rect = text_surface.get_rect()
        text_rect.center = (x, y)
        self.display.blit(text_surface, text_rect)







# SCREEN_WITDH = 800
# SCREEN_HEIGHT = 480

# screen = pygame.display.set_mode((SCREEN_WITDH, SCREEN_HEIGHT))
# pygame.display.set_caption('Shooter')

# player1 = Player(200, 200, 18)

# def main_game():
#     run = True
#     background_img_game = pygame.image.load('Space-side-scroller/Images/background_game.jpg')
#     background_img_game = pygame.transform.scale(background_img_game, (1200, 500))
#     while run:
        
#         screen.blit(background_img_game, (0,0))
#         screen.blit(player1.image, player1.rect)
#         pygame.display.update()


#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 pygame.display.quit()
#                 run = False