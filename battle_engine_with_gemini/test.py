import pygame
import sys
from battle_engine_with_gemini.class_move import Move
from battle_engine_with_gemini.class_pokemon import Pokemon
from battle_engine_with_gemini.battle_engine import BattleEngine
from debug import Debug


# Initialisation de Pygame
pygame.init()

# Constantes d'affichage
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 400
FPS = 30

def get_pickachu():
    # Création des attaques
    t_shock = Move("Thunder Shock", "Electric", 40, 100)
    quick_atk = Move("Quick Attack", "Normal", 40, 100)
    # Création des Pokémon (Stats basées sur les Base Stats réelles adaptées au Lvl 5)
    # Pikachu: Haut speed/special, défense faible
    pikachu = Pokemon("Pikachu", 5, ["Electric"], 20, attack=11, defense=9, special=11, speed=15,
                      moves=[t_shock, quick_atk])
    return pikachu

def get_bulbasaur():
    # Création des attaques
    vine_whip = Move("Vine Whip", "Grass", 45, 100)
    tackle = Move("Tackle", "Normal", 35, 95)
    # Création des Pokémon (Stats basées sur les Base Stats réelles adaptées au Lvl 5)
    # Bulbasaur: Plus tanky, moins rapide
    bulbasaur = Pokemon("Bulbasaur", 5, ["Grass", "Poison"], 21, attack=10, defense=10, special=12, speed=10,
                        moves=[vine_whip, tackle])
    return bulbasaur

# =====================================================================
# INITIALISATION DES DONNÉES ET BOUCLE PRINCIPALE
# =====================================================================

def main():
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Pokémon Gen 1 Battle System")
    clock = pygame.time.Clock()

    # Création des Pokémon (Stats basées sur les Base Stats réelles adaptées au Lvl 5)
    pikachu = get_pickachu()
    bulbasaur = get_bulbasaur()

    # Initialisation du moteur
    engine = BattleEngine(screen, pikachu, bulbasaur)

    # Lancement du premier message
    # engine.advance_message()

    debug_box = Debug(screen)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            else:
                engine.handle_event(event)

        engine.update()
        new_string = f"{engine.state} / MSG: {len(engine.message_queue)} / ACTIONS: {len(engine.action_queue)})"
        debug_box.update(new_string)
        engine.draw(screen)
        debug_box.display(screen)
        pygame.display.flip()
        pygame.display.set_caption(f"Pokemon Battle System Test (fps: {clock.get_fps(): .1f})")
        clock.tick(FPS)

    pygame.quit()
    sys.exit()


# if __name__ == "__main__":
#     main()

main()
