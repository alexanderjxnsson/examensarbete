from game import Game
from player import Player
import main_menu

g = Game()

while g.running:
    g.playing = True
    g.game_loop()