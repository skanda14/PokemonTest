import pygame
from battle_2.battle_settings import TILE_WIDTH, TILE_HEIGHT, TILE_SIZE, BACKGROUND_COLOR


def get_convert_pos(grid_pos):
    return grid_pos[0] * TILE_WIDTH, grid_pos[1] * TILE_HEIGHT

def get_convert_size(grid_size):
    return grid_size[0] * TILE_WIDTH, grid_size[1] * TILE_HEIGHT

def get_convert_rect_from_grid_rect(grid_pos, grid_size):
    return pygame.Rect(grid_pos[0] * TILE_WIDTH, grid_pos[1] * TILE_WIDTH,
                       grid_size[0] * TILE_WIDTH, grid_size[1] * TILE_HEIGHT)

def get_rect(pos, size):
    return pygame.Rect(pos, size)

def get_relative_rect(pos, size, rect_ref):
    return pygame.Rect(rect_ref.left+pos[0], rect_ref.top+pos[1], size[0], size[1])

def get_relative_pos_from_rect(pos, rect_ref):
    return rect_ref.left+pos[0], rect_ref.top+pos[1]