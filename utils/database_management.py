from pokemon.species import Species
from pokemon.pokemon import Pokemon
from pokemon.move import Move
import json


def load_moves_datas():
    database = {}
    try:
        with open('../pokemon/data/moves.json', 'r') as file:
            database = json.load(file)
        print(f"Successfully loaded {len(database)} moves datas.")
    except FileNotFoundError:
        print("Error: moves.json not found.")
    return database


def load_species_data():
    database = {}
    try:
        with open('../pokemon/data/pokemon.json', 'r') as file:
            database = json.load(file)
        print(f"Successfully loaded {len(database)} species datas.")

    except FileNotFoundError:
        print("Error: pokemon.json not found.")
    return database


def load_types_data():
    database = {}
    try:
        with open('../pokemon/data/type_chart.json', 'r') as file:
            database = json.load(file)
        print(f"Successfully loaded {len(database)} types datas.")

    except FileNotFoundError:
        print("Error: type_chart.json not found.")
    return database


def get_species_dict():
    species_dict = {}
    database = load_species_data()
    for key in database:
        new_species = Species(database[key])
        species_dict[key] = new_species
    return species_dict


# Chargement unique au début du jeu
SPECIES_DATABASE = get_species_dict()
MOVE_DATABASE = load_moves_datas()
TYPE_DATABASE = load_types_data()


def get_a_new_pokemon(name, level, nickname=None):
    # 1 On récupère l'espèce depuis notre base de données
    new_species = SPECIES_DATABASE[name]
    # 2 On crée l'individu (Instance)
    return Pokemon(new_species, level, MOVE_DATABASE, nickname)


def get_a_new_move(name):
    # 1 On récupère le modèle depuis notre base de données (simulé ici)
    data = MOVE_DATABASE[name]
    # 2 On crée le move (Instance)
    return Move(data)


def print_species_data(species):
    for attr, value in vars(species).items():
        print(f"{attr}: {value}")


# print_species_data(SPECIES_DATABASE["bulbasaur"])
# new_pokemon = get_a_new_pokemon("bulbasaur", 5, SPECIES_DATABASE, "Bulby")
# print(f"{new_pokemon.nickname} has {new_pokemon.stats['hp']} HP.")
