import pygame
import random
import sys
from settings import RESOLUTION, ZOOM, FPS, GAME_BOY_RESOLUTION
from battle_2.battle_settings import TILE_WIDTH, TILE_HEIGHT, SHOW_GRID
from debug import Debug
# from battle.battle_engine import BattleEngine
from battle_2.battle_engine import BattleEngine
from get_sprite_dict import get_sprite_dict
from trainer_and_pokemon_in_battle.in_battle_trainer import InBattleTrainer, InBattlePokemon

#
# def get_pickachu():
#     # Création des attaques
#     t_shock = Move("Thunder Shock", "Electric", 40, 100)
#     quick_atk = Move("Quick Attack", "Normal", 40, 100)
#     # Création des Pokémon (Stats basées sur les Base Stats réelles adaptées au Lvl 5)
#     # Pikachu: Haut speed/special, défense faible
#     pikachu = Pokemon("Pikachu", 5, ["Electric"], 20, attack=11, defense=9, special=11, speed=15,
#                       moves=[t_shock, quick_atk])
#     return pikachu
#
# def get_bulbasaur():
#     # Création des attaques
#     vine_whip = Move("Vine Whip", "Grass", 45, 100)
#     tackle = Move("Tackle", "Normal", 35, 95)
#     # Création des Pokémon (Stats basées sur les Base Stats réelles adaptées au Lvl 5)
#     # Bulbasaur: Plus tanky, moins rapide
#     bulbasaur = Pokemon("Bulbasaur", 5, ["Grass", "Poison"], 21, attack=10, defense=10, special=12, speed=10,
#                         moves=[vine_whip, tackle])
#     return bulbasaur

# =====================================================================
# INITIALISATION DES DONNÉES ET BOUCLE PRINCIPALE
# =====================================================================

def display_grid(screen, rect, tile_size):
    tile_width, tile_height = tile_size
    grid_color = (220, 220, 220)
    for y in range(rect.top, rect.bottom, tile_height):
        for x in range(rect.left, rect.right, tile_width):
            pygame.draw.rect(screen, grid_color, (x, y, tile_width, tile_height), 1)


def get_grid_sprite(screen, tile_size):
    color_key = (255,255,255)
    rect = screen.get_rect()
    new_surf = pygame.Surface(rect.size, pygame.SRCALPHA)
    new_surf.fill(color_key)
    tile_width, tile_height = tile_size
    grid_light_color = (150,150,150)
    grid_color = (220,0,0)
    for y in range(rect.top, rect.bottom, tile_height):
        for x in range(rect.left, rect.right, tile_width):
            pygame.draw.rect(new_surf, grid_light_color, (x, y, tile_width, tile_height), 1)
    for y in range(rect.top, rect.bottom, tile_height*2):
        for x in range(rect.left, rect.right, tile_width*2):
            pygame.draw.rect(new_surf, grid_color, (x, y, tile_width*2, tile_height*2), 1)
    new_surf.set_colorkey(color_key)
    new_surf.set_alpha(50)
    return new_surf


def display(screen, surface, engine, zoom, debug, grid):
    screen.fill((0, 0, 0))
    engine.display(surface)
    screen.blit(pygame.transform.scale_by(surface, zoom), (0, 0))
    debug.display(screen)
    if SHOW_GRID:
        screen.blit(grid, (0, 0))

def main():
    pygame.init()
    screen = pygame.display.set_mode(RESOLUTION)
    surface = pygame.Surface(GAME_BOY_RESOLUTION)
    zoom = ZOOM
    clock = pygame.time.Clock()
    fps = FPS
    tile_size = TILE_WIDTH*ZOOM,TILE_HEIGHT*ZOOM
    grid_sprite = get_grid_sprite(screen, tile_size)

    pokemon_team = [InBattlePokemon(name) for name in ["charizard", "bulbasaur", "mew"]]
    random.shuffle(pokemon_team)
    items = []
    trainer = InBattleTrainer('red', pokemon_team, items)
    wild_pokemon = InBattlePokemon('muk')

    sprites_dict = get_sprite_dict()
    engine = BattleEngine(sprites_dict, trainer, wild_pokemon)
    debug_box = Debug(screen)

    running = True
    while running:
        events = pygame.event.get()
        keys = pygame.key.get_pressed()
        for event in events:
            if event.type == pygame.QUIT:
                running = False
            # else:
            #     engine.handle_event(event)

        engine.update(events, keys)
        new_string = "Test" # f"{engine.state} / MSG: {len(engine.message_queue)} / ACTIONS: {len(engine.action_queue)})"
        debug_box.update(new_string)

        display(screen, surface, engine, zoom, debug_box, grid_sprite)

        pygame.display.flip()

        pygame.display.set_caption(f"Pokemon Battle System Test (fps: {clock.get_fps(): .1f})")
        clock.tick(fps)

    pygame.quit()
    sys.exit()


# if __name__ == "__main__":
#     main()

main()



