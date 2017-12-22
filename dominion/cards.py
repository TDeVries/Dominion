import six


def gain_card(player, supply_piles, cost_limit=99):
    '''The player gets to gain a card for free, as long as there are 
    enough left, and it is below the cost limit.

    Args:
        player (instance): The player who gets the free card.
        supply_piles (instance): The supply piles from which the card
        will be taken.
        cost_limit (int): The maximum allowed cost of the free card. If
        not specified, then there is (effectively) no limit. Default: 99.
    '''

    valid_gains = []
    for card_name, supply_pile in six.iteritems(supply_piles):
        if len(supply_pile) > 0:
            card = supply_pile[0]
            if card.cost <= cost_limit:
                valid_gains.append(card.name)

    selected_gain = player.agent.select_gain(valid_gains)

    for card_name, supply_pile in six.iteritems(supply_piles):
        if len(supply_pile) > 0:
            card = supply_pile[0]
            if card.name == selected_gain:
                supply_piles[card_name].remove(card)
                player.deck.discard_pile.append(card)
                break


def discard_card(player):
    '''The player selects a card to discard. It is moved from their hand
    to the discard pile.

    Args:
        player (instance): The player who discards a card.
    '''
    valid_discard = []
    for card in player.hand.hand:
        if card.name not in valid_discard:
            valid_discard.append(card.name)

    selected_discard = player.agent.select_discard(valid_discard)

    for card in player.hand.hand:
        if card.name == selected_discard:
            player.hand.hand.remove(card)
            player.deck.discard_pile.append(card)
            break


def trash_card(player):
    '''The player selects a card to trash. It is removed from the game.

    Args:
        player (instance): The player who trashes a card.
    '''
    valid_trash = []
    for card in player.hand.hand:
        if card.name not in valid_trash:
            valid_trash.append(card.name)

    selected_trash = player.agent.select_trash(valid_trash)

    for card in player.hand.hand:
        if card.name == selected_trash:
            player.hand.hand.remove(card)
            break

    return card


class Copper(object):
    def __init__(self):
        self.name = 'Copper'
        self.cost = 0
        self.card_type = 'Treasure'
        self.card_subtype = None
        self.coins = 1


class Silver(object):
    def __init__(self):
        self.name = 'Silver'
        self.cost = 3
        self.card_type = 'Treasure'
        self.card_subtype = None
        self.coins = 2


class Gold(object):
    def __init__(self):
        self.name = 'Gold'
        self.cost = 6
        self.card_type = 'Treasure'
        self.card_subtype = None
        self.coins = 3


class Estate(object):
    def __init__(self):
        self.name = 'Estate'
        self.cost = 2
        self.card_type = 'Victory'
        self.card_subtype = None
        self.victory_points = 1


class Duchy(object):
    def __init__(self):
        self.name = 'Duchy'
        self.cost = 5
        self.card_type = 'Victory'
        self.card_subtype = None
        self.victory_points = 3


class Province(object):
    def __init__(self):
        self.name = 'Province'
        self.cost = 8
        self.card_type = 'Victory'
        self.card_subtype = None
        self.victory_points = 6


class Curse(object):
    def __init__(self):
        self.name = 'Curse'
        self.cost = 0
        self.card_type = 'Curse'
        self.card_subtype = None
        self.victory_points = -1


class Cellar(object):
    def __init__(self):
        self.name = 'Cellar'
        self.cost = 2
        self.card_type = 'Action'
        self.card_subtype = None
        self.plus_action = 1


class Chapel(object):
    def __init__(self):
        self.name = 'Chapel'
        self.cost = 2
        self.card_type = 'Action'
        self.card_subtype = None


class Moat(object):
    def __init__(self):
        self.name = 'Moat'
        self.cost = 2
        self.card_type = 'Action'
        self.card_subtype = 'Reaction'
        self.plus_cards = 2


class Chancellor(object):
    def __init__(self):
        self.name = 'Chancellor'
        self.cost = 3
        self.card_type = 'Action'
        self.card_subtype = None
        self.coins = 2


class Village(object):
    def __init__(self):
        self.name = 'Village'
        self.cost = 3
        self.card_type = 'Action'
        self.card_subtype = None
        self.plus_cards = 1
        self.plus_actions = 2


