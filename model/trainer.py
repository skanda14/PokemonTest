from model.bag import Bag
from model.party import Party
import random


class Trainer:
    def __init__(self, name=None, party=None, bag=None):
        self.name = name if name is not None else 'Generic Trainer'
        self.id = random.randint(0,65535)
        self.party = party if party is not None else Party()
        self.bag = bag if bag is not None else Bag()
