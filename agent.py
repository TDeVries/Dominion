import random

import click


class Agent(object):
    def __init__(self):
        '''Base agent class. Agents are used to make decisions for each
        player in the game. Custom agents can be created by inheriting
        this class and modifying the decision functions.'''
        pass

    def _get_game_state(self):
        pass

    def select_action(self, valid_actions):
        raise NotImplementedError

    def select_buy(self, valid_buys):
        raise NotImplementedError


def _user_select_from_list(option_name, options):
    """Prompt the user to select options of type `option_name` (e.g. buys or
    actions) from the list `options`, by entering a number at the keyboard (or
    q to exit the program).

    Returns the selected element of `options`.
    """
    assert len(options) < 100

    click.echo(
        'Select {} (h for help, q to quit Dominion):'.format(option_name))

    for i, action in enumerate(options):
        click.echo('{}: {}'.format(i, action))

    while True:
        char = click.getchar()
        if char.lower() == 'h':
            click.echo()
            click.echo('  Enter the digit of the desired option.\n\n'
                       '  If there are more than 10 options:\n'
                       '  Enter <digit><space> for single-digit options, and\n'
                       '        <digit><digit> for double-digit options.')
            click.echo()

        elif char.lower() == 'q':
            click.echo('Farewell.')
            exit()

        elif char.isdigit():
            index = int(char)
            if len(options) <= index:
                continue

            # NOTE(brendan): This hacky code handles the case where there are
            # >= 10 options, and the user has to distinguish between single
            # digit and double digit indices.
            if (len(options) > 10) and ((len(options) // 10) >= index):
                next_char = click.getchar()
                if next_char.isspace():
                    return options[index]

                if not next_char.isdigit():
                    continue

                index = int(char + next_char)
                if len(options) <= index:
                    continue

            return options[index]


class HMIAgent(Agent):
    """A Human Machine Interface agent, which takes input from the command
    line.
    """
    def __init__(self):
        super(HMIAgent, self).__init__()

    def select_action(self, valid_actions):
        """Select an action from the list of enumerated valid actions, by
        inputting a number at the keyboard.

        Typing Q quits the Dominion game.
        """
        return _user_select_from_list('action', valid_actions)

    def select_buy(self, valid_buys):
        return _user_select_from_list('buy', valid_buys)


class RandomAgent(Agent):
    def __init__(self):
        '''Agent that makes decisions randomly.'''
        super(RandomAgent, self).__init__()

    def select_action(self, valid_actions):
        '''Randomly select an action from the list of valid actions.

        Args:
            valid_actions (list): Contains the actions that can be
            played this turn.
        '''
        selected_action = random.choice(valid_actions)
        return selected_action

    def select_buy(self, valid_buys):
        '''Randomly select a card to purchase from the list of valid buys.

        Args:
            valid_buys (list): Contains the cards that can be purchased
            this turn.
        '''
        selected_buy = random.choice(valid_buys)
        return selected_buy
