from menu import *
from game import Game
from global_var import *

g = Game()


HighscoreMenu.read_highscore()  # Read file

while g.running:
    g.curr_menu.display_menu()
    g.game_loop()