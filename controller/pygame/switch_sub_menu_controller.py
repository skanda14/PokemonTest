import pygame


class SwitchSubMenuController:
    def __init__(self, model, view, item_chosen, stats_chosen, cancel_chosen):
        self.model = model
        self.view = view
        self.cursor_index = 0
        self.items = ['ORDRE', 'STATS', 'RETOUR']
        self.pokemon = None
        self.choice_length = len(self.items)
        self.item_chosen = item_chosen
        self.stats_chosen = stats_chosen
        self.cancel_chosen = cancel_chosen
        self.view.init_items(self.items)

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
                    if self.cursor_index == 0:
                        self.item_chosen(self.pokemon)
                    elif self.cursor_index == 1:
                        self.stats_chosen(self.pokemon)
                    else:
                        self.cancel_chosen()
                elif event.key == pygame.K_ESCAPE:
                    self.view.hide()
                    self.cancel_chosen()
                elif event.key == pygame.K_UP:
                    self.cursor_index = max(0, self.cursor_index - 1)
                    # self.cursor_index = (self.cursor_index - 1) % self.choice_length
                    self.view.update(self.cursor_index)
                elif event.key == pygame.K_DOWN:
                    self.cursor_index = min(len(self.items)-1, self.cursor_index + 1)
                    # self.cursor_index = (self.cursor_index + 1) % self.choice_length
                    self.view.update(self.cursor_index)

    def update(self, dt):
        pass


    def update_index(self, index):
        self.cursor_index = index
        self.view.update(self.cursor_index)
