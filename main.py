import pygame

from overworld.tilemap import Tilemap
from settings import RESOLUTION
from overworld.overworld import Overworld
from overworld.character import Character


def get_tilemap(path):
    return Tilemap(path)


def get_char(path):
    return Character(path)


pygame.init()
screen = pygame.display.set_mode(RESOLUTION)

new_chars = [get_char(char_json_path) for char_json_path in ["assets/json/players/player02.json", "assets/json/players/player01.json"]]
new_tilemap = get_tilemap("assets/json/tilemaps/tilemap02.json")
new_tilemap.characters = new_chars

new_level = Overworld(new_tilemap, new_chars)
new_level.run()