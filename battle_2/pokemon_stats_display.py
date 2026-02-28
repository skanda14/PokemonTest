import pygame
from battle_2.battle_settings import SHOW_RECT, SHOW_GRID, TILE_SIZE, TILE_WIDTH, TILE_HEIGHT,BACKGROUND_COLOR
from battle_2.character_display import CharDisplay
from battle_2.get_box_sprite import get_box_sprite
from battle_2.battle_display_fun import get_convert_rect_from_grid_rect, get_rect, get_relative_rect, get_relative_pos_from_rect
from battle_2.switch_pokemon_display import SwitchPokemonDisplay
from battle_2 .status_display import NameDisplay, LevelDisplay, LifeBarDisplay, LifeDisplay, BottomHookDisplay, StatusHUD
from battle_2.pokemon_display import PokemonDisplay
from battle_2.pokemon_stats_2_display import PokemonStats2Display


class PokemonStatsDisplay:
    def __init__(self, grid_pos, sprite_dict):
        grid_size = 20,18
        self.grid_rect = get_rect(grid_pos, grid_size)
        self.rect = get_convert_rect_from_grid_rect(grid_pos, grid_size)
        self.sprite_dict = sprite_dict
        self.sprite = pygame.Surface(self.rect.size)
        self.sprite.fill(BACKGROUND_COLOR)
        self.items = [f"PIKACHU"]
        self.items_display = [
            BasicStatsMenuDisplay((0,8), sprite_dict),
            FullStatusHUD(sprite_dict),
            PokemonDisplay((1,0), sprite_dict),
            StringDisplay((1, 7), (6,1), sprite_dict, "No.004"),
            StringDisplay((10, 6), (9, 1), sprite_dict, "STATUS/OK"),
            StringDisplay((10,9), (6,1), sprite_dict, "TYPE1/"),
            StringDisplay((11, 10), (4, 1), sprite_dict, "FIRE"),
            StringDisplay((10, 13), (5, 1), sprite_dict, "IDNo/"),
            StringDisplay((11, 14), (5, 1), sprite_dict, "49153"),
            StringDisplay((10, 15), (3, 1), sprite_dict, "OT/"),
            StringDisplay((11, 16), (3, 1), sprite_dict, "RED"),
        ]
        self.next_stat_menu_class = PokemonStats2Display
        self.current_menu = None
        self.menu_index = 0
        self.visible = True
        # self.init_items()

    def init_items(self):
        for i, item in enumerate(self.items):
            x = 1
            y = i*2
            self.init_item_display((x,y), item)

    def init_item_display(self, grid_pos, name):
        new_item_display = SwitchPokemonDisplay(name, get_relative_pos_from_rect((grid_pos[0], grid_pos[1]), self.grid_rect), self.sprite_dict)
        self.items_display.append(new_item_display)

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
        else:
            for event in events:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        choice = "BACK"
                    if event.key == pygame.K_SPACE:
                        self.current_menu = self.next_stat_menu_class((0, 0), self.sprite_dict)
                    elif event.key == pygame.K_DOWN:
                        self.menu_index = (self.menu_index + 1) % len(self.items)
                    elif event.key == pygame.K_UP:
                        self.menu_index = (self.menu_index - 1) % len(self.items)
        return choice

    def display(self, surface):
        if self.visible:
            surface.blit(self.sprite, self.rect)
            self.display_chars(surface)
            # if SHOW_RECT: pygame.draw.rect(surface, (255,0,0), self.rect, 1)
            if self.current_menu:
                self.current_menu.display(surface)

    def display_chars(self, surface):
        for char_display in self.items_display:
            char_display.display(surface)



class BasicStatsMenuDisplay:
    def __init__(self, grid_pos, sprite_dict):
        grid_size = 10,10
        self.grid_rect = get_rect(grid_pos, grid_size)
        self.rect = get_convert_rect_from_grid_rect(grid_pos, grid_size)
        self.sprite_dict = sprite_dict
        self.sprite = get_box_sprite(grid_size, sprite_dict)
        self.items = []
        self.fixe_items = ["FOR", "DEF", "VIT", "SPE"]
        self.items_display = []
        self.fixe_items_display = []
        self.visible = True
        self.init_fixe_display()
        self.init_items([16,9,9,12])

    def init_fixe_display(self):
        self.fixe_items_display = []
        for i, item in enumerate(self.fixe_items):
            y = 1+i*2
            x = 1
            new_list = []
            for j,char in enumerate(item):
                new_list.append(CharDisplay((get_relative_pos_from_rect((x+j, y), self.grid_rect)), self.sprite_dict, char))
            self.fixe_items_display.append(new_list)

    def init_items(self, items):
        self.reset()
        self.items = items
        self.items_display = []
        for i, item in enumerate(self.items):
            y = 2 + i * 2
            x = 8
            new_list = []
            for j, char in enumerate(reversed(str(item))):
                new_list.append(
                    CharDisplay((get_relative_pos_from_rect((x - j, y), self.grid_rect)), self.sprite_dict, char))
            self.items_display.append(new_list)

    def init_item_display(self, string, grid_pos):
        new_item_display = []
        for i,char in enumerate(reversed(string)):
            new_item_display.append(CharDisplay(get_relative_pos_from_rect((grid_pos[0]+i, grid_pos[1]), self.grid_rect), self.sprite_dict, char))
        self.items_display.append(new_item_display)

    def show(self):
        self.visible = True

    def hide(self):
        self.visible = False

    def reset(self):
        for item_display in self.items_display:
            for char_display in item_display:
                char_display.erase()

    def update(self):
        pass

    def display(self, surface):
        if self.visible:
            surface.blit(self.sprite, self.rect)
            self.display_chars(surface)
            self.display_fixe_chars(surface)
            if SHOW_RECT: pygame.draw.rect(surface, (255,0,0), self.rect, 1)

    def display_chars(self, surface):
        for item_display in self.items_display:
            for char_display in item_display:
                char_display.display(surface)

    def display_fixe_chars(self, surface):
        for item_display in self.fixe_items_display:
            for char_display in item_display:
                char_display.display(surface)


class FullStatusHUD(StatusHUD):
    def __init__(self, sprites_dict, name="POKEMON 2", level=99, current_hp=456, max_hp=789):
        grid_pos = 8,0
        grid_size = 12,17
        name_grid = (1, 1)
        level_grid = (6, 2)
        life_bar_grid = (3, 3)
        life_grid = (4,4)
        hook_grid = (2, 5)
        super().__init__(grid_pos, grid_size, sprites_dict, name_grid, level_grid, life_bar_grid, life_grid, hook_grid, name, level, current_hp, max_hp, top=False)


# #####################################################################################
# #####################################################################################

class StringDisplay:
    def __init__(self, grid_pos, grid_size, sprites_dict, name=None):
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