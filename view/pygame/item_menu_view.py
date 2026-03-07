import pygame
from settings import SHOW_RECT
from view.pygame.character_display import CharDisplay
from view.pygame.get_box_sprite import get_box_sprite
from view.pygame.battle_display_fun import get_convert_rect_from_grid_rect, get_rect, get_relative_rect, get_relative_pos_from_rect


class ItemMenuView:
    def __init__(self, grid_pos, sprite_dict, cursor_index=0):
        grid_size = 16,11
        self.grid_rect = get_rect(grid_pos, grid_size)
        self.rect = get_convert_rect_from_grid_rect(grid_pos, grid_size)
        self.sprite_dict = sprite_dict
        self.sprite = get_box_sprite(grid_size, sprite_dict)
        self.items = []
        self.items_display = []
        self.go_on_chars_display = [
            CharDisplay(get_relative_pos_from_rect((14, 1), self.grid_rect), sprite_dict, "^"),
            CharDisplay(get_relative_pos_from_rect((14, 9), self.grid_rect), sprite_dict, "µ")]

        self.blink_interval = 600
        self.shift = 0
        self.max_row = (self.grid_rect.height-3)//2
        self.cursors_display = []
        self.menu_index = cursor_index
        self.visible = False

    def init_items(self, items):
        self.items = items
        self.init_items_display()

    def init_items_display(self):
        self.reset()
        self.cursors_display = []
        for i, slot in enumerate(self.items[0+self.shift:self.max_row+self.shift]):
            if type(slot) == type(''):
                name, quantity = slot, None
            else:
                name, quantity = slot.item_name, str(slot.quantity)
            x = 2
            y = 2 + i * 2
            self.init_item_display(name, quantity,(x, y))
            self.init_cursor_display((x - 1, y))

    def init_item_display(self, name_string, quantity_string, grid_pos):
        new_item_display = []
        for i,char in enumerate(name_string):
            new_item_display.append(CharDisplay(get_relative_pos_from_rect((grid_pos[0]+i, grid_pos[1]), self.grid_rect), self.sprite_dict, char))
        if quantity_string:
            new_item_display.append(
                CharDisplay(get_relative_pos_from_rect((grid_pos[0] + 8, grid_pos[1] + 1), self.grid_rect),
                            self.sprite_dict,
                            "*"))
            for i, char in enumerate(reversed(quantity_string)):
                new_item_display.append(
                    CharDisplay(get_relative_pos_from_rect((grid_pos[0] + 10 - i, grid_pos[1] + 1), self.grid_rect),
                                self.sprite_dict, char))
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

    def update(self, cursor_index):
        self.menu_index = cursor_index
        self.update_shift()

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
            self.display_go_on_chars(surface)
            self.display_chars(surface)
            self.display_cursor(surface)
            if SHOW_RECT: pygame.draw.rect(surface, (255,0,0), self.rect, 1)

    def display_chars(self, surface):
        for item_display in self.items_display:
            for char_display in item_display:
                char_display.display(surface)

    def display_go_on_chars(self, surface):
        current_time = pygame.time.get_ticks()
        if int(current_time / self.blink_interval) % 2 == 0:
            up_char, down_char = self.go_on_chars_display
            if self.shift > 0:
                up_char.display(surface)
            if len(self.items) > self.max_row+self.shift:
                down_char.display(surface)

    def display_cursor(self, surface):
        self.cursors_display[self.menu_index-self.shift].display(surface)
