import pygame
from main_menu import *
import math



class Game():
    def __init__(self):
        pygame.init()
        pygame.mouse.set_visible(False)
        self.running, self.playing = True, False
        self.UP_KEY, self.DOWN_KEY, self.START_KEY, self.BACK_KEY = False, False, False, False
        self.DISPLAY_W, self.DISPLAY_H = 800, 480
        self.display = pygame.Surface((self.DISPLAY_W, self.DISPLAY_H))
        
        pygame.display.set_caption("Space Sider Scroller")
        self.BLACK, self.WHITE = (0, 0, 0), (255, 255, 255)
        self.main_menu = MainMenu(self)
        self.highscore = HighscoreMenu(self)
        self.credits = CreditsMenu(self)
        self.quit = QuitMenu(self)
        self.curr_menu = self.main_menu
        if rpi:
            import gpiozero
            import board
            import busio
            import adafruit_ads1x15.ads1115 as ADS
            from adafruit_ads1x15.analog_in import AnalogIn
            # Create the I2C bus
            i2c = busio.I2C(board.SCL, board.SDA)

            # Create the ADC object using the I2C bus
            ads = ADS.ADS1115(i2c)

            # Create single-ended input on channel 0
            self.chanX = AnalogIn(ads, ADS.P0)
            self.chanY = AnalogIn(ads, ADS.P1)

            self.start_btn = gpiozero.Button(18, pull_up=False, hold_time=0.05, hold_repeat=False)
            self.back_btn = gpiozero.Button(17, pull_up=False, hold_time=0.05, hold_repeat=False)

            self.window = pygame.display.set_mode(((self.DISPLAY_W, self.DISPLAY_H)), pygame.FULLSCREEN)
            self.start_btn.when_held = self.start_pressed
            self.back_btn.when_held = self.back_pressed
            self.font_name = 'Font/8-BIT_WONDER.TTF'
            self.bg_img_menu = pygame.image.load('Images/bg_menu.jpg')
            self.bg_img_game = pygame.image.load('Images/bg_game.jpg')
            self.testing = pygame.image.load('Images/testing.png')
        else:
            self.bg_img_menu = pygame.image.load('Space-side-scroller/Images/bg_menu.jpg')
            self.bg_img_game = pygame.image.load('Space-side-scroller/Images/bg_game.jpg')
            self.testing = pygame.image.load('Space-side-scroller/Images/testing.png')
            self.window = pygame.display.set_mode(((self.DISPLAY_W, self.DISPLAY_H)))
            self.font_name = 'Space-side-scroller/Font/8-BIT_WONDER.TTF'
        self.bg_img_menu = pygame.transform.scale(self.bg_img_menu, (900, 600))
        self.bg_img_game = pygame.transform.scale(self.bg_img_game, (1200, 500))
        self.testing_width = self.testing.get_width()
        self.scroll = 0
        self.tiles = 3
        self.FPS = 60
        self.clock = pygame.time.Clock()
        self.ship = pygame.image.load(player_ship)
        self.ship = pygame.transform.scale(self.ship, (127, 162))
        self.ship_x = 0
        self.ship_y = self.DISPLAY_H / 2 - 81
        

    def game_loop(self):
        while self.playing:
            self.clock.tick(self.FPS)
            self.check_events()
            if self.START_KEY:
                self.playing = False
                scores.append(7999)
            #self.display.fill(self.BLACK)
            for i in range(0, self.tiles):
                self.display.blit(self.testing, (i * self.testing_width + self.scroll, 0))
            self.scroll -= 5
            if abs(self.scroll) > self.testing_width:
                self.scroll = 0
            self.display.blit(self.ship, (self.ship_x, self.ship_y))
            self.window.blit(self.display, (0,0))
            pygame.display.update()
            self.reset_keys()
    
    def start_pressed(self):
        self.START_KEY = True
    def back_pressed(self):
        self.BACK_KEY = True
        
    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running, self.playing = False, False
                self.curr_menu.run_display = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.START_KEY = True
                if event.key == pygame.K_BACKSPACE:
                    self.BACK_KEY = True
                if event.key == pygame.K_DOWN:
                    self.DOWN_KEY = True
                    self.ship_y += 5
                if event.key == pygame.K_UP:
                    self.UP_KEY = True
                    self.ship_y -= 5
                if event.key == pygame.K_LEFT:
                    self.LEFT_KEY = True
                    self.ship_x -= 5
                if event.key == pygame.K_RIGHT:
                    self.RIGHT_KEY = True
                    self.ship_x += 5
        if rpi:
            if (self.main_menu.joystick_timer >= 1) and (self.chanY.value / 55 < 235): # Y DOWN
                self.DOWN_KEY = True
                self.ship_y += 5
                self.main_menu.joystick_timer = 0
            elif (self.main_menu.joystick_timer >= 1) and (self.chanY.value / 55 > 245): # Y UP
                self.UP_KEY = True
                self.ship_y -= 5
                self.main_menu.joystick_timer = 0 
            elif (self.main_menu.joystick_timer >= 1) and (self.chanX.value / 55 > 405): # X RIGHT
                self.RIGHT_KEY = True
                self.ship_x += 5
                self.main_menu.joystick_timer = 0
            elif (self.main_menu.joystick_timer >= 1) and (self.chanX.value / 55 < 395): # X LEFT
                self.LEFT_KEY = True
                self.ship_x -= 5
                self.main_menu.joystick_timer = 0
            else:
                self.main_menu.joystick_timer += self.main_menu.dt    
    
    def reset_keys(self):
        self.UP_KEY, self.DOWN_KEY, self.START_KEY, self.BACK_KEY = False, False, False, False

    def draw_text(self, text, size, x, y):
        font = pygame.font.Font(self.font_name, size)
        text_surface = font.render(text, True, self.WHITE)
        text_rect = text_surface.get_rect()
        text_rect.center = (x, y)
        self.display.blit(text_surface, text_rect)
