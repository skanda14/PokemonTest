import requests
from utils.file_IO import create_json_from_dict, get_dict_from_json_path, update_json_file, download_image


def get_data_from_full_url(full_url):
    try:
        response = requests.get(full_url)

        # Vérifie si la requête a réussi (code 200)
        if response.status_code == 200:
            data = response.json()
            return data
        else:
            print(f"Erreur : Impossible d'accéder à {full_url}")
            return None

    except Exception as e:
        print(f"Une erreur est survenue : {e}")
        return None


def get_data_from_end_of_url(url_part):
    # L'URL de base de l'API
    full_url = f"https://pokeapi.co/api/v2/{url_part}"
    return get_data_from_full_url(full_url)


def get_species_data(name):
    url_part = f"pokemon-species/{name.lower()}"
    return get_data_from_end_of_url(url_part)

def get_pokemon_data(name):
    url_part = f"pokemon/{name.lower()}"
    return get_data_from_end_of_url(url_part)

def get_move_data(name):
    url_part = f"move/{name.lower()}"
    return get_data_from_end_of_url(url_part)

# def get_evolution_chain_data(n):
#     url_part = f"evolution-chain/{str(n)}"
#     return get_data_from_end_of_url(url_part)

def get_generation_data(n):
    url_part = f"generation/{str(n)}"
    return get_data_from_end_of_url(url_part)


# # Exemple d'utilisation
# pokemon = get_pokemon_data("pikachu")
#
# if pokemon:
#     id = pokemon['id']
#     name = pokemon['name']
#     types = [type['type']['name'] for type in pokemon['types']]
#
#     # base_stats = {}
#     # for stat_dict in pokemon['stats']:
#     #     base_stat = stat_dict['base_stat']
#     #     effort = stat_dict['effort']
#     #     name = stat_dict['stat']['name']
#
#     base_stats = {}
#     for stat_dict in pokemon['past_stats']:
#         base_stat = stat_dict['base_stat']
#         effort = stat_dict['effort']
#         name = stat_dict['stat']['name']
#
#
#
#     print(types)


def get_language_version_of_item_in_list(curent_list, language):
    result = None
    for item in curent_list:
        if item['language']['name'] == language:
            result = item['name']
    return result

def get_english_and_french_dict_from_list(curent_list):
    new_dict = {}
    for language in ["fr", "en"]:
        new_dict[language] = get_language_version_of_item_in_list(curent_list, language)
    return new_dict

def get_details_dict(evo):
    new_list = []
    for details in evo['evolution_details']:
        new_dict = {}
        for key in details:
            if not details[key]:
                pass
            elif details[key] is False:
                pass
            elif key == "url":
                pass
            elif key in ["trigger", "item"]:
                new_dict[key] = details[key]['name']
            else:
                new_dict[key] = details[key]
        new_list.append(new_dict)
    return new_list


def add_all_evo_for_a_pokemon_in_a_dict(chain, total_evo_for_chain_dict, species_name_list):
    pokemon_name = chain['species']['name']
    if chain['evolves_to']:
        for evo_chain in chain['evolves_to']:
            evolution_details_list = get_details_dict(evo_chain)
            evolved_pokemon_name = evo_chain['species']['name']
            evo_link = {evolved_pokemon_name: evolution_details_list}

            add_all_evo_for_a_pokemon_in_a_dict(evo_chain, total_evo_for_chain_dict, species_name_list)

            if pokemon_name in species_name_list:
                if evolved_pokemon_name in species_name_list:
                    total_evo_for_chain_dict[pokemon_name] = evo_link
                else:
                    total_evo_for_chain_dict[pokemon_name] = {}
    else:
        if pokemon_name in species_name_list:
            total_evo_for_chain_dict[pokemon_name] = {}


