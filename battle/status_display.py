import pygame
from battle.status_display_fun import get_converted_rect
from battle.settings import SHOW_RECT, SHOW_GRID, TILE_SIZE, TILE_WIDTH, TILE_HEIGHT, BOTTOM_STATUS_SIZE, TOP_STATUS_SIZE
from battle.character_display import CharDisplay


class StatusHUD:
    def __init__(self, grid_pos, grid_size, sprites_dict, name_grid, level_grid, life_bar_grid, life_grid, hook_grid, name, level, current_hp, max_hp, top=True):
        self.tile_width, self.tile_height = self.tile_size = TILE_SIZE
        self.rect = pygame.Rect(grid_pos[0]*TILE_WIDTH, grid_pos[1]*TILE_WIDTH, grid_size[0]*TILE_WIDTH, grid_size[1]*TILE_HEIGHT)
        self.name_rect = get_converted_rect(self.rect, name_grid)
        self.name_display = NameDisplay(self.name_rect, sprites_dict, name)

        self.level_rect = get_converted_rect(self.rect, level_grid)
        self.level_display = LevelDisplay(self.level_rect, sprites_dict, level)

        self.life_bar_rect = get_converted_rect(self.rect, life_bar_grid)
        self.life_bar_display = LifeBarDisplay(self.life_bar_rect, sprites_dict, current_hp/max_hp)

        self.life_rect = get_converted_rect(self.rect, life_grid) if not top else None
        self.life_display = LifeDisplay(self.life_rect, sprites_dict, current_hp, max_hp) if not top else None

        self.hook_rect = get_converted_rect(self.rect, hook_grid)
        self.hook_display = TopHookDisplay(self.hook_rect) if top else BottomHookDisplay(self.hook_rect)
        self.visible = True

    def show(self):
        self.visible = True

    def hide(self):
        self.visible = False

    def modify_name(self, name):
        self.name_display.modify(name)

    def modify_level(self, level):
        self.level_display.modify(level)

    def modify_life(self, current_hp, max_hp):
        if self.life_display: self.life_display.modify(current_hp, max_hp)
        self.life_bar_display.modify(current_hp/max_hp)

    def display(self, surface):
        if SHOW_GRID:
            for y in range(self.rect.top, self.rect.bottom, self.tile_height):
                for x in range(self.rect.left, self.rect.right, self.tile_width):
                    pygame.draw.rect(surface, (247, 220, 220), (x, y, self.tile_width, self.tile_height), 1)
        if SHOW_RECT: pygame.draw.rect(surface, (247, 0, 0), self.rect, 1)
        if self.visible:
            if self.name_display: self.name_display.display(surface)
            if self.level_display: self.level_display.display(surface)
            if self.life_bar_display: self.life_bar_display.display(surface)
            if self.life_display: self.life_display.display(surface)
            if self.hook_display: self.hook_display.display(surface)


class TopStatusHUD(StatusHUD):
    def __init__(self, sprites_dict, name="POKEMON 1", level=99, current_hp=123, max_hp=456):
        grid_pos = 1,0
        grid_size = 10,4
        name_grid = (0,0), (10,1)
        level_grid = (3,1), (4,1)
        life_bar_grid = (1,2), (9,1)
        life_grid = None
        hook_grid = 0, 2, 10, 2
        super().__init__(grid_pos, grid_size, sprites_dict, name_grid, level_grid, life_bar_grid, life_grid, hook_grid, name, level, current_hp, max_hp, top=True)



class BottomStatusHUD(StatusHUD):
    def __init__(self, sprites_dict, name="POKEMON 2", level=99, current_hp=456, max_hp=789):
        grid_pos = 9,7
        grid_size = 11,5
        name_grid = (1, 0), (10, 1)
        level_grid = (5, 1), (4, 1)
        life_bar_grid = (1, 2), (9, 1)
        life_grid = (2,3),(7,1)
        hook_grid = 0, 2, 10, 3
        super().__init__(grid_pos, grid_size, sprites_dict, name_grid, level_grid, life_bar_grid, life_grid, hook_grid, name, level, current_hp, max_hp, top=False)


