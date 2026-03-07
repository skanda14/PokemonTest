import pygame


class ItemTargetMenuController:
    def __init__(self, model, view, go_message_box, pokemon_chosen, cancel_chosen):
        self.model = model
        self.view = view.item_target_selection_menu_view
        self.cursor_index = 0
        self.chosen_consommable = None
        self.items = []
        self.choice_length = 0
        self.pokemon_chosen = pokemon_chosen
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
        pokemon = self.items[self.cursor_index]
        # self.go_message_box([f"Impossible to select {pokemon.name.upper()}"])
        self.pokemon_chosen(pokemon, self.chosen_consommable)

    def go_escape(self):
        self.view.hide()
        self.cancel_chosen()

    def go_up(self):
        self.cursor_index = (self.cursor_index - 1) % self.choice_length
        self.view.update(self.cursor_index)

    def go_down(self):
        self.cursor_index = (self.cursor_index + 1) % self.choice_length
        self.view.update(self.cursor_index)

    def update(self, dt):
        pass

    def update_consommable(self, consommable):
        self.chosen_consommable = consommable

    def update_items(self, items):
        self.items = items
        self.choice_length = len(items)
        self.view.init_items(self.items)
        self.update_index(self.cursor_index)

    def update_index(self, index):
        self.cursor_index = index
        self.view.update(self.cursor_index)