def get_all_evo_for_all_pokemon_from_a_chain(url, species_name_list ):
    every_evo_of_the_chain_dict = {}
    evo_chain = get_data_from_full_url(url)
    id = evo_chain['id']


    chain = evo_chain['chain']
    add_all_evo_for_a_pokemon_in_a_dict(chain, every_evo_of_the_chain_dict, species_name_list)
    # if id == 10:
    #     print('pikachu evo chain detected')
    #     for key in every_evo_of_the_chain_dict:
    #         print(key, every_evo_of_the_chain_dict[key])
    #     print("pikachu chain over")
    return id, every_evo_of_the_chain_dict


def get_all_evo_chain_from_gen_1():
    new_dict = {}
    # dir_path = "assets/json/pokemon_species/"
    # file_name = f"gen_1_pokemon.json"
    # pokedex_name = "kanto"
    gen_1_species = get_dict_from_json_path("../assets/json/generation/generation-1.json")['pokemon_species']
    print("len species found for chain:", len(gen_1_species))
    species_name_list = [gen_1_species[key] for key in gen_1_species]
    for name in species_name_list:
        species = get_species_data(name)
        evolution_chain_url = species['evolution_chain']['url']
        chain_n, evo_chain = get_all_evo_for_all_pokemon_from_a_chain(evolution_chain_url, species_name_list)

        for key in evo_chain:
            if not key in new_dict:
                new_dict[key] = evo_chain[key]
            # else:
            #     print(f"{key} already exists in chain")
    print("len chain:", len(new_dict))
    return new_dict


def get_pokemon_stats(pokemon):
    new_dict = {}
    for stat in pokemon['stats']:
        name = stat['stat']['name']
        if name in ['hp', 'attack', 'defense','special','speed']:
            new_dict[name] = stat['base_stat']
    for stats in pokemon['past_stats']:
        if stats['generation']['name'] == 'generation-i':
            for stat in stats['stats']:
                name = stat['stat']['name']
                if name in ['hp', 'attack', 'defense', 'special', 'speed']:
                    new_dict[name] = stat['base_stat']
    return new_dict


def get_pokemon_moves(pokemon):
    allowed_version = ['red-blue', 'yellow']
    new_dict = {}
    for move in pokemon['moves']:
        found_versions = {}
        name = move['move']['name']
        for ver in move['version_group_details']:
            version_group = ver['version_group']['name']
            if version_group in allowed_version:
                found_versions[version_group] = ver
        for version in allowed_version:
            if version in found_versions:
                ver = found_versions[version]
                level_learned_at = ver['level_learned_at']
                move_learn_method = ver['move_learn_method']['name']
                new_dict[name] = {
                    "name": name,
                    "level_learned_at": level_learned_at,
                    "move_learn_method": move_learn_method,
                }
    return new_dict

def get_pokemon_sprites(pokemon):
    new_dict = {}
    if 'other' in pokemon['sprites']:
        if 'official-artwork' in pokemon['sprites']['other']:
            new_dict['official_artwork'] = {}
            for key in pokemon['sprites']['other']['official-artwork']:
                new_dict['official_artwork'][key] = {'url': pokemon['sprites']['other']['official-artwork'][key]}
    if 'versions' in pokemon['sprites']:
        if 'generation-i' in pokemon['sprites']['versions']:
            for key in pokemon['sprites']['versions']['generation-i']:
                new_dict[key] = {}
                for key_2 in pokemon['sprites']['versions']['generation-i'][key]:
                    new_dict[key][key_2] = {'url': pokemon['sprites']['versions']['generation-i'][key][key_2]}
    return new_dict

def get_species_index(species, pokedex_name_requested):
    pokedex_numbers = species['pokedex_numbers']
    for pokedex_number in pokedex_numbers:
        entry_number = pokedex_number['entry_number']
        pokedex_name = pokedex_number['pokedex']['name']

        if pokedex_name == pokedex_name_requested:
            return entry_number
    return None

