import pygame
from controller.pygame.main_menu_controller import MainMenuController
from controller.pygame.fight_menu_controller import FightMenuController
from controller.pygame.item_menu_controller import ItemMenuController

# Les différents états du contrôleur
STATE_WAITING_FOR_INPUT = "WAITING_FOR_INPUT"
STATE_EXECUTING_EVENTS = "EXECUTING_EVENTS"
STATE_WAITING_FOR_VIEW = "WAITING_FOR_VIEW"
STATE_BATTLE_OVER = "BATTLE_OVER"


class BattleController:
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.state = STATE_WAITING_FOR_INPUT
        self.main_menu = MainMenuController(model=self.model, view=self.view.main_menu_view, on_fight_chosen=self.open_fight_menu, on_item_chosen=self.open_item_menu, on_run_chosen=self.run_chosen)
        self.fight_menu = FightMenuController(model=self.model, view=self.view.fight_menu_view, move_chosen=self.move_chosen, cancel_chosen=self.cancel_chosen)
        self.item_menu = ItemMenuController(model=self.model, view=self.view.item_menu_view, item_chosen=self.item_chosen, cancel_chosen=self.cancel_chosen)
        self.current_menu = None

        # Copie de la file d'événements générée par le modèle
        self.event_queue = []
        self.current_event = None
        self.open_main_menu()

    # -----------------------------------------------------------------
    # --- Les Callbacks de navigation ---
    # -----------------------------------------------------------------

    def cancel_chosen(self):
        self.current_menu = self.main_menu
        print('Cancel !')

    def move_chosen(self, choice_index):
        self.current_menu = self.main_menu
        print(f'Move {choice_index} !')

    def item_chosen(self, choice_index):
        self.current_menu = self.main_menu
        print(f'Item {choice_index} !')

    def open_fight_menu(self):
        self.current_menu = self.fight_menu
        self.current_menu.update_items(self._get_current_pokemon_moves())
        self.current_menu.show()

    def open_item_menu(self):
        self.current_menu = self.item_menu
        self.current_menu.update_items(self._get_current_items())
        self.current_menu.show()

    def run_chosen(self):
        self.current_menu = self.main_menu
        print("Run !")

    def open_main_menu(self):
        self.current_menu = self.main_menu
        self.current_menu.show()

    def handle_input(self, events):
        """Traite les touches pressées par le joueur selon l'état actuel."""
        if self.state == STATE_WAITING_FOR_INPUT:
            if self.current_menu:
                self.current_menu.handle_input(events)

        # elif self.state == STATE_WAITING_FOR_VIEW:
        #     # Si un texte est affiché, on attend que le joueur appuie pour continuer
        #     if self.view.needs_input_to_advance():
        #         for event in events:
        #             if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
        #                 self.view.clear_message()
        #                 self._process_next_event()

    def display_new_menu(self):
        print(f" {self.current_menu} : {self.cursor_index}")
        if self.current_menu == "MAIN_MENU":
            match self.cursor_index:
                case 0:
                    current_moves = self._get_current_pokemon_moves()
                    self.len_items = len(current_moves)
                    self.view.display_move_menu(current_moves)
                    self.current_menu = "MOVE_MENU"
                    self.cursor_index = 0

        elif self.current_menu == "MOVE_MENU":
            self.view.display_move_menu(self._get_current_pokemon_moves())


    def update(self, dt):
        """Met à jour la logique continue (appelé à chaque frame)."""
        # # Si la vue est en train d'animer une barre de vie ou un sprite, on attend
        # if self.state == STATE_WAITING_FOR_VIEW:
        #     if not self.view.is_busy() and not self.view.needs_input_to_advance():
        #         # L'animation (ex: baisse des HP) est finie, on passe à la suite
        #         self._process_next_event()
        # elif self.state == STATE_WAITING_FOR_INPUT:
        #     if self.current_menu == "MAIN_MENU":
        #         self.view.display_main_menu()
        #     elif self.current_menu == "MOVE_MENU":
        #         self.view.display_move_menu(self._get_current_pokemon_moves())

    def _get_current_pokemon_moves(self):
        pokemon = self.model.active_player_pokemon
        moves = [pokemon.moves[key] for key in pokemon.moves if pokemon.moves[key]]
        return moves

    def _get_current_items(self):
        bag = self.model.player.bag
        items = [slot for slot in bag.slots.copy()]
        return items

    def _trigger_turn(self, player_action):
        """Lance les calculs du modèle et récupère les événements à afficher."""
        # IA très basique pour l'adversaire
        enemy_action = {"type": "FIGHT", "move": "Tackle"}

        # Le Modèle calcule tout instantanément
        self.event_queue = self.model.execute_turn(player_action, enemy_action)

        # On change l'état pour commencer à "dépiler" les événements
        self.state = STATE_EXECUTING_EVENTS
        self._process_next_event()

    def _process_next_event(self):
        """Prend le prochain événement de la liste et demande à la View de l'afficher."""
        if not self.event_queue:
            # S'il n'y a plus d'événements, le tour est fini
            if self.model.is_over:
                self.state = STATE_BATTLE_OVER
            else:
                self.state = STATE_WAITING_FOR_INPUT
            return

        self.current_event = self.event_queue.pop(0)
        self.state = STATE_WAITING_FOR_VIEW
        event_type = self.current_event["type"]

        # -----------------------------------------------------------------
        # Le Controller "traduit" les données du Model en commandes visuelles
        # -----------------------------------------------------------------
        if event_type == "MESSAGE":
            self.view.display_text(self.current_event["text"])

        elif event_type == "DAMAGE":
            target = self.current_event["target"]
            new_hp = self.current_event["new_hp"]
            self.view.animate_hp_bar(target, new_hp)

        elif event_type == "FAINT":
            target = self.current_event["target"]
            self.view.animate_faint(target)

        elif event_type == "BATTLE_END":
            winner = self.current_event["winner"]
            self.view.display_text(f"Battle Ended! Winner: {winner}")