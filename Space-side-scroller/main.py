from game import Game
from main_menu import HighscoreMenu

g = Game()

HighscoreMenu.read_highscore()
while g.running:
    g.curr_menu.display_menu()
    g.game_loop()