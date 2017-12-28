import six


def gain_card(player, supply_piles, cost_limit=99, valid_gains=None,
              destination='discard_pile'):
    '''The player gets to gain a card for free, as long as there are
    enough left, and it is below the cost limit.

    Args:
        player (instance): The player who gets the free card.
        supply_piles (instance): The supply piles from which the card
        will be taken.
        cost_limit (int): The maximum allowed cost of the free card. If
        not specified, then there is (effectively) no limit. Default: 99.
        valid_gains (list): List of card names that can be gained. If
        None, all cards in the player's hand are valid. Default: None.
        destination (str): Where the gained card will be placed. Options
        are 'discard_pile' and 'hand'. Default: 'discard_pile'.
    '''
    assert destination in ['discard_pile', 'hand'], 'destination must be \
        either "discard_pile" or "hand"'

    if valid_gains is None:
        valid_gains = []
        for card_name, supply_pile in six.iteritems(supply_piles):
            if len(supply_pile) > 0:
                card = supply_pile[0]
                if card.cost <= cost_limit:
                    valid_gains.append(card.name)
    else:
        for card_name, supply_pile in six.iteritems(supply_piles):
            if card_name in valid_gains:
                if len(supply_pile) == 0:
                    valid_gains.remove(card_name)
                else:
                    card = supply_pile[0]
                    if card.cost > cost_limit:
                        valid_gains.remove(card_name)

    selected_gain = player.agent.select_gain(valid_gains=valid_gains)

    for card_name, supply_pile in six.iteritems(supply_piles):
        if len(supply_pile) > 0:
            card = supply_pile[0]
            if card.name == selected_gain:
                supply_piles[card_name].remove(card)

                if destination == 'discard_pile':
                    player.deck.discard_pile.append(card)
                elif destination == 'hand':
                    player.hand.hand.append(card)
                break


def discard_card(player, valid_discard=None):
    '''The player selects a card to discard. It is moved from their hand
    to the discard pile.

    Args:
        player (instance): The player who discards a card.
        valid_discard (list): List of card names that can be discarded.
        If None, all cards in the player's hand are valid. Default: None
    '''
    if valid_discard is None:
        valid_discard = []
        for card in player.hand.hand:
            if card.name not in valid_discard:
                valid_discard.append(card.name)

    selected_discard = player.agent.select_discard(valid_discard=valid_discard)

    for card in player.hand.hand:
        if card.name == selected_discard:
            player.hand.hand.remove(card)
            player.deck.discard_pile.append(card)
            break


def trash_card(player, valid_trash=None):
    '''The player selects a card to trash. It is removed from the game.

    Args:
        player (instance): The player who trashes a card.
        valid_trash (list): List of card names that can be trashed. If
        None, all cards in the player's hand are valid. Default: None

    Return:
        card (instance): The card that was trashed.
    '''
    if valid_trash is None:
        valid_trash = []
        for card in player.hand.hand:
            if card.name not in valid_trash:
                valid_trash.append(card.name)

    selected_trash = player.agent.select_trash(valid_trash=valid_trash)

    for card in player.hand.hand:
        if card.name == selected_trash:
            player.hand.hand.remove(card)
            break

    return card


def successful_attack(player):
    '''Check to see if the player has a moat in their hand. If they do,
    the attack fails. If not, the attack succeeds.

    Args:
        player (instance): The player who is being attacked.

    Return:
        successful_attack (bool): True if the attack is successful,
        False if the atack fails.
    '''
    for card in player.hand.hand:
        if card.name == 'Moat':
            return False
    return True


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
        self.plus_actions = 1

    def special_ability(self, game, player):
        '''Player discards any number of cards, then draws that many.

        Args:
            game (instance): The current game.
            player (instance): The player who played the card
        '''
        valid_n = range(len(player.hand.hand) + 1)
        n = player.agent.select_n_discard(valid_n=valid_n)

        for i in range(n):
            discard_card(player=player)

        for i in range(n):
            player.hand.draw_card()


