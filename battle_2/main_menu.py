import pygame
from battle_2.battle_settings import SHOW_RECT, SHOW_GRID, TILE_SIZE, TILE_WIDTH, TILE_HEIGHT,BACKGROUND_COLOR
from battle_2.character_display import CharDisplay
from battle_2.get_box_sprite import get_box_sprite
from battle_2.battle_display_fun import get_convert_rect_from_grid_rect, get_rect, get_relative_rect, get_relative_pos_from_rect
from battle_2.move_menu_display import MoveMenuDisplay
from battle_2.switch_menu_display import SwitchMenuDisplay
from battle_2.item_menu_display import ItemMenuDisplay


class MainMenuDisplay:
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
        self.visible = True
        self.pokemon = None
        self.init_items([
            ("ATTAQ", MoveMenuDisplay, (4,12)),
            ("%#", SwitchMenuDisplay, (0,0)),
            ("OBJET", ItemMenuDisplay, (4,2)),
            ("FUITE", None, (0,0))])
        self.current_menu = None

    def init_items(self, items):
        self.items = items
        self.cursors_display = []
        for i,item_tuple in enumerate(self.items):
            name, class_menu, grid_pos = item_tuple
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

    def update(self, events, current_pokemon):
        self.pokemon = current_pokemon
        choice = None
        if self.current_menu:
            choice = self.current_menu.update(events)
            if choice:
                self.visible = True
                self.current_menu = None
        else:
            for event in events:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        name, class_menu, grid_pos = self.items[self.menu_index]
                        if name == "FUITE":
                            choice = "Fuite!"
                        else:
                            self.visible = False
                            self.current_menu = class_menu(grid_pos, self.sprite_dict, self.pokemon)
                    elif event.key == pygame.K_RIGHT:
                        self.menu_index = self.menu_index + 1 if self.menu_index%2 == 0 else self.menu_index - 1
                    elif event.key == pygame.K_LEFT:
                        self.menu_index = self.menu_index + 1 if self.menu_index%2 == 0 else self.menu_index - 1
                    elif event.key == pygame.K_DOWN:
                        self.menu_index = (self.menu_index + 2) % len(self.items)
                    elif event.key == pygame.K_UP:
                        self.menu_index = (self.menu_index - 2) % len(self.items)
        return choice

    def display(self, surface):
        if self.visible:
            surface.blit(self.sprite, self.rect)
            self.display_chars(surface)
            self.display_cursor(surface)
            if SHOW_RECT: pygame.draw.rect(surface, (255, 0, 0), self.rect, 1)
        if self.current_menu:
            self.current_menu.display(surface)

    def display_chars(self, surface):
        for item_display in self.items_display:
            for char_display in item_display:
                char_display.display(surface)

    def display_cursor(self, surface):
        self.cursors_display[self.menu_index].display(surface)
