# useful guide for the rules
#https://boardgamegeek.com/wiki/page/Complete_and_All-Encompassing_Dominion_FAQ
from player import Player
from cards import *
from random import shuffle


class Game:
    def __init__(self, n_players):
        '''Initialize a new game, with n players.

        Args:
            n_players (int): Number of players in this game. Must be
                between 2 and 4.
        '''
        assert n_players >= 2 and n_players <= 4, "n_players must be between 2 and 4"
        self.n_players = n_players

        players = []
        for n in range(self.n_players):
            players.append(Player(player_id=n))
        self.players = players

        self.init_supply_piles(card_set='random')

    def init_supply_piles(self, card_set='random'):
        '''Initialize the supply piles.

        Args:
            card_set (str): Indicates which pre-specified card set to 
            use. Options are 'random' and 'base'. Default: 'random'.
        '''
        self.supply_piles = SupplyPiles(n_players=self.n_players,
                                        card_set=card_set)
        self.supply_piles.display_supply_pile_count()


class SupplyPiles:
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
        self.supply_piles = {'Copper': [Copper()] * (60 - 7 * n_players),
                             'Silver': [Silver()] * 40,
                             'Gold': [Gold()] * 30,
                             'Estate': [Estate()] * 12,
                             'Duchy': [Duchy()] * 12,
                             'Province': [Province()] * 12,
                             'Curse': [Curse()] * (10 + 10 * (n_players - 2))}

        if self.card_set == 'random':
            card_options = [Cellar(), Chapel(), Moat(), Chancellor(), Village(),
                            Woodcutter(), Workshop(), Bureaucrat(), Feast(),
                            Gardens(), Militia(), Moneylender(), Remodel(),
                            Smithy(), Spy(), Thief(), ThroneRoom(), CouncilRoom(),
                            Festival(), Laboratory(), Library(), Market(), Mine(),
                            Witch(), Adventurer()]
            shuffle(card_options)
            card_options = card_options[:10]

        elif self.card_set == 'base':
            card_options = [Cellar(), Moat(), Village(), Woodcutter(),
                            Workshop(), Militia(), Remodel(), Smithy(),
                            Market(), Mine()]

        for card in card_options:
            if card.card_type == 'Victory':
                self.supply_piles[card.name] = [card] * 12
            else:
                self.supply_piles[card.name] = [card] * 10

    def display_supply_pile_count(self):
        '''Print out the number of cards remaining in each supply pile.'''
        base_cards = ['Copper', 'Silver', 'Gold', 'Estate', 'Duchy',
                       'Province', 'Curse']

        for key in base_cards:
            print(key + ': ' + str(len(self.supply_piles[key])))

        for key, value in self.supply_piles.iteritems():
            if key not in base_cards:
                print(key + ': ' + str(len(value)))
        print('')
