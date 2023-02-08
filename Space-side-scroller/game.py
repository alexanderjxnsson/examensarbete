import pygame
from menu import *
from player import Player
import math



class Game():
    def __init__(self):
        pygame.init()
        pygame.mouse.set_visible(False)
        self.running, self.playing, self.paused = True, False, False
        self.UP_KEY, self.DOWN_KEY, self.START_KEY, self.BACK_KEY = False, False, False, False
        self.DISPLAY_W, self.DISPLAY_H = 800, 480
        self.display = pygame.Surface((self.DISPLAY_W, self.DISPLAY_H))
        
        if rpi:
            from gpiozero import Button, MCP3008

            self.chanY = MCP3008(channel=0)
            self.chanX = MCP3008(channel=1)

            self.start_btn = Button(2)
            self.back_btn = Button(3)

            self.window = pygame.display.set_mode(((self.DISPLAY_W, self.DISPLAY_H)), pygame.FULLSCREEN)
            self.start_btn_press = pygame.USEREVENT + 0
            self.back_btn_press = pygame.USEREVENT + 1
            self.start_event = pygame.event.Event(self.start_btn_press)
            self.back_event = pygame.event.Event(self.back_btn_press)
            self.start_btn.when_pressed = self.start_pressed
            self.back_btn.when_pressed = self.back_pressed

            self.font_name = 'Font/8-BIT_WONDER.TTF'
            self.bg_game_scroll = pygame.image.load('Images/bg_game_scroll.png').convert()
        else:
            self.window = pygame.display.set_mode(((self.DISPLAY_W, self.DISPLAY_H)))
            self.bg_game_scroll = pygame.image.load('Space-side-scroller/Images/bg_game_scroll.png').convert()
            self.font_name = 'Space-side-scroller/Font/8-BIT_WONDER.TTF'
    
        pygame.display.set_caption("Space Sider Scroller")
        self.BLACK, self.WHITE = (0, 0, 0), (255, 255, 255)
        self.main_menu = MainMenu(self)
        self.highscore = HighscoreMenu(self)
        self.credits = CreditsMenu(self)
        self.quit = QuitMenu(self)
        self.curr_menu = self.main_menu
        self.player_sprite = Player(self, (0, self.DISPLAY_H / 2))
        self.player = pygame.sprite.GroupSingle(self.player_sprite)
        self.bg_game_scroll_width = self.bg_game_scroll.get_width()
        self.scroll = 0
        self.tiles = 3
        self.clock = pygame.time.Clock()
        self.FPS = 60

    def game_loop(self):
        while self.playing:
            self.check_events()
            
            #Exit game loop with back key
            if self.BACK_KEY:
                self.playing = False
                scores.append(7999)
            
            #Scrolling Background
            for i in range(0, self.tiles):
                self.display.blit(self.bg_game_scroll, (i * self.bg_game_scroll_width + self.scroll, 0))
            self.scroll -= 5
            if abs(self.scroll) > self.bg_game_scroll_width:
                self.scroll = 0

            #Loop to pause the game
            while self.paused:
                self.draw_text('PAUSED', 40, self.DISPLAY_W / 2, self.DISPLAY_H / 2 - 100)
                self.check_events()
                self.window.blit(self.display, (0,0))
                pygame.display.update()

            #Updates
            self.player_sprite.update()
            #self.player.draw(self.display)
            self.window.blit(self.display, (0,0))
            pygame.display.update()
            self.reset_keys()
            self.clock.tick(self.FPS)
 
    def start_pressed(self):
        pygame.event.post(self.start_event)
    def back_pressed(self):
        pygame.event.post(self.back_event)
        
    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                pygame.display.quit()
                pygame.quit()
                exit()
            if rpi:
                if event.type == self.start_btn_press:
                        self.START_KEY = True
                if event.type == self.back_btn_press:
                        self.BACK_KEY = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.START_KEY = True
                if event.key == pygame.K_BACKSPACE:
                    self.BACK_KEY = True
                if event.key == pygame.K_DOWN:
                    self.DOWN_KEY = True
                if event.key == pygame.K_UP:
                    self.UP_KEY = True
                if event.key == pygame.K_LEFT:
                    self.LEFT_KEY = True
                if event.key == pygame.K_RIGHT:
                    self.RIGHT_KEY = True
                if event.key == pygame.K_SPACE:
                    if self.paused == True:
                        self.paused = False
                    else:
                        self.paused = True
        if rpi:
            if (self.main_menu.joystick_timer >= 0.5) and ((self.chanY.value * 480) < 220): # Y DOWN
                self.DOWN_KEY = True
                self.main_menu.joystick_timer = 0
            elif (self.main_menu.joystick_timer >= 0.5) and ((self.chanY.value * 480) > 260): # Y UP
                self.UP_KEY = True
                self.main_menu.joystick_timer = 0 
            elif (self.main_menu.joystick_timer >= 0.5) and ((self.chanX.value * 800) > 420): # X RIGHT
                self.RIGHT_KEY = True
                self.main_menu.joystick_timer = 0
            elif (self.main_menu.joystick_timer >= 0.5) and ((self.chanX.value * 800) < 380): # X LEFT
                self.LEFT_KEY = True
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
