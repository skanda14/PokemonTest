import pygame
from view.pygame.view_settings import SHOW_RECT, SHOW_GRID, TILE_SIZE, TILE_WIDTH, TILE_HEIGHT,BACKGROUND_COLOR
from view.pygame.character_display import CharDisplay
from view.pygame.get_box_sprite import get_box_sprite
from view.pygame.battle_display_fun import get_convert_rect_from_grid_rect, get_rect, get_relative_rect, get_relative_pos_from_rect
from view.pygame.data_move_menu_view import DataMoveView
from view.pygame.status_display import StatusHUD


class StatsMenu1View:
    def __init__(self, grid_pos, sprite_dict, cursor_index=0):
        grid_size = 20,18
        self.grid_rect = get_rect(grid_pos, grid_size)
        self.rect = get_convert_rect_from_grid_rect(grid_pos, grid_size)
        self.sprite_dict = sprite_dict
        # self.sprite = get_box_sprite(grid_size, sprite_dict)
        self.sprite = pygame.Surface(self.rect.size)
        self.sprite.fill(BACKGROUND_COLOR)
        self.target = None
        self.items_display = []

        self.cursors_display = []
        self.menu_index = cursor_index
        self.visible = False

    def init_items(self, pokemon):
        self.target = pokemon
        self.init_items_display()

    def init_items_display(self):
        trainer_name = self.target.trainer.name.upper()
        trainer_id = str(self.target.trainer.id)
        while len(trainer_id) < 5:
            trainer_id = "0"+trainer_id
        string_id = str(self.target.index)
        while len(string_id) < 3:
            string_id = "0"+string_id
        string_type_2 = None
        string_type_1 = self.target.types[0].upper()
        if len(self.target.types) > 1:
            string_type_2 = self.target.types[1].upper()
        self.items_display = [
            BasicStatsMenuDisplay((0,8), self.sprite_dict, self.target),
            FullStatusHUD(self.sprite_dict, self.target),
            PokemonDisplay((1,0), self.sprite_dict, self.target),
            StringDisplay((1, 7), (9,1), self.sprite_dict, f"No.{string_id}"),
            StringDisplay((10, 6), (9, 1), self.sprite_dict, "STATUS/OK"),
            StringDisplay((10,9), (6,1), self.sprite_dict, "TYPE1/"),
            StringDisplay((11, 10), (9, 1), self.sprite_dict, string_type_1),
            StringDisplay((10, 13), (5, 1), self.sprite_dict, "IDNo/"),
            StringDisplay((11, 14), (9, 1), self.sprite_dict, trainer_id),
            StringDisplay((10, 15), (3, 1), self.sprite_dict, "OT/"),
            StringDisplay((11, 16), (9, 1), self.sprite_dict, trainer_name),
        ]
        if string_type_2:
            self.items_display.append(StringDisplay((10, 11), (6, 1), self.sprite_dict, "TYPE2/"))
            self.items_display.append(StringDisplay((11, 12), (9, 1), self.sprite_dict, string_type_2))

    def show(self):
        self.visible = True

    def hide(self):
        self.visible = False

    def reset(self):
        for item_display in self.items_display:
            for char_display in item_display:
                char_display.erase()

    def update(self, cursor_index):
        pass

    def display(self, surface):
        if self.visible:
            surface.blit(self.sprite, self.rect)
            self.display_items(surface)
            if SHOW_RECT: pygame.draw.rect(surface, (255,0,0), self.rect, 1)

    def display_items(self, surface):
        for item_display in self.items_display:
            item_display.display(surface)



############################################################################################
############################################################################################
############################################################################################

class PokemonDisplay:
    def __init__(self, grid_pos, sprite_dict, pokemon=None, back=False):
        grid_size = 7,7
        self.tile_width, self.tile_height = self.tile_size = TILE_SIZE
        self.rect = get_convert_rect_from_grid_rect(grid_pos, grid_size)
        self.back = back
        if pokemon:
            self.sprite = pokemon.sprite
        else:
            self.sprite_dict = sprite_dict
            self.sprite = pygame.Surface(self.rect.size)
            self.sprite.fill(pygame.Color('blue'))
            self.sprite.set_alpha(100)
        self.pokemon = pokemon
        self.visible = True

    def modify_pokemon(self, pokemon):
        self.pokemon = pokemon
        category = "back_default" if self.back else "front_default"
        sprite = self.pokemon.sprites[category]
        sprite.set_alpha(255)
        if self.back:
            sprite = pygame.transform.scale_by(sprite, 2)
        self.sprite = sprite

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


class BasicStatsMenuDisplay:
    def __init__(self, grid_pos, sprite_dict, pokemon):
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
        self.init_items(pokemon)

    def init_fixe_display(self):
        self.fixe_items_display = []
        for i, item in enumerate(self.fixe_items):
            y = 1+i*2
            x = 1
            new_list = []
            for j,char in enumerate(item):
                new_list.append(CharDisplay((get_relative_pos_from_rect((x+j, y), self.grid_rect)), self.sprite_dict, char))
            self.fixe_items_display.append(new_list)

    def init_items(self, pokemon):
        self.reset()
        self.items = [pokemon.stats['attack'], pokemon.stats['defense'], pokemon.stats['speed'],pokemon.stats['special']]
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