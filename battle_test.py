from unittest import case

from test import get_a_new_pokemon
import random


def get_general_stage_multiplier(n):
    numerator, denominator = 2,2
    if n>0:
        numerator += n
    elif n<0:
        denominator += abs(n)
    return numerator/denominator

def get_accuracy_stage_multiplier(n):
    numerator, denominator = 3,3
    if n>0:
        numerator += n
    elif n<0:
        denominator += abs(n)
    return numerator/denominator

def get_evasion_stage_multiplier(n):
    numerator, denominator = 3,3
    if n<0:
        numerator += n
    elif n>0:
        denominator += abs(n)
    return numerator/denominator


class PokemonInBattle:
    def __init__(self, pokemon):
        self.pokemon = pokemon
        self.calculated_speed = 0
        # stage range -6 to 6
        self.stat_stages = {key:0 for (key,value) in pokemon.stats.items() if key != "hp"}
        self.stat_stages["accuracy"] = 0
        self.stat_stages["evasion"] = 0
        # for key in self.stat_stages:
        #     print(key, self.stat_stages[key])

    def modify_stat_stage(self, stat, n):
        if stat in self.stat_stages:
            self.stat_stages[stat] += n
            self.stat_stages[stat] = max(min(self.stat_stages[stat], 6), -6)
            print(f"{self.pokemon.nickname}'s {stat} modified to stage {self.stat_stages[stat]}")
        else:
            print(f"{stat} is not a valid stage stat")

    def reset_stat_stages(self):
        for stat in self.stat_stages:
            self.stat_stages[stat] = 0


def print_moves(pokemon):
    for move in pokemon.moves:
        print(f"{move.name}: {move.type}, {move.category}")
    print("")

def who_switch_pokemon(pokemon_a, picked_move_a, pokemon_b, picked_move_b):
    if picked_move_a.name == "recall":
        return [pokemon_a, pokemon_b]
    elif picked_move_b.name == "recall":
        return [pokemon_b, pokemon_a]
    else:
        return None


def who_has_highest_priority(pokemon_a, picked_move_a, pokemon_b, picked_move_b):
    if picked_move_a.priority > picked_move_b.priority:
        return [pokemon_a, pokemon_b]
    elif picked_move_a.priority < picked_move_b.priority:
        return [pokemon_b, pokemon_a]
    else:
        return None

def who_has_highest_calculated_speed(pokemon_a, pokemon_b):
    calculated_speed_a = pokemon_a.pokemon.stats["speed"] * get_general_stage_multiplier(
        pokemon_a.stat_stages["speed"])
    calculated_speed_b = pokemon_b.pokemon.stats["speed"] * get_general_stage_multiplier(
        pokemon_b.stat_stages["speed"])
    if calculated_speed_a > calculated_speed_b:
        return [pokemon_a, pokemon_b]
    elif calculated_speed_a < calculated_speed_b:
        return [pokemon_b, pokemon_a]
    else:
        return None

def get_order_of_actions(pokemon_in_battle_a, picked_move_a, pokemon_in_battle_b, picked_move_b):
    recalling_pokemon_list = who_switch_pokemon(pokemon_in_battle_a, picked_move_a, pokemon_in_battle_b, picked_move_b)
    if recalling_pokemon_list:
        return recalling_pokemon_list

    highest_priority_pokemon_list = who_has_highest_priority(pokemon_in_battle_a, picked_move_a, pokemon_in_battle_b, picked_move_b)
    if highest_priority_pokemon_list:
        return highest_priority_pokemon_list

    highest_calculated_speed_pokemon = who_has_highest_calculated_speed(pokemon_in_battle_a, pokemon_in_battle_b)
    if highest_calculated_speed_pokemon:
        return highest_calculated_speed_pokemon

    return random.sample([pokemon_in_battle_a, pokemon_in_battle_b], 2)



pokemon_a = PokemonInBattle(get_a_new_pokemon("bulbasaur", 10, "Potato"))

pokemon_b = PokemonInBattle(get_a_new_pokemon("bulbasaur", 6, "Herbs"))
picked_move_a = random.choice(pokemon_a.pokemon.moves)
picked_move_b = random.choice(pokemon_b.pokemon.moves)
action_order = get_order_of_actions(pokemon_a, picked_move_a, pokemon_b, picked_move_b)
i = 0
for thing in action_order:
    if thing == pokemon_a:
        print(f"{str(i)}: {thing.pokemon.nickname} use {picked_move_a.name}")
    else:
        print(f"{str(i)}: {thing.pokemon.nickname} use {picked_move_b.name}")
    i += 1
#
#
#
# print(f"go {pokemon_a.nickname}")
# print(f"go {pokemon_b.nickname}")
#
# battle_a = PokemonInBattle(pokemon_a)

# for i in range(-6, 7):
#     print(f"{str(i)}=> {str(get_general_stage_multiplier(i))}")