import os
import json
import requests
from pathlib import Path


def download_image(url, save_path):
    """
    Télécharge une image depuis une URL et l'enregistre sur le disque.
    """
    try:
        # 1. Envoyer la requête de téléchargement
        # stream=True permet de ne pas charger toute l'image en RAM d'un coup
        response = requests.get(url, stream=True, timeout=10)

        # Vérifier si la requête a réussi (code 200)
        response.raise_for_status()

        # 2. Créer les dossiers parents si ils n'existent pas
        folder = os.path.dirname(save_path)
        if folder and not os.path.exists(folder):
            os.makedirs(folder)

        # 3. Écrire le contenu dans le fichier par blocs (chunks)
        with open(save_path, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)

        print(f"Succès : Image enregistrée sous {save_path}")
        return True

    except requests.exceptions.RequestException as e:
        print(f"Erreur lors du téléchargement : {e}")
        return False


def update_json_file(key, data, file_path):
    """
    Ajoute ou met à jour une clé avec un dictionnaire dans un fichier JSON existant.
    """
    # 1. Charger les données existantes
    if os.path.exists(file_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                content = json.load(file)
        except (json.JSONDecodeError, ValueError):
            # Si le fichier est vide ou corrompu, on initialise un dictionnaire
            content = {}
    else:
        content = {}

    # 2. Ajouter/Mettre à jour la nouvelle entrée
    content[key] = data

    # 3. Réécrire le fichier avec les données mises à jour
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(content, file, indent=4, ensure_ascii=False)


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
    path_obj = Path(json_path)
    # Crée les dossiers parents si nécessaire
    path_obj.parent.mkdir(parents=True, exist_ok=True)

    with open(path_obj, "w", encoding="utf-8") as f:
        json.dump(current_dict, f, ensure_ascii=False, indent=4)
    print(f'{path_obj.name}: File created/updated in {path_obj.parent}')


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
