import pygame

class FightMenuController:
    def __init__(self, model, view, go_message_box, move_chosen, cancel_chosen):
        self.model = model
        self.view = view.fight_menu_view
        self.cursor_index = 0
        self.items = []
        self.choice_length = 0
        self.move_chosen = move_chosen
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
                    self.view.hide()
                    move = self.items[self.cursor_index]
                    if move.current_pp > 0:
                        self.move_chosen(move)
                    else:
                        self.go_message_box([f"Plus assez de PP pour {move.name} !"])
                elif event.key == pygame.K_ESCAPE:
                    self.view.hide()
                    self.cancel_chosen()
                elif event.key == pygame.K_UP:
                    if self.choice_length > 0:
                        self.cursor_index = (self.cursor_index - 1) % self.choice_length
                        self.view.update(self.cursor_index)
                elif event.key == pygame.K_DOWN:
                    if self.choice_length > 0:
                        self.cursor_index = (self.cursor_index + 1) % self.choice_length
                        self.view.update(self.cursor_index)

    def update(self, dt):
        pass

    def update_items(self, items):
        self.items = items
        self.choice_length = len(items)
        if self.choice_length == 0:
            self.cursor_index = -1
        self.view.init_items(self.items)

    def update_index(self, index):
        self.cursor_index = index
        self.view.update(self.cursor_index)
