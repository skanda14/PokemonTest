import pygame
from view.pygame.view_settings import SHOW_RECT, SHOW_GRID, TILE_SIZE, TILE_WIDTH, TILE_HEIGHT,BACKGROUND_COLOR
from view.pygame.character_display import CharDisplay
from view.pygame.get_box_sprite import get_box_sprite
from view.pygame.battle_display_fun import get_convert_rect_from_grid_rect, get_rect, get_relative_rect, get_relative_pos_from_rect


class DataMoveView:
    def __init__(self, grid_pos, sprite_dict):
        grid_size = 11,5
        self.grid_rect = get_rect(grid_pos, grid_size)
        self.rect = get_convert_rect_from_grid_rect(grid_pos, grid_size)
        self.sprite_dict = sprite_dict
        self.sprite = get_box_sprite(grid_size, sprite_dict)
        self.items = []
        self.items_display = []
        self.fixe_items_display = []
        self.visible = False
        self.init_fixe_display()
        # self.init_items()

    def init_items(self, move):
        self.reset()
        data = (move.move_type.upper(), move.current_pp, move.max_pp)
        for i, item in enumerate(data):
            if i == 0:
                x, y = 9, 2
            elif i == 1:
                x, y = 6, 3
            elif i == 2:
                x, y = 9, 3
            else:
                x, y = 0, 0
            self.init_item_display(str(item), (x, y))

    def init_fixe_display(self):
        self.fixe_items_display = []
        new_string = "TYPE/"
        x,y = 1,1
        new_list = []
        for i,char in enumerate(new_string):
            new_list.append(CharDisplay((get_relative_pos_from_rect((x+i, y), self.grid_rect)), self.sprite_dict, char))
        self.fixe_items_display.append(new_list)
        new_list = [CharDisplay((get_relative_pos_from_rect((7, 3), self.grid_rect)), self.sprite_dict, "/")]
        self.fixe_items_display.append(new_list)

    def init_item_display(self, string, grid_pos):
        new_item_display = []
        for i,char in enumerate(reversed(string)):
            new_item_display.append(CharDisplay(get_relative_pos_from_rect((grid_pos[0]-i, grid_pos[1]), self.grid_rect), self.sprite_dict, char))
        self.items_display.append(new_item_display)

    def show(self):
        self.visible = True

    def hide(self):
        self.visible = False

    def reset(self):
        for item_display in self.items_display:
            for char_display in item_display:
                char_display.erase()

    def update_items(self, move):
        self.items = move
        self.init_items(move)

    def display(self, surface):
        if self.visible:
            surface.blit(self.sprite, self.rect)
            self.display_chars(surface)
            self.display_fixe_chars(surface)
            if SHOW_RECT: pygame.draw.rect(surface, (255,0,0), self.rect, 1)

    def display_chars(self, surface):
        for item_display in self.items_display:
            for char_display in item_display:
                char_display.display(surface)

    def display_fixe_chars(self, surface):
        for item_display in self.fixe_items_display:
            for char_display in item_display:
                char_display.display(surface)
