from math import floor
from pokemon.species import Species
from test import get_a_new_pokemon, TYPE_DATABASE, SPECIES_DATABASE
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


class PokemonTeam:
    def __init__(self, pokemon_list):
        self.pokemons = pokemon_list
        self.picked_pokemon = None

    def is_alive(self):
        return not all(not pokemon.is_alive() for pokemon in self.pokemons)

    def get_picked_pokemon(self):
        if not self.picked_pokemon:
            self.switch()
        elif not self.picked_pokemon.is_alive():
            self.switch()
        return self.picked_pokemon

    def switch(self):
        previous_pokemon = self.picked_pokemon

        # filtrer pokemon ko et ordonner liste à partir du pokemon actuel
        if previous_pokemon:
            i = self.pokemons.index(self.picked_pokemon)
            filtered_list = self.pokemons[i + 1:] + self.pokemons[0:i + 1]
        else:
            filtered_list = self.pokemons
        filtered_list = [pokemon for pokemon in filtered_list if pokemon.is_alive()]

        # prendre premier élement si existe
        if filtered_list:
            self.picked_pokemon = filtered_list[0]
        else:
            self.picked_pokemon = None

        # create string to display
        string = ""
        if previous_pokemon:
            string += f"{previous_pokemon.nickname}"
        else:
            string += f"None"
        string += " => "
        if self.picked_pokemon:
            string += f"{self.picked_pokemon.nickname}"
        else:
            string += f"None"
        print(string)
        print("")




class PokemonInBattle:
    def __init__(self, pokemon):
        self.pokemon = pokemon
        self.nickname = self.pokemon.nickname
        self.calculated_speed = 0
        # stage range -6 to 6
        self.moves = self.pokemon.moves
        self.level = self.pokemon.level
        self.stats = self.pokemon.stats
        self.stat_stages = {key:0 for (key,value) in self.stats.items() if key != "hp"}
        self.stat_stages["accuracy"] = 0
        self.stat_stages["evasion"] = 0
        # for key in self.stat_stages:
        #     print(key, self.stat_stages[key])

    def is_alive(self):
        return self.pokemon.current_hp > 0

    def pick_random_move(self):
        return random.choice([move for move in self.moves if move.current_pp > 0])

    def modify_stat_stage(self, stat, n):
        if stat in self.stat_stages:
            self.stat_stages[stat] += n
            self.stat_stages[stat] = max(min(self.stat_stages[stat], 6), -6)
            print(f"{self.pokemon.nickname}'s {stat} modified to stage {self.stat_stages[stat]}")
        else:
            print(f"{stat} is not a valid stage stat")

    def modify_current_hp(self, n):
        a = self.pokemon.current_hp
        self.pokemon.current_hp = max(min(self.pokemon.current_hp - n, self.stats["hp"]), 0)
        # print(f"{str(a)}HP -{str(n)}=> {str(self.pokemon.current_hp)}HP")

    def reset_stat_stages(self):
        for stat in self.stat_stages:
            self.stat_stages[stat] = 0


def print_moves(pokemon):
    for move in pokemon.moves:
        print(f"{move.name}: {move.type}, {move.category}")
    print("")


def who_switch_pokemon(pokemon_in_battle_a, picked_move_a, pokemon_in_battle_b, picked_move_b):
    if picked_move_a.name == "recall":
        return [(pokemon_in_battle_a, picked_move_a), (pokemon_in_battle_b, picked_move_b)]
    elif picked_move_b.name == "recall":
        return [(pokemon_in_battle_b, picked_move_b), (pokemon_in_battle_a, picked_move_a)]
    else:
        return None


def who_has_highest_priority(pokemon_in_battle_a, picked_move_a, pokemon_in_battle_b, picked_move_b):
    if picked_move_a.priority > picked_move_b.priority:
        return [(pokemon_in_battle_a, picked_move_a), (pokemon_in_battle_b, picked_move_b)]
    elif picked_move_a.priority < picked_move_b.priority:
        return [(pokemon_in_battle_b, picked_move_b), (pokemon_in_battle_a, picked_move_a)]
    else:
        return None


def who_has_highest_calculated_speed(pokemon_in_battle_a, picked_move_a, pokemon_in_battle_b, picked_move_b):
    calculated_speed_a = pokemon_in_battle_a.pokemon.stats["speed"] * get_general_stage_multiplier(
        pokemon_in_battle_a.stat_stages["speed"])
    calculated_speed_b = pokemon_in_battle_b.pokemon.stats["speed"] * get_general_stage_multiplier(
        pokemon_in_battle_b.stat_stages["speed"])
    if calculated_speed_a > calculated_speed_b:
        return [(pokemon_in_battle_a, picked_move_a), (pokemon_in_battle_b, picked_move_b)]
    elif calculated_speed_a < calculated_speed_b:
        return [(pokemon_in_battle_b, picked_move_b), (pokemon_in_battle_a, picked_move_a)]
    else:
        return None


