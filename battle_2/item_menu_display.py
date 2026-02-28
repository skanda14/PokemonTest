import pygame
import random
from battle_2.battle_settings import SHOW_RECT, SHOW_GRID, TILE_SIZE, TILE_WIDTH, TILE_HEIGHT,BACKGROUND_COLOR
from battle_2.item_target_choice_menu_display import ItemTargetChoiceMenuDisplay
from battle_2.character_display import CharDisplay
from battle_2.get_box_sprite import get_box_sprite
from battle_2.battle_display_fun import get_convert_rect_from_grid_rect, get_rect, get_relative_rect, get_relative_pos_from_rect
from battle_2.item_target_choice_menu_display import ItemTargetChoiceMenuDisplay


class ItemMenuDisplay:
    def __init__(self, grid_pos, sprite_dict):
        grid_size = 16,11
        self.grid_rect = get_rect(grid_pos, grid_size)
        self.rect = get_convert_rect_from_grid_rect(grid_pos, grid_size)
        self.sprite_dict = sprite_dict
        self.sprite = get_box_sprite(grid_size, sprite_dict)
        self.items = []
        self.items_display = []
        self.cursors_display = []
        self.cursors_2_display = []
        self.go_on_chars_display = [
            CharDisplay(get_relative_pos_from_rect((14,1), self.grid_rect), sprite_dict, "^"),
            CharDisplay(get_relative_pos_from_rect((14,9), self.grid_rect), sprite_dict, "µ")]
        self.menu_index = 0
        self.menu_index_2 = -1
        self.max_row = (self.grid_rect.height-3)//2
        self.blink_interval = 600
        self.shift = 0
        self.visible = True
        self.init_items([("Potion"+chr(65+i), random.randint(1,10)) for i in range(6)]+["RETOUR"])
        self.init_items_display()
        self.item_target_menu_class = ItemTargetChoiceMenuDisplay
        self.current_menu = None

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
            self.init_cursor_2_display((x-1,y))

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

    def init_cursor_2_display(self, grid_pos):
        new_cursor = CharDisplay(get_relative_pos_from_rect(grid_pos, self.grid_rect), self.sprite_dict, "<")
        self.cursors_2_display.append(new_cursor)

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
        if self.current_menu:
            choice = self.current_menu.update(events)
            if choice:
                self.current_menu = None
                if choice == "BACK":
                    choice = None
        else:
            for event in events:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        choice = "BACK"
                    elif event.key == pygame.K_SPACE:
                        string = self.items[self.menu_index]
                        if string == "RETOUR":
                            choice = "BACK"
                        else:
                            self.current_menu  = self.item_target_menu_class((0,0), string, self.sprite_dict)
                    elif event.key == pygame.K_LCTRL: # switch items places
                        if self.menu_index != len(self.items)-1:
                            if self.menu_index_2 > -1:
                                if self.menu_index_2 == self.menu_index:
                                    self.menu_index_2 = -1
                                else:
                                    # print(f"{self.menu_index_2} <=> {self.menu_index}")
                                    self.items[self.menu_index_2], self.items[self.menu_index] = self.items[
                                        self.menu_index], self.items[self.menu_index_2]
                                    self.menu_index_2 = -1
                                    self.init_items_display()
                            else:
                                self.menu_index_2 = self.menu_index
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
            self.display_cursor_2(surface)
            self.display_cursor(surface)
            if SHOW_RECT: pygame.draw.rect(surface, (255,0,0), self.rect, 1)
        if self.current_menu:
            self.current_menu.display(surface)

    def display_chars(self, surface):
        for item_display in self.items_display:
            for char_display in item_display:
                char_display.display(surface)

    def display_cursor(self, surface):
        self.cursors_display[self.menu_index-self.shift].display(surface)

    def display_cursor_2(self, surface):
        if self.menu_index_2 > -1:
            if self.shift <= self.menu_index_2 <= self.shift+self.max_row-1:
                self.cursors_2_display[self.menu_index_2-self.shift].display(surface)

    def display_go_on_chars(self, surface):
        current_time = pygame.time.get_ticks()
        if int(current_time / self.blink_interval) % 2 == 0:
            up_char, down_char = self.go_on_chars_display
            if self.shift > 0:
                up_char.display(surface)
            if len(self.items) > self.max_row+self.shift:
                down_char.display(surface)
