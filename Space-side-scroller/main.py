from main_menu import *
from game import Game
from global_var import *

g = Game()

HighscoreMenu.read_highscore()  # Read file 
if not scores:  # Checking if list is empty, if so we write five zeros to fill up.
    HighscoreMenu.write_highscore(True) # So we don't get any errors while entering the highscore menu
    HighscoreMenu.read_highscore() # Read our file and save to list

while g.running:
    g.curr_menu.display_menu()
    g.game_loop()