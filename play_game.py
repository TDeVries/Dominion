from game import Game
from agent import RandomAgent
from cards import *

agent_dict = {'DemoBot 1': RandomAgent()}
demo_game = Game(n_players=3, agents=agent_dict, card_set='base', verbose=True)

demo_game.players[0].display_deck()
print("")

demo_game.players[0].display_hand()
print("")

demo_game.players[0].display_draw_pile()
print("")

demo_game.players[0].display_discard_pile()
print("")

scores = demo_game.play_game()
