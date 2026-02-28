import pygame
from battle.battle_settings import TILE_WIDTH, TILE_HEIGHT, TILE_SIZE, BACKGROUND_COLOR
from battle.battle_display_fun import get_convert_pos


def get_box_sprite(grid_size, sprites_dict):
    new_surf = pygame.Surface((grid_size[0]*TILE_WIDTH, grid_size[1]*TILE_HEIGHT)).convert()
    new_surf.fill(BACKGROUND_COLOR)

    new_surf.blit(sprites_dict["tl"], get_convert_pos((0,0)))
    new_surf.blit(sprites_dict["tr"], get_convert_pos((grid_size[0]-1,0)))
    new_surf.blit(sprites_dict["bl"], get_convert_pos((0,grid_size[1]-1)))
    new_surf.blit(sprites_dict["br"], get_convert_pos((grid_size[0]-1,grid_size[1]-1)))

    for y in range(1, (grid_size[1]-1)):
        for x in [0, grid_size[0]-1]:
            new_surf.blit(sprites_dict["ve"], get_convert_pos((x,y)))

    for x in range(1, (grid_size[0]-1)):
        for y in [0, grid_size[1]-1]:
            new_surf.blit(sprites_dict["ho"], get_convert_pos((x,y)))

    return new_surf
