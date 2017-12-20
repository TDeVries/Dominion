from game import Game
from cards import *

demo_game = Game(n_players=3, card_set='base', verbose=True)

demo_game.players[0].display_deck()
print("")

demo_game.players[0].display_hand()
print("")

demo_game.players[0].display_draw_pile()
print("")

demo_game.players[0].display_discard_pile()
print("")

scores = demo_game.play_game()
