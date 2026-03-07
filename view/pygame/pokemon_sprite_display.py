import pygame
from view.pygame.battle_display_fun import get_convert_rect_from_grid_rect
from view.pygame.view_settings import TILE_SIZE, SHOW_RECT


class PokemonSpriteDisplay:
    GRID_SIZE = 7,7
    def __init__(self, grid_pos, sprite_dict, pokemon=None, back=False):
        self.tile_width, self.tile_height = self.tile_size = TILE_SIZE
        self.rect = get_convert_rect_from_grid_rect(grid_pos, self.GRID_SIZE)
        self.sprite_dict = sprite_dict
        self.sprite = None
        self.pokemon = None
        self.visible = False
        self.back = back
        self.modify_pokemon(pokemon)

    def modify_pokemon(self, pokemon):
        if pokemon:
            self.visible = True
            self.pokemon = pokemon
            if self.back:
                self.sprite = pygame.transform.scale_by(self.pokemon.sprites['back_default'], 2)
            else:
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
