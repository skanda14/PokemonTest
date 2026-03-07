import pygame
from settings import SHOW_RECT
from view.pygame.character_display import CharDisplay
from view.pygame.get_box_sprite import get_box_sprite
from view.pygame.battle_display_fun import get_convert_rect_from_grid_rect, get_rect, get_relative_pos_from_rect
from view.pygame.data_move_menu_view import DataMoveView


class FightMenuView:
    def __init__(self, grid_pos, sprite_dict, cursor_index=0):
        grid_size = 16,6
        self.grid_rect = get_rect(grid_pos, grid_size)
        self.rect = get_convert_rect_from_grid_rect(grid_pos, grid_size)
        self.sprite_dict = sprite_dict
        self.sprite = get_box_sprite(grid_size, sprite_dict)
        self.items = []
        self.items_display = []
        self.fixe_items_display = []

        self.data_move_view = DataMoveView((0,8), self.sprite_dict)
        self.cursors_display = []
        self.menu_index = cursor_index
        self.visible = False
        self.init_fixe_display()

    def init_fixe_display(self):
        self.fixe_items_display = []
        new_string = "-"*4
        x,y = 2,1
        new_list = []
        for i,char in enumerate(new_string):
            new_list.append(CharDisplay((get_relative_pos_from_rect((x, y+i), self.grid_rect)), self.sprite_dict, char))
        self.fixe_items_display.append(new_list)

    def init_items(self, moves):
        self.items = moves
        self.cursors_display = []
        for i,item in enumerate(self.items):
            name = item.name.upper()
            x = 2
            y = 1 + i
            self.init_item_display(name, (x,y))
            self.init_cursor_display((x-1,y))

    def init_item_display(self, string, grid_pos):
        new_item_display = []
        for i,char in enumerate(string[:13]):
            new_item_display.append(CharDisplay(get_relative_pos_from_rect((grid_pos[0]+i, grid_pos[1]), self.grid_rect), self.sprite_dict, char))
        self.items_display.append(new_item_display)
        self.data_move_view.update_items(self.items[self.menu_index])

    def init_cursor_display(self, grid_pos):
        new_cursor = CharDisplay(get_relative_pos_from_rect(grid_pos, self.grid_rect), self.sprite_dict, ">")
        self.cursors_display.append(new_cursor)


    def show(self):
        self.visible = True
        self.data_move_view.show()

    def hide(self):
        self.visible = False
        self.data_move_view.hide()

    def reset(self):
        for item_display in self.items_display:
            for char_display in item_display:
                char_display.erase()

    def update(self, cursor_index):
        self.menu_index = cursor_index
        self.data_move_view.update_items(self.items[self.menu_index])

    def display(self, surface):
        if self.visible:
            surface.blit(self.sprite, self.rect)
            self.display_fixe_chars(surface)
            self.display_chars(surface)
            self.display_cursor(surface)
            self.data_move_view.display(surface)
            if SHOW_RECT: pygame.draw.rect(surface, (255,0,0), self.rect, 1)

    def display_chars(self, surface):
        for item_display in self.items_display:
            for char_display in item_display:
                char_display.display(surface)

    def display_fixe_chars(self, surface):
        for item_display in self.fixe_items_display:
            for char_display in item_display:
                char_display.display(surface)

    def display_cursor(self, surface):
        if self.menu_index >= 0:
            self.cursors_display[self.menu_index].display(surface)
