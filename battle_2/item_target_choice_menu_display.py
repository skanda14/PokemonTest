import pygame
from battle_2.battle_settings import SHOW_RECT, SHOW_GRID, TILE_SIZE, TILE_WIDTH, TILE_HEIGHT,BACKGROUND_COLOR
from battle_2.character_display import CharDisplay
from battle_2.get_box_sprite import get_box_sprite
from battle_2.battle_display_fun import get_convert_rect_from_grid_rect, get_rect, get_relative_rect, get_relative_pos_from_rect
from battle_2.switch_pokemon_display import SwitchPokemonDisplay


class ItemTargetChoiceMenuDisplay:
    def __init__(self, grid_pos, selected_item, sprite_dict):
        grid_size = 20,12
        self.grid_rect = get_rect(grid_pos, grid_size)
        self.rect = get_convert_rect_from_grid_rect(grid_pos, grid_size)
        self.sprite_dict = sprite_dict
        self.sprite = pygame.Surface(self.rect.size)
        self.sprite.fill(BACKGROUND_COLOR)
        self.items = [f"PIKACHU{str(i)}" for i in range(6)]
        self.items_display = []
        self.selected_item = selected_item

        self.cursors_display = []
        self.menu_index = 0
        self.visible = True
        self.init_items()

    def init_items(self):
        self.cursors_display = []
        for i, item in enumerate(self.items):
            x = 1
            y = i*2
            self.init_item_display((x,y), item)
            self.init_cursor_display((x-1,y+1))

    def init_item_display(self, grid_pos, name):
        new_item_display = SwitchPokemonDisplay(name, get_relative_pos_from_rect((grid_pos[0], grid_pos[1]), self.grid_rect), self.sprite_dict)
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

    def update(self, events):
        choice = None
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    choice = "BACK"
                if event.key == pygame.K_SPACE:
                    string = self.selected_item[0]+" => "+self.items[self.menu_index]
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
            self.display_cursor(surface)
            # if SHOW_RECT: pygame.draw.rect(surface, (255,0,0), self.rect, 1)

    def display_chars(self, surface):
        for char_display in self.items_display:
            char_display.display(surface)

    def display_cursor(self, surface):
        self.cursors_display[self.menu_index].display(surface)
