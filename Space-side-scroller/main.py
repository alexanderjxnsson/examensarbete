from menu import *
from game import Game

g = Game()


HighscoreMenu.read_highscore()  # Read file

while g.running:
    g.curr_menu.display_menu()
    g.game_loop()