class Chapel(object):
    def __init__(self):
        self.name = 'Chapel'
        self.cost = 2
        self.card_type = 'Action'
        self.card_subtype = None

    def special_ability(self, game, player):
        '''Player can trash up to 4 cards, as long as they have that
        many cards in their hand.

        Args:
            game (instance): The current game.
            player (instance): The player who played the card
        '''
        valid_n = range(min(len(player.hand.hand) + 1, 5))
        n = player.agent.select_n_trash(valid_n=valid_n)

        for i in range(n):
            trash_card(player=player)


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

    def special_ability(self, game, player):
        '''Player may immediately put their deck into their discard pile.

        Args:
            game (instance): The current game.
            player (instance): The player who played the card.
        '''
        selected_shuffle = player.agent.select_shuffle()
        if selected_shuffle == 'Yes':
            player.deck.shuffle_deck()


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
        self.plus_buys = 1
        self.coins = 2


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
            player (instance): The player who played the card.
        '''
        gain_card(player=player, supply_piles=game.supply_piles.supply_piles,
                  cost_limit=4)


class Bureaucrat(object):
    def __init__(self):
        self.name = 'Bureaucrat'
        self.cost = 4
        self.card_type = 'Action'
        self.card_subtype = 'Attack'

    def special_ability(self, game, player_who_played_the_card):
        '''Player gains a Silver on the top of their deck. Each other
        player puts a Victory card from their hand to the top of their 
        deck (if they have one).

        Args:
            game (instance): The current game.
            player (instance): The player who played the card.
        '''
        silver_pile = game.supply_piles.supply_piles['Silver']
        if len(silver_pile) > 0:
            silver_card = silver_pile.pop(0)
            player_who_played_the_card.deck.draw_pile.insert(0, silver_card)

        for player in game.players:
            if player is not player_who_played_the_card:
                if successful_attack(player=player):
                    for card in player.hand.hand:
                        if card.card_type == 'Victory':
                            player.hand.hand.remove(card)
                            player.deck.draw_pile.insert(0, card)
                            break


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
            player (instance): The player who played the card
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

    def special_ability(self, game, player_who_played_the_card):
        '''Each other player discards down to 3 cards, unless they have
        a moat in their hand.

        Args:
            game (instance): The current game.
            player (instance): The player who played the card
        '''
        for player in game.players:
            if player is not player_who_played_the_card:
                if successful_attack(player=player):
                    while len(player.hand.hand) > 3:
                        discard_card(player=player)


class Moneylender(object):
    def __init__(self):
        self.name = 'Moneylender'
        self.cost = 4
        self.card_type = 'Action'
        self.card_subtype = None

    def special_ability(self, game, player):
        '''Player may trash a copper to gain 3 coins. It is assumed that
        if they play this card and have a copper in their hand, that
        they would like to trash it.

        Args:
            game (instance): The current game.
            player (instance): The player who played the card
        '''
        for card in player.hand.hand:
            if card.name == 'Copper':
                player.hand.hand.remove(card)
                player.turn_state['coins'] += 3
                break


class Remodel(object):
    def __init__(self):
        self.name = 'Remodel'
        self.cost = 4
        self.card_type = 'Action'
        self.card_subtype = None

    def special_ability(self, game, player):
        '''Players trashes a card, and then gains a card worth up to 2
        coins more than the trashed card's worth.

        Args:
            game (instance): The current game.
            player (instance): The player who played the card
        '''
        trashed_card = trash_card(player=player)
        cost_limit = trashed_card.cost + 2
        gain_card(player=player, supply_piles=game.supply_piles.supply_piles,
                  cost_limit=cost_limit)


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

    def special_ability(self, game, player):
        '''Player can play an action card from their hand twice.

        Args:
            game (instance): The current game.
            player (instance): The player who played the card
        '''

        # Change the text of the first valid action to distinguish
        # between throne room and the actual action phase
        valid_actions = game._get_valid_actions(player.hand.hand)
        valid_actions[0] = 'no_action'

        selected_action = player.agent.select_action(valid_actions)

        if selected_action == 'no_action':
            pass
        else:
            for card in player.hand.hand:
                if card.name == selected_action:
                    # Remove the card from the hand first so that the player cannot
                    # choose to discard or trash it after they have already played it
                    player.hand.hand.remove(card)
                    player.deck.discard_pile.append(card)

                    for repeats in range(2):
                        if hasattr(card, 'plus_cards'):
                            for i in range(card.plus_cards):
                                player.hand.draw_card()
                        if hasattr(card, 'plus_actions'):
                            player.turn_state['actions'] += card.plus_actions
                        if hasattr(card, 'plus_buys'):
                            player.turn_state['buys'] += card.plus_buys
                        if hasattr(card, 'coins'):
                            player.turn_state['coins'] += card.coins
                        if hasattr(card, 'special_ability'):
                            card.special_ability(game, player)

                    break


class CouncilRoom(object):
    def __init__(self):
        self.name = 'Council Room'
        self.cost = 5
        self.card_type = 'Action'
        self.card_subtype = None
        self.plus_cards = 4
        self.plus_buys = 1

    def special_ability(self, game, player_who_played_the_card):
        '''Each other player draws a card.

        Args:
            game (instance): The current game.
            player (instance): The player who played the card
        '''

        for player in game.players:
            if player is not player_who_played_the_card:
                player.hand.draw_card()


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

    def special_ability(self, game, player):
        '''Player draws until they have 7 cards. They can immediately
        discard any Action card they draw, and it will not count towards
        the 7 card limit.

        Args:
            game (instance): The current game.
            player (instance): The player who played the card
        '''

        # Keep track of the deck size to make sure we don't get stuck in
        #   a loop if there are not enough cards to draw 7.
        deck_size = len(player.deck.discard_pile) + len(player.deck.draw_pile)
        cards_drawn = 0

        # Cards are not returned to the deck until the action has been 
        #   fully completed
        discarded_cards = []

        while len(player.hand.hand) < 7 and cards_drawn < deck_size:
            player.hand.draw_card()
            cards_drawn += 1
            card = player.hand.hand[-1]

            if card.card_type == 'Action':
                valid_discard = ['keep_card', card.name]
                selected_discard = player.agent.select_discard(valid_discard=valid_discard)

                if selected_discard != 'keep_card':
                    player.hand.hand.remove(card)
                    discarded_cards.append(card)

        for card in discarded_cards:
            player.deck.discard_pile.append(card)


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

    def special_ability(self, game, player):
        '''Players trashes a Treasure card, and then gains a card worth up to 3
        coins more than the trashed card's worth.

        Args:
            game (instance): The current game.
            player (instance): The player who played the card
        '''
        valid_trash = []
        for card in player.hand.hand:
            if card.card_type == 'Treasure' and card.name not in valid_trash:
                valid_trash.append(card.name)

        if len(valid_trash) > 0:
            trashed_card = trash_card(player=player, valid_trash=valid_trash)

            valid_gains = ['Copper', 'Silver', 'Gold']
            cost_limit = trashed_card.cost + 3
            gain_card(player=player, supply_piles=game.supply_piles.supply_piles,
                      cost_limit=cost_limit, valid_gains=valid_gains,
                      destination='hand')


class Witch(object):
    def __init__(self):
        self.name = 'Witch'
        self.cost = 5
        self.card_type = 'Action'
        self.card_subtype = 'Attack'
        self.plus_cards = 2

    def special_ability(self, game, player_who_played_the_card):
        '''Each other player discards down to 3 cards, unless they have
        a moat in their hand.

        Args:
            game (instance): The current game.
            player (instance): The player who played the card
        '''
        for player in game.players:
            if player is not player_who_played_the_card:
                if successful_attack(player=player):
                    curse_pile = game.supply_piles.supply_piles['Curse']
                    if len(curse_pile) > 0:
                        curse_card = curse_pile.pop(0)
                        player.deck.discard_pile.append(curse_card)


class Adventurer(object):
    def __init__(self):
        self.name = 'Adventurer'
        self.cost = 6
        self.card_type = 'Action'
        self.card_subtype = None

    def special_ability(self, game, player):
        '''Player draws cards until they gain two Treasure cards.
        All other card types are discarded.

        Args:
            game (instance): The current game.
            player (instance): The player who played the card
        '''

        # Keep track of the deck size to make sure we don't get stuck in
        #   a loop if there are not enough cards to draw 7.
        deck_size = len(player.deck.discard_pile) + len(player.deck.draw_pile)
        cards_drawn = 0
        treasures_drawn = 0

        while treasures_drawn < 2 and cards_drawn < deck_size:
            player.hand.draw_card()
            cards_drawn += 1
            card = player.hand.hand[-1]

            if card.card_type == 'Treasure':
                treasures_drawn += 1
            else:
                player.hand.hand.remove(card)
                player.deck.discard_pile.append(card)
