# useful guide for the rules
#https://boardgamegeek.com/wiki/page/Complete_and_All-Encompassing_Dominion_FAQ
from player import Player
from cards import *


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

        self.init_supply_piles()

    def init_supply_piles(self, action_cards=None):
        '''Initialize the supply piles.

        Action Cards: 10 different actions, 10 cards each
        Victory Cards: 12 Estates, 12 Duchies, 12 Provinces
        Treasure Cards: 60 Coppers, 40 Silvers, 30 Golds

        Args:
            action_cards (tuple or list): Action cards which will be included
                in this game. Random cards will be used if not specified.
        '''
        self.supply_piles = SupplyPiles(n_players=self.n_players)
        self.supply_piles.display_supply_pile_count()


class SupplyPiles:
    def __init__(self, n_players):
        self.supply_piles = {'Copper': [Copper()] * (60 - 7 * n_players),
                             'Silver': [Silver()] * 40,
                             'Gold': [Gold()] * 30,
                             'Estate': [Estate()] * 12,
                             'Duchy': [Duchy()] * 12,
                             'Province': [Province()] * 12,
                             'Curse': [Curse()] * (10 + 10 * (n_players - 2))}

    def display_supply_pile_count(self):
        for key, value in self.supply_piles.iteritems():
            print(key + ': ' + str(len(value)))
