class Pokemon:
    def __init__(self, species, level=1, exp=0, stats=None, moves=None, name=None):
        self.species = species
        self.name = name if name is not None else species
        self.level = level
        self.current_exp = exp
        self.stats = {"hp":stats['hp'], "max_hp":stats['hp'], "attack":stats['attack'],"defense":stats['defense'],
                      "special":stats['special'], "speed":stats['speed']} if stats is not None \
            else {"hp":100, "max_hp":100, "attack":10, "defense":10, "special":10, "speed":10}
        self.moves = moves.copy() if moves is not None \
            else {0:None, 1:None, 2:None, 3:None}
