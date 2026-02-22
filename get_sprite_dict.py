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
    image = pygame.image.load("assets/sprites/pokemon_font.png").convert_alpha()
    sprites = get_images_list_from_big_image(image)

    str_list = (
            [" "]+
            [chr(65+i) for i in range(0, 26)]+
            ["(",")",":",";","[","]"]+
            [chr(97+i) for i in range(26)]+
            ["à","è","é","ù","ß","ç","Ä","Ö","Ü","ä","ö","ü","ë","ï","â","ô","û","ê","î"]+
            ["<","c'","d'","j'","l'","m'","n'","p'","s'","'s","t'","u'","y'","'","pk","mn","-","+","?","!",".","&",">","{","}","^","male","$","*","/",",","female"]+
            [str(i) for i in range(0, 10)])

    new_dict = {key:sprites[i] for i,key in enumerate(str_list)}
    return new_dict