# #####################################################################################
# #####################################################################################

class NameDisplay:
    def __init__(self, rect, sprites_dict, name=None):
        self.rect = rect
        self.chars_display = [CharDisplay(pygame.Rect(i, self.rect.top, TILE_WIDTH, TILE_HEIGHT), sprites_dict) for i in range(self.rect.left, self.rect.right, TILE_WIDTH)]
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
        if SHOW_RECT: pygame.draw.rect(surface, (200,200,200), self.rect, 1)
        if self.visible:
            [char.display(surface) for char in self.chars_display]

# #########################################################################################################

class LevelDisplay:
    def __init__(self, rect, sprites_dict, level=None):
        self.rect = rect
        path = "assets/sprites/battle interface/level_label.png"
        self.sprite = pygame.image.load(path).convert_alpha()
        self.chars_display = [CharDisplay(pygame.Rect(i, self.rect.top, TILE_WIDTH, TILE_HEIGHT), sprites_dict) for i in range(self.rect.left+TILE_WIDTH, self.rect.right, TILE_WIDTH)]
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
        if SHOW_RECT: pygame.draw.rect(surface, (200,0,200), self.rect, 1)
        if self.visible:
            surface.blit(self.sprite, self.rect)
            [char.display(surface) for char in self.chars_display]


# #########################################################################################################

class LifeBarDisplay:
    def __init__(self, rect, sprites_dict, completion=0.0):
        self.rect = rect
        self.inner_rect = pygame.Rect(self.rect.left+2*TILE_WIDTH, self.rect.top+TILE_HEIGHT*3/8, 6*TILE_WIDTH, TILE_HEIGHT//4)
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
        if SHOW_RECT: pygame.draw.rect(surface, (200,0,200), self.rect, 1)
        if self.visible:
            surface.blit(self.sprite, self.rect)
            pygame.draw.rect(surface, self.colors[self.color_index], (self.inner_rect.topleft, (self.inner_rect.width*self.completion, self.inner_rect.height)), 0)


# #########################################################################################################

class LifeDisplay:
    def __init__(self, rect, sprites_dict, current_hp=0, max_hp=0):
        self.rect = rect
        self.chars_display = [CharDisplay(pygame.Rect(i, self.rect.top, TILE_WIDTH, TILE_HEIGHT), sprites_dict) for i in range(self.rect.left, self.rect.right, TILE_WIDTH)]
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
        if SHOW_RECT: pygame.draw.rect(surface, (200,0,200), self.rect, 1)
        if self.visible:
            [char.display(surface) for char in self.chars_display]

# #########################################################################################################

class TopHookDisplay:
    def __init__(self, rect):
        self.rect = rect
        path = "assets/sprites/battle interface/top_status_hook.png"
        self.sprite = pygame.image.load(path).convert_alpha()
        self.visible = True

    def show(self):
        self.visible = True

    def hide(self):
        self.visible = False

    def display(self, surface):
        if SHOW_RECT: pygame.draw.rect(surface, (0,0,0), self.rect, 1)
        if self.visible:
            surface.blit(self.sprite, self.rect)

class BottomHookDisplay:
    def __init__(self, rect):
        self.rect = rect
        path = "assets/sprites/battle interface/bottom_status_hook.png"
        self.sprite = pygame.image.load(path).convert_alpha()
        self.visible = True

    def show(self):
        self.visible = True

    def hide(self):
        self.visible = False

    def display(self, surface):
        if SHOW_RECT: pygame.draw.rect(surface, (0,0,0), self.rect, 1)
        if self.visible:
            surface.blit(self.sprite, self.rect)


# #####################################################################################

# class CharDisplay:
#     def __init__(self, rect, sprites_dict, char=None):
#         self.char = char
#         self.rect = rect
#         self.sprites_dict = sprites_dict
#
#     def update(self, new_char):
#         self.char = new_char
#
#     def display(self, surface):
#         if SHOW_RECT: pygame.draw.rect(surface, (0,0,255), self.rect, 1)
#         if self.char: surface.blit(self.sprites_dict["all"][self.char], self.rect)
#
