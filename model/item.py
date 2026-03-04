class Item:
    def __init__(self, name=None, id=None):
        self.name = name if name is not None else 'Generic Item'
        self.id = id if id is not None else 0