class Woodcutter(object):
    def __init__(self):
        self.name = 'Woodcutter'
        self.cost = 3
        self.card_type = 'Action'
        self.card_subtype = None


class Workshop(object):
    def __init__(self):
        self.name = 'Workshop'
        self.cost = 3
        self.card_type = 'Action'
        self.card_subtype = None

    def special_ability(self, game, player):
        '''Player gains a card worth up to 4 coins.

        Args:
            game (instance): The current game.
            player (instance): The player who gains the card
        '''
        gain_card(player=player, supply_piles=game.supply_piles.supply_piles,
                  cost_limit=4)


class Bureaucrat(object):
    def __init__(self):
        self.name = 'Bureaucrat'
        self.cost = 4
        self.card_type = 'Action'
        self.card_subtype = 'Attack'


class Feast(object):
    def __init__(self):
        self.name = 'Feast'
        self.cost = 4
        self.card_type = 'Action'
        self.card_subtype = None

    def special_ability(self, game, player):
        '''Player gains a card worth up to 5 coins, and the Feast card
        is trashed.

        Args:
            game (instance): The current game.
            player (instance): The player who gains the card
        '''
        gain_card(player=player, supply_piles=game.supply_piles.supply_piles,
                  cost_limit=5)
        player.deck.discard_pile.remove(self)


class Gardens(object):
    def __init__(self):
        self.name = 'Gardens'
        self.cost = 4
        self.card_type = 'Victory'
        self.card_subtype = None


class Militia(object):
    def __init__(self):
        self.name = 'Militia'
        self.cost = 4
        self.card_type = 'Action'
        self.card_subtype = 'Attack'
        self.coins = 2


class Moneylender(object):
    def __init__(self):
        self.name = 'Moneylender'
        self.cost = 4
        self.card_type = 'Action'
        self.card_subtype = None


class Remodel(object):
    def __init__(self):
        self.name = 'Remodel'
        self.cost = 4
        self.card_type = 'Action'
        self.card_subtype = None


class Smithy(object):
    def __init__(self):
        self.name = 'Smithy'
        self.cost = 4
        self.card_type = 'Action'
        self.card_subtype = None
        self.plus_cards = 3


class Spy(object):
    def __init__(self):
        self.name = 'Spy'
        self.cost = 4
        self.card_type = 'Action'
        self.card_subtype = 'Attack'
        self.plus_cards = 1
        self.plus_actions = 1


class Thief(object):
    def __init__(self):
        self.name = 'Thief'
        self.cost = 4
        self.card_type = 'Action'
        self.card_subtype = 'Attack'


class ThroneRoom(object):
    def __init__(self):
        self.name = 'Throne Room'
        self.cost = 4
        self.card_type = 'Action'
        self.card_subtype = None


class CouncilRoom(object):
    def __init__(self):
        self.name = 'Council Room'
        self.cost = 5
        self.card_type = 'Action'
        self.card_subtype = None
        self.plus_cards = 4
        self.plus_buys = 1


class Festival(object):
    def __init__(self):
        self.name = 'Festival'
        self.cost = 5
        self.card_type = 'Action'
        self.card_subtype = None
        self.plus_actions = 2
        self.plus_buys = 1
        self.coins = 2


class Laboratory(object):
    def __init__(self):
        self.name = 'Laboratory'
        self.cost = 5
        self.card_type = 'Action'
        self.card_subtype = None
        self.plus_cards = 2
        self.plus_actions = 1


class Library(object):
    def __init__(self):
        self.name = 'Library'
        self.cost = 5
        self.card_type = 'Action'
        self.card_subtype = None


class Market(object):
    def __init__(self):
        self.name = 'Market'
        self.cost = 5
        self.card_type = 'Action'
        self.card_subtype = None
        self.plus_cards = 1
        self.plus_actions = 1
        self.plus_buys = 1
        self.coins = 1


class Mine(object):
    def __init__(self):
        self.name = 'Mine'
        self.cost = 5
        self.card_type = 'Action'
        self.card_subtype = None


class Witch(object):
    def __init__(self):
        self.name = 'Witch'
        self.cost = 5
        self.card_type = 'Action'
        self.card_subtype = 'Attack'
        self.plus_cards = 2


class Adventurer(object):
    def __init__(self):
        self.name = 'Adventurer'
        self.cost = 6
        self.card_type = 'Action'
        self.card_subtype = None
