import time
import pygame

from view.pygame.main_menu_view import MainMenuView
from view.pygame.fight_menu_view import FightMenuView
from view.pygame.pokemon_selection_menu_view import PokemonSelectionMenuView
from view.pygame.item_menu_view import ItemMenuView
from view.pygame.switch_sub_menu_view import SwitchSubMenuView
from view.pygame.stats_menu_1_view import StatsMenu1View
from view.pygame.stats_menu_2_view import StatsMenu2View
from view.pygame.message_box_view import MessageBoxView
from view.pygame.status_display import TopStatusHUD, BottomStatusHUD
from view.pygame.pokemon_sprite_display import PokemonSpriteDisplay
from view.pygame.view_settings import RESOLUTION, GAME_BOY_RESOLUTION, ZOOM, BACKGROUND_COLOR
from get_sprite_dict import get_sprite_dict
from view.pygame.get_box_sprite import get_box_sprite
from view.pygame.battle_display_fun import get_rect, get_convert_rect_from_grid_rect

MENUS = ['MAIN_MENU', 'FIGHT_MENU', 'SWITCH_MENU']

class BattleView:
    def __init__(self, top_pokemon=None, bottom_pokemon=None):
        # Pour une vue console, l'affichage est instantané
        self.screen = pygame.display.set_mode(RESOLUTION)
        self.surface = pygame.Surface(GAME_BOY_RESOLUTION)
        self.dialogue_box_grid_rect = get_rect((0,12), (20,6))
        self.dialogue_box_rect = get_convert_rect_from_grid_rect(self.dialogue_box_grid_rect.topleft, self.dialogue_box_grid_rect.size)
        self.sprites_dict = get_sprite_dict()
        self._is_animating = False
        self._waiting_for_input = False
        self.state = None  # "SHOWING_MAIN_MENU"
        self.dialogue_box_sprite = get_box_sprite((20,6), self.sprites_dict)

        self.top_status_hud = TopStatusHUD(self.sprites_dict, pokemon=top_pokemon)
        self.bottom_status_hud = BottomStatusHUD(self.sprites_dict, pokemon=bottom_pokemon)
        self.top_pokemon_display = PokemonSpriteDisplay((12,0), self.sprites_dict, top_pokemon)
        self.bottom_pokemon_display = PokemonSpriteDisplay((1,5), self.sprites_dict, bottom_pokemon, back=True)


        self.main_menu_view = MainMenuView((6,12), self.sprites_dict)
        self.fight_menu_view = FightMenuView((4,12), self.sprites_dict)
        self.item_menu_view = ItemMenuView((4,2), self.sprites_dict)
        self.item_target_selection_menu_view = PokemonSelectionMenuView((0,0), self.sprites_dict)
        self.switch_sub_menu_view = SwitchSubMenuView((11,11), self.sprites_dict)
        self.switch_target_selection_menu_view = PokemonSelectionMenuView((0,0), self.sprites_dict)
        self.stats_menu_1_view = StatsMenu1View((0,0), self.sprites_dict)
        self.stats_menu_2_view = StatsMenu2View((0,0), self.sprites_dict)

        self.message_box_view = MessageBoxView((0,12), self.sprites_dict)

    # def update(self, index):
    #     if self.state == "SHOWING_MAIN_MENU":
    #         self.main_menu_view.update(index)
    #     elif self.state == "SHOWING_FIGHT_MENU":
    #         self.fight_menu_view.update(index)
    #     elif self.state == "SHOWING_SWITCH_MENU":
    #         self.pokemon_selection_menu_view.update(index)

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

    # def display_move_menu(self, moves):
    #     self.state = "SHOWING_MOVE_MENU"
    #     self.fight_menu_view = MoveMenuDisplay((4,12), self.sprites_dict, moves)

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
        self.surface.fill(BACKGROUND_COLOR)
        if self.top_pokemon_display:
            self.top_pokemon_display.display(self.surface)
        if self.bottom_pokemon_display:
            self.bottom_pokemon_display.display(self.surface)
        if self.top_status_hud:
            self.top_status_hud.display(self.surface)
        if self.bottom_status_hud:
            self.bottom_status_hud.display(self.surface)
        if self.dialogue_box_sprite:
            self.surface.blit(self.dialogue_box_sprite, self.dialogue_box_rect)
        if self.main_menu_view:
            self.main_menu_view.display(self.surface)
        if self.fight_menu_view:
            self.fight_menu_view.display(self.surface)
        if self.item_menu_view:
            self.item_menu_view.display(self.surface)
        if self.item_target_selection_menu_view:
            self.item_target_selection_menu_view.display(self.surface)
        if self.switch_target_selection_menu_view:
            self.switch_target_selection_menu_view.display(self.surface)
        if self.switch_sub_menu_view:
            self.switch_sub_menu_view.display(self.surface)
        if self.stats_menu_1_view:
            self.stats_menu_1_view.display(self.surface)
        if self.stats_menu_2_view:
            self.stats_menu_2_view.display(self.surface)

        if self.message_box_view:
            self.message_box_view.display(self.surface)

        self.screen.blit(pygame.transform.scale_by(self.surface, ZOOM), (0, 0))
        pygame.display.flip()