def get_order_of_actions(pokemon_in_battle_a, picked_move_a, pokemon_in_battle_b, picked_move_b):
    recalling_pokemon_list = who_switch_pokemon(pokemon_in_battle_a, picked_move_a, pokemon_in_battle_b, picked_move_b)
    if recalling_pokemon_list:
        return recalling_pokemon_list

    highest_priority_pokemon_list = who_has_highest_priority(pokemon_in_battle_a, picked_move_a, pokemon_in_battle_b, picked_move_b)
    if highest_priority_pokemon_list:
        return highest_priority_pokemon_list

    highest_calculated_speed_pokemon = who_has_highest_calculated_speed(pokemon_in_battle_a, picked_move_a, pokemon_in_battle_b, picked_move_b)
    if highest_calculated_speed_pokemon:
        return highest_calculated_speed_pokemon

    return random.sample([(pokemon_in_battle_a, picked_move_a), (pokemon_in_battle_b, picked_move_b)], 2)


def is_move_successful(move, actor, target):
    base_accuracy = move.accuracy
    accuracy_stage = max(min(actor.stat_stages["accuracy"] - target.stat_stages["evasion"], 6), -6)
    accuracy_multiplier = get_accuracy_stage_multiplier(accuracy_stage)
    calculated_accuracy = int(min(base_accuracy*accuracy_multiplier, 100))
    if random.randint(0,99) < calculated_accuracy:
        return True
    return False


def is_critical_hit(move):
    c = 0
    if move.high_critical_hit:
        c += 1
    match c:
        case 0:
            rate = 100/24
        case 1:
            rate = 100/8
        case 2:
            rate = 100/2
        case 3:
            rate = 100
        case _:
            rate = 100
    if random.randint(0,99) < rate:
        return True
    return False


def is_move_share_type_with_attacker(move, actor):
    if move.type in actor.pokemon.types:
        return True
    return False


def get_effectiveness_modifier(move, target):
    attack_type = move.type
    target_types = target.pokemon.types
    multiplier = 1
    for target_type in target_types:
        if attack_type in TYPE_DATABASE and target_type in TYPE_DATABASE[attack_type]:
            multiplier *= TYPE_DATABASE[attack_type][target_type]
    if multiplier < 1:
        print("Not very effective...")
    elif multiplier > 1:
        print("Very effective !")
    return multiplier


def get_damage(move, actor, target):
    l = actor.level
    p = move.power
    if move.category == "physical":
        a = actor.stats["attack"]
        d = target.stats["defense"]
    else:
        a = actor.stats["sp_atk"]
        d = target.stats["sp_def"]
    damage = floor(floor(floor(2*l/5+2)*a*p/d)/50)+2
    damage = floor(damage * get_effectiveness_modifier(move, target))
    if is_critical_hit(move):
        print("Critical hit !")
        damage *= 1.5
    return floor(damage)


def battle(team_a, team_b):
    print("\nBattle start !")
    running = True
    while running:
        print("")
        pokemon_a = team_a.get_picked_pokemon()
        pokemon_b = team_b.get_picked_pokemon()
        print(f"{pokemon_a.nickname} has {pokemon_a.pokemon.current_hp} HP")
        print(f"{pokemon_b.nickname} has {pokemon_b.pokemon.current_hp} HP")
        move_a = pokemon_a.pick_random_move()
        move_b = pokemon_b.pick_random_move()

        action_order = get_order_of_actions(pokemon_a, move_a, pokemon_b, move_b)
        for actor,move in action_order:
            target = pokemon_a if actor != pokemon_a else pokemon_b
            if actor.is_alive() and target.is_alive():
                if is_move_successful(move, actor, target):
                    damage = get_damage(move, actor, target)
                    target.modify_current_hp(damage)
                    move.current_pp -= 1
                    print(f"{actor.nickname} uses {move.name} ({move.current_pp}/{move.max_pp}) on {target.nickname} ({damage} damage)")

                    if not target.is_alive():
                        print(f"{target.nickname} KO")
                else:
                    print(f"{actor.nickname} miss ({move.name})")


        if not team_a.is_alive() or not team_b.is_alive():
            running = False
        # else:
        #     if not pokemon_a.is_alive():
        #         team_a.switch()
        #     if not pokemon_b.is_alive():
        #         team_b.switch()
    if team_a.is_alive():
        print(f"Team A won!")
    else:
        print(f"Team B won!")



def get_n_pokemon_of_species(n, species_name):
    species = SPECIES_DATABASE[species_name]
    new_list = []
    for i in range(n):
        new_list.append(PokemonInBattle(get_a_new_pokemon(species_name, random.randint(5,20), f"{species.name}_{str(i)}")))
    return new_list


# new_pokemon_a = PokemonInBattle(get_a_new_pokemon("charmander", 10, "Salamèche"))
# # new_pokemon_b = PokemonInBattle(get_a_new_pokemon("bulbasaur", 8, "PotatoB"))
# new_pokemon_c = PokemonInBattle(get_a_new_pokemon("bulbasaur", 10, "Bulbizarre"))
# # new_pokemon_d = PokemonInBattle(get_a_new_pokemon("bulbasaur", 6, "HerbsD"))

new_team_a = PokemonTeam(get_n_pokemon_of_species(6, "charmander"))
new_team_b = PokemonTeam(get_n_pokemon_of_species(6, "bulbasaur"))

battle(new_team_a, new_team_b)
