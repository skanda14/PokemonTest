import pygame
from battle.status_display_fun import get_converted_rect
from battle.battle_settings import SHOW_RECT, SHOW_GRID, TILE_SIZE, TILE_WIDTH, TILE_HEIGHT, BOTTOM_STATUS_SIZE, TOP_STATUS_SIZE
from battle.battle_display_fun import get_convert_rect_from_grid_rect, get_rect, get_relative_rect, get_relative_pos_from_rect


class PokemonDisplay:
    def __init__(self, grid_pos, sprite_dict, pokemon=None, back=False):
        grid_size = 7,7
        self.tile_width, self.tile_height = self.tile_size = TILE_SIZE
        self.rect = get_convert_rect_from_grid_rect(grid_pos, grid_size)
        self.sprite_dict = sprite_dict
        self.sprite = pygame.Surface(self.rect.size)
        self.sprite.fill(pygame.Color('blue'))
        self.sprite.set_alpha(100)
        self.pokemon = pokemon
        self.visible = True

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
