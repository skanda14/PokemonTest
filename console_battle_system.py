import random
from database_management import get_a_new_pokemon, TYPE_DATABASE, SPECIES_DATABASE


class Team:
    def __init__(self, member_list, dresser):
        self.members = member_list
        self.dresser = dresser
        self.selected_member_index = 0

    def get_current_pokemon(self):
        return self.members[self.selected_member_index]

    def is_alive(self):
        return not all(not member.is_alive() for member in self.members)

class PokemonInBattle:
    def __init__(self, pokemon):
        self.pokemon = pokemon
        self.nickname = self.pokemon.nickname
        self.calculated_speed = 0
        self.moves = self.pokemon.moves
        self.level = self.pokemon.level
        self.stats = self.pokemon.stats
        self.stat_stages = {key:0 for (key,value) in self.stats.items() if key != "hp"} # stage range -6 to 6
        self.stat_stages["accuracy"] = 0
        self.stat_stages["evasion"] = 0

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


class ConsoleBattleSystem:
    def __init__(self, team_a, team_b):
        self.teams = [team_a, team_b]

    def update(self):
        pass



def get_n_pokemon_of_species(n=6, species_name=None):
    new_list = []
    for i in range(n):
        if species_name:
            if species_name in SPECIES_DATABASE:
                species = SPECIES_DATABASE[species_name]
            else:
                species = SPECIES_DATABASE[random.choice([key for key in SPECIES_DATABASE])]
        else:
            species = SPECIES_DATABASE[random.choice([key for key in SPECIES_DATABASE])]
        print(species)
        new_pokemon = get_a_new_pokemon(species_name, random.randint(5,20), f"{species.name}_{str(i)}")
        new_list.append(PokemonInBattle(new_pokemon))
    return new_list


new_team_a = Team(get_n_pokemon_of_species())
new_team_b = Team(get_n_pokemon_of_species())
