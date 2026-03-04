import time
import pygame

from view.pygame.item_menu_view import ItemMenuView
from view.pygame.main_menu_view import MainMenuView
from view.pygame.fight_menu_view import FightMenuView
from view.pygame.view_settings import RESOLUTION, GAME_BOY_RESOLUTION, ZOOM
from get_sprite_dict import get_sprite_dict


MENUS = ['MAIN_MENU', 'FIGHT_MENU', 'SWITCH_MENU']

class BattleView:
    def __init__(self):
        # Pour une vue console, l'affichage est instantané
        self.screen = pygame.display.set_mode(RESOLUTION)
        self.surface = pygame.Surface(GAME_BOY_RESOLUTION)
        self.sprites_dict = get_sprite_dict()
        self._is_animating = False
        self._waiting_for_input = False
        self.state = None  # "SHOWING_MAIN_MENU"
        self.main_menu_view = MainMenuView((6,12), self.sprites_dict)
        self.fight_menu_view = FightMenuView((4,12), self.sprites_dict)
        self.item_menu_view = ItemMenuView((4,2), self.sprites_dict)

    def update(self, index):
        if self.state == "SHOWING_MAIN_MENU":
            self.main_menu_view.update(index)
        elif self.state == "SHOWING_FIGHT_MENU":
            self.fight_menu_view.update(index)

    # -----------------------------------------------------------------
    # Méthodes d'Affichage (Appelées par le Controller)
    # -----------------------------------------------------------------
    def display_text(self, text):
        """Affiche le message dans la console."""
        print(f"\n💬 {text}")

        # On simule un petit délai pour que le texte soit lisible
        # (Sinon la console affiche tout en 1 milliseconde)
        time.sleep(1)

    def display_main_menu(self):
        self.state = "SHOWING_MAIN_MENU"
        self.main_menu_view.show()

    def hide_main_menu(self):
        self.state = "SHOWING_MAIN_MENU"
        self.main_menu_view.hide()


    def display_move_menu(self, moves):
        self.state = "SHOWING_MOVE_MENU"
        self.fight_menu_view = MoveMenuDisplay((4,12), self.sprites_dict, moves)

    # -----------------------------------------------------------------
    # Méthodes d'État (Interrogées par le Controller)
    # -----------------------------------------------------------------
    def is_busy(self):
        """
        Indique au Controller si une animation est en cours.
        Ici, comme on utilise time.sleep() pour ralentir, on n'est jamais 'busy'
        au sens de la boucle frame-par-frame.
        """
        return self._is_animating

    def needs_input_to_advance(self):
        """
        Indique si le jeu doit attendre que le joueur appuie sur une touche.
        Pour ce test console, on retourne False pour que le combat se déroule tout seul,
        mais on pourrait utiliser un input() classique ici.
        """
        return self._waiting_for_input

    def clear_message(self):
        """Efface le texte à l'écran (inutile en console, mais requis par le Controller)."""
        pass


    def display(self):
        self.screen.fill((0, 0, 0))
        self.surface.fill((0, 0, 0))
        if self.main_menu_view:
            self.main_menu_view.display(self.surface)
        if self.fight_menu_view:
            self.fight_menu_view.display(self.surface)
        if self.item_menu_view:
            self.item_menu_view.display(self.surface)
        self.screen.blit(pygame.transform.scale_by(self.surface, ZOOM), (0, 0))
        pygame.display.flip()
