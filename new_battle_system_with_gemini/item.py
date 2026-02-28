class Item:
    """
    Represents an item in the game.
    """

    def __init__(self, item_id, name, price=0, effect=None):
        self.item_id = item_id
        self.name = name
        self.price = price
        self.effect = effect
