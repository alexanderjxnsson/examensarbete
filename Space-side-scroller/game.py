import pygame
from main_menu import *



class Game():
    def __init__(self):
        pygame.init()
        pygame.mouse.set_visible(False)
        self.running, self.playing = True, False
        self.UP_KEY, self.DOWN_KEY, self.START_KEY, self.BACK_KEY = False, False, False, False
        self.DISPLAY_W, self.DISPLAY_H = 800, 480
        self.display = pygame.Surface((self.DISPLAY_W, self.DISPLAY_H))
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

            start_btn = gpiozero.Button(18, pull_up=False)
            back_btn = gpiozero.Button(17, pull_up=False)

            self.window = pygame.display.set_mode(((self.DISPLAY_W, self.DISPLAY_H)), pygame.FULLSCREEN)
            start_btn.when_pressed = self.start_pressed
            back_btn.when_pressed = self.back_pressed
            self.font_name = 'Font/8-BIT_WONDER.TTF'
        else:
            self.window = pygame.display.set_mode(((self.DISPLAY_W, self.DISPLAY_H)))
            self.font_name = 'Space-side-scroller/Font/8-BIT_WONDER.TTF'
            
        
        self.BLACK, self.WHITE = (0, 0, 0), (255, 255, 255)
        self.main_menu = MainMenu(self)
        self.highscore = HighscoreMenu(self)
        self.credits = CreditsMenu(self)
        self.quit = QuitMenu(self)
        self.curr_menu = self.main_menu
        

    def game_loop(self):
        while self.playing:
            self.check_events()
            if self.START_KEY:
                self.playing = False
                scores.append(7999)
            self.display.fill(self.BLACK)
            self.draw_text("Thanks for playing", 20, self.DISPLAY_W/2, self.DISPLAY_H/2)
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
                if event.key == pygame.K_UP:
                    self.UP_KEY = True
        if rpi:
            if (self.main_menu.joystick_timer >= 1) and (self.chanY.value / 55 < 235):
                self.DOWN_KEY = True
                self.main_menu.joystick_timer = 0
            else:
                self.main_menu.joystick_timer += self.main_menu.dt
            if (self.main_menu.joystick_timer >= 1) and (self.chanY.value / 55 > 245):
                self.UP_KEY = True
                self.main_menu.joystick_timer = 0
            else:
                self.main_menu.joystick_timer += self.main_menu.dt
        # if start_btn.is_pressed:
        #     self.START_KEY = True
        # if back_btn.is_pressed:
        #     self.BACK_KEY = True
    
    def reset_keys(self):
        self.UP_KEY, self.DOWN_KEY, self.START_KEY, self.BACK_KEY = False, False, False, False

    def draw_text(self, text, size, x, y):
        font = pygame.font.Font(self.font_name, size)
        text_surface = font.render(text, True, self.WHITE)
        text_rect = text_surface.get_rect()
        text_rect.center = (x, y)
        self.display.blit(text_surface, text_rect)
