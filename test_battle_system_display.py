import pygame
from get_sprite_dict import get_sprite_dict
from battle.status_display import BottomStatusHUD, TopStatusHUD
from settings import GAME_BOY_RESOLUTION


def display(screen, surface, zoom, bottom_status_hud, top_status_hud):
    screen.fill((0,0,0))
    surface.fill((247, 247, 247))
    if bottom_status_hud:
        bottom_status_hud.display(surface)
    if top_status_hud:
        top_status_hud.display(surface)
    screen.blit(pygame.transform.scale_by(surface, zoom), (0, 0))


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
        display(screen, surface, zoom, bottom_status_hud, top_status_hud)
        pygame.display.flip()

        pygame.display.set_caption(f"Pokemon Battle System Test (fps: {clock.get_fps(): .1f})")
        clock.tick(fps)


test()