def get_full_species_data(name, pokedex_name, evo_chain):
    species = get_species_data(name)
    pokemon = get_pokemon_data(name)
    new_dict = {}
    if species and pokemon:
        # print(species['name'])
        new_dict = {
            "id": get_species_index(species, pokedex_name),
            'name': species['name'],
            'names': get_english_and_french_dict_from_list(species['names']),
            "capture_rate": species['capture_rate'],
            "growth_rate": species['growth_rate']['name'],
            "habitat": species['habitat']['name'],
            "evolves_from": species['evolves_from_species']['name'] if species['evolves_from_species'] else None,
            "evolutions": evo_chain[species['name']],

            "types": [t['type']['name'] for t in pokemon['types']],
            "base_experience": pokemon['base_experience'],
            "base_stats": get_pokemon_stats(pokemon),
            "moves": get_pokemon_moves(pokemon),
            "cries": pokemon['cries']['legacy'],
            "sprites": get_pokemon_sprites(pokemon),
            "height": pokemon['height'],
            "weight": pokemon['weight'],
        }
        # print("")
        # for key in new_dict:
        #     print(key)
        #     print(new_dict[key])
        #     print('')
    return new_dict


def save_all_species_data_in_json():
    n = 1
    dir_path = "../assets/json/generation/"
    file_name = f"gen_{str(n)}_pokemon_species.json"
    pokedex_name = "kanto"

    gen_1_dict = get_dict_from_json_path("../assets/json/generation/generation-1.json")
    names = [gen_1_dict['pokemon_species'][key] for key in gen_1_dict['pokemon_species']]
    evo_chain_dict = get_all_evo_chain_from_gen_1()
    for key in gen_1_dict['pokemon_species']:
        name = gen_1_dict['pokemon_species'][key]
        if not name in evo_chain_dict:
            print(f"Evolution chain for {key} {name} not found")

    i = 1
    max = len(names)
    for name in names:
        species = get_species_data(name)
        pokemon = get_pokemon_data(name)
        if species and pokemon:
            new_dict = get_full_species_data(name, pokedex_name, evo_chain_dict)
            update_json_file(name, new_dict, dir_path + file_name)

            print(f"{str(i)}/{str(max)} {name} added to dict")
            i += 1

        else:
            print(f"{name} not added to dict !!!")

    # create_json_from_dict(new_dict, dir_path+file_name)


def save_generation_n_data_in_json(n):
    gen = get_generation_data(n)
    if gen:
        dir_path = "../assets/json/generation/"
        new_dict = {
            "id": gen['id'],
            "name": gen['name'],
            "main_region": gen['main_region']['name'],
            "types": {i:type['name'] for i,type in enumerate(gen['types'])},
            "pokemon_species": {i:species['name'] for i,species in enumerate(gen['pokemon_species'])},
            "moves": {i:move['name'] for i,move in enumerate(gen['moves'])},
        }
        file_name = f"generation-{str(n)}.json"
        create_json_from_dict(new_dict, dir_path+file_name)


def get_move_effect_entry(move):
    entries = move['effect_entries']
    new_dict = {"effect": {}, "short_effect": {}}
    for entry in entries:
        language = entry['language']['name']
        if language in ["fr", "en"]:
            new_dict["effect"][language] = entry['effect']
            new_dict["short_effect"][language] = entry['short_effect']
    return new_dict

def get_move_meta(move):
    meta = move['meta']
    new_dict = {}
    for key in meta:
        if key == "ailment":
            new_dict[key] = meta[key]['name']
        elif key == "category":
            new_dict[key] = meta[key]['name']
        else:
            new_dict[key] = meta[key]
    return new_dict


def get_move_dict(name):
    move = get_move_data(name)

    new_dict = {
        "id": move['id'],
        "name": move['name'],
        "names": get_english_and_french_dict_from_list(move['names']),
        "type": move['type']['name'],
        "category": move['damage_class']['name'],
        "power": move['power'],
        "accuracy": move['accuracy'],
        "pp": move['pp'],
        "priority": move['priority'],
        "effects": [],
        "meta": get_move_meta(move),
        "effect_entry": get_move_effect_entry(move),
    }
    # for key in new_dict:
    #     print(key, new_dict[key])

    return new_dict


