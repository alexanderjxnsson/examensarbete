import pygame
import os

scores = []
fileName = "Space-side-scroller/highscore.txt"

class Menu():
    def __init__(self, game):
        self.game = game
        self.mid_w, self.mid_h = self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2
        self.run_display = True
        self.cursor_rect = pygame.Rect(0, 0, 20, 20)
        self.offset = -100

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
        self.startx, self.starty = self.mid_w, self.mid_h + 30
        self.highscorex, self.highscorey = self.mid_w, self.mid_h + 50
        self.creditsx, self.creditsy = self.mid_w, self.mid_h + 70
        self.quitx, self.quity = self.mid_w, self.mid_h + 90
        self.cursor_rect.midtop = (self.startx + self.offset, self.starty)

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            self.check_input()
            self.game.display.fill(self.game.BLACK)
            self.game.draw_text('Main menu', 20, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 - 20)
            self.game.draw_text('Start game', 20, self.startx, self.starty)
            self.game.draw_text('Highscore', 20, self.highscorex, self.highscorey)
            self.game.draw_text('Credits', 20, self.creditsx, self.creditsy)
            self.game.draw_text('Quit', 20, self.quitx, self.quity)
            self.draw_cursor()
            self.blit_screen()

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
                pygame.display.quit()
                exit() # remove when finished
                # os.system("shutdown now -h")
            self.run_display = False

class HighscoreMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        """ self.state = 'Volume'
        self.volx, self.voly = self.mid_w, self.mid_h + 20
        self.controlsx, self.controlsy = self.mid_w, self.mid_h + 40 
        self.cursor_rect.midtop = (self.volx + self.offset, self.voly) """
        self.highscorex, self.highscorey = self.mid_w, self.mid_h - 50

    def display_menu(self):
        HighscoreMenu.read_highscore()
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            self.check_input()
            self.game.display.fill((0, 0, 0))
            self.game.draw_text('Highscores', 30, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 - 100)
            """ self.game.draw_text('Volume', 15, self.volx, self.voly)
            self.game.draw_text('Controls', 15, self.controlsx, self.controlsy) """
            
            self.game.draw_text(str(scores[0]), 25, self.highscorex, self.highscorey)
            self.game.draw_text(str(scores[1]), 25, self.highscorex, self.highscorey + 25)
            self.game.draw_text(str(scores[2]), 25, self.highscorex, self.highscorey + 50)
            self.game.draw_text(str(scores[3]), 25, self.highscorex, self.highscorey + 75)
            self.game.draw_text(str(scores[4]), 25, self.highscorex, self.highscorey + 100)

            # self.draw_cursor()
            self.blit_screen()

    def read_highscore():
        file = open(fileName, 'r')
        for line in file.readlines():
            scores.append(int(line))
        scores.sort(reverse=True)
        file.close()

    def write_highscore(newScore):
        file = open(fileName, 'a')
        file.write(str(newScore) + '\n')
        file.close()
        
        """ for x in scores:
            if newScore > x:
                x = newScore
        file = open(fileName, 'w+')
        file.write(str(scores)) """

        """ with open(fileName, 'w') as file:
            for item in scores:
                # write each item on a new line
                file.write("%s\n" % item) """
            
    def check_input(self):
        if self.game.BACK_KEY or self.game.START_KEY:
            self.game.curr_menu = self.game.main_menu
            self.run_display = False
        """ elif self.game.UP_KEY or self.game.DOWN_KEY:
            if self.state == 'Volume':
                self.cursor_rect.midtop = (self.controlsx + self.offset, self.controlsy)
                self.state = 'Controls'
            elif self.state == 'Controls':
                self.cursor_rect.midtop = (self.volx + self.offset, self.voly)
                self.state = 'Volume'
        elif self.game.START_KEY:
            pass """

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
            self.game.display.fill(self.game.BLACK)
            self.game.draw_text('Credits', 20, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 - 20)
            self.game.draw_text('Adam Johansson Kusnierz', 20, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 + 10)
            self.game.draw_text('Alexander Jxnsson', 20, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 + 30)
            self.blit_screen()

    





""" SCREEN_WITDH = 800
SCREEN_HEIGHT = 480

screen = pygame.display.set_mode((SCREEN_WITDH, SCREEN_HEIGHT))
pygame.display.set_caption('Main Menu')

def menu():
    background_img_menu = pygame.image.load('Space-side-scroller/Images/background_menu.jpg')
    background_img_menu = pygame.transform.scale(background_img_menu, (900, 600))

    while True:
        screen.blit(background_img_menu, (0,0))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.display.quit()
                exit() """