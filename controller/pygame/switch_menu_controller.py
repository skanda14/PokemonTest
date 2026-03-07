import pygame

class SwitchMenuController:
    def __init__(self, model, view, go_message_box, pokemon_chosen, cancel_chosen):
        self.model = model
        self.view = view.switch_target_selection_menu_view
        self.cursor_index = 0
        self.items = []
        self.choice_length = 0
        self.pokemon_chosen = pokemon_chosen
        self.cancel_chosen = cancel_chosen
        self.go_message_box = go_message_box


    def show(self):
        self.view.show()

    def hide(self):
        self.view.hide()

    def handle_input(self, events, keys):
        """Traite les touches pressées par le joueur selon l'état actuel."""
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    # self.view.hide()
                    self.pokemon_chosen(self.items[self.cursor_index])
                elif event.key == pygame.K_ESCAPE:
                    # self.view.hide()
                    self.cancel_chosen()
                elif event.key == pygame.K_UP:
                    self.cursor_index = (self.cursor_index - 1) % self.choice_length
                    self.view.update(self.cursor_index)
                elif event.key == pygame.K_DOWN:
                    self.cursor_index = (self.cursor_index + 1) % self.choice_length
                    self.view.update(self.cursor_index)

    def update(self, dt):
        pass

    def update_items(self, items):
        self.items = items
        self.choice_length = len(items)
        self.view.init_items(self.items)

    def update_index(self, index):
        self.cursor_index = index
        self.view.update(self.cursor_index)


