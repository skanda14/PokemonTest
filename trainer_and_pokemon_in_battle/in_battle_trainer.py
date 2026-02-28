import pygame
from utils.file_IO import get_dict_from_json_path
import random


def get_species_dict_from_json_by_index(index):
    name_key = get_dict_from_json_path("assets/json/generation/generation-1.json")['pokemon_species'][str(index)]
    pokemon_dict = get_dict_from_json_path("assets/json/generation/gen_1_pokemon_species.json")[name_key]
    return pokemon_dict


def get_species_dict_from_json_by_name(key):
    pokemon_dict = get_dict_from_json_path("assets/json/generation/gen_1_pokemon_species.json")[key]
    return pokemon_dict


def get_sprite_path(version, index, category):
    index_string = str(index)
    while len(index_string) < 3:
        index_string = "0"+index_string
    return f"assets/sprites/pokemon/{version}/{index_string}/{category}.png"


def get_all_sprites_for_pokemon_instance(in_battle_pokemon):
    index = in_battle_pokemon.data_dict['id']
    for category in ['front_default', 'back_default']:
        path = get_sprite_path("yellow", index, category)
        sprite = pygame.image.load(path).convert_alpha()
        sprite.set_colorkey(sprite.get_at((0, 0)))
        in_battle_pokemon.sprites[category] = sprite

def get_random_moves(in_battle_pokemon):
    moves_list = []
    moves_dict = in_battle_pokemon.data_dict['moves']
    level = in_battle_pokemon.stats['level']
    print(in_battle_pokemon.name)

    print('level')
    for key in moves_dict:
        move = moves_dict[key]
        if move['move_learn_method'] == 'level-up' and move['level_learned_at'] <= level:
            moves_list.append(move['name'])
    print(len(moves_list))
    for i,move in enumerate(moves_list[:4]):
        in_battle_pokemon.moves[i] = move
    for key in in_battle_pokemon.moves:
        print(f"{key}: {in_battle_pokemon.moves[key]}")


class InBattleTrainer:
    def __init__(self, name, team, items):
        self.name = name
        self.team = team
        self.items = items
        self.current_pokemon_index = 0

    def get_current_pokemon(self):
        return self.team[self.current_pokemon_index]




class InBattlePokemon:
    def __init__(self, species, name=None):
        self.species = species
        self.data_dict = get_species_dict_from_json_by_name(species)
        self.name = name if name is not None else self.data_dict['names']['fr']

        base_stats_dict = self.data_dict['base_stats']
        self.stats = {
            "level": random.randint(1, 7),
            "hp": base_stats_dict["hp"],
            "max_hp": base_stats_dict["hp"],
        }
        self.moves = {0:None, 1:None, 2:None, 3:None}
        self.sprites = {}
        get_all_sprites_for_pokemon_instance(self)
        get_random_moves(self)
