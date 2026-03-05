import pygame
from view.pygame.view_settings import SHOW_RECT, SHOW_GRID, TILE_SIZE, TILE_WIDTH, TILE_HEIGHT,BACKGROUND_COLOR
from view.pygame.get_box_sprite import get_box_sprite
from view.pygame.battle_display_fun import get_convert_rect_from_grid_rect, get_rect, get_relative_rect, get_relative_pos_from_rect
from view.pygame.status_display import StatusHUD
from view.pygame.string_display import StringDisplay


class StatsMenu2View:
    def __init__(self, grid_pos, sprite_dict, cursor_index=0):
        grid_size = 20,18
        self.grid_rect = get_rect(grid_pos, grid_size)
        self.rect = get_convert_rect_from_grid_rect(grid_pos, grid_size)
        self.sprite_dict = sprite_dict
        self.sprite = pygame.Surface(self.rect.size)
        self.sprite.fill(BACKGROUND_COLOR)
        self.strings_display = []
        self.cursors_display = []
        self.menu_index = cursor_index
        self.visible = False

    def init_items(self, pokemon):
        self.init_items_display(pokemon)

    def init_items_display(self, pokemon):
        self.strings_display = [
            MovesWithPPMenuDisplay((0, 8), self.sprite_dict, pokemon),
            PokemonFrontSpriteDisplay((1, 0), self.sprite_dict, pokemon),
            StringDisplay((1, 7), (6, 1), self.sprite_dict, f"No.{pokemon.index:03}"),
            StringDisplay((9, 1), (11, 1), self.sprite_dict, pokemon.name.upper()),
            StringDisplay((9, 3), (11, 1), self.sprite_dict, "EXP POINTS"),
            StringDisplay((15, 4), (11, 1), self.sprite_dict, pokemon.current_exp),
            StringDisplay((9, 5), (11, 1), self.sprite_dict, "LEVEL UP"),
            StringDisplay((11, 6), (11, 1), self.sprite_dict,
                          f"{pokemon.remaining_exp}}} :{pokemon.level + 1}"),
        ]

    def show(self):
        self.visible = True

    def hide(self):
        self.visible = False

    def reset(self):
        self.strings_display = []

    def update(self, cursor_index):
        pass

    def display(self, surface):
        if self.visible:
            surface.blit(self.sprite, self.rect)
            self.display_items(surface)
            if SHOW_RECT: pygame.draw.rect(surface, (255,0,0), self.rect, 1)

    def display_items(self, surface):
        for string_display in self.strings_display:
            string_display.display(surface)



############################################################################################
############################################################################################
############################################################################################

class PokemonFrontSpriteDisplay:
    def __init__(self, grid_pos, sprite_dict, pokemon=None):
        grid_size = 7,7
        self.tile_width, self.tile_height = self.tile_size = TILE_SIZE
        self.rect = get_convert_rect_from_grid_rect(grid_pos, grid_size)
        self.sprite_dict = sprite_dict
        self.sprite = pygame.Surface(self.rect.size)
        self.sprite.fill(pygame.Color('blue'))
        self.sprite.set_alpha(100)
        self.pokemon = None
        self.visible = True
        self.modify_pokemon(pokemon)

    def modify_pokemon(self, pokemon):
        if pokemon:
            self.pokemon = pokemon
            self.sprite = self.pokemon.sprites['front_default']

    def show(self):
        self.visible = True

    def hide(self):
        self.visible = False

    def update(self):
        pass

    def display(self, surface):
        if self.visible:
            surface.blit(self.sprite, self.rect)
            if SHOW_RECT: pygame.draw.rect(surface, (255, 0, 0), self.rect, 1)


class MovesWithPPMenuDisplay:
    def __init__(self, grid_pos, sprite_dict, pokemon):
        grid_size = 20,10
        self.grid_rect = get_rect(grid_pos, grid_size)
        self.rect = get_convert_rect_from_grid_rect(grid_pos, grid_size)
        self.sprite_dict = sprite_dict
        self.sprite = get_box_sprite(grid_size, sprite_dict)
        self.items_display = []
        self.visible = True
        self.init_items(pokemon)

    def init_items(self, pokemon):
        self.reset()
        self.items_display = []
        for i, move in enumerate(m for m in pokemon.moves.values() if m):
            self.init_name_display(i, move)
            self.init_data_display(i, move)

    def init_name_display(self, i, move):
        string = move.name.upper()
        x,y = 2, 1 + i * 2
        self.items_display.append(
            StringDisplay(get_relative_pos_from_rect((x, y), self.grid_rect),
                          (len(string),1), self.sprite_dict, string))

    def init_data_display(self, i, move):
        string = f'PP {move.current_pp:>2}/{move.max_pp:>2}'
        x,y = self.grid_rect.right-len(string)-1, 2 + i * 2
        self.items_display.append(
            StringDisplay(get_relative_pos_from_rect((x, y), self.grid_rect),
                          (len(string),1), self.sprite_dict, string))

    def show(self):
        self.visible = True

    def hide(self):
        self.visible = False

    def reset(self):
        for char_display in self.items_display:
            char_display.erase()

    def update(self):
        pass

    def display(self, surface):
        if self.visible:
            surface.blit(self.sprite, self.rect)
            self.display_chars(surface)
            if SHOW_RECT: pygame.draw.rect(surface, (255,0,0), self.rect, 1)

    def display_chars(self, surface):
        for string_d in self.items_display:
            string_d.display(surface)


class FullStatusHUD(StatusHUD):
    def __init__(self, sprites_dict, target, name="POKEMON 2", level=99, current_hp=456, max_hp=789):
        grid_pos = 8,0
        grid_size = 12,17
        name_grid = (1, 1)
        level_grid = (6, 2)
        life_bar_grid = (3, 3)
        life_grid = (4,4)
        hook_grid = (2, 5)
        super().__init__(grid_pos, grid_size, sprites_dict, name_grid, level_grid, life_bar_grid, life_grid, hook_grid, target.name.upper(), target.level, target.stats['hp'], target.stats['max_hp'], top=False)


# #####################################################################################
# #####################################################################################

