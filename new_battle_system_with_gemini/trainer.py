class Trainer:
    """Represents a trainer (Player or AI)."""
    def __init__(self, name, is_player=False):
        self.name = name
        self.is_player = is_player
        self.party = []  # List of Pokemon objects, max 6
        self.inventory = {}  # Dictionary mapping Item ID to quantity

    def add_pokemon(self, pokemon):
        if len(self.party) < 6:
            self.party.append(pokemon)
            return True
        return False

    def add_item(self, item_id, quantity=1):
        if item_id in self.inventory:
            self.inventory[item_id] += quantity
        else:
            self.inventory[item_id] = quantity
