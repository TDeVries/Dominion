"""Currently a debugging script, however this will manage the main game loop.
"""
import click

from dominion.game import Game
from dominion.agent import HMIAgent


@click.command()
@click.option('--card-set',
              default='base',
              help='The set of cards to play with, e.g. base or random.')
@click.option('--num-players',
              default=3,
              help="""Number of players to play with (currently assumed one
                   human, others machine.)""")
@click.option('--verbose', is_flag=True)
def play_game(card_set, num_players, verbose):
    """Plays a game of Dominion, displaying the initial game state and then
    running the game simulation.
    """
    agent_dict = {'Human Player 1': HMIAgent()}
    demo_game = Game(n_players=num_players,
                     agents=agent_dict,
                     card_set=card_set,
                     verbose=verbose)

    demo_game.players[0].display_deck()
    print("")

    demo_game.players[0].display_hand()
    print("")

    demo_game.players[0].display_draw_pile()
    print("")

    demo_game.players[0].display_discard_pile()
    print("")

    demo_game.play_game()
