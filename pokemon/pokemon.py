import random
import math
from pokemon.move import Move


def get_moves(species, level, move_database):
    moves = []
    for move in species.learnset:
        move_level, move_id = move['level'], move['move_id']
        if move_level <= level and len(moves) < 4:
            new_move = Move(move_database[move_id])
            moves.append(new_move)
    return moves


class Pokemon:
    def __init__(self, species, level, move_database, nickname=None):
        self.species = species  # Référence à l'objet Species
        self.level = level
        self.nickname = nickname if nickname else species.name

        # 1. Individual Values (Générés aléatoirement de 0 à 31)
        self.ivs = {
            "hp": random.randint(0, 31),
            "attack": random.randint(0, 31),
            "defense": random.randint(0, 31),
            "sp_atk": random.randint(0, 31),
            "sp_def": random.randint(0, 31),
            "speed": random.randint(0, 31)
        }

        # 2. Effort Values (Initialisés à 0)
        self.evs = {"hp": 0, "attack": 0, "defense": 0, "sp_atk": 0, "sp_def": 0, "speed": 0}

        # 3. Calcul des statistiques réelles
        self.stats = species.base_stats.copy()
        # self.calculate_stats()

        # 4. État actuel
        self.current_hp = self.stats["hp"]
        self.experience = 0  # À calculer selon la courbe de progression
        self.status_condition = None  # ex: "Paralyzed", "Poisoned"

        # 5. Moves (Une liste de 4 objets Move maximum)
        self.moves = get_moves(self.species, self.level, move_database)  # À remplir via une méthode de sélection du learnset


    def calculate_stats(self):
        # Calcul spécial pour les HP
        base_hp = self.species.base_stats["hp"]
        self.stats["hp"] = math.floor(
            ((2 * base_hp + self.ivs["hp"] + (self.evs["hp"] // 4)) * self.level / 100)
            + self.level + 10
        )

        # Calcul pour les autres statistiques
        for stat in ["attack", "defense", "sp_atk", "sp_def", "speed"]:
            base = self.species.base_stats[stat]
            self.stats[stat] = math.floor(
                ((2 * base + self.ivs[stat] + (self.evs[stat] // 4)) * self.level / 100)
                + 5
            )
            # Note: On pourrait ajouter ici le multiplicateur de "Nature" (* 1.1 ou * 0.9)

    def learn_move(self, move_id, move_database):
        if len(self.moves) < 4 and move_id in move_database:
            # On récupère le template et on en fait une copie unique
            data = move_database[move_id]
            new_move = Move(data)
            self.moves.append(new_move)

