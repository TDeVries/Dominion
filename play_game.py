from game import Game
from cards import *

demo_game = Game(n_players=2, card_set='base', verbose=True)

demo_game.players[0].display_deck()
print("")

demo_game.players[0].display_hand()
print("")

demo_game.players[0].display_draw_pile()
print("")

demo_game.players[0].display_discard_pile()
print("")

# Add a Market to the hand for testing
demo_game.players[0].hand.hand.append(Market())
demo_game.take_turn(demo_game.players[0])
print("")

print("Game over: " + str(demo_game.check_game_over()))
