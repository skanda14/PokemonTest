import pygame
from overworld.tilemap import Tilemap
from settings import RESOLUTION
from overworld.overworld import Overworld
from overworld.character import Character
from utils.file_IO import get_files_list


tilemap_json_path = ""
char_json_path = ""

pygame.init()
screen = pygame.display.set_mode(RESOLUTION)

tilemaps_dir = "assets/json/tilemaps/"
characters_dir = "assets/json/players/"
tilemap_json_list = get_files_list(tilemaps_dir)
characters_json_list = get_files_list(characters_dir)

new_tilemap = Tilemap(tilemaps_dir+tilemap_json_list[0])
new_chars = [Character(char_json_path) for char_json_path in ["assets/json/players/player03.json", "assets/json/players/player01.json"]]

new_tilemap.characters = new_chars

new_level = Overworld(new_tilemap, new_chars)
new_level.run()
