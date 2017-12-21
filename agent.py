import random


class Agent(object):
    def __init__(self):
        '''Base agent class. Agents are used to make decisions for each
        player in the game. Custom agents can be created by inheriting
        this class and modifying the decision functions.'''
        pass

    def _get_game_state(self):
        pass

    def select_action(self, valid_actions):
        pass

    def select_buy(self, valid_buys):
        pass


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
