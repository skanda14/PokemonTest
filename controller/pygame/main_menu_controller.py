import pygame
import random

class MainMenuController:
    def __init__(self, model, view, go_message_box, on_fight_chosen, on_switch_chosen, on_item_chosen, on_run_chosen):
        self.model = model
        self.view = view.main_menu_view
        self.cursor_index = 0
        self.choice_length = 4
        self.go_fight = on_fight_chosen
        self.go_item = on_item_chosen
        self.go_run = on_run_chosen
        self.go_switch = on_switch_chosen
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
                    if self.cursor_index == 0:
                        self.go_fight()
                    elif self.cursor_index == 1:
                        self.go_switch()
                    elif self.cursor_index == 2:
                        self.go_item()
                    elif self.cursor_index == 3:
                        # self.go_run()
                        if random.randint(0,10) < 5:
                            self.go_message_box(["Impossible de fuir!"])
                        else:
                            self.go_message_box(["Vous prenez la fuite!"])
                elif event.key == pygame.K_ESCAPE:
                    print("main_menu Escape !")
                elif event.key == pygame.K_UP:
                    self.cursor_index = (self.cursor_index - 2) % self.choice_length
                    self.view.update(self.cursor_index)
                elif event.key == pygame.K_DOWN:
                    self.cursor_index = (self.cursor_index + 2) % self.choice_length
                    self.view.update(self.cursor_index)
                elif event.key == pygame.K_LEFT:
                    self.cursor_index = self.cursor_index - 1 if self.cursor_index % 2 == 0 else self.cursor_index - 1
                    self.view.update(self.cursor_index)
                elif event.key == pygame.K_RIGHT:
                    self.cursor_index = self.cursor_index + 1 if self.cursor_index % 2 == 0 else self.cursor_index - 1
                    self.view.update(self.cursor_index)

    def update(self, dt):
        pass
