import pygame
from view.pygame.view_settings import SHOW_RECT, SHOW_GRID, TILE_SIZE, TILE_WIDTH, TILE_HEIGHT,BACKGROUND_COLOR
from view.pygame.character_display import CharDisplay
from view.pygame.get_box_sprite import get_box_sprite
from view.pygame.battle_display_fun import get_convert_rect_from_grid_rect, get_rect, get_relative_rect, get_relative_pos_from_rect


class MainMenuView:
    def __init__(self, grid_pos, sprite_dict):
        grid_size = 14,6
        self.grid_rect = get_rect(grid_pos, grid_size)
        self.rect = get_convert_rect_from_grid_rect(grid_pos, grid_size)
        self.sprite_dict = sprite_dict
        self.sprite = get_box_sprite(grid_size, sprite_dict)
        self.items = []
        self.items_display = []
        self.cursors_display = []
        self.menu_index = 0
        self.visible = False
        self.init_items(["ATTAQ", "%#","OBJET","FUITE"])

    def init_items(self, items):
        self.items = items
        self.cursors_display = []
        for i,name in enumerate(self.items):
            x = 2 + 6* (i%2)
            y = 2 + 2*(i//2)
            self.init_item_display(str(name), (x,y))
            self.init_cursor_display((x-1,y))

    def init_item_display(self, string, grid_pos):
        new_item_display = []
        for i,char in enumerate(string):
            new_item_display.append(CharDisplay(get_relative_pos_from_rect((grid_pos[0]+i, grid_pos[1]), self.grid_rect), self.sprite_dict, char))
        self.items_display.append(new_item_display)

    def init_cursor_display(self, grid_pos):
        new_cursor = CharDisplay(get_relative_pos_from_rect(grid_pos, self.grid_rect), self.sprite_dict, ">")
        self.cursors_display.append(new_cursor)

    def show(self):
        self.visible = True

    def hide(self):
        self.visible = False

    def update(self, cursor_index):
        self.menu_index = cursor_index

    def display(self, surface):
        if self.visible:
            surface.blit(self.sprite, self.rect)
            self.display_chars(surface)
            self.display_cursor(surface)
            if SHOW_RECT: pygame.draw.rect(surface, (255, 0, 0), self.rect, 1)

    def display_chars(self, surface):
        for item_display in self.items_display:
            for char_display in item_display:
                char_display.display(surface)

    def display_cursor(self, surface):
        self.cursors_display[self.menu_index].display(surface)
