import pygame
from battle.settings import TILE_WIDTH, TILE_HEIGHT


def get_converted_rect(parent_rect, rect):
    if isinstance(rect, tuple): # cas tuple
        if len(rect) == 1:  # forme (pos, size)
            return pygame.Rect(get_converted_pos(parent_rect, (rect[0],rect[1])), get_converted_size((rect[2], rect[3])))
        elif len(rect) == 2:  # forme (pos, size)
            return pygame.Rect(get_converted_pos(parent_rect, rect[0]), get_converted_size(rect[1]))
        else:  # forme (x, y, width, height)
            return pygame.Rect(get_converted_pos(parent_rect, (rect[0],rect[1])), get_converted_size((rect[2], rect[3])))
    else:  # cas pygame.Rect()
        return pygame.Rect(get_converted_pos(parent_rect, rect.topleft), get_converted_size(rect.size))

def get_converted_pos(parent_rect, pos):
    x,y = pos
    return get_converted_x(parent_rect, x),get_converted_y(parent_rect, y)

def get_converted_x(parent_rect, x):
    return parent_rect.left + x*TILE_WIDTH

def get_converted_y(parent_rect, y):
    return parent_rect.top + y*TILE_HEIGHT

def get_converted_size(size):
    width, height = size
    return get_converted_width(width),get_converted_height(height)

def get_converted_width(width):
    return width*TILE_WIDTH

def get_converted_height(height):
    return height * TILE_HEIGHT
