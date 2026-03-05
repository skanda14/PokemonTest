import random
import pygame


class Pokemon:
    def __init__(self, species, index, types, level=1, exp=0, stats=None, moves=None, name=None, trainer=None, sprite_front_path=None, sprite_back_path=None):
        self.species = species
        self.index = index
        self.trainer = trainer
        self.types = types
        self.name = name if name is not None else species
        self.level = level
        self.current_exp = random.randint(1,9999)
        self.remaining_exp = random.randint(1,999)
        self.stats = {"hp":random.randint(0, stats['hp']), "max_hp":stats['hp'], "attack":stats['attack'],"defense":stats['defense'],
                      "special":stats['special'], "speed":stats['speed']} if stats is not None \
            else {"hp":100, "max_hp":100, "attack":10, "defense":10, "special":10, "speed":10}
        self.moves = moves.copy() if moves is not None \
            else {0:None, 1:None, 2:None, 3:None}
        self.sprites = {
            'front_default': pygame.image.load(sprite_front_path) if sprite_front_path is not None else None,
            'back_default': pygame.image.load(sprite_back_path) if sprite_back_path is not None else None,
        }

