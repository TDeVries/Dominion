from cards import *
import random


class Player:
    def __init__(self, player_id):
        '''Initialize a new player, with identifier and starting deck

        Args:
            player_id (int): A numerical identifier.
        '''
        self.player_id = player_id
        self.deck = Deck()
        self.hand = Hand(self.deck)

        self.hand.draw_hand()

    def display_deck(self):
        '''Print out the name of each card in the deck, in order.'''
        deck = self.deck.draw_pile + self.deck.discard_pile + self.hand.hand
        cards = []
        for card in deck:
            cards.append(card.name)
        print('Deck: ' + str(cards))

    def display_draw_pile(self):
        '''Print out the name of each card in the draw pile, in order.'''
        cards = []
        for card in self.deck.draw_pile:
            cards.append(card.name)
        print('Draw Pile: ' + str(cards))

    def display_discard_pile(self):
        '''Print out the name of each card in the discard pile, in order.'''
        cards = []
        for card in self.deck.discard_pile:
            cards.append(card.name)
        print('Discard Pile: ' + str(cards))

    def display_hand(self):
        '''Print out the name of each card in the hand, in order.'''
        cards = []
        for card in self.hand.hand:
            cards.append(card.name)
        print('Hand: ' + str(cards))


class Deck:
    def __init__(self):
        '''Initialize deck with 7 Coppers and 3 Estates, then shuffle.
        Cards start in the draw pile.'''
        self.draw_pile = [Copper()] * 7 + [Estate()] * 3
        self.discard_pile = []

        self.shuffle_deck()

    def shuffle_deck(self):
        '''Transfer the discard pile into the draw pile, then shuffle'''
        self.draw_pile += self.discard_pile
        self.discard_pile = []
        random.shuffle(self.draw_pile)


class Hand:
    def __init__(self, deck):
        '''Initializes a new hand, which contains the cards that
         the player can play each turn.

        Args:
            deck (Deck instance): The deck that cards will be drawn from,
            and discarded to.
        '''
        self.hand = []
        self.deck = deck

    def draw_card(self):
        '''Move a single card from the draw pile to the player's hand.
        Reshuffle the deck if the draw pile has run out. If no more cards
        available, do nothing.'''

        if len(self.deck.draw_pile) == 0:
            self.deck.shuffle_deck()

        if len(self.deck.draw_pile) > 0:
            next_card = self.deck.draw_pile.pop(0)
            self.hand.append(next_card)

    def draw_hand(self):
        '''Move 5 cards from the draw pile to the player's hand'''
        assert len(self.hand) == 0, 'Hand must be empty before drawing a new one'

        for i in range(5):
            self.draw_card()

    def discard_hand(self):
        '''Move cards from the hand into discard pile'''
        self.deck.discard_pile += self.hand
        self.hand = []
