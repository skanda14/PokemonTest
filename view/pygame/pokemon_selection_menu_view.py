import pygame
from settings import SHOW_RECT,BACKGROUND_COLOR
from view.pygame.character_display import CharDisplay
from view.pygame.battle_display_fun import get_convert_rect_from_grid_rect, get_rect, get_relative_pos_from_rect
from view.pygame.message_box_view import MessageBoxView


class PokemonSelectionMenuView:
    def __init__(self, grid_pos, sprite_dict, cursor_index=0):
        grid_size = 20,12
        self.grid_rect = get_rect(grid_pos, grid_size)
        self.rect = get_convert_rect_from_grid_rect(grid_pos, grid_size)
        self.sprite_dict = sprite_dict
        # self.sprite = get_box_sprite(grid_size, sprite_dict)
        self.sprite = pygame.Surface(self.rect.size)
        self.sprite.fill(BACKGROUND_COLOR)
        self.items = []
        self.items_display = []

        self.cursors_display = []
        self.menu_index = cursor_index
        self.message_box_view = MessageBoxView((0,12), self.sprite_dict)
        self.visible = False

    def init_items(self, moves):
        self.reset()
        self.items = moves
        self.cursors_display = []
        for i,item in enumerate(self.items):
            x = 1
            y = 0+ i*2
            self.init_item_display(item, (x,y))
            self.init_cursor_display((x-1,y))

    def init_item_display(self, item, grid_pos):
        new_item_display = SwitchPokemonDisplay(item, grid_pos, self.sprite_dict)
        # new_item_display = []
        # for i,char in enumerate(string):
        #     new_item_display.append(CharDisplay(get_relative_pos_from_rect((grid_pos[0]+i, grid_pos[1]), self.grid_rect), self.sprite_dict, char))
        self.items_display.append(new_item_display)

    def init_cursor_display(self, grid_pos):
        new_cursor = CharDisplay(get_relative_pos_from_rect(grid_pos, self.grid_rect), self.sprite_dict, ">")
        self.cursors_display.append(new_cursor)


    def show(self):
        self.visible = True

    def hide(self):
        self.visible = False

    def reset(self):
        self.items_display = []

    def update(self, cursor_index):
        self.menu_index = cursor_index

    def display(self, surface):
        if self.visible:
            surface.blit(self.sprite, self.rect)
            self.message_box_view.display(surface)
            self.display_chars(surface)
            self.display_cursor(surface)
            if SHOW_RECT: pygame.draw.rect(surface, (255,0,0), self.rect, 1)

    def display_chars(self, surface):
        for item_display in self.items_display:
            item_display.display(surface)

    def display_cursor(self, surface):
        self.cursors_display[self.menu_index].display(surface)



############################################################################################
############################################################################################
############################################################################################

class SwitchPokemonDisplay:
    def __init__(self, pokemon, grid_pos, sprites_dict):
        grid_size = 19,2
        self.grid_rect = get_rect(grid_pos, grid_size)
        self.rect = get_convert_rect_from_grid_rect(grid_pos, grid_size)
        self.sprite = pygame.Surface((self.rect.height, self.rect.height))
        self.sprite.fill((247,0,0))
        pygame.draw.rect(self.sprite, (0,0,0), self.sprite.get_rect(), 1)
        self.sprite.set_alpha(50)
        self.name_display = NameDisplay(get_relative_pos_from_rect((2, 0), self.grid_rect), sprites_dict, pokemon)
        self.level_display = LevelDisplay(get_relative_pos_from_rect((12,0), self.grid_rect), sprites_dict, pokemon)
        self.life_bar_display = LifeBarDisplay(get_relative_pos_from_rect((3,1), self.grid_rect), sprites_dict, pokemon)
        self.life_display = LifeDisplay(get_relative_pos_from_rect((12,1), self.grid_rect), sprites_dict, pokemon)
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
    def __init__(self, grid_pos, sprites_dict, pokemon):
        grid_size = 10,1
        self.grid_rect = get_rect(grid_pos, grid_size)
        self.rect = get_convert_rect_from_grid_rect(grid_pos, grid_size)
        self.chars_display = [CharDisplay(get_relative_pos_from_rect((i, 0), self.grid_rect), sprites_dict) for i in range(grid_size[0])]
        self.modify(pokemon.name)
        self.visible = True

    def show(self):
        self.visible = True

    def hide(self):
        self.visible = False

    def modify(self, name):
        if name:
            max_chars = len(self.chars_display)
            formated_string = str(name.upper())[:max_chars]
            while len(formated_string) < max_chars: formated_string = formated_string+" "
            [char_display.update(char) for char, char_display in zip(formated_string, self.chars_display)]

    def display(self, surface):
        if self.visible:
            [char.display(surface) for char in self.chars_display]
            # pygame.draw.rect(surface, (0,0,255), self.rect, 1)

