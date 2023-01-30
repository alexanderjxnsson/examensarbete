from game import Game
from main_menu import *

if not scores:  # Checking if file is empty, if so we write five zeros to fill up.
    HighscoreMenu.write_highscore(True) # So we don't get any errors while entering the highscore menu
HighscoreMenu.read_highscore() # Read our file and save to list

g = Game()
while g.running:
    g.curr_menu.display_menu()
    #g.playing = True
    g.game_loop()