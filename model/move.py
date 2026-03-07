import random

class Move:
    def __init__(self, names, move_type, category, power, accuracy, pp, priority):
        self.name = names['fr']
        self.names = names
        self.move_type = move_type
        self.category = category
        self.power = power
        self.accuracy = accuracy
        self.max_pp = pp
        self.current_pp = random.randint(0, self.max_pp)
        self.priority = priority
        self.effects = []

    def modify_current_pp(self, n=-1):
        self.current_pp = min(self.max_pp, max(0, self.current_pp + n))