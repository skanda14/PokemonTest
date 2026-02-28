import pygame
from get_sprite_dict import get_sprite_dict
from battle.status_display import BottomStatusHUD, TopStatusHUD
from battle.pokemon_display import PokemonDisplay
from settings import GAME_BOY_RESOLUTION
from battle.battle_settings import SHOW_GRID, TILE_WIDTH, TILE_HEIGHT


def display(screen, surface, surface_rect, zoom, bottom_status_hud, top_status_hud):
    screen.fill((0,0,0))
    surface.fill((247, 247, 247))
    if SHOW_GRID:
        grid_color = (247, 220, 220)
        for y in range(surface_rect.top, surface_rect.bottom, TILE_HEIGHT):
            pygame.draw.line(surface, grid_color, (surface_rect.left, y), (surface_rect.right,y), 1)
        for x in range(surface_rect.left, surface_rect.right, TILE_WIDTH):
            pygame.draw.line(surface, grid_color, (x, surface_rect.top), (x, surface_rect.bottom), 1)

    if bottom_status_hud:
        bottom_status_hud.display(surface)
    if top_status_hud:
        top_status_hud.display(surface)
    screen.blit(pygame.transform.scale_by(surface, zoom), (0, 0))

def display_grid():
    pass


def update(keys):
    pass


def test():
    fps = 60
    zoom = 4
    game_resolution = GAME_BOY_RESOLUTION
    screen_resolution = game_resolution[0]*zoom, game_resolution[1]*zoom

    pygame.init()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode(screen_resolution)
    surface = pygame.Surface(game_resolution)

    surface_rect = surface.get_rect()
    sprites_dict = get_sprite_dict()
    bottom_status_hud = BottomStatusHUD(sprites_dict)
    top_status_hud = TopStatusHUD(sprites_dict)

    running = True
    while running:
        events = pygame.event.get()
        keys = pygame.key.get_pressed()
        for event in events:
            if event.type == pygame.QUIT:
                running = False

        update(keys)
        display(screen, surface, surface_rect, zoom, bottom_status_hud, top_status_hud)
        pygame.display.flip()

        pygame.display.set_caption(f"Pokemon Battle System Test (fps: {clock.get_fps(): .1f})")
        clock.tick(fps)


test()
