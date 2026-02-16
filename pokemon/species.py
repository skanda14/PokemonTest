

class Species:
    def __init__(self, data):
        self.dex_number = data["id"]    # ID unique (ex: 25)
        self.name = data["name"]                 # Nom de l'espèce (ex: "Pikachu")
        self.types = data["types"]                # Liste (ex: ["Electric"])
        # Base stats: dict pour un accès clair (ex: self.base_stats["hp"])
        self.base_stats = data["base_stats"]      # {"hp": 35, "attack": 55, "defense": 40, ...}
        self.growth_rate = data["growth_rate"]    # Chaîne (ex: "medium-fast")
        self.learnset = data["learnset"]          # Dictionnaire {level: move_id}
        self.catch_rate = data["catch_rate"]
        self.evolution_data = data["evolution"] # Infos sur l'évolution (niveau, objet, etc.)
