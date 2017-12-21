# useful guide for the rules
#https://boardgamegeek.com/wiki/page/Complete_and_All-Encompassing_Dominion_FAQ
import random
import six

from player import Player
from cards import *
from agent import RandomAgent


class Game(object):
    def __init__(self, n_players, agents=None, card_set='random', verbose=False):
        '''Initialize a new game, with n players.

        Args:
            n_players (int): Number of players in this game. Must be
                between 2 and 4.
            agents (dict): Contains the agents who will play in this
            game. The dict key is used as the player_id. If n_players is
            greater than the number of agents provided, RandomAgents
            will be used for the remaining players.
            card_set (str): Indicates which pre-specified card set to
            use. Options are 'random' and 'base'. Default: 'random'.
            verbose (bool): Indicates whether to print game state as
            actions take place. Default: 'False'.
        '''
        if agents is None:
            agents = {}

        assert n_players >= 2 and n_players <= 4, "n_players must be between 2 and 4"
        assert len(agents) <= n_players, "must not have more agents than n_players"
        self.n_players = n_players
        self.card_set = card_set
        self.verbose = verbose

        players = []
        for player_id, agent in six.iteritems(agents):
            players.append(Player(player_id=player_id, agent=agent))

        for n in range(len(agents), self.n_players):
            players.append(Player(player_id='Player ' + str(n), agent=RandomAgent()))
        self.players = players

        self.supply_piles = SupplyPiles(n_players=self.n_players,
                                        card_set=self.card_set)
        if self.verbose:
            self.supply_piles.display_supply_pile_count()

    def play_game(self):
        '''Loop through players' turns until the game has finished.
        Count victory points to determine a winner.

        Return:
            victory_point_count (dict): Contains score for each player
        '''
        while not self.check_game_over():
            for player in self.players:
                if self.verbose:
                    print(str(player.player_id) + "'s Turn")
                self.take_turn(player)
                print("")
                if self.check_game_over():
                    break

        victory_point_count = {}
        for player in self.players:
            victory_points = self.count_victory_points(player)
            victory_point_count[str(player.player_id)] = victory_points
        if self.verbose:
            print(victory_point_count)
        return victory_point_count

    def reset_game(self):
        '''Begin a new game using the current settings.'''
        self.__init__(n_players=self.n_players, card_set=self.card_set,
                      verbose=self.verbose)

    def count_victory_points(self, player):
        '''Count the number of victory points in the given player's deck

        Args:
            player (instance): The player whose deck to count

        Return:
            victory_points (int): Number of victory points in the
            player's deck
        '''

        victory_points = 0
        deck = player.deck.draw_pile + player.deck.discard_pile + player.hand.hand
        for card in deck:
            if hasattr(card, 'victory_points'):
                victory_points += card.victory_points
        return victory_points

    def check_game_over(self):
        '''Check to see if any of the game end conditions have been met.
        The game ends whenever any three supply piles are empty, or when
        there are no Province cards left.

        Return (bool): Returns True if the game is over, False if the
            game is not over.
        '''
        n_empty_piles = 0

        for key, value in six.iteritems(self.supply_piles.supply_piles):
            if len(value) == 0:
                n_empty_piles += 1
                if key == 'Province':
                    return True
        if n_empty_piles >= 3:
            return True
        else:
            return False

    def take_turn(self, player):
        '''Player begins with one action and one buy. During the action
        phase they can play actions cards, and during the buy phase they
        can buy additional cards for their deck.

        Args:
            player (instance): The player whose turn it is
        '''
        turn_state = {'actions': 1, 'buys': 1, 'coins': 0}
        turn_state = self._action_phase(player, turn_state)
        turn_state = self._buy_phase(player, turn_state)

        player.hand.discard_hand()
        player.hand.draw_hand()

    def _buy_phase(self, player, turn_state):
        '''Buy cards from the supply piles until out of money, or the
        player decides to stop buying cards.

        Args:
            player (instance): The player who is playing the cards
            turn_state (dict): Current phase state

        Return:
            turn_state (dict): Updated phase state
        '''
        if self.verbose:
            print('Buy Phase')

        end_buy_phase = False

        while (turn_state['buys'] > 0) and not end_buy_phase:
            valid_buys = self._get_valid_buys(turn_state['coins'])

            if self.verbose:
                print('Turn state: ' + str(turn_state))
                print('Options: ' + str(valid_buys))

            selected_buy = player.agent.select_buy(valid_buys)

            if self.verbose:
                print('Selection: ' + str(selected_buy))

            if selected_buy == 'end_buy_phase':
                end_buy_phase = True
            else:
                turn_state = self._buy_card(player, selected_buy, turn_state)
        return turn_state

    def _buy_card(self, player, selected_buy, turn_state):
        '''Buy a card by moving it from the supply piles to the player's
        discard pile. The cost of the card is removed from the player's
        coin count.

        Args:
            player (instance): The player who is playing the card
            selected_buy (str): The card that is being purchased
            turn_state (dict): Current phase state

        Return:
            turn_state (dict): Updated phase state
        '''
        for key, value in six.iteritems(self.supply_piles.supply_piles):
            if len(value) > 0:
                card = value[0]
                if card.name == selected_buy:
                    turn_state['coins'] -= card.cost
                    turn_state['buys'] -= 1
                    self.supply_piles.supply_piles[key].remove(card)
                    player.deck.discard_pile.append(card)
        return turn_state

    def _get_valid_buys(self, coins):
        '''Find all supply piles which still have cards left, and which
        the player has enough coins to buy from. Not buying anything is
        also always an option.

        Args:
            coins (int): How much money the player has to spend.

        Return:
            valid_buys (list): Returns a list of cards which the player
            has enough money to buy.
        '''
        valid_buys = ['end_buy_phase']

        for key, value in six.iteritems(self.supply_piles.supply_piles):
            if len(value) > 0:
                card = value[0]
                if card.cost <= coins:
                    valid_buys.append(card.name)
        return valid_buys

    def _action_phase(self, player, turn_state):
        '''Plays actions cards from the player's hand until they run out,
        or until they decide to stop playing them. Counts the number of
        coins in the player's hand at the end.

        Args:
            player (instance): The player who is playing the cards
            turn_state (dict): Current phase state

        Return:
            turn_state (dict): Updated phase state
        '''

        if self.verbose:
            print('Action Phase')

        end_action_phase = False

        while (turn_state['actions'] > 0) and not end_action_phase:
            if self.verbose:
                print('Turn state: ' + str(turn_state))
                player.display_hand()

            valid_actions = self._get_valid_actions(player.hand.hand)

            if self.verbose:
                print('Options: ' + str(valid_actions))

            selected_action = player.agent.select_action(valid_actions)

            if self.verbose:
                print('Selection: ' + str(selected_action))

            if selected_action == 'end_action_phase':
                end_action_phase = True
            else:
                for card in player.hand.hand:
                    if card.name == selected_action:
                        turn_state = self._play_card(player, card, turn_state)

        turn_state['coins'] += self._count_coins(player.hand.hand)
        return turn_state

    def _count_coins(self, hand):
        '''Count value of Treasure cards in the player's hand

        Args:
            hand (instance): The player's hand

        Return:
            coin_count (int): The number of coins the player's
            Treasure cards are worth
        '''
        coin_count = 0
        for card in hand:
            if (card.card_type == 'Treasure'):
                coin_count += card.coins
        return coin_count

    def _play_card(self, player, card, turn_state):
        '''Play a card by triggering it's effects (draw cards, add
        actions, add buys, and add coins). Card is moved from the
        player's hand to the discard pile. Playing a card costs one
        action.

        Args:
            player (instance): The player who is playing the card
            card (instance): The card that is being played
            turn_state (dict): Current phase state

        Return:
            turn_state (dict): Updated phase state
        '''
        if hasattr(card, 'plus_cards'):
            for i in range(card.plus_cards):
                player.hand.draw_card()
        if hasattr(card, 'plus_actions'):
            turn_state['actions'] += card.plus_actions
        if hasattr(card, 'plus_buys'):
            turn_state['buys'] += card.plus_buys
        if hasattr(card, 'coins'):
            turn_state['coins'] += card.coins

        player.hand.hand.remove(card)
        player.deck.discard_pile.append(card)

        turn_state['actions'] -= 1
        return turn_state

    def _get_valid_actions(self, hand):
        '''Find all action cards in a player's hand. If duplicates of
        a card exist, only one is shown. Ending the action phase is also
        an option, which is always available.

        Args:
            hand (instance): A hand object, which contains the cards to
            be played

        Return:
            valid_action (list): Returns a list of action cards that the
            player can play this action phase.
        '''
        valid_actions = ['end_action_phase']
        for card in hand:
            if (card.card_type == 'Action') and (card.name not in valid_actions):
                valid_actions.append(card.name)
        return valid_actions


