import random

class Move:
    def __init__(self, names, move_type, category, power, accuracy, pp, priority):
        self.name = names['fr']
        self.names = names
        self.move_type = move_type
        self.category = category
        self.power = power
        self.accuracy = accuracy
        self.current_pp = random.randint(0, pp)
        self.max_pp = pp
        self.priority = priority
        self.effects = []