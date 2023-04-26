import pygame
import os
from global_var import *

scores = [("test", 0), ("test2", 0), ("test3", 0), ("test4", 0), ("test5", 0)]

class Menu():
    def __init__(self, game):
        
        self.game = game
        self.mid_w, self.mid_h = self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2
        self.run_display = True
        self.cursor_rect = pygame.Rect(0, 0, 20, 20)
        self.offset = -150
        if rpi:
            self.bg_img_menu = pygame.image.load('Images/menu_background.jpg').convert()
            self.ahlm_logo = pygame.image.load('Images/ahlm.png').convert_alpha()
        else:
            self.bg_img_menu = pygame.image.load('Space-side-scroller/Images/menu_background.jpg').convert()
            self.ahlm_logo = pygame.image.load('Space-side-scroller/Images/ahlm.png').convert_alpha()
    def draw_cursor(self):
        self.game.draw_text('*', 25, self.cursor_rect.x, self.cursor_rect.y)

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
        self.testx, self.testy = self.mid_w, self.mid_h + 200
        self.cursor_rect.midtop = ((self.startx + self.offset), self.starty)
        self.dt = 0
        self.clock = pygame.time.Clock()
        self.joystick_timer = 0

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            self.check_input()
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
                self.cursor_rect = pygame.Rect.move(self.cursor_rect, 0, 40)
                self.state = 'Highscore'
            elif self.state  == 'Highscore':
                self.cursor_rect = pygame.Rect.move(self.cursor_rect, 0, 40)
                self.state = 'Credits'
            elif self.state == 'Credits':
                self.cursor_rect = pygame.Rect.move(self.cursor_rect, 0, 40)
                self.state = 'Quit'
            elif self.state == 'Quit':
                self.cursor_rect = pygame.Rect.move(self.cursor_rect, 0, -120)
                self.state = 'Start'

        if self.game.UP_KEY:
            if self.state == 'Start':
                self.cursor_rect = pygame.Rect.move(self.cursor_rect, 0, 120)
                self.state = 'Quit'
            elif self.state  == 'Highscore':
                self.cursor_rect = pygame.Rect.move(self.cursor_rect, 0, -40)
                self.state = 'Start'
            elif self.state == 'Credits':
                self.cursor_rect = pygame.Rect.move(self.cursor_rect, 0, -40)
                self.state = 'Highscore'
            elif self.state == 'Quit':
                self.cursor_rect = pygame.Rect.move(self.cursor_rect, 0, -40)
                self.state = 'Credits'
    
    def check_input(self):
        self.move_cursor()
        if self.game.START_KEY:
            if self.state == 'Start':
                self.game.playing = True
                self.game.start_time = int(pygame.time.get_ticks() / 1000)
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
        self.offset = -200
        self.highscorex, self.highscorey = self.mid_w, self.mid_h - 50
        self.startx, self.starty = self.mid_w + 10, self.mid_h + 25
        self.cursor_rect = pygame.Rect(0, 0, 20, 20)
        self.cursor_rect.midtop = ((self.startx + self.offset), self.starty)
        self.state = 'First'
        self.firstChar, self.secondChar, self.thirdChar, self.fourthChar = 65, 65, 65, 65
        self.highscoreName = " "

    def draw_char_cursor(self):
        self.game.draw_text("^", 50, self.cursor_rect.x, self.cursor_rect.y - 15)
        self.game.draw_text("<  >", 50, self.cursor_rect.x, self.cursor_rect.y)
        # ASCII value 711 is a arrow down char
        self.game.draw_text(chr(711), 50, self.cursor_rect.x, self.cursor_rect.y + 43)

    def display_menu(self):
        sorted_scores = sorted(scores, key=lambda x: x[1], reverse=True)
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            self.check_input()
            self.game.display.blit(self.bg_img_menu, (0,0))
            self.game.draw_text('Highscores', 40, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 - 100)
            self.game.draw_text(str(sorted_scores[0][0]) + " " + str(sorted_scores[0][1]), 35, self.highscorex, self.highscorey)
            self.game.draw_text(str(sorted_scores[1][0]) + " " + str(sorted_scores[1][1]), 35, self.highscorex, self.highscorey + 40)
            self.game.draw_text(str(sorted_scores[2][0]) + " " + str(sorted_scores[2][1]), 35, self.highscorex, self.highscorey + 80)
            self.game.draw_text(str(sorted_scores[3][0]) + " " + str(sorted_scores[3][1]), 35, self.highscorex, self.highscorey + 120)
            self.game.draw_text(str(sorted_scores[4][0]) + " " + str(sorted_scores[4][1]), 35, self.highscorex, self.highscorey + 160)
            self.blit_screen()

    def writename_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            self.check_input_writename()
            self.game.display.blit(self.bg_img_menu, (0,0))
            self.game.draw_text('Write your name', 40, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 - 80)
            self.game.draw_text(chr(self.firstChar), 35, 0 + 200, self.game.DISPLAY_H / 2 + 25)
            self.game.draw_text(chr(self.secondChar), 35, 0 + 300, self.game.DISPLAY_H / 2 + 25)
            self.game.draw_text(chr(self.thirdChar), 35, 0 + 400, self.game.DISPLAY_H / 2 + 25)
            self.game.draw_text(chr(self.fourthChar), 35, 0 + 500, self.game.DISPLAY_H / 2 + 25)
            self.game.draw_text('*', 35, 0 + 600, self.game.DISPLAY_H / 2 + 25)
            self.draw_char_cursor()
            self.blit_screen()
            if self.run_display == False:
                return self.highscoreName
            
    def move_cursor_writename(self):
        if self.game.RIGHT_KEY:
            if self.state == 'First':
                self.cursor_rect = pygame.Rect.move(self.cursor_rect, 100, 0)
                self.state = 'Second'
            elif self.state  == 'Second':
                self.cursor_rect = pygame.Rect.move(self.cursor_rect, 100, 0)
                self.state = 'Third'
            elif self.state == 'Third':
                self.cursor_rect = pygame.Rect.move(self.cursor_rect, 100, 0)
                self.state = 'Fourth'
            elif self.state == 'Fourth':
                self.cursor_rect = pygame.Rect.move(self.cursor_rect, 100, 0)
                self.state = 'Done'
            elif self.state == 'Done':
                self.cursor_rect = pygame.Rect.move(self.cursor_rect, -400, 0)
                self.state = 'First'

        if self.game.LEFT_KEY:
            if self.state == 'First':
                self.cursor_rect = pygame.Rect.move(self.cursor_rect, 400, 0)
                self.state = 'Done'
            elif self.state  == 'Second':
                self.cursor_rect = pygame.Rect.move(self.cursor_rect, -100, 0)
                self.state = 'First'
            elif self.state == 'Third':
                self.cursor_rect = pygame.Rect.move(self.cursor_rect, -100, 0)
                self.state = 'Second'
            elif self.state == 'Fourth':
                self.cursor_rect = pygame.Rect.move(self.cursor_rect, -100, 0)
                self.state = 'Third'
            elif self.state == 'Done':
                self.cursor_rect = pygame.Rect.move(self.cursor_rect, -100, 0)
                self.state = 'Fourth'
    
    def check_input_writename(self):
        self.move_cursor_writename()
        if self.game.UP_KEY:
            if self.state == 'First':
                self.firstChar += -1
                if self.firstChar < 65:
                   self.firstChar = 90
            if self.state == 'Second':
                self.secondChar += -1
                if self.secondChar < 65:
                   self.secondChar = 90
            if self.state == 'Third':
                self.thirdChar += -1
                if self.thirdChar < 65:
                   self.thirdChar = 90
            if self.state == 'Fourth':
                self.fourthChar += -1
                if self.fourthChar < 65:
                   self.fourthChar = 90
        
        if self.game.DOWN_KEY:
            if self.state == 'First':
                self.firstChar += 1
                if self.firstChar > 90:
                   self.firstChar = 65
            if self.state == 'Second':
                self.secondChar += 1
                if self.secondChar > 90:
                   self.secondChar = 65
            if self.state == 'Third':
                self.thirdChar += 1
                if self.thirdChar > 90:
                   self.thirdChar = 65
            if self.state == 'Fourth':
                self.fourthChar += 1
                if self.fourthChar > 90:
                   self.fourthChar = 65
        if self.game.START_KEY:
            if self.state == 'Done':
                self.highscoreName = chr(self.firstChar) + chr(self.secondChar) + chr(self.thirdChar) + chr(self.fourthChar)
                self.firstChar, self.secondChar, self.thirdChar, self.fourthChar = 65, 65, 65, 65
                self.game.curr_menu = self.game.main_menu
                self.run_display = False

    def read_highscore():
        if not os.path.isfile(file_name):
            file = open(file_name, 'w+')
        else:
            file = open(file_name, 'r')
        for line in file.readlines():
            name, score = line.strip().split()
            scores.append ((name, int(score)))
        file.close()

    def write_highscore():
        file = open(file_name, 'a')
        sorted_scores = sorted(scores, key=lambda x: x[1], reverse=True)
        file.truncate(0)
        for item in sorted_scores[:5]:
            file.write(str(item[0]) + " " + str(item[1]) + '\n')
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
            self.game.display.blit(self.bg_img_menu, (0,0))
            self.game.draw_text('Credits', 40, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 - 30)
            self.game.draw_text('Adam Johansson Kusnierz', 35, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 + 20)
            self.game.draw_text('Alexander Jxnsson', 35, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 + 60)
            self.game.draw_text('Sponsored by ', 15, self.game.DISPLAY_W / 2 + 250, self.game.DISPLAY_H / 2 + 125)
            self.game.display.blit(self.ahlm_logo, (500, 380))
            self.blit_screen()

class QuitMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        self.state = 'No'
        self.offset = -100
        self.nox, self.noy = self.mid_w, self.mid_h + 20
        self.yesx, self.yesy = self.mid_w, self.mid_h + 60
        self.cursor_rect.midtop = ((self.nox + self.offset), self.noy)
        self.clock = pygame.time.Clock()

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            self.check_input()
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
                self.cursor_rect = pygame.Rect.move(self.cursor_rect, 0, 40)
            elif self.state == 'Yes':
                self.state = 'No'
                self.cursor_rect = pygame.Rect.move(self.cursor_rect, 0, -40)
        elif self.game.START_KEY:
            if self.state == 'No':
                self.game.curr_menu = self.game.main_menu
                self.run_display = False
            elif self.state == 'Yes':
                HighscoreMenu.write_highscore()
                pygame.display.quit()
                exit() # remove when finished
                # os.system("shutdown now -h")