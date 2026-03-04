import pygame

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
        self.cursor_index = 0
        self.current_menu = "MAIN_MENU"

        # Copie de la file d'événements générée par le modèle
        self.event_queue = []
        self.current_event = None

    def handle_input(self, events):
        """Traite les touches pressées par le joueur selon l'état actuel."""
        if self.state == STATE_WAITING_FOR_INPUT:
            choice = input("")

            for event in events:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        # Exemple : le joueur choisit la première attaque
                        self._trigger_turn({"type": "FIGHT", "move": "Thunderbolt"})
                    elif event.key == pygame.K_UP:
                        self.cursor_index = (self.cursor_index - 2) % 4
                    elif event.key == pygame.K_DOWN:
                        print("downnnnnnnn!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                        self.cursor_index = (self.cursor_index + 2) % 4
                    elif event.key == pygame.K_LEFT:
                        self.cursor_index = self.cursor_index + 1 if self.cursor_index%2 == 0 else self.cursor_index - 1
                    elif event.key == pygame.K_RIGHT:
                        self.cursor_index = self.cursor_index + 1 if self.cursor_index%2 == 0 else self.cursor_index - 1


        elif self.state == STATE_WAITING_FOR_VIEW:
            # Si un texte est affiché, on attend que le joueur appuie pour continuer
            if self.view.needs_input_to_advance():
                for event in events:
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                        self.view.clear_message()
                        self._process_next_event()

    def update(self, dt):
        """Met à jour la logique continue (appelé à chaque frame)."""
        # Si la vue est en train d'animer une barre de vie ou un sprite, on attend
        if self.state == STATE_WAITING_FOR_VIEW:
            if not self.view.is_busy() and not self.view.needs_input_to_advance():
                # L'animation (ex: baisse des HP) est finie, on passe à la suite
                self._process_next_event()
        elif self.state == STATE_WAITING_FOR_INPUT:
            self.view.display_main_menu(self.cursor_index)

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