# #########################################################################################################

class LevelDisplay:
    def __init__(self, grid_pos, sprites_dict, pokemon):
        grid_size = 4,1
        self.grid_rect = get_rect(grid_pos, grid_size)
        self.rect = get_convert_rect_from_grid_rect(grid_pos, grid_size)
        path = "assets/sprites/battle interface/level_label.png"
        self.sprite = pygame.image.load(path).convert_alpha()
        self.chars_display = [CharDisplay(get_relative_pos_from_rect((1+i, 0), self.grid_rect), sprites_dict) for i in range(grid_size[0])]
        self.modify(pokemon)
        self.visible = True

    def show(self):
        self.visible = True

    def hide(self):
        self.visible = False

    def modify(self, pokemon):
        level = pokemon.level
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
    def __init__(self, grid_pos, sprites_dict, pokemon):
        grid_size = 8,1
        self.grid_rect = get_rect(grid_pos, grid_size)
        self.rect = get_convert_rect_from_grid_rect(grid_pos, grid_size)
        self.inner_rect = pygame.Rect(self.rect.left+2*8, self.rect.top+8*3/8, 6*8, 8//4)
        path = "assets/sprites/battle interface/life_bar.png"
        self.sprite = pygame.image.load(path).convert_alpha()
        self.completion = 0
        self.colors = [(72,160,88), (208,160,0), (208,80,48)]
        self.color_index = 0
        self.modify(pokemon)
        self.visible = True

    def show(self):
        self.visible = True

    def hide(self):
        self.visible = False

    def modify(self, pokemon):
        self.completion = round(pokemon.stats['hp']/pokemon.stats['max_hp'], 1)
        if self.completion >= 0.6: self.color_index = 0
        elif self.completion >= 0.3: self.color_index = 1
        else: self.color_index = 2

    def display(self, surface):
        if self.visible:
            surface.blit(self.sprite, self.rect)
            pygame.draw.rect(surface, self.colors[self.color_index], (self.inner_rect.topleft, (self.inner_rect.width*self.completion, self.inner_rect.height)), 0)

# #########################################################################################################

class LifeDisplay:
    def __init__(self, grid_pos, sprites_dict, pokemon):
        grid_size = 7,1
        self.grid_rect = get_rect(grid_pos, grid_size)
        self.rect = get_convert_rect_from_grid_rect(grid_pos, grid_size)
        self.chars_display = [CharDisplay(get_relative_pos_from_rect((i, 0), self.grid_rect), sprites_dict) for i in range(grid_size[0])]
        self.string = None
        self.modify(pokemon)
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

    def modify(self, pokemon):
        current_hp, max_hp = pokemon.stats['hp'], pokemon.stats['max_hp']
        self.string = self.get_formated_string(current_hp, max_hp)
        [char_display.update(char) for char, char_display in zip(self.string, self.chars_display)]

    def display(self, surface):
        if self.visible:
            [char.display(surface) for char in self.chars_display]