class SupplyPiles(object):
    def __init__(self, n_players, card_set='random'):
        '''Initialize the supply piles.

        Action Cards: 10 different actions, 10 cards each
        Victory Cards: 12 Estates, 12 Duchies, 12 Provinces
        Treasure Cards: 60 Coppers (minus 7 for each player), 40 Silvers, 30 Golds
        Curse Cards: 10 for 2 players, plus 10 for each extra player

        Args:
            n_players (int): Number of players in the game.
            card_set (str): Indicates which pre-specified card set to
            use. Options are 'random' and 'base'. Default: 'random'.
        '''
        self.card_set = card_set

        if n_players == 2:
            n_victory_cards = 8
        else:
            n_victory_cards = 12

        self.supply_piles = {'Copper': [Copper()] * (60 - 7 * n_players),
                             'Silver': [Silver()] * 40,
                             'Gold': [Gold()] * 30,
                             'Estate': [Estate()] * n_victory_cards,
                             'Duchy': [Duchy()] * n_victory_cards,
                             'Province': [Province()] * n_victory_cards,
                             'Curse': [Curse()] * (10 + 10 * (n_players - 2))}

        if self.card_set == 'random':
            card_options = [Cellar(), Chapel(), Moat(), Chancellor(), Village(),
                            Woodcutter(), Workshop(), Bureaucrat(), Feast(),
                            Gardens(), Militia(), Moneylender(), Remodel(),
                            Smithy(), Spy(), Thief(), ThroneRoom(), CouncilRoom(),
                            Festival(), Laboratory(), Library(), Market(), Mine(),
                            Witch(), Adventurer()]
            random.shuffle(card_options)
            card_options = card_options[:10]

        elif self.card_set == 'base':
            card_options = [Cellar(), Moat(), Village(), Woodcutter(),
                            Workshop(), Militia(), Remodel(), Smithy(),
                            Market(), Mine()]

        for card in card_options:
            if card.card_type == 'Victory':
                self.supply_piles[card.name] = [card] * n_victory_cards
            else:
                self.supply_piles[card.name] = [card] * 10

    def display_supply_pile_count(self):
        '''Print out the number of cards remaining in each supply pile.'''
        base_cards = ['Copper', 'Silver', 'Gold', 'Estate', 'Duchy',
                      'Province', 'Curse']

        for key in base_cards:
            print(key + ': ' + str(len(self.supply_piles[key])))

        for key, value in six.iteritems(self.supply_piles):
            if key not in base_cards:
                print(key + ': ' + str(len(value)))
        print('')
