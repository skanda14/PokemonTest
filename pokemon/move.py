

class Move:
    def __init__(self, data):
        self.name = data["name"]  # ex: "Thunderbolt"
        self.power = data["power"]  # Puissance (ex: 90)
        self.accuracy = data["accuracy"]  # Précision (ex: 100)
        self.type = data["type"]  # Type (Electric, Water...)
        self.category = data["category"]  # Physical, Special, or Status
        self.priority = data["priority"] # 0, +1, +2 etc.
        self.max_pp = data["pp"]  # Points de Pouvoir
        self.current_pp = data["pp"] # Chaque instance aura ses propres PPs
    #
    # def get_copy(self):
    #     # Retourne une nouvelle instance identique
    #     return Move(self.name, self.power, self.accuracy,
    #                 self.move_type, self.category, self.max_pp)
