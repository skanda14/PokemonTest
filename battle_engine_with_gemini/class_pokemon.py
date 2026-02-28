class Pokemon:
    def __init__(self, name, level, types, hp, attack, defense, special, speed, moves):
        self.name = name
        self.level = level
        self.types = types
        self.max_hp = hp
        self.hp = hp

        # Statistiques de la Gen 1 (Spécial est unique)
        self.attack = attack
        self.defense = defense
        self.special = special
        self.speed = speed
        self.base_speed = speed  # Utilisé pour les coups critiques

        self.moves = moves