def save_all_moves_in_json():
    new_dict = {}
    gen_1_dict = get_dict_from_json_path("../assets/json/generation/generation-1.json")
    for key in gen_1_dict["moves"]:
        move_name = gen_1_dict["moves"][key]
        new_dict[move_name] = get_move_dict(move_name)

    print(f"{len(new_dict)} moves available")
    dir_path = "../assets/json/generation/"
    file_name = f"gen_1_moves.json"
    create_json_from_dict(new_dict, dir_path + file_name)


def modif_sprite_url_field_in_pokemon_species_json():
    pokemon_species_dict = get_dict_from_json_path("assets/json/generation/gen_1_pokemon_species_copy.json")
    for key in pokemon_species_dict:
        pokemon_dict = pokemon_species_dict[key]
        sprites_dict = pokemon_dict['sprites']
        for category_key in sprites_dict:
            category_dict = sprites_dict[category_key]
            for element_key in category_dict:
                element = category_dict[element_key]
                category_dict[element_key] = {'url': element, 'path': None}
    create_json_from_dict(pokemon_species_dict, "../assets/json/generation/gen_1_pokemon_species.json")



# modif_sprite_url_field_in_pokemon_species_json()

def reorganized_gen_1_main_json():
    gen_1_dict = get_dict_from_json_path("../assets/json/generation/generation-1.json")
    # gen_1_species_dict = get_dict_from_json_path("assets/json/generation/gen_1_pokemon_species.json")
    # for i in range(1, len(gen_1_species_dict)+1):
    #     key_name = [key for key in gen_1_species_dict if gen_1_species_dict[key]['id'] == i][0]
    #
    #     print(f"{i} : {key_name}")
    #     new_dict[i] = key_name
    #
    #
    # # for key in new_dict:
    # #     print(f"{key} : {new_dict[key]}")
    # print("")
    # print(len(new_dict))
    # gen_1_dict['pokemon_species'] = new_dict


    gen_1_moves_dict = get_dict_from_json_path("../assets/json/generation/gen_1_moves.json")
    for i in range(1, len(gen_1_moves_dict)+1):
        key_name = [key for key in gen_1_moves_dict if gen_1_moves_dict[key]['id'] == i][0]

        print(f"{i} : {key_name}")
        new_dict[i] = key_name


    # for key in new_dict:
    #     print(f"{key} : {new_dict[key]}")
    print("")
    print(len(new_dict))
    gen_1_dict['moves'] = new_dict

    create_json_from_dict(gen_1_dict, "../assets/json/generation/generation-1.json")
    # update_json_file('pokemon_species', gen_1_dict, "assets/json/generation/generation-1.json")






def save_all_gen_1_pokemon_battle_sprites():
    json_path = "../assets/json/generation/gen_1_pokemon_species.json"
    gen_1_pokemon_dict = get_dict_from_json_path(json_path)
    category = "yellow"
    sub_categories = ["back_default", "front_default"]
    for name_key in gen_1_pokemon_dict:
        pokemon_dict = gen_1_pokemon_dict[name_key]
        pokemon_id = str(pokemon_dict['id'])
        while len(pokemon_id) < 3:
            pokemon_id = "0"+pokemon_id
        if category in pokemon_dict['sprites']:
            for sub_category in sub_categories:
                if sub_category in pokemon_dict['sprites'][category]:
                    sprite_dict = pokemon_dict['sprites'][category][sub_category]
                    url = sprite_dict['url']
                    path = f"assets/sprites/pokemon/{category}/{pokemon_id}/{sub_category}.png"
                    download_image(url, path)
                    sprite_dict['path'] = path
                else:
                    print(f"{name_key} : no subcategory {sub_category} found")
        else:
            print(f"{name_key} : no category {category} found")
    create_json_from_dict(gen_1_pokemon_dict, json_path)


