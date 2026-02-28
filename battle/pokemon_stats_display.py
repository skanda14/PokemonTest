import pygame
from battle.battle_settings import SHOW_RECT, SHOW_GRID, TILE_SIZE, TILE_WIDTH, TILE_HEIGHT,BACKGROUND_COLOR
from message_system.character_display import CharDisplay
from battle.get_box_sprite import get_box_sprite
from battle.battle_display_fun import get_convert_rect_from_grid_rect, get_rect, get_relative_rect, get_relative_pos_from_rect
from battle.switch_pokemon_display import SwitchPokemonDisplay


class PokemonStatsDisplay:
    def __init__(self, grid_pos, sprite_dict):
        grid_size = 20,18
        self.grid_rect = get_rect(grid_pos, grid_size)
        self.rect = get_convert_rect_from_grid_rect(grid_pos, grid_size)
        self.sprite_dict = sprite_dict
        self.sprite = pygame.Surface(self.rect.size)
        self.sprite.fill(BACKGROUND_COLOR)
        self.items = [f"PIKACHU"]
        self.items_display = [BasicStatsMenuDisplay((0,8), sprite_dict)]

        self.menu_index = 0
        self.visible = True
        self.init_items()

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
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    choice = "SWITCH_SUB_MENU"
                if event.key == pygame.K_SPACE:
                    string = self.items[self.menu_index]
                    choice = string
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


