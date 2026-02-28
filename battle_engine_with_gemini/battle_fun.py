import sys
import math
import random


def get_type_effectiveness(move_type, defender_types, type_chart):
    """Calcule le multiplicateur de type."""
    multiplier = 1.0
    if move_type in type_chart:
        for def_type in defender_types:
            if def_type in type_chart[move_type]:
                multiplier *= type_chart[move_type][def_type]
    return multiplier


def calculate_damage(attacker, defender, move, physical_types, type_chart):
    """
    Formule de dégâts fidèle à la Génération 1.
    """
    if move.power == 0:
        return 0, False, 1.0

    # 1. Vérifier si l'attaque est Physique ou Spéciale selon le type
    is_physical = move.type in physical_types

    atk_stat = attacker.attack if is_physical else attacker.special
    def_stat = defender.defense if is_physical else defender.special

    # 2. Coup Critique (Basé sur la vitesse de base dans la Gen 1)
    # Taux de critique Gen 1 : (Vitesse de base / 2) / 256
    crit_chance = (attacker.base_speed / 2.0) / 256.0
    is_crit = random.random() < crit_chance

    # Dans la Gen 1, le niveau est doublé lors d'un coup critique dans la formule
    level_calc = attacker.level * 2 if is_crit else attacker.level

    # 3. Calcul de base
    # Formule Gen 1: Damage = ((((2 * Level / 5) + 2) * Power * A / D) / 50) + 2
    base_damage = math.floor(math.floor(math.floor(2 * level_calc / 5 + 2) * move.power * atk_stat / def_stat) / 50) + 2

    # 4. STAB (Same Type Attack Bonus)
    if move.type in attacker.types:
        base_damage = math.floor(base_damage * 1.5)

    # 5. Efficacité des Types
    type_modifier = get_type_effectiveness(move.type, defender.types, type_chart)
    base_damage = math.floor(base_damage * type_modifier)

    # 6. Random (Nombre entre 217 et 255 dans Gen 1)
    if base_damage > 0:
        random_factor = random.randint(217, 255)
        base_damage = math.floor((base_damage * random_factor) / 255)

    return max(1, base_damage), is_crit, type_modifier


def check_accuracy(move):
    """
    Reproduit le bug de précision de la Gen 1 (1 chance sur 256 de rater
    même avec 100% de précision).
    """
    # Génère un nombre entre 0 et 255
    rand = random.randint(0, 255)
    # L'attaque touche si rand est strictement inférieur à la précision
    # Précision convertie sur une base 255 (ex: 100% = 255)
    acc_255 = int((move.accuracy / 100.0) * 255)
    return rand < acc_255
