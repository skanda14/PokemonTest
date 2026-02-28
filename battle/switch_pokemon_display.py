from battle.battle_display_fun import get_rect, get_convert_rect_from_grid_rect, get_relative_pos_from_rect
from battle.battle_settings import SHOW_RECT
from message_system.character_display import CharDisplay
import pygame


class SwitchPokemonDisplay:
    def __init__(self, name, grid_pos, sprites_dict):
        grid_size = 19,2
        self.grid_rect = get_rect(grid_pos, grid_size)
        self.rect = get_convert_rect_from_grid_rect(grid_pos, grid_size)
        self.sprite = pygame.Surface((self.rect.height, self.rect.height))
        self.sprite.fill((247,0,0))
        pygame.draw.rect(self.sprite, (0,0,0), self.sprite.get_rect(), 1)
        self.sprite.set_alpha(50)
        self.name_display = NameDisplay(get_relative_pos_from_rect((2, 0), self.grid_rect), sprites_dict, name)
        self.level_display = LevelDisplay(get_relative_pos_from_rect((12,0), self.grid_rect), sprites_dict, 78)
        self.life_bar_display = LifeBarDisplay(get_relative_pos_from_rect((3,1), self.grid_rect), sprites_dict, 0.5)
        self.life_display = LifeDisplay(get_relative_pos_from_rect((12,1), self.grid_rect), sprites_dict, 123, 456)
        self.visible = True

    def display(self, surface):
        if self.visible:
            surface.blit(self.sprite, self.rect)
            self.life_bar_display.display(surface)
            self.name_display.display(surface)
            self.level_display.display(surface)
            self.life_display.display(surface)
            if SHOW_RECT: pygame.draw.rect(surface, (255,0,0), self.rect, 1)



# #####################################################################################
# #####################################################################################

class NameDisplay:
    def __init__(self, grid_pos, sprites_dict, name=None):
        grid_size = 10,1
        self.grid_rect = get_rect(grid_pos, grid_size)
        self.rect = get_convert_rect_from_grid_rect(grid_pos, grid_size)
        self.chars_display = [CharDisplay(get_relative_pos_from_rect((i, 0), self.grid_rect), sprites_dict) for i in range(grid_size[0])]
        self.modify(name)
        self.visible = True

    def show(self):
        self.visible = True

    def hide(self):
        self.visible = False

    def modify(self, name):
        if name:
            max_chars = len(self.chars_display)
            formated_string = str(name)[:max_chars]
            while len(formated_string) < max_chars: formated_string = formated_string+" "
            [char_display.update(char) for char, char_display in zip(formated_string, self.chars_display)]

    def display(self, surface):
        if self.visible:
            [char.display(surface) for char in self.chars_display]
            # pygame.draw.rect(surface, (0,0,255), self.rect, 1)

# #########################################################################################################

class LevelDisplay:
    def __init__(self, grid_pos, sprites_dict, level=None):
        grid_size = 4,1
        self.grid_rect = get_rect(grid_pos, grid_size)
        self.rect = get_convert_rect_from_grid_rect(grid_pos, grid_size)
        path = "assets/sprites/battle interface/level_label.png"
        self.sprite = pygame.image.load(path).convert_alpha()
        self.chars_display = [CharDisplay(get_relative_pos_from_rect((1+i, 0), self.grid_rect), sprites_dict) for i in range(grid_size[0])]
        self.modify(level)
        self.visible = True

    def show(self):
        self.visible = True

    def hide(self):
        self.visible = False

    def modify(self, level):
        if level:
            max_chars = len(self.chars_display)
            formated_string = str(level)[:max_chars]
            while len(formated_string) < max_chars: formated_string = formated_string+" "
            [char_display.update(char) for char, char_display in zip(formated_string, self.chars_display)]

    def display(self, surface):
        if self.visible:
            surface.blit(self.sprite, self.rect)
            [char.display(surface) for char in self.chars_display]

# #########################################################################################################

class LifeBarDisplay:
    def __init__(self, grid_pos, sprites_dict, completion=0.0):
        grid_size = 8,1
        self.grid_rect = get_rect(grid_pos, grid_size)
        self.rect = get_convert_rect_from_grid_rect(grid_pos, grid_size)
        self.inner_rect = pygame.Rect(self.rect.left+2*8, self.rect.top+8*3/8, 6*8, 8//4)
        path = "assets/sprites/battle interface/life_bar.png"
        self.sprite = pygame.image.load(path).convert_alpha()
        self.completion = completion
        self.colors = [(72,160,88), (208,160,0), (208,80,48)]
        self.color_index = 0
        self.modify(completion)
        self.visible = True

    def show(self):
        self.visible = True

    def hide(self):
        self.visible = False

    def modify(self, new_completion):
        self.completion = new_completion
        if self.completion >= 0.6: self.color_index = 0
        elif self.completion >= 0.3: self.color_index = 1
        else: self.color_index = 2

    def display(self, surface):
        if self.visible:
            surface.blit(self.sprite, self.rect)
            pygame.draw.rect(surface, self.colors[self.color_index], (self.inner_rect.topleft, (self.inner_rect.width*self.completion, self.inner_rect.height)), 0)

# #########################################################################################################

class LifeDisplay:
    def __init__(self, grid_pos, sprites_dict, current_hp=0, max_hp=0):
        grid_size = 7,1
        self.grid_rect = get_rect(grid_pos, grid_size)
        self.rect = get_convert_rect_from_grid_rect(grid_pos, grid_size)
        self.chars_display = [CharDisplay(get_relative_pos_from_rect((i, 0), self.grid_rect), sprites_dict) for i in range(grid_size[0])]
        self.string = None
        self.modify(current_hp, max_hp)
        self.visible = True

    def show(self):
        self.visible = True

    def hide(self):
        self.visible = False

    def get_formated_string(self, current_hp, max_hp):
        current_hp = str(int(current_hp))
        while len(current_hp) < 3: current_hp = " " + current_hp
        max_hp = str(int(max_hp))
        while len(max_hp) < 3: max_hp = " " + max_hp
        return current_hp+"/"+max_hp

    def modify(self, current_hp, max_hp):
        self.string = self.get_formated_string(current_hp, max_hp)
        [char_display.update(char) for char, char_display in zip(self.string, self.chars_display)]

    def display(self, surface):
        if self.visible:
            [char.display(surface) for char in self.chars_display]