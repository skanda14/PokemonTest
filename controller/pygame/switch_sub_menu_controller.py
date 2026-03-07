import pygame


class SwitchSubMenuController:
    def __init__(self, model, view, go_message_box, item_chosen, stats_chosen, cancel_chosen):
        self.model = model
        self.view = view.switch_sub_menu_view
        self.cursor_index = 0
        self.items = ['ORDRE', 'STATS', 'RETOUR']
        self.pokemon = None
        self.choice_length = len(self.items)
        self.item_chosen = item_chosen
        self.stats_chosen = stats_chosen
        self.cancel_chosen = cancel_chosen
        self.go_message_box = go_message_box
        self.view.init_items(self.items)

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
        if self.cursor_index == 0:
            self.item_chosen(self.pokemon)

            # if self.pokemon.stats['hp'] <= 0:
            #     self.go_message_box([f"{self.pokemon.name.upper()} est KO !"])
            # else:
            #     self.item_chosen(self.pokemon)
        elif self.cursor_index == 1:
            self.stats_chosen(self.pokemon)
        else:
            self.cancel_chosen()

    def go_escape(self):
        self.view.hide()
        self.cancel_chosen()

    def go_up(self):
        self.cursor_index = max(0, self.cursor_index - 1)
        # self.cursor_index = (self.cursor_index - 1) % self.choice_length
        self.view.update(self.cursor_index)

    def go_down(self):
        self.cursor_index = min(len(self.items) - 1, self.cursor_index + 1)
        # self.cursor_index = (self.cursor_index + 1) % self.choice_length
        self.view.update(self.cursor_index)

    def update(self, dt):
        pass


    def update_index(self, index):
        self.cursor_index = index
        self.view.update(self.cursor_index)
