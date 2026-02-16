import os
import json
from pathlib import Path


def get_files_list(path, extension=None):
    items = os.listdir(path)
    if extension:
        return [item for item in items if item.endswith(f".{extension}")]
    else:
        return items


def get_dict_from_json_path(full_path):
    data = None
    with open(full_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data


def create_json_from_dict(current_dict, json_path):
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(current_dict, f, ensure_ascii=False, indent=4)
    print(f'{json_path}: fichier créé/modifié.')


def delete_json_file(file_full_path):
    fichier = Path(file_full_path)
    try:
        fichier.unlink()
        print(f"{file_full_path}: fichier supprimé.")
    except FileNotFoundError:
        print(f"{file_full_path}: fichier n'existe pas.")
    except PermissionError:
        print(f"{file_full_path}: permission refusé pour suppression.")
    except Exception as e:
        print(f"{file_full_path}: erreur inattendue pour suppression ({e}).")


def check_file_validity_from_path(file_path, extension=None):
    """
    Vérifie si le chemin est valide, s'il s'agit bien d'un fichier,
    et si l'extension correspond (si spécifiée).

    Args:
        file_path (str): Chemin du fichier à vérifier.
        extension (str, optionnel): Extension attendue (sans le point).

    Returns:
        tuple: (bool, str) où le booléen indique le succès, et la chaîne contient un message d'erreur ou None.
    """
    try:
        if not isinstance(file_path, str):
            return (False, "Erreur : le chemin doit être une chaîne de caractères.")
        if not os.path.exists(file_path):
            return (False, "Erreur : le chemin spécifié n'existe pas.")
        if not os.path.isfile(file_path):
            return (False, "Erreur : le chemin ne pointe pas vers un fichier.")
        if extension is not None:
            _, ext = os.path.splitext(file_path)
            if not ext or ext[1:].lower() != extension.lower():
                return (False, f"Erreur : l'extension du fichier n'est pas '{extension}'.")
        return (True, None)
    except PermissionError:
        return (False, "Erreur : permission refusée pour accéder au fichier.")
    except OSError as e:
        return (False, f"Erreur système : {str(e)}")
    except Exception as e:
        return (False, f"Erreur inattendue : {str(e)}")
