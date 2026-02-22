import pygame
from battle_zoom.settings import ZOOM, ORIGINAL_TILE_WIDTH, ORIGINAL_TILE_HEIGHT


# def get_original_rect_from_grid_data(*args):
#     if len(args) == 1:
#         grid_x, grid_y, grid_w, grid_h = args[0]
#     if len(args) == 1:
#         grid_x, grid_y, grid_w, grid_h = args[0]
#     elif len(args) == 2:
#         grid_x, grid_y = args[0]
#         grid_w, grid_h = args[1]
#     elif len(args) == 4:
#         grid_x, grid_y, grid_w, grid_h = args[0], args[1], args[2], args[3]
#     else:
#         print("Wrong arguments len for rect creation from grid data")
#         grid_x, grid_y, grid_w, grid_h = 0,0,0,0
#     return pygame.Rect(grid_x * ORIGINAL_TILE_WIDTH, grid_y * ORIGINAL_TILE_HEIGHT,
#                                 grid_w * ORIGINAL_TILE_WIDTH, grid_h * ORIGINAL_TILE_HEIGHT)


def get_original_rect_from_grid_data(*args):
    args = args[0]
    if len(args) == 1:
        grid_x, grid_y, grid_w, grid_h = args[0]
    elif len(args) == 2:
        grid_x, grid_y = args[0]
        grid_w, grid_h = args[1]
    elif len(args) == 4:
        grid_x, grid_y, grid_w, grid_h = args[0], args[1], args[2], args[3]
    else:
        print("Wrong arguments len for rect creation from grid data")
        grid_x, grid_y, grid_w, grid_h = 0,0,0,0
    return pygame.Rect(grid_x * ORIGINAL_TILE_WIDTH, grid_y * ORIGINAL_TILE_HEIGHT,
                                grid_w * ORIGINAL_TILE_WIDTH, grid_h * ORIGINAL_TILE_HEIGHT)

def get_converted_rect(parent_rect, rect):
    if isinstance(rect, tuple): # cas tuple
        if len(rect) == 2:  # forme (pos, size)
            return pygame.Rect(get_converted_pos(parent_rect, rect[0]), get_converted_size(rect[1]))
        else:  # forme (x, y, width, height)
            return pygame.Rect(get_converted_pos(parent_rect, (rect[0],rect[1])), get_converted_size((rect[2], rect[3])))
    else:  # cas pygame.Rect()
        return pygame.Rect(get_converted_pos(parent_rect, rect.topleft), get_converted_size(rect.size))

def get_converted_pos(parent_rect, pos):
    x,y = pos
    return get_converted_x(parent_rect, x),get_converted_y(parent_rect, y)

def get_converted_x(parent_rect, x):
    converted_x = parent_rect.left + x * ZOOM
    return converted_x

def get_converted_y(parent_rect, y):
    converted_y = parent_rect.top + y * ZOOM
    return converted_y

def get_converted_size(size):
    width, height = size
    return get_converted_width(width),get_converted_height(height)

def get_converted_width(width):
    return width*ZOOM

def get_converted_height(height):
    return height * ZOOM
