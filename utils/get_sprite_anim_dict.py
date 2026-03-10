from utils.file_IO import get_files_list, create_json_from_dict
import os


def get_filename_without_extension(file_path):
    # os.path.splitext sépare le chemin en deux : (racine, extension)
    # Exemple : ("image.png") -> ("image", ".png")
    root, extension = os.path.splitext(file_path)

    # On retourne uniquement la partie racine
    return os.path.basename(root)

def get_sprite_anim_dict():
    abs_dir_path = "C:\\Users\\User\\PycharmProjects\\PokemonTest\\assets\\sprites\\battle_sprites\\"
    dir_path = "assets\\sprites\\battle_sprites\\"
    file_list = get_files_list(abs_dir_path)
    new_dict = {}
    print("")
    for file_name in file_list:
        key_name = get_filename_without_extension(file_name)
        abs_file_path = os.path.join(abs_dir_path, file_name)
        file_path = os.path.join(dir_path, file_name)
        print(key_name)
        print(abs_file_path)
        print(file_path)
        new_item = {'name': key_name, 'file_path': file_path, 'abs_file_path': abs_file_path}
        new_dict[key_name] = new_item
    create_json_from_dict(new_dict, "../assets/json/sprite_anim_dict.json")

get_sprite_anim_dict()