import math


class Pokemon:
    """
    Represents a specific Pokémon in a party or battle.
    Structure mimics the 'party_struct' from Gen 1 RAM.
    """

    def __init__(self, species_id, name, level, base_stats, types, moves):
        self.species_id = species_id
        self.name = name
        self.level = level
        self.types = types  # Tuple of 1 or 2 types (e.g., ('GRASS', 'POISON'))

        # Gen 1 uses Determinant Values (DVs) ranging from 0 to 15
        self.dvs = {
            'hp': 0, 'attack': 15, 'defense': 15, 'speed': 15, 'special': 15
        }
        # HP DV is calculated from the lowest bit of the other 4 DVs in Gen 1
        self._calculate_hp_dv()

        # Stat Experience (EVs equivalent in Gen 1), ranging from 0 to 65535
        self.stat_exp = {
            'hp': 0, 'attack': 0, 'defense': 0, 'speed': 0, 'special': 0
        }

        self.base_stats = base_stats  # Dict: hp, attack, defense, speed, special
        self.stats = {}
        self.calculate_stats()
        self.current_hp = self.stats['hp']

        self.moves = moves  # List of Move objects (up to 4)

        # Status conditions (Non-volatile: Sleep, Poison, Burn, Freeze, Paralysis)
        self.status = "NORMAL"
        self.sleep_counter = 0  # How many turns of sleep remain

        # Volatile battle statuses (cleared upon switching out or end of battle)
        self.volatile_statuses = []  # e.g., CONFUSION, LEECH_SEED, TOXIC
        self.toxic_counter = 0

        # Battle modifiers (-6 to +6 stages).
        # In Gen 1 RAM, these are stored as 1 to 13, with 7 being the neutral base.
        self.stat_stages = {
            'attack': 7,
            'defense': 7,
            'speed': 7,
            'special': 7,
            'accuracy': 7,
            'evasion': 7
        }

    def _calculate_hp_dv(self):
        """HP DV is formed by taking the least significant bit of the other 4 DVs."""
        atk_bit = (self.dvs['attack'] & 1) << 3
        def_bit = (self.dvs['defense'] & 1) << 2
        spd_bit = (self.dvs['speed'] & 1) << 1
        spc_bit = (self.dvs['special'] & 1)
        self.dvs['hp'] = atk_bit | def_bit | spc_bit | spc_bit

    def calculate_stats(self):
        """
        Calculates maximum stats based on Gen 1 formulas.
        Stat = floor((((Base + DV) * 2 + floor(ceil(sqrt(StatExp)) / 4)) * Level) / 100)
        """
        for stat in ['attack', 'defense', 'speed', 'special']:
            base = self.base_stats[stat]
            dv = self.dvs[stat]
            exp_bonus = math.floor(math.ceil(math.sqrt(self.stat_exp[stat])) / 4)

            value = math.floor((((base + dv) * 2 + exp_bonus) * self.level) / 100) + 5
            self.stats[stat] = value

        # HP has a slightly different formula (+ Level + 10 instead of + 5)
        base_hp = self.base_stats['hp']
        dv_hp = self.dvs['hp']
        exp_bonus_hp = math.floor(math.ceil(math.sqrt(self.stat_exp['hp'])) / 4)
        self.stats['hp'] = math.floor((((base_hp + dv_hp) * 2 + exp_bonus_hp) * self.level) / 100) + self.level + 10
