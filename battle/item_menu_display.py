import pygame
import random
from battle.battle_settings import SHOW_RECT, SHOW_GRID, TILE_SIZE, TILE_WIDTH, TILE_HEIGHT,BACKGROUND_COLOR
from battle.item_target_choice_menu_display import ItemTargetChoiceMenuDisplay
from message_system.character_display import CharDisplay
from battle.get_box_sprite import get_box_sprite
from battle.battle_display_fun import get_convert_rect_from_grid_rect, get_rect, get_relative_rect, get_relative_pos_from_rect


class ItemMenuDisplay:
    def __init__(self, grid_pos, sprite_dict, item_target_menu):
        grid_size = 16,11
        self.grid_rect = get_rect(grid_pos, grid_size)
        self.rect = get_convert_rect_from_grid_rect(grid_pos, grid_size)
        self.sprite_dict = sprite_dict
        self.sprite = get_box_sprite(grid_size, sprite_dict)
        self.items = []
        self.items_display = []
        self.cursors_display = []
        self.go_on_chars_display = [
            CharDisplay(get_relative_pos_from_rect((14,1), self.grid_rect), sprite_dict, "^"),
            CharDisplay(get_relative_pos_from_rect((14,9), self.grid_rect), sprite_dict, "µ")]
        self.menu_index = 0
        self.max_row = (self.grid_rect.height-3)//2
        self.blink_interval = 600
        self.shift = 0
        self.visible = True
        self.init_items([("Potion"+chr(65+i), random.randint(1,10)) for i in range(6)]+["RETOUR"])
        self.init_items_display()
        self.item_target_menu_display = item_target_menu

    def init_items(self, items):
        self.items = items

    def init_items_display(self):
        self.reset()
        self.cursors_display = []
        for i, item_tuple in enumerate(self.items[0+self.shift:self.max_row+self.shift]):
            if len(item_tuple) == 2:
                item, number = item_tuple
                number = str(number)
            else:
                item,number = item_tuple, None
            x = 2
            y = 2 + i * 2
            self.init_item_display(str(item), number, (x, y))
            self.init_cursor_display((x-1,y))

    def init_item_display(self, string, number, grid_pos):
        new_item_display = []
        for i,char in enumerate(string):
            new_item_display.append(CharDisplay(get_relative_pos_from_rect((grid_pos[0]+i, grid_pos[1]), self.grid_rect), self.sprite_dict, char))

        if number:
            new_item_display.append(
                CharDisplay(get_relative_pos_from_rect((grid_pos[0]+8, grid_pos[1]+1), self.grid_rect), self.sprite_dict,
                            "*"))
            for i,char in enumerate(reversed(str(number))):
                new_item_display.append(CharDisplay(get_relative_pos_from_rect((grid_pos[0]+10-i,grid_pos[1]+1), self.grid_rect), self.sprite_dict, char))
        self.items_display.append(new_item_display)

    def init_cursor_display(self, grid_pos):
        new_cursor = CharDisplay(get_relative_pos_from_rect(grid_pos, self.grid_rect), self.sprite_dict, ">")
        self.cursors_display.append(new_cursor)

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
                if event.key == pygame.K_ESCAPE:
                    choice = "MAIN_MENU"
                elif event.key == pygame.K_SPACE:
                    string = self.items[self.menu_index]
                    choice = string
                    if choice == "RETOUR":
                        choice = "MAIN_MENU"
                    else:
                        self.item_target_menu_display.selected_item = string
                        choice = "ITEM_TARGET_MENU"
                elif event.key == pygame.K_DOWN:
                    self.menu_index = (self.menu_index + 1) % len(self.items)
                    self.update_shift()
                elif event.key == pygame.K_UP:
                    self.menu_index = (self.menu_index - 1) % len(self.items)
                    self.update_shift()
        return choice

    def update_shift(self):
        if self.menu_index >= self.max_row-1 + self.shift:
            self.shift = self.menu_index - (self.max_row - 1)+1
            self.init_items_display()
        elif self.menu_index < self.shift:
            self.shift = self.menu_index
            self.init_items_display()

    def display(self, surface):
        if self.visible:
            surface.blit(self.sprite, self.rect)
            self.display_chars(surface)
            self.display_go_on_chars(surface)
            self.display_cursor(surface)
            if SHOW_RECT: pygame.draw.rect(surface, (255,0,0), self.rect, 1)

    def display_chars(self, surface):
        for item_display in self.items_display:
            for char_display in item_display:
                char_display.display(surface)

    def display_cursor(self, surface):
        self.cursors_display[self.menu_index-self.shift].display(surface)

    def display_go_on_chars(self, surface):
        current_time = pygame.time.get_ticks()
        if int(current_time / self.blink_interval) % 2 == 0:
            up_char, down_char = self.go_on_chars_display
            if self.shift > 0:
                up_char.display(surface)
            if len(self.items) > self.max_row+self.shift:
                down_char.display(surface)
