import pygame


class StatsMenuController:
    def __init__(self, model, view, go_next):
        self.model = model
        self.view = view
        self.cursor_index = 0
        self.pokemon = None
        self.items = []
        self.choice_length = 0
        self.go_next = go_next

    def show(self):
        self.view.show()

    def hide(self):
        self.view.hide()

    def handle_input(self, events):
        """Traite les touches pressées par le joueur selon l'état actuel."""
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.view.hide()
                    self.go_next(self.items)
                elif event.key == pygame.K_ESCAPE:
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
