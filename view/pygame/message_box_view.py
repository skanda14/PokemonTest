from view.pygame.battle_display_fun import get_rect,  get_convert_rect_from_grid_rect, get_relative_pos_from_rect
from view.pygame.get_box_sprite import get_box_sprite
from view.pygame.character_display import CharDisplay
import pygame


class MessageBoxView:
    GRID_SIZE = (20,6)
    def __init__(self, grid_pos, sprites_dict):
        self.grid_rect = get_rect(grid_pos, self.GRID_SIZE)
        self.rect = get_convert_rect_from_grid_rect(grid_pos, self.GRID_SIZE)
        self.sprites_dict = sprites_dict
        self.sprite = get_box_sprite(self.GRID_SIZE, self.sprites_dict)
        self.chars_display = [
            [CharDisplay(get_relative_pos_from_rect((x,y), self.grid_rect), self.sprites_dict)
             for x in range(1, self.GRID_SIZE[0]-2)]
            for y in range(1, self.GRID_SIZE[1]-1)]
        self.go_on_char = CharDisplay(get_relative_pos_from_rect((self.GRID_SIZE[0]-2, self.GRID_SIZE[1]-2), self.grid_rect), sprites_dict, "µ")
        self.column_len = len(self.chars_display[0])
        self.row_len = len(self.chars_display)
        self.blink_interval = 600
        self.visible = False
        self.showing_cursor = False

    def show(self):
        self.visible = True

    def hide(self):
        self.visible = False

    def display_a_character(self, grid_pos, char):
        self.chars_display[grid_pos[1]][grid_pos[0]].update(char)

    def erase_all_lines(self):
        for i in range(self.row_len):
            self.erase_a_line(i)

    def erase_a_line(self, n):
        for char in self.chars_display[n]:
            char.update(None)

    def scroll_upward(self):
        for y in range(1, self.row_len):
            for x in range(self.column_len):
                above_char = self.chars_display[y-1][x]
                below_char = self.chars_display[y][x]
                above_char.cut(below_char)

    ##########################################################################
    ##########################################################################
    ##########################################################################


    def display(self, surface):
        if self.visible:
            surface.blit(self.sprite, self.rect)
            self.display_chars(surface)
            self.display_go_on_char(surface)

    def display_chars(self, surface):
        for line in self.chars_display:
            for char in line:
                char.display(surface)

    def display_go_on_char(self, surface):
        if self.showing_cursor:
            if (pygame.time.get_ticks() // self.blink_interval) % 2 == 0:
                self.go_on_char.display(surface)
