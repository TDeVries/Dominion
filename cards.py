class Copper:
    def __init__(self):
        self.name = 'Copper'
        self.cost = 0
        self.card_type = 'Treasure'
        self.card_subtype = None
        self.coins = 1


class Silver:
    def __init__(self):
        self.name = 'Silver'
        self.cost = 3
        self.card_type = 'Treasure'
        self.card_subtype = None
        self.coins = 2


class Gold:
    def __init__(self):
        self.name = 'Gold'
        self.cost = 6
        self.card_type = 'Treasure'
        self.card_subtype = None
        self.coins = 3


class Estate:
    def __init__(self):
        self.name = 'Estate'
        self.cost = 2
        self.card_type = 'Victory'
        self.card_subtype = None
        self.victory_points = 1


class Duchy:
    def __init__(self):
        self.name = 'Duchy'
        self.cost = 5
        self.card_type = 'Victory'
        self.card_subtype = None
        self.victory_points = 3


class Province:
    def __init__(self):
        self.name = 'Province'
        self.cost = 8
        self.card_type = 'Victory'
        self.card_subtype = None
        self.victory_points = 6


class Curse:
    def __init__(self):
        self.name = 'Curse'
        self.cost = 0
        self.card_type = 'Curse'
        self.card_subtype = None
        self.victory_points = -1


class Cellar:
    def __init__(self):
        self.name = 'Cellar'
        self.cost = 2
        self.card_type = 'Action'
        self.card_subtype = None


class Chapel:
    def __init__(self):
        self.name = 'Chapel'
        self.cost = 2
        self.card_type = 'Action'
        self.card_subtype = None


class Moat:
    def __init__(self):
        self.name = 'Moat'
        self.cost = 2
        self.card_type = 'Action'
        self.card_subtype = 'Reaction'


class Chancellor:
    def __init__(self):
        self.name = 'Chancellor'
        self.cost = 3
        self.card_type = 'Action'
        self.card_subtype = None


class Village:
    def __init__(self):
        self.name = 'Village'
        self.cost = 3
        self.card_type = 'Action'
        self.card_subtype = None


class Woodcutter:
    def __init__(self):
        self.name = 'Woodcutter'
        self.cost = 3
        self.card_type = 'Action'
        self.card_subtype = None


class Workshop:
    def __init__(self):
        self.name = 'Workshop'
        self.cost = 3
        self.card_type = 'Action'
        self.card_subtype = None


class Bureaucrat:
    def __init__(self):
        self.name = 'Bureaucrat'
        self.cost = 4
        self.card_type = 'Action'
        self.card_subtype = 'Attack'


class Feast:
    def __init__(self):
        self.name = 'Feast'
        self.cost = 4
        self.card_type = 'Action'
        self.card_subtype = None


class Gardens:
    def __init__(self):
        self.name = 'Gardens'
        self.cost = 4
        self.card_type = 'Victory'
        self.card_subtype = None


class Militia:
    def __init__(self):
        self.name = 'Militia'
        self.cost = 4
        self.card_type = 'Action'
        self.card_subtype = 'Attack'


class Moneylender:
    def __init__(self):
        self.name = 'Moneylender'
        self.cost = 4
        self.card_type = 'Action'
        self.card_subtype = None


class Remodel:
    def __init__(self):
        self.name = 'Remodel'
        self.cost = 4
        self.card_type = 'Action'
        self.card_subtype = None


class Smithy:
    def __init__(self):
        self.name = 'Smithy'
        self.cost = 4
        self.card_type = 'Action'
        self.card_subtype = None


class Spy:
    def __init__(self):
        self.name = 'Spy'
        self.cost = 4
        self.card_type = 'Action'
        self.card_subtype = 'Attack'


class Thief:
    def __init__(self):
        self.name = 'Thief'
        self.cost = 4
        self.card_type = 'Action'
        self.card_subtype = 'Attack'


class ThroneRoom:
    def __init__(self):
        self.name = 'Throne Room'
        self.cost = 4
        self.card_type = 'Action'
        self.card_subtype = None


class CouncilRoom:
    def __init__(self):
        self.name = 'Council Room'
        self.cost = 5
        self.card_type = 'Action'
        self.card_subtype = None


class Festival:
    def __init__(self):
        self.name = 'Festival'
        self.cost = 5
        self.card_type = 'Action'
        self.card_subtype = None


class Laboratory:
    def __init__(self):
        self.name = 'Laboratory'
        self.cost = 5
        self.card_type = 'Action'
        self.card_subtype = None


class Library:
    def __init__(self):
        self.name = 'Library'
        self.cost = 5
        self.card_type = 'Action'
        self.card_subtype = None


class Market:
    def __init__(self):
        self.name = 'Market'
        self.cost = 5
        self.card_type = 'Action'
        self.card_subtype = None


class Mine:
    def __init__(self):
        self.name = 'Mine'
        self.cost = 5
        self.card_type = 'Action'
        self.card_subtype = None


class Witch:
    def __init__(self):
        self.name = 'Witch'
        self.cost = 5
        self.card_type = 'Action'
        self.card_subtype = 'Attack'


class Adventurer:
    def __init__(self):
        self.name = 'Adventurer'
        self.cost = 6
        self.card_type = 'Action'
        self.card_subtype = None