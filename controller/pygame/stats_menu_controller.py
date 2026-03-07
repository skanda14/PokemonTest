import pygame


class StatsMenuController:
    def __init__(self, model, view, id, go_message_box, go_next):
        self.model = model
        self.view = view.stats_menu_1_view if id==1 else view.stats_menu_2_view
        self.cursor_index = 0
        self.pokemon = None
        self.items = []
        self.choice_length = 0
        self.go_next = go_next
        self.go_message_box = go_message_box

    def show(self):
        self.view.show()

    def hide(self):
        self.view.hide()

    def handle_input(self, inputs_manager):
        """Traite les touches pressées par le joueur selon l'état actuel."""
        if inputs_manager.is_key_just_pressed(pygame.K_SPACE) or inputs_manager.is_key_just_pressed(pygame.K_ESCAPE):
            self.view.hide()
            self.go_next(self.items)

    def update(self, dt):
        pass

    def update_items(self, pokemon):
        self.items = pokemon
        self.view.init_items(self.items)

    def update_index(self, index):
        self.cursor_index = index
        self.view.update(self.cursor_index)
