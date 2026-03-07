import pygame

class FightMenuController:
    def __init__(self, model, view, go_message_box, move_chosen, cancel_chosen):
        self.model = model
        self.view = view.fight_menu_view
        self.cursor_index = -1
        self.items = []
        self.choice_length = 0
        self.move_chosen = move_chosen
        self.cancel_chosen = cancel_chosen
        self.go_message_box = go_message_box


    def show(self):
        self.view.show()

    def hide(self):
        self.view.hide()

    def handle_input(self, inputs_manager):
        """Traite les touches pressées par le joueur selon l'état actuel."""
        if inputs_manager.is_key_just_pressed(pygame.K_SPACE):
            self.go_space()
        elif inputs_manager.is_key_just_pressed(pygame.K_ESCAPE):
            self.go_escape()
        elif inputs_manager.is_key_just_pressed(pygame.K_UP):
            self.go_up()
        elif inputs_manager.is_key_just_pressed(pygame.K_DOWN):
            self.go_down()

    def go_space(self):
        self.view.hide()
        move = self.items[self.cursor_index]
        if move.current_pp > 0:
            self.move_chosen(move)
        else:
            self.go_message_box([f"Plus assez de PP pour {move.name} !"])

    def go_escape(self):
        self.view.hide()
        self.cancel_chosen()

    def go_up(self):
        # Recule d'un cran. Si index = 0, le modulo renvoie automatiquement au dernier élément.
        self.cursor_index = (self.cursor_index - 1) % self.choice_length
        self.view.update(self.cursor_index)

    def go_down(self):
        # Avance d'un cran. Si on dépasse le dernier élément, le modulo ramène à 0.
        self.cursor_index = (self.cursor_index + 1) % self.choice_length
        self.view.update(self.cursor_index)

    def update(self, dt):
        pass

    def update_items(self, items):
        self.items = items
        self.choice_length = len(items)
        if self.choice_length == 0:
            self.cursor_index = -1
        else:
            if self.cursor_index == -1:
                self.cursor_index = 0
        self.view.init_items(self.items)

    def update_index(self, index):
        self.cursor_index = index
        self.view.update(self.cursor_index)
