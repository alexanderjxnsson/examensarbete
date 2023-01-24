from game import Game
from player import Player
import main_menu

g = Game()

while g.running:
    g.curr_menu.display_menu()
    #g.playing = True
    g.game_loop()