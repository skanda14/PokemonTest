import pygame
from controller.pygame.main_menu_controller import MainMenuController
from controller.pygame.fight_menu_controller import FightMenuController
from controller.pygame.switch_menu_controller import SwitchMenuController
from controller.pygame.switch_sub_menu_controller import SwitchSubMenuController
from controller.pygame.item_menu_controller import ItemMenuController
from controller.pygame.item_target_selection_menu_controller import ItemTargetMenuController
from controller.pygame.stats_menu_controller import StatsMenuController
from controller.pygame.message_box_controller import MessageBoxController

# Les différents états du contrôleur
STATE_BATTLE_INTRODUCTION = "STATE_BATTLE_INTRODUCTION"
STATE_WAITING_FOR_INPUT = "WAITING_FOR_INPUT"
STATE_RESOLVING_TURN = "STATE_RESOLVING_TURN"
STATE_EXECUTING_EVENTS = "EXECUTING_EVENTS"
# STATE_WAITING_FOR_VIEW = "WAITING_FOR_VIEW"
STATE_BATTLE_OVER = "BATTLE_OVER"


class BattleController:
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.state = STATE_BATTLE_INTRODUCTION
        self.main_menu = MainMenuController(model=self.model, view=self.view, go_message_box=self.open_message_box, on_fight_chosen=self.open_fight_menu, on_switch_chosen=self.open_switch_menu, on_item_chosen=self.open_item_menu, on_run_chosen=self.run_chosen)

        self.fight_menu = FightMenuController(model=self.model, view=self.view, go_message_box=self.open_message_box, move_chosen=self.move_chosen, cancel_chosen=self.cancel_chosen)

        self.switch_menu = SwitchMenuController(model=self.model, view=self.view, go_message_box=self.open_message_box, pokemon_chosen=self.open_switch_sub_menu, cancel_chosen=self.cancel_chosen)
        self.switch_sub_menu = SwitchSubMenuController(model=self.model, view=self.view, go_message_box=self.open_message_box, item_chosen=self.switch_pokemon_chosen, stats_chosen=self.stats_chosen, cancel_chosen=self.cancel_chosen)
        self.stats_menu = StatsMenuController(model=self.model, view=self.view, id=1, go_message_box=self.open_message_box, go_next=self.open_stats_2_menu)
        self.stats_2_menu = StatsMenuController(model=self.model, view=self.view, id=2, go_message_box=self.open_message_box, go_next=self.cancel_chosen)

        self.item_menu = ItemMenuController(model=self.model, view=self.view, go_message_box=self.open_message_box, item_chosen=self.item_chosen, cancel_chosen=self.cancel_chosen)
        self.item_target_selection_menu = ItemTargetMenuController(model=self.model, view=self.view, go_message_box=self.open_message_box, pokemon_chosen=self.item_target_chosen, cancel_chosen=self.cancel_chosen)

        self.message_box = MessageBoxController(model=self.model, view=self.view, back=self.cancel_chosen)

        self.current_menu = None
        self.previous_menus = []

        # self.max_waiting_time = 120
        # self.current_waiting_time = 0

        # Copie de la file d'événements générée par le modèle
        self.event_queue = []
        self.current_event = None
        # self.open_main_menu()

    # -----------------------------------------------------------------
    # --- Les Callbacks de navigation ---
    # -----------------------------------------------------------------

    def cancel_chosen(self, item=None):
        self.current_menu = None
        if self.previous_menus:
            self.current_menu = self.previous_menus[-1]
            self.previous_menus = self.previous_menus[:-1]
            self.current_menu.show()
            print(f'Back to {self.current_menu}')

    def run_chosen(self):
        new_action_data = ('RUN', None, None)
        print("Run chosen!")
        self.end_player_choice_phase(new_action_data)

    def move_chosen(self, move):
        self.fight_menu.hide()
        new_action_data = ('FIGHT', move, None)
        print(f'{move.name} chosen !')
        self.end_player_choice_phase(new_action_data)

    def switch_pokemon_chosen(self, pokemon):
        self.switch_menu.hide()
        self.switch_sub_menu.hide()
        new_action_data = ('SWITCH', None, pokemon)
        print(f'Switch to {pokemon.name} !')
        self.end_player_choice_phase(new_action_data)

    def stats_chosen(self, pokemon):
        self.open_stats_menu(pokemon)
        print(f'Pokemon {pokemon.name} stats')

    def item_chosen(self, item):
        self.open_item_target_selection_menu(item)
        # print(f'Item {item.item_name} chosen to...')

    def item_target_chosen(self, pokemon, item):
        self.item_target_selection_menu.hide()
        self.item_menu.hide()
        new_action_data = ('ITEM', item, pokemon)
        print(f'{item.item_name} use on {pokemon.name} !')
        self.end_player_choice_phase(new_action_data)

    def open_switch_sub_menu(self, pokemon):
        # print(f'Pokemon {pokemon.name} to switch sub menu')
        self.save_current_menu_to_previous_menus()
        self.current_menu = self.switch_sub_menu
        self.switch_sub_menu.pokemon = pokemon
        self.current_menu.show()

    def open_stats_menu(self, pokemon):
        # self.save_current_menu_to_previous_menus()
        self.stats_menu.pokemon = pokemon
        self.stats_menu.update_items(pokemon)
        self.current_menu = self.stats_menu
        self.current_menu.show()

    def open_stats_2_menu(self, pokemon):
        self.stats_2_menu.pokemon = pokemon
        self.stats_2_menu.update_items(pokemon)
        self.current_menu = self.stats_2_menu
        self.current_menu.show()

    def open_item_target_selection_menu(self, chosen_item):
        self.save_current_menu_to_previous_menus()
        self.current_menu = self.item_target_selection_menu
        self.current_menu.update_consommable(chosen_item)
        self.current_menu.update_items(self._get_pokemons())
        self.current_menu.show()

    def open_fight_menu(self):
        self.save_current_menu_to_previous_menus()
        self.current_menu = self.fight_menu
        self.current_menu.update_items(self._get_current_pokemon_moves())
        self.current_menu.show()

    def open_switch_menu(self):
        self.save_current_menu_to_previous_menus()
        self.current_menu = self.switch_menu
        self.current_menu.update_items(self._get_pokemons())
        self.current_menu.show()

    def open_item_menu(self):
        self.save_current_menu_to_previous_menus()
        self.current_menu = self.item_menu
        self.current_menu.update_items(self._get_current_items())
        self.current_menu.show()

    def open_message_box(self, text_list):
        self.save_current_menu_to_previous_menus()
        self.message_box.reset_display()
        self.current_menu = self.message_box
        # self.current_menu.update_items(self._get_current_items())
        self.current_menu.show()
        self.current_menu.load_text_list(text_list)

    def open_main_menu(self):
        self.previous_menus = []
        self.current_menu = self.main_menu
        self.current_menu.show()

    def save_current_menu_to_previous_menus(self):
        if self.current_menu:
            self.previous_menus.append(self.current_menu)

    def start_player_choice_phase(self):
        self.current_menu = None
        self.state = STATE_WAITING_FOR_INPUT
        print(f"\nGO STATE_WAITING_FOR_INPUT {self.model.turn_number}\n")

    def end_player_choice_phase(self, player_action):
        self.current_menu = None
        self.previous_menus = []
        self.view.hide_all_menus()
        self.model.add_player_action(player_action)
        # self.model.add_opponent_action(None)
        self.model.prepare_turn()
        self.state = STATE_RESOLVING_TURN
        self.current_event = None
        # self.current_waiting_time = self.max_waiting_time
        print("\nGO STATE_RESOLVING_TURN\n")


    def update(self, dt, events, keys):
        if keys[pygame.K_l]:
            self.view.bottom_status_hud.set_target_hp(-100)
        if keys[pygame.K_m]:
            self.view.bottom_status_hud.set_target_hp(100)

        self.view.update(dt)
        """Traite les touches pressées par le joueur selon l'état actuel."""
        if self.state == STATE_BATTLE_INTRODUCTION:
            self.start_player_choice_phase()

        if self.state == STATE_WAITING_FOR_INPUT:
            if not self.current_menu:
                self.open_main_menu()
            if self.current_menu:
                self.current_menu.handle_input(events, keys)

        elif self.state == STATE_RESOLVING_TURN:
            # 1. PING : On demande l'étape suivante au Model
            if self.current_event is None:
                self.current_event = self.model.get_next_step()
                if self.current_event is None:
                    # Le tour est fini, retour au choix du joueur
                    self.start_player_choice_phase()
                    return
                # On lance l'événement (ex: ouvrir une message_box, lancer une animation)
                self.execute_event(self.current_event)
            # 2. PONG : On vérifie si l'événement en cours est terminé visuellement
            if self.current_event is not None:

                # Si l'événement nécessite une interaction (ex: fermer une message_box)
                # il faut passer les events/keys à l'interface active.
                if self.current_menu:
                    self.current_menu.handle_input(events, keys)
                is_finished = self._is_event_finished()
                if is_finished:
                    # L'action est terminée à l'écran, on remet à None pour redéclencher le PING
                    self.current_event = None

    def execute_event(self, event):
        """Traite l'événement et met à jour l'interface graphique."""
        text_to_display = ""
        if event.type == "FIGHT":
            text_to_display = f"{event.actor.name} utilise {event.detail.name} sur {event.target.name}!"
        elif event.type == "ITEM":
            text_to_display = f"{event.trainer} utilise {event.detail.item_name} sur {event.target.name}!"
        elif event.type == "SWITCH":
            text_to_display = f"{event.trainer}: Reviens {event.actor.name}, go {event.target.name}!"
        elif event.type == "RUN":
            text_to_display = f"{event.trainer} prend la fuite!"

        elif event.type == "DAMAGE":
            # On ne fait pas de texte, on lance juste l'animation !
            self.view.animate_hp(event.new_hp, event.target)
            print(f"Animation des dégâts sur {event.target.name} vers {event.new_hp} HP")
        elif event.type == "ANIMATION":
            self.view.play_animation(event.name, event.target)
            print(f"Playing animation: {event.name} on {event.target}")

        # Au lieu du print, on ouvre la boîte de dialogue avec le texte généré
        if text_to_display:
            print(text_to_display)  # Gardé pour ton debug console
            self.open_message_box([text_to_display])

    def _is_event_finished(self):
        """Vérifie si l'événement visuel en cours est terminé."""
        if not self.current_event:
            return True

        event_type = self.current_event.type

        # Exemple 1 : Événement texte
        if event_type in ["FIGHT", "ITEM", "SWITCH", "RUN", "FAINT"]:
            # L'événement est fini si la message_box n'est plus le menu actif
            # (Cela implique que execute_event a ouvert la message_box, et que le joueur l'a fermée)
            if self.current_menu != self.message_box:
                return True
            return False

        # # Exemple 2 : Animation (pour plus tard)
        elif event_type == "ANIMATION":
            # On demande directement à la vue si l'animation joue encore
            return not self.view.is_animation_playing()

        elif event_type == "DAMAGE":
            # Le Controller "bloque" (renvoie False) tant que la barre bouge !
            # Dès que view.is_hp_animating() devient False, le Controller fera son prochain PING.
            return not self.view.is_hp_animating()

        return True


    def _get_pokemons(self):
        pokemons = self.model.player.party.members
        return pokemons

    def _get_current_pokemon_moves(self):
        pokemon = self.model.active_player_pokemon
        moves = [pokemon.moves[key] for key in pokemon.moves if pokemon.moves[key]]
        return moves

    def _get_current_items(self):
        bag = self.model.player.bag
        items = [slot for slot in bag.slots.copy()]
        return items
