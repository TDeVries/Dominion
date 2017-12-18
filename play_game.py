from game import Game

demo_game = Game(n_players=2)

print('Deck:')
demo_game.players[0].display_deck()
print("")

print('Hand:')
demo_game.players[0].display_hand()
print("")

print('Draw Pile:')
demo_game.players[0].display_draw_pile()
print("")

print('Discard Pile:')
demo_game.players[0].display_discard_pile()
print("")
