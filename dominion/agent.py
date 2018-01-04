import random
import inspect
import six
import cards

import click


class Agent(object):
    def __init__(self):
        '''Base agent class. Agents are used to make decisions for each
        player in the game. Custom agents can be created by inheriting
        this class and modifying the decision functions.'''

        self.player = None

        # This function collects the names of all the classes from the
        # cards module, i.e. all the card names.
        card_names = [m[0] for m in inspect.getmembers(cards, inspect.isclass)
                      if m[1].__module__ == 'dominion.cards']

        cards_base_dict = {}
        for card_name in card_names:
            cards_base_dict[card_name] = 0

        self.cards_base_dict = cards_base_dict

    def _get_game_state(self):
        '''Retrieve the game state and encode it. The game state consists
        of three parts:

        1) The number of each card in the player's deck
        2) The number of cards in each of the supply piles
        3) The player's current hand

        Information is first encoded in dictionaries which count the
        number of all cards for each part of the game state. The
        dictionaries are then converted to lists and concatenated to get
        a single list containing a bunch of numbers the represents the
        current game state.

        Return:
            game_state (list): A list which contains the encoded game
            state.
        '''
        assert self.player is not None, 'player object is not instantiated!'

        deck = self.player.deck.draw_pile + self.player.deck.discard_pile + \
            self.player.hand.hand
        supply_piles = self.player.game.supply_piles.supply_piles
        hand = self.player.hand.hand

        deck_dict = self.cards_base_dict.copy()
        supply_piles_dict = self.cards_base_dict.copy()
        hand_dict = self.cards_base_dict.copy()

        for card in deck:
            deck_dict[card.name] += 1

        for card_name, supply_pile in six.iteritems(supply_piles):
            supply_piles_dict[card_name] = len(supply_pile)

        for card in hand:
            hand_dict[card.name] += 1

        deck_list = self._dict_to_list(deck_dict)
        supply_pile_list = self._dict_to_list(supply_piles_dict)
        hand_list = self._dict_to_list(hand_dict)

        game_state = deck_list + supply_pile_list + hand_list
        return game_state

    def _dict_to_list(self, card_dict):
        '''Converts a dictionary of cards and their corresponding counts
        to a list of the card counts. Cards are sorted in alphabetical
        order so that each index always contains the count for the same
        card.

        Args:
            card_dict (dict): A dictionary where the keys are card names
            and the values are integers representing the number of that
            card.

        Return:
            card_list (list): A list where each value represents the
            count of the corresponding card.
        '''
        assert len(card_dict) == len(self.cards_base_dict), 'dict ' + \
            'should have one index for each possible card (even ' + \
            'those not included in this game)'

        card_list = [value for (key, value) in sorted(card_dict.items())]
        return card_list

    def _list_to_dict(self, card_list):
        '''Converts a list of cards to a dictionary. Counts are remapped
        to the corresponding card.

        Args:
            card_list (list): A list where each value represents the
            count of the corresponding card.

        Return:
            card_dict (dict): A dictionary where the keys are card names
            and the values are integers representing the number of that
            card.
        '''
        assert len(card_list) == len(self.cards_base_dict), 'list ' + \
            'should have one index for each possible card (even ' + \
            'those not included in this game)'

        card_dict = {}
        for key, value in zip(sorted(self.cards_base_dict.keys()), card_list):
            card_dict[key] = value
        return card_dict

    def select_action(self, valid_actions):
        raise NotImplementedError

    def select_buy(self, valid_buys):
        raise NotImplementedError

    def select_gain(self, valid_gains):
        raise NotImplementedError

    def select_discard(self, valid_discard):
        raise NotImplementedError

    def select_trash(self, valid_trash):
        raise NotImplementedError

    def select_n_discard(self, valid_n):
        raise NotImplementedError

    def select_n_trash(self, valid_n):
        raise NotImplementedError

    def select_shuffle(self, valid_options=['Yes', 'No']):
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

    def select_gain(self, valid_gains):
        return _user_select_from_list('gain', valid_gains)

    def select_discard(self, valid_discard):
        return _user_select_from_list('discard', valid_discard)

    def select_trash(self, valid_trash):
        return _user_select_from_list('trash', valid_trash)

    def select_n_discard(self, valid_n):
        return _user_select_from_list('number of cards to discard', valid_n)

    def select_n_trash(self, valid_n):
        return _user_select_from_list('number of cards to trash', valid_n)

    def select_shuffle(self, valid_options=['Yes', 'No']):
        return _user_select_from_list('shuffle deck', valid_options)


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

    def select_gain(self, valid_gains):
        '''Randomly select a card to gain from the list of valid cards.

        Args:
            valid_gain (list): Contains the card that will be gained.
        '''
        selected_gain = random.choice(valid_gains)
        return selected_gain

    def select_discard(self, valid_discard):
        '''Randomly select a card to discard.

        Args:
            valid_discard (list): Contains the card that will be discarded.
        '''
        selected_discard = random.choice(valid_discard)
        return selected_discard

    def select_trash(self, valid_trash):
        '''Randomly select a card to trash.

        Args:
            valid_trash (list): Contains the card that will be trashed.
        '''
        selected_trash = random.choice(valid_trash)
        return selected_trash

    def select_n_discard(self, valid_n):
        '''Randomly select a number of cards to discard

        Args:
            valid_n (list): Contains the options for the number of cards
            to discard.
        '''
        selected_n = random.choice(valid_n)
        return selected_n

    def select_n_trash(self, valid_n):
        '''Randomly select a number of cards to trash

        Args:
            valid_n (list): Contains the options for the number of cards
            to trash.
        '''
        selected_n = random.choice(valid_n)
        return selected_n

    def select_shuffle(self, valid_options=['Yes', 'No']):
        '''Randomly select whether or not to put the deck in the discard
        pile (i.e. to reshuffle).

        Args:
            valid_options (list): Should always be a list containing
            'yes' and 'no'.
        '''
        selected_shuffle = random.choice(valid_options)
        return selected_shuffle
