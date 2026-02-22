import pygame
from overworld.tilemap import Tilemap
from settings import RESOLUTION
from overworld.overworld import Overworld
from overworld.character import Character


tilemap_json_path = ""
char_json_path = ""

pygame.init()
screen = pygame.display.set_mode(RESOLUTION)

new_chars = [Character(char_json_path) for char_json_path in ["assets/json/players/player02.json", "assets/json/players/player01.json"]]
new_tilemap = Tilemap("assets/json/tilemaps/tilemap02.json")
new_tilemap.characters = new_chars

new_level = Overworld(new_tilemap, new_chars)
new_level.run()
