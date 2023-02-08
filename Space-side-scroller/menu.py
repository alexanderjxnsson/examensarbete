import pygame
import os
from global_var import *
#rpi = False

scores = []

class Menu():
    def __init__(self, game):
        
        self.game = game
        self.mid_w, self.mid_h = self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2
        self.run_display = True
        self.cursor_rect = pygame.Rect(0, 0, 20, 20)
        self.offset = -200
        if rpi:
            self.bg_img_menu = pygame.image.load('Images/bg_menu.jpg')
        else:
            self.bg_img_menu = pygame.image.load('Space-side-scroller/Images/bg_menu.jpg')
        self.bg_img_menu = pygame.transform.scale(self.bg_img_menu, (900, 600))
    def draw_cursor(self):
        self.game.draw_text('*', 15, self.cursor_rect.x, self.cursor_rect.y)

    def blit_screen(self):
        self.game.window.blit(self.game.display, (0, 0))
        pygame.display.update()
        self.game.reset_keys()

class MainMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        self.state = "Start"
        self.startx, self.starty = self.mid_w, self.mid_h + 40
        self.highscorex, self.highscorey = self.mid_w, self.mid_h + 80
        self.creditsx, self.creditsy = self.mid_w, self.mid_h + 120
        self.quitx, self.quity = self.mid_w, self.mid_h + 160
        self.cursor_rect.midtop = (self.startx + self.offset, self.starty)
        self.dt = 0
        self.clock = pygame.time.Clock()
        self.joystick_timer = 0

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            self.check_input()
            #self.game.display.fill(self.game.BLACK)
            self.game.display.blit(self.bg_img_menu, (0,0))
            self.game.draw_text('Space Side Scroller', 40, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 - 80)
            self.game.draw_text('Start game', 35, self.startx, self.starty)
            self.game.draw_text('Highscore', 35, self.highscorex, self.highscorey)
            self.game.draw_text('Credits', 35, self.creditsx, self.creditsy)
            self.game.draw_text('Quit', 35, self.quitx, self.quity)
            self.draw_cursor()
            self.blit_screen()
            self.dt = self.clock.tick(60) / 1000

    def move_cursor(self):
        if self.game.DOWN_KEY:
            if self.state == 'Start':
                self.cursor_rect.midtop = (self.highscorex + self.offset, self.highscorey)
                self.state = 'Highscore'
            elif self.state  == 'Highscore':
                self.cursor_rect.midtop = (self.creditsx + self.offset, self.creditsy)
                self.state = 'Credits'
            elif self.state == 'Credits':
                self.cursor_rect.midtop = (self.quitx + self.offset, self.quity)
                self.state = 'Quit'
            elif self.state == 'Quit':
                self.cursor_rect.midtop = (self.startx + self.offset, self.starty)
                self.state = 'Start'

        if self.game.UP_KEY:
            if self.state == 'Start':
                self.cursor_rect.midtop = (self.quitx + self.offset, self.quity)
                self.state = 'Quit'
            elif self.state  == 'Highscore':
                self.cursor_rect.midtop = (self.startx + self.offset, self.starty)
                self.state = 'Start'
            elif self.state == 'Credits':
                self.cursor_rect.midtop = (self.highscorex + self.offset, self.highscorey)
                self.state = 'Highscore'
            elif self.state == 'Quit':
                self.cursor_rect.midtop = (self.creditsx + self.offset, self.creditsy)
                self.state = 'Credits'
    
    def check_input(self):
        self.move_cursor()
        if self.game.START_KEY:
            if self.state == 'Start':
                self.game.playing = True
            if self.state == 'Highscore':
                self.game.curr_menu = self.game.highscore
            if self.state == 'Credits':
                self.game.curr_menu = self.game.credits
            if self.state == 'Quit':
                self.game.curr_menu = self.game.quit  
            self.run_display = False

class HighscoreMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        self.highscorex, self.highscorey = self.mid_w, self.mid_h - 50

    def display_menu(self):
        scores.sort(reverse=True)
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            self.check_input()
            #self.game.display.fill((0, 0, 0))
            self.game.display.blit(self.bg_img_menu, (0,0))
            self.game.draw_text('Highscores', 40, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 - 100)
            self.game.draw_text(str(scores[0]), 35, self.highscorex, self.highscorey)
            self.game.draw_text(str(scores[1]), 35, self.highscorex, self.highscorey + 40)
            self.game.draw_text(str(scores[2]), 35, self.highscorex, self.highscorey + 80)
            self.game.draw_text(str(scores[3]), 35, self.highscorex, self.highscorey + 120)
            self.game.draw_text(str(scores[4]), 35, self.highscorex, self.highscorey + 160)
            self.blit_screen()

    def read_highscore():
        if not os.path.isfile(fileName):
            file = open(fileName, 'w+')
        else:
            file = open(fileName, 'r')
        for line in file.readlines():
            scores.append(int(line))
        file.close()

    def write_highscore(fill_list):
        file = open(fileName, 'a')
        scores.sort(reverse=True)
        if fill_list:
            for x in range(0, 5):
                file.write(str(0) + '\n')
        else :
            file.truncate(0)
            for x in range(0, 5):
                file.write(str(scores[x]) + '\n')
        file.close()
            
    def check_input(self):
        if self.game.BACK_KEY or self.game.START_KEY:
            self.game.curr_menu = self.game.main_menu
            self.run_display = False

class CreditsMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            if self.game.START_KEY or self.game.BACK_KEY:
                self.game.curr_menu = self.game.main_menu
                self.run_display = False
            #self.game.display.fill(self.game.BLACK)
            self.game.display.blit(self.bg_img_menu, (0,0))
            self.game.draw_text('Credits', 40, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 - 30)
            self.game.draw_text('Adam Johansson Kusnierz', 35, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 + 20)
            self.game.draw_text('Alexander Jxnsson', 35, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 + 60)
            self.blit_screen()

class QuitMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        self.state = 'No'
        self.nox, self.noy = self.mid_w, self.mid_h + 20
        self.yesx, self.yesy = self.mid_w, self.mid_h + 60
        self.cursor_rect.midtop = (self.nox + self.offset, self.noy)
        self.clock = pygame.time.Clock()

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            self.check_input()
            #self.game.display.fill((0, 0, 0))
            self.game.display.blit(self.bg_img_menu, (0,0))
            self.game.draw_text('Are you sure', 40, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 - 30)
            self.game.draw_text('No', 35, self.nox, self.noy)
            self.game.draw_text('Yes', 35, self.yesx, self.yesy)
            self.draw_cursor()
            self.blit_screen()
            self.dt = self.clock.tick(60) / 1000

    def check_input(self):
        if self.game.BACK_KEY:
            self.game.curr_menu = self.game.main_menu
            self.run_display = False
        elif self.game.UP_KEY or self.game.DOWN_KEY:
            if self.state == 'No':
                self.state = 'Yes'
                self.cursor_rect.midtop = (self.yesx + self.offset, self.yesy)
            elif self.state == 'Yes':
                self.state = 'No'
                self.cursor_rect.midtop = (self.nox + self.offset, self.noy)
        elif self.game.START_KEY:
            if self.state == 'No':
                self.game.curr_menu = self.game.main_menu
                self.run_display = False
            elif self.state == 'Yes':
                HighscoreMenu.write_highscore(False)
                pygame.display.quit()
                exit() # remove when finished
                # os.system("shutdown now -h")