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

    def handle_input(self, inputs_manager):
        """Traite les touches pressées par le joueur selon l'état actuel."""
        if inputs_manager.is_key_just_pressed(pygame.K_SPACE):
            self.go_space()
        elif inputs_manager.is_key_just_pressed(pygame.K_ESCAPE):
            print("main_menu Escape !")
        elif inputs_manager.is_key_just_pressed(pygame.K_UP):
            self.go_up()
        elif inputs_manager.is_key_just_pressed(pygame.K_DOWN):
            self.go_down()
        elif inputs_manager.is_key_just_pressed(pygame.K_LEFT):
            self.go_left()
        elif inputs_manager.is_key_just_pressed(pygame.K_RIGHT):
            self.go_right()

    def go_space(self):
        if self.cursor_index == 0:
            self.go_fight()
        elif self.cursor_index == 1:
            self.go_switch()
        elif self.cursor_index == 2:
            self.go_item()
        elif self.cursor_index == 3:
            if random.randint(0, 10) < 5:
                self.go_message_box(["Impossible de fuir!"])
            else:
                self.go_run()

    def go_up(self):
        if self.cursor_index >= 2:
            self.cursor_index -= 2
        self.view.update(self.cursor_index)

    def go_down(self):
        if (self.cursor_index + 2) < self.choice_length:
            self.cursor_index += 2
        self.view.update(self.cursor_index)

    # def _toggle_column(self):
    #     # L'opérateur XOR (^) inverse le dernier bit.
    #     # Un index pair (ex: 0, 2) devient impair (+1), et un impair (ex: 1, 3) devient pair (-1).
    #     target_index = self.cursor_index ^ 1
    #
    #     # On applique le mouvement uniquement si la case d'à côté existe
    #     if target_index < self.choice_length:
    #         self.cursor_index = target_index
    #         self.view.update(self.cursor_index)

    def go_left(self):
        # Si l'index est impair, on est dans la colonne de droite, donc on peut aller à gauche (-1).
        # S'il est pair, on est déjà tout à gauche, on ne fait rien.
        if self.cursor_index % 2 != 0:
            self.cursor_index -= 1

        self.view.update(self.cursor_index)

    def go_right(self):
        # Il faut impérativement vérifier que l'élément de droite existe (qu'il est inférieur à choice_length).
        if self.cursor_index % 2 == 0 and (self.cursor_index + 1) < self.choice_length:
            self.cursor_index += 1

        self.view.update(self.cursor_index)

    def update(self, dt):
        pass
