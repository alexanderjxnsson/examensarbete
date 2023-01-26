from game import Game

g = Game()

while g.running:
    g.curr_menu.display_menu()
    #g.playing = True
    g.game_loop()