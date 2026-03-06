import pygame
from view.pygame.battle_display_fun import get_relative_pos_from_rect, get_rect, get_convert_rect_from_grid_rect
from view.pygame.view_settings import SHOW_RECT, SHOW_GRID, TILE_SIZE, TILE_WIDTH, TILE_HEIGHT, BOTTOM_STATUS_SIZE, TOP_STATUS_SIZE
from view.pygame.character_display import CharDisplay


class StatusHUD:
    def __init__(self, grid_pos, grid_size, sprites_dict, name_grid_pos, level_grid_pos, life_bar_grid_pos, life_grid_pos, hook_grid_pos, name, level, current_hp, max_hp, top=True):
        self.tile_width, self.tile_height = self.tile_size = TILE_SIZE
        self.grid_rect = get_rect(grid_pos, grid_size)
        self.rect = get_convert_rect_from_grid_rect(grid_pos, grid_size)

        self.current_hp = current_hp
        self.target_hp = current_hp
        self.max_hp = max_hp
        self.animation_speed = 10

        self.name_display = NameDisplay(get_relative_pos_from_rect(name_grid_pos, self.grid_rect), sprites_dict, name)
        self.level_display = LevelDisplay(get_relative_pos_from_rect(level_grid_pos, self.grid_rect), sprites_dict, level)
        self.life_bar_display = LifeBarDisplay(get_relative_pos_from_rect(life_bar_grid_pos, self.grid_rect), sprites_dict, self.current_hp, self.max_hp)
        self.life_display = LifeDisplay(get_relative_pos_from_rect(life_grid_pos, self.grid_rect), sprites_dict, self.current_hp, self.max_hp) if not top else None
        self.hook_display = TopHookDisplay(get_relative_pos_from_rect(hook_grid_pos, self.grid_rect), sprites_dict) if top else BottomHookDisplay(get_relative_pos_from_rect(hook_grid_pos, self.grid_rect), sprites_dict)

        self.visible = True

    def show(self):
        self.visible = True

    def hide(self):
        self.visible = False

    def update(self, dt):
        if self.current_hp > self.target_hp:
            # La barre descend (Dégâts)
            self.current_hp -= self.animation_speed * dt
            if self.current_hp < self.target_hp:
                self.current_hp = self.target_hp
            self.modify_life(self.current_hp, self.max_hp)
        elif self.current_hp < self.target_hp:
            # La barre monte (Soin)
            self.current_hp += self.animation_speed * dt
            if self.current_hp > self.target_hp:
                self.current_hp = self.target_hp
            self.modify_life(self.current_hp, self.max_hp)

    def is_animating(self):
        """Vérifie si la barre de vie est en train de bouger."""
        return self.current_hp != self.target_hp

    def set_target_hp(self, target_hp):
        self.target_hp = max(0, min(self.max_hp, int(target_hp)))

    def modify_name(self, name):
        self.name_display.modify(name.upper())

    def modify_level(self, level):
        self.level_display.modify(level)

    def modify_life(self, current_hp, max_hp):
        if self.life_display: self.life_display.modify(current_hp, max_hp)
        self.life_bar_display.modify(current_hp, max_hp)

    def display(self, surface):
        if self.visible:
            if self.name_display: self.name_display.display(surface)
            if self.level_display: self.level_display.display(surface)
            if self.life_bar_display: self.life_bar_display.display(surface)
            if self.life_display: self.life_display.display(surface)
            if self.hook_display: self.hook_display.display(surface)
            if SHOW_RECT:
                pygame.draw.rect(surface, (255,0,0), self.rect, 1)


class TopStatusHUD(StatusHUD):
    def __init__(self, sprites_dict, pokemon=None, name="POKEMON 1", level=99, current_hp=123, max_hp=456):
        grid_pos = 1,0
        grid_size = 10,4
        name_grid = (0,0)
        level_grid = (3,1)
        life_bar_grid = (1,2)
        life_grid = None
        hook_grid = (0, 2)
        if pokemon:
            name = pokemon.name.upper()
            level = pokemon.level
            current_hp = pokemon.stats['hp']
            max_hp = pokemon.stats['max_hp']
        super().__init__(grid_pos, grid_size, sprites_dict, name_grid, level_grid, life_bar_grid, life_grid, hook_grid, name, level, current_hp, max_hp, top=True)



class BottomStatusHUD(StatusHUD):
    def __init__(self, sprites_dict, pokemon=None, name="POKEMON 2", level=99, current_hp=456, max_hp=789):
        grid_pos = 9,7
        grid_size = 11,5
        name_grid = (1, 0)
        level_grid = (5, 1)
        life_bar_grid = (1, 2)
        life_grid = (2,3)
        hook_grid = (0, 2)
        if pokemon:
            name = pokemon.name.upper()
            level = pokemon.level
            current_hp = pokemon.stats['hp']
            max_hp = pokemon.stats['max_hp']
        super().__init__(grid_pos, grid_size, sprites_dict, name_grid, level_grid, life_bar_grid, life_grid, hook_grid, name, level, current_hp, max_hp, top=False)


# #####################################################################################
# #####################################################################################

class NameDisplay:
    def __init__(self, grid_pos, sprites_dict, name=None):
        grid_size = 10,1
        self.grid_rect = get_rect(grid_pos, grid_size)
        self.rect = get_convert_rect_from_grid_rect(grid_pos, grid_size)
        self.sprite_dict = sprites_dict
        self.chars_display = [CharDisplay(get_relative_pos_from_rect((i,0), self.grid_rect), sprites_dict) for i in range(grid_size[0])]
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

# #########################################################################################################

class LevelDisplay:
    def __init__(self, grid_pos, sprites_dict, level=None):
        grid_size = 4,1
        self.grid_rect = get_rect(grid_pos, grid_size)
        self.rect = get_convert_rect_from_grid_rect(grid_pos, grid_size)
        self.sprite_dict = sprites_dict
        path = "assets/sprites/battle interface/level_label.png"
        self.sprite = pygame.image.load(path).convert_alpha()
        self.chars_display = [CharDisplay(get_relative_pos_from_rect((i,0), self.grid_rect), sprites_dict) for i in range(1, grid_size[0])]
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
    def __init__(self, grid_pos, sprites_dict, current_hp, max_hp):
        grid_size = 9,1
        self.grid_rect = get_rect(grid_pos, grid_size)
        self.rect = get_convert_rect_from_grid_rect(grid_pos, grid_size)
        self.sprite_dict = sprites_dict
        self.inner_rect = pygame.Rect(self.rect.left+2*TILE_WIDTH, self.rect.top+TILE_HEIGHT*3/8, 6*TILE_WIDTH, TILE_HEIGHT//4)
        path = "assets/sprites/battle interface/life_bar.png"
        self.sprite = pygame.image.load(path).convert_alpha()
        self.completion = 0.0
        self.colors = [(72,160,88), (208,160,0), (208,80,48)]
        self.color_index = 0
        self.visible = True
        self.animation_speed = 1
        self.modify(current_hp, max_hp)

    def show(self):
        self.visible = True

    def hide(self):
        self.visible = False

    def modify(self, current_hp, max_hp):
        self.completion = current_hp/max_hp
        self.update_display()

    def update_display(self):
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
        self.sprite_dict = sprites_dict
        self.chars_display = [CharDisplay(get_relative_pos_from_rect((i,0), self.grid_rect), sprites_dict) for i in range(grid_size[0])]
        self.string = None
        self.visible = True
        self.animation_speed = 1
        self.modify(current_hp, max_hp)

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
        self.update_display(current_hp, max_hp)

    def update_display(self, current_hp, max_hp):
        self.string = self.get_formated_string(current_hp, max_hp)
        for char, char_display in zip(self.string, self.chars_display):
            char_display.update(char)

    def display(self, surface):
        if self.visible:
            for char in self.chars_display:
                char.display(surface)

# #########################################################################################################

class TopHookDisplay:
    def __init__(self, grid_pos, sprites_dict):
        grid_size = 10,2
        self.grid_rect = get_rect(grid_pos, grid_size)
        self.rect = get_convert_rect_from_grid_rect(grid_pos, grid_size)
        self.sprite_dict = sprites_dict
        path = "assets/sprites/battle interface/top_status_hook.png"
        self.sprite = pygame.image.load(path).convert_alpha()
        self.visible = True

    def show(self):
        self.visible = True

    def hide(self):
        self.visible = False

    def display(self, surface):
        if self.visible:
            surface.blit(self.sprite, self.rect)

class BottomHookDisplay:
    def __init__(self, grid_pos, sprites_dict):
        grid_size = 10,3
        self.grid_rect = get_rect(grid_pos, grid_size)
        self.rect = get_convert_rect_from_grid_rect(grid_pos, grid_size)
        self.sprite_dict = sprites_dict
        path = "assets/sprites/battle interface/bottom_status_hook.png"
        self.sprite = pygame.image.load(path).convert_alpha()
        self.visible = True

    def show(self):
        self.visible = True

    def hide(self):
        self.visible = False

    def display(self, surface):
        if self.visible:
            surface.blit(self.sprite, self.rect)
