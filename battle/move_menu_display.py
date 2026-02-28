import pygame
from battle.battle_settings import SHOW_RECT, SHOW_GRID, TILE_SIZE, TILE_WIDTH, TILE_HEIGHT,BACKGROUND_COLOR
from message_system.character_display import CharDisplay
from battle.get_box_sprite import get_box_sprite
from battle.battle_display_fun import get_convert_rect_from_grid_rect, get_rect, get_relative_rect, get_relative_pos_from_rect


class MoveMenuDisplay:
    def __init__(self, grid_pos, move_data_menu, sprite_dict):
        grid_size = 16,6
        self.grid_rect = get_rect(grid_pos, grid_size)
        self.rect = get_convert_rect_from_grid_rect(grid_pos, grid_size)
        self.sprite_dict = sprite_dict
        self.sprite = get_box_sprite(grid_size, sprite_dict)
        self.items = []
        self.items_display = []
        self.fixe_items_display = []

        self.move_data_menu = move_data_menu
        self.cursors_display = []
        self.menu_index = 0
        self.visible = True
        self.init_fixe_display()
        self.init_items([("ECLAIR", "ELECTRIK", 12,30), ("MIMI-QUEUE", "NORMAL", 5, 30), ("RUGISSEMENT", "NORMAL", 31, 40)])

    def init_fixe_display(self):
        self.fixe_items_display = []
        new_string = "-"*4
        x,y = 2,1
        new_list = []
        for i,char in enumerate(new_string):
            new_list.append(CharDisplay((get_relative_pos_from_rect((x, y+i), self.grid_rect)), self.sprite_dict, char))
        self.fixe_items_display.append(new_list)

    def init_items(self, items):
        self.items = items
        self.cursors_display = []
        for i,item_tuple in enumerate(self.items):
            x = 2
            y = 1 + i
            self.init_item_display(str(item_tuple[0]), (x,y))
            self.init_cursor_display((x-1,y))

    def init_item_display(self, string, grid_pos):
        new_item_display = []
        for i,char in enumerate(string):
            new_item_display.append(CharDisplay(get_relative_pos_from_rect((grid_pos[0]+i, grid_pos[1]), self.grid_rect), self.sprite_dict, char))
        self.items_display.append(new_item_display)
        self.update_move_datat_display()

    def init_cursor_display(self, grid_pos):
        new_cursor = CharDisplay(get_relative_pos_from_rect(grid_pos, self.grid_rect), self.sprite_dict, ">")
        self.cursors_display.append(new_cursor)

    def update_move_datat_display(self):
        data = self.items[self.menu_index]
        self.move_data_menu.init_items(data[1:])

    def show(self):
        self.visible = True

    def hide(self):
        self.visible = False

    def reset(self):
        for item_display in self.items_display:
            for char_display in item_display:
                char_display.erase()

    def update(self, events):
        choice = None
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    string = self.items[self.menu_index]
                    choice = string
                elif event.key == pygame.K_ESCAPE:
                    choice = "MAIN_MENU"
                elif event.key == pygame.K_DOWN:
                    self.menu_index = (self.menu_index + 1) % len(self.items)
                    self.update_move_datat_display()
                elif event.key == pygame.K_UP:
                    self.menu_index = (self.menu_index - 1) % len(self.items)
                    self.update_move_datat_display()
        return choice

    def display(self, surface):
        if self.visible:
            surface.blit(self.sprite, self.rect)
            self.display_fixe_chars(surface)
            self.display_chars(surface)
            self.display_cursor(surface)
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
        self.cursors_display[self.menu_index].display(surface)
