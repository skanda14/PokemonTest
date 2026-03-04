import pygame
from settings import MESSAGE_TILE_WIDTH, MESSAGE_TILE_HEIGHT


def get_images_list_from_big_image(image):
    sprites = []
    for y in range(0, image.get_height(), MESSAGE_TILE_HEIGHT):
        for x in range(0, image.get_width(), MESSAGE_TILE_WIDTH):
            new_image = image.copy().subsurface((x, y, MESSAGE_TILE_WIDTH, MESSAGE_TILE_HEIGHT))
            sprites.append(new_image)
    return sprites


def get_sprite_dict():
    new_image = pygame.image.load("assets/sprites/pokemon_font.png").convert_alpha()
    new_sprites = get_images_list_from_big_image(new_image)

    str_list = (
            [" "]+
            [chr(65+i) for i in range(0, 26)]+
            ["(",")",":",";","[","]"]+
            [chr(97+i) for i in range(26)]+
            ["à","è","é","ù","ß","ç","Ä","Ö","Ü","ä","ö","ü","ë","ï","â","ô","û","ê","î"]+
            ["{","c'","d'","j'","l'","m'","n'","p'","s'","'s","t'","u'","y'","'","%","#","-","+","?","!",".","&","}","<",">","µ", "male","$","*","/",",","female"]+
            [str(i) for i in range(0, 10)]+
            ["^"])
    new_dict = {key:new_sprites[i] for i,key in enumerate(str_list)}
    new_dict['É'] = new_dict['E']
    new_dict['È'] = new_dict['E']
    new_dict['Ê'] = new_dict['E']
    new_dict['Â'] = new_dict['A']
    new_dict['À'] = new_dict['A']
    new_dict['’'] = new_dict["'"]

    str_list = ["tl", "tr", "bl", "br", "ho", "ve"]
    new_image = pygame.image.load("assets/sprites/battle interface/box_parts_sprites.png")
    new_sprites = get_images_list_from_big_image(new_image)

    for i,key in enumerate(str_list):
        new_dict[key] = new_sprites[i]

    return new_dict

# def get_battle_sprite_pokemon():
#     image = pygame.image.load("assets/sprites/battle/sprites crystal gen1 pokemon.png").convert_alpha()
#     image.set_colorkey()