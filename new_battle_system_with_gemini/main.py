import pygame
import sys
import math
from new_battle_system_with_gemini.pokemon import Pokemon
from new_battle_system_with_gemini.move import Move
from new_battle_system_with_gemini.item import Item
from new_battle_system_with_gemini.trainer import Trainer
from new_battle_system_with_gemini.battle_engine import BattleEngine

#
# # --- Classes de base (Modèles de données) ---
#
# class Move:
#     """
#     Représente une attaque (dégâts ou statut) dans la Génération 1.
#     """
#
#     def __init__(self, move_id, name, effect, power, move_type, accuracy, max_pp):
#         self.move_id = move_id
#         self.name = name
#         self.effect = effect  # ID de l'effet secondaire (ex: empoisonnement)
#         self.power = power
#         self.move_type = move_type  # ex: 'NORMAL', 'FIRE'
#         self.accuracy = accuracy  # 0 à 255 (255 = ~99.6% de précision)
#         self.max_pp = max_pp
#         self.current_pp = max_pp
#
#
# class Item:
#     """
#     Représente un objet dans le jeu.
#     """
#
#     def __init__(self, item_id, name, price=0, effect=None):
#         self.item_id = item_id
#         self.name = name
#         self.price = price
#         self.effect = effect
#
#
# class Pokemon:
#     """
#     Représente un Pokémon spécifique dans l'équipe ou en combat.
#     """
#
#     def __init__(self, species_id, name, level, base_stats, types, moves):
#         self.species_id = species_id
#         self.name = name
#         self.level = level
#         self.types = types  # Tuple d'un ou deux types
#
#         # Valeurs Déterminantes (DVs), de 0 à 15
#         self.dvs = {
#             'hp': 0, 'attack': 15, 'defense': 15, 'speed': 15, 'special': 15
#         }
#         self._calculate_hp_dv()
#
#         # Expérience de Stat (Stat Exp), de 0 à 65535
#         self.stat_exp = {
#             'hp': 0, 'attack': 0, 'defense': 0, 'speed': 0, 'special': 0
#         }
#
#         self.base_stats = base_stats
#         self.stats = {}
#         self.calculate_stats()
#         self.current_hp = self.stats['hp']
#
#         self.moves = moves  # Liste d'objets Move (maximum 4)
#
#         # Altérations d'état majeures
#         self.status = "NORMAL"
#         self.sleep_counter = 0
#
#         # Altérations d'état mineures/volatiles
#         self.volatile_statuses = []
#         self.toxic_counter = 0
#
#         # Modificateurs de statistiques en combat (1 à 13, base = 7)
#         self.stat_stages = {
#             'attack': 7, 'defense': 7, 'speed': 7,
#             'special': 7, 'accuracy': 7, 'evasion': 7
#         }
#
#     def _calculate_hp_dv(self):
#         """Calcule le DV des PV basé sur le bit de poids faible des autres DVs."""
#         atk_bit = (self.dvs['attack'] & 1) << 3
#         def_bit = (self.dvs['defense'] & 1) << 2
#         spd_bit = (self.dvs['speed'] & 1) << 1
#         spc_bit = (self.dvs['special'] & 1)
#         self.dvs['hp'] = atk_bit | def_bit | spc_bit | spc_bit
#
#     def calculate_stats(self):
#         """Calcule les statistiques maximales basées sur les formules de la Gen 1."""
#         for stat in ['attack', 'defense', 'speed', 'special']:
#             base = self.base_stats[stat]
#             dv = self.dvs[stat]
#             exp_bonus = math.floor(math.ceil(math.sqrt(self.stat_exp[stat])) / 4)
#             value = math.floor((((base + dv) * 2 + exp_bonus) * self.level) / 100) + 5
#             self.stats[stat] = value
#
#         base_hp = self.base_stats['hp']
#         dv_hp = self.dvs['hp']
#         exp_bonus_hp = math.floor(math.ceil(math.sqrt(self.stat_exp['hp'])) / 4)
#         self.stats['hp'] = math.floor((((base_hp + dv_hp) * 2 + exp_bonus_hp) * self.level) / 100) + self.level + 10
#
#
# class Trainer:
#     """
#     Représente un dresseur (Le joueur ou une IA).
#     """
#
#     def __init__(self, name, is_player=False):
#         self.name = name
#         self.is_player = is_player
#         self.party = []
#         self.inventory = {}
#
#     def add_pokemon(self, pokemon):
#         if len(self.party) < 6:
#             self.party.append(pokemon)
#             return True
#         return False
#
#     def add_item(self, item, quantity=1):
#         if item.item_id in self.inventory:
#             self.inventory[item.item_id]['quantity'] += quantity
#         else:
#             self.inventory[item.item_id] = {'item': item, 'quantity': quantity}





# --- Fonction Principale ---

def main():
    # Initialisation de Pygame
    pygame.init()

    # Résolution originale de la Game Boy : 160x144.
    # On la multiplie par 4 pour une fenêtre moderne lisible.
    screen_width = 160 * 4
    screen_height = 144 * 4
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Pokémon Rouge/Bleu - Moteur de Combat")

    clock = pygame.time.Clock()

    # --- Initialisation des données de test ---

    # Création d'objets
    potion = Item(item_id="POTION", name="Potion", price=300, effect="HEAL_20")

    # Création des attaques
    tackle = Move(move_id="TACKLE", name="Charge", effect="NORMAL_HIT", power=35, move_type="NORMAL", accuracy=255,
                  max_pp=35)
    growl = Move(move_id="GROWL", name="Rugissement", effect="ATTACK_DOWN_1", power=0, move_type="NORMAL", accuracy=255,
                 max_pp=40)
    scratch = Move(move_id="SCRATCH", name="Griffe", effect="NORMAL_HIT", power=40, move_type="NORMAL", accuracy=255,
                   max_pp=35)

    # Création du Dresseur Joueur et de son équipe
    player_trainer = Trainer(name="RED", is_player=True)
    player_trainer.add_item(potion, quantity=3)

    bulbasaur_base_stats = {'hp': 45, 'attack': 49, 'defense': 49, 'speed': 45, 'special': 65}
    player_pokemon = Pokemon(
        species_id="BULBASAUR",
        name="BULBIZARRE",
        level=5,
        base_stats=bulbasaur_base_stats,
        types=("GRASS", "POISON"),
        moves=[tackle, growl]
    )
    player_trainer.add_pokemon(player_pokemon)

    # Création du Pokémon Ennemi Sauvage
    charmander_base_stats = {'hp': 39, 'attack': 52, 'defense': 43, 'speed': 65, 'special': 50}
    enemy_pokemon = Pokemon(
        species_id="CHARMANDER",
        name="SALAMECHE",
        level=5,
        base_stats=charmander_base_stats,
        types=("FIRE", None),
        moves=[scratch, growl]
    )

    # Initialisation du moteur de combat
    battle_engine = BattleEngine(screen, player_trainer, enemy_pokemon)

    # Boucle Principale
    running = True
    while running:
        # Récupération de tous les événements Pygame
        events = pygame.event.get()

        for event in events:
            if event.type == pygame.QUIT:
                running = False

        # 1. Mise à jour de la logique
        battle_engine.update(events)

        # 2. Affichage à l'écran
        battle_engine.display()

        # 3. Rafraîchissement de l'écran
        pygame.display.flip()

        # 4. Limite à 60 images par seconde (GameBoy tournait à ~59.7 fps)
        clock.tick(60)

    # Quitter proprement
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()