import pygame
import random
import names
from model.bag import Bag
from model.battle import Battle
from model.pokemon import Pokemon
from model.party import Party
from model.move import Move
from model.trainer import Trainer
from controller.pygame.battle_controller import BattleController
from view.pygame.battle_view import BattleView
from utils.file_IO import get_dict_from_json_path


def get_a_random_trainer(species_dict, moves_dict, items_dict):
    new_trainer = Trainer(name=names.get_first_name(), bag=get_a_random_bag())
    new_trainer.party = get_a_random_party(species_dict, moves_dict, new_trainer)
    print(f"trainer {new_trainer.name} created\n")
    return new_trainer

def get_a_random_party(species_dict, moves_dict, trainer):
    new_party = Party()
    for i in range(6):
        new_party.add_a_member(get_a_random_pokemon(species_dict, moves_dict, trainer))
    return new_party


def get_a_random_pokemon(species_dict, moves_dict, trainer):
    species_key = random.choice([key for key in species_dict])
    species = species_dict[species_key]
    sprite_path = species['sprites']['yellow']['front_default']['path']
    new_pokemon = Pokemon(species_key, species['id'], species['types'], random.randint(1,100), exp=0, stats=species["base_stats"], name=species['names']['fr'], trainer=trainer, sprite_path=sprite_path)
    print(f"pokemon {new_pokemon.name} l{new_pokemon.level} created")
    set_random_moves_for_pokemon(new_pokemon, species_dict, moves_dict)
    return new_pokemon


def set_random_moves_for_pokemon(pokemon, species_dict, all_moves_dict):
    pokemon_dict = species_dict[pokemon.species]

    key_list = []
    moves_dict = pokemon_dict['moves']
    level = pokemon.level
    name = pokemon.name
    # print(f"{name} l:{str(level)}")

    for key in moves_dict:
        move = moves_dict[key]
        if move['move_learn_method'] == 'level-up' and move['level_learned_at'] <= level:
            key_list.append(move['name'])
    # print(f"compatible moves: {len(key_list)}")
    random.shuffle(key_list)
    for i,key in enumerate(key_list[:4]):
        pokemon.moves[i] = get_a_new_move(key, all_moves_dict)
    for key in pokemon.moves:
        if pokemon.moves[key]:
            # print(f"{key}: {pokemon.moves[key]}")
            pass
    # print("")


def get_a_new_move(move_key, all_moves_dict):
    move_dict = all_moves_dict[move_key]
    move_names = move_dict['names']
    move_type = move_dict['type']
    move_power = move_dict['power']
    move_accuracy = move_dict['accuracy']
    move_category = move_dict['category']
    move_max_pp = move_dict['pp']
    move_priority = move_dict['priority']
    return Move(move_names, move_type, move_category, move_power, move_accuracy, move_max_pp, move_priority)


def get_a_random_bag():
    new_bag = Bag()
    for i in range(random.randint(1,20)):
        new_bag.add_item(random.randint(1,100), random.randint(1,99))
    for slot in new_bag.slots:
        print(f"item{slot.item_id} x{slot.quantity}")
    return new_bag

# def get_a_random_pokemon_of_species(species, data_dict):
#     species_data = data_dict["species"]
#     new_moves = {}
#     return Pokemon(species, level=random.randint(2, 99), moves=new_moves, name=species_data["names"]['fr'])


def get_a_random_battle():
    species_dict = get_dict_from_json_path('assets/json/generation/gen_1_pokemon_species.json')
    moves_dict = get_dict_from_json_path('assets/json/generation/gen_1_moves.json')
    items_dict = get_dict_from_json_path('assets/json/generation/gen_1_items.json')

    trainer_a = get_a_random_trainer(species_dict, moves_dict, items_dict)
    trainer_b = get_a_random_trainer(species_dict, moves_dict, items_dict)
    return Battle(trainer_a, trainer_b)


def pygame_test():
    pygame.init()
    clock = pygame.time.Clock()

    model = get_a_random_battle()
    view = BattleView()
    controller = BattleController(model, view)

    running = True
    while running:
        # 2. Calcul du dt (limité à 60 FPS)
        # clock.tick(60) renvoie des millisecondes. / 1000.0 convertit en secondes.
        dt = clock.tick(60) / 1000.0

        # 3. Récupération des événements
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                running = False

        # 4. Transmission aux contrôleurs
        controller.handle_input(events)
        controller.update(dt)  # <-- Le dt est injecté ici

        # 5. Rendu
        view.display()
        pygame.display.set_caption(f"Pokemon Battle System Test (fps: {clock.get_fps(): .1f})")


# def console_test():
#     model = get_a_random_battle()
#     view = ConsoleBattleView()
#     controller = BattleController(model, view)
#
#     running = True
#     while running:
#         # 4. Transmission aux contrôleurs
#         controller.handle_input()
#         controller.update()  # <-- Le dt est injecté ici
#
#         # 5. Rendu
#         # pygame.display.flip()


pygame_test()