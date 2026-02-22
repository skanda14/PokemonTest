import pygame
from get_sprite_dict import get_sprite_dict
from message_system.message_box_display import MessageBox
from settings import GAME_BOY_RESOLUTION


PLAYER_NAME = "Jean-Michel"
RIVAL_NAME = "Bobby"

texts = [
    "Bien le bonjour!\nBienvenue dans le monde magique des POKéMON!",
    "Mon nom est CHEN!\nLes gens souvent m'appellent le PROF POKéMON!",
    "Ce monde est peuplé de créatures du nom de POKéMON!",
    "Pour certains, les POKéMON sont des animaux domestiques, pour d'autres, ils sont un moyen de combattre.",
    "Pour ma part... L'étude des Pokémon est\nma profession.",
    "Tout d'abord, quel est ton nom?",
    f"OK! Ton nom est donc {PLAYER_NAME}!",
    "Voici mon petit-fils. Il est ton rival depuis sa toute jeunesse.",
    "...Heu...\nC'est quoi donc son nom déjà?",
    f"Ah oui! Je me souviens! Son nom est {RIVAL_NAME}!",
    f"{PLAYER_NAME}!",
    "Ta quête des Pokémon est sur le point de commencer!\nUn tout nouveau monde de rêves, d'aventures et\nde Pokémon t'attend! Dingue!",
    f"Salut {PLAYER_NAME},  la pêche?    *%/*#¤    abcdefg   hijklmn-opqrstuv        wxyz12345678 90 Moi,\n je suis grave           boosté\ndepuis que j'ai rempli mon Pokédex!\n C'est\n trop\n fou\n\n\n\n\nEnfin, tu vois quoi!"
]


def display(screen, surface, zoom, message_box):
    screen.fill((0,0,0))
    surface.fill((247, 247, 247))
    if message_box:
        message_box.display(surface)
    screen.blit(pygame.transform.scale_by(surface, zoom), (0, 0))


def update(message_box, keys):
    if message_box:
        return message_box.update(keys)
    else:
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        return None


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
    message_box = MessageBox(texts[:-1], sprites_dict)

    running = True
    while running:
        events = pygame.event.get()
        keys = pygame.key.get_pressed()
        for event in events:
            if event.type == pygame.QUIT:
                running = False

        message_box = update(message_box, keys)
        display(screen, surface, zoom, message_box)
        pygame.display.flip()
        pygame.display.set_caption(f"Pokemon Message System Test (fps: {clock.get_fps(): .1f})")
        clock.tick(fps)


test()
