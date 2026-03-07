import pygame
from settings import DELAY_BETWEEN_CHARS, DELAY_FOR_SCROLLING, AUTO_SCROLL_DELAY, AUTO_SCROLL


class MessageBoxController:
    def __init__(self, model, view, back, displaying_speed="default"):
        self.model = model
        self.view = view.message_box_view
        self.back = back

        self.text_list = []
        self.current_string = None
        self.current_word = None

        self.column_len = self.view.column_len
        self.row_len = self.view.row_len
        self.column = 0
        self.row = 0
        self.scrolling = 0
        self.delay_between_chars = DELAY_BETWEEN_CHARS if displaying_speed=="default" else 0
        self.delay_for_scrolling = DELAY_FOR_SCROLLING
        self.auto_scroll_delay = AUTO_SCROLL_DELAY
        self.timer_before_next_char = self.delay_between_chars
        self.timer_before_auto_scroll = self.auto_scroll_delay

        self.column = 0
        self.row = 1
        self.scrolling = 0
        self.go_reset = False
        self.over = True
        self.pause = False
        self.auto_scroll = AUTO_SCROLL
        self.view.showing_cursor = False

    def show(self):
        self.view.show()

    def hide(self):
        self.view.hide()
        # self.back()

    def load_text_list(self, text_list):
        if text_list:
            self.view.erase_all_lines()
            self.text_list = text_list
            self.current_string = self.text_list.pop(0)
            self.over = False
            self.pause = False
            self.view.showing_cursor = False
            self.view.visible = True

    def reset_display(self):
        self.view.erase_all_lines()
        self.column = 0
        self.row = 1
        self.scrolling = 0
        self.timer_before_next_char = self.delay_between_chars

    def handle_input(self, inputs_manager):
        self.update(inputs_manager)

    def wait_a_press(self):
        self.pause = True
        if not self.auto_scroll:
            self.view.showing_cursor = True  # affiche le curseur si pas d'auto-scroll
        # On réinitialise le timer d'auto-scroll à chaque nouvelle pause
        self.timer_before_auto_scroll = self.auto_scroll_delay

    def wait_a_press_for_next_text(self):
        self.go_reset = True
        self.current_string = self.text_list.pop(0)
        self.wait_a_press()

    def display_text_instantly(self, text_list=None):
        """Affiche instantanément tout le texte jusqu'à remplir la boîte."""
        # 1. On charge le nouveau texte si on en fournit un
        if text_list is not None:
            self.load_text_list(text_list)

        # 2. On sauvegarde les délais originaux pour les restaurer à la fin
        original_char_delay = self.delay_between_chars
        original_scroll_delay = self.delay_for_scrolling

        # On force les délais à 0 pour tout afficher sur la même frame
        self.delay_between_chars = 0
        self.delay_for_scrolling = 0
        self.timer_before_next_char = 0

        # 3. On boucle pour traiter tous les mots jusqu'à ce que la boîte demande une pause
        while not self.over and not self.pause:
            # Gestion du défilement instantané
            if self.scrolling > 0:
                self.scrolling -= 1
                self.view.scroll_upward()
                continue

            # Fin de la chaîne en cours
            if not self.current_word and not self.current_string:
                if self.text_list:
                    self.wait_a_press_for_next_text()  # Ceci va mettre self.pause = True
                else:
                    self.go_reset = True
                    self.over = True
                    self.wait_a_press()  # Ceci va mettre self.pause = True
                break

            # Récupération d'un nouveau mot
            if not self.current_word:
                self.current_word = self.cut_first_word()
                if self.current_word not in [" ",
                                             "\n"] and not self.is_there_room_for_current_word_on_the_current_row():
                    if self.is_the_current_word_a_compound_word() and self.is_there_room_for_first_part_of_current_compound_word():
                        self.keep_first_half_of_current_compound_word_and_returns_second_part_in_message()
                    else:
                        self.go_next_row()
                        if self.pause:
                            break
                        continue

            # Affichage du mot
            if self.current_word:
                self.display_word()

        # 4. On restaure les paramètres normaux pour la prochaine fois
        self.delay_between_chars = original_char_delay
        self.delay_for_scrolling = original_scroll_delay
        self.view.showing_cursor = False

    def update(self, inputs_manager):
        # 1. ÉTAT DE PAUSE : On attend une action du joueur (ou l'auto-scroll)
        if self.pause:
            # Par défaut, on valide si le joueur appuie sur Espace
            validate_input = inputs_manager.is_key_just_pressed(pygame.K_SPACE)

            # Si l'auto-scroll est actif, on décrémente le timer
            if self.auto_scroll:
                self.timer_before_auto_scroll = max(self.timer_before_auto_scroll - 1, 0)
                # Si le timer est écoulé, on simule une validation
                if self.timer_before_auto_scroll <= 0:
                    validate_input = True

            # Si l'entrée est validée (par le joueur OU par l'auto-scroll)
            if validate_input:
                if self.over:
                    self.hide()
                    self.back()
                    self.pause = False
                    self.view.showing_cursor = False
                    return

                if self.go_reset:
                    self.reset_display()
                    self.go_reset = False

                self.pause = False
                self.view.showing_cursor = False
                self.scrolling = 2
            return  # On bloque la suite du code tant qu'on est en pause

        # 2. Si le dialogue est totalement terminé (et qu'on a déjà quitté la dernière pause)
        if self.over:
            return

        # --- BOUCLE PRINCIPALE : Permet d'afficher tout d'un coup si le délai est à 0 ---
        while True:
            # 3. ÉTAT D'ATTENTE : Gestion du délai entre chaque caractère
            self.timer_before_next_char = max(self.timer_before_next_char - 1, 0)
            if self.timer_before_next_char > 0:
                return  # Le timer n'est pas à 0, on attend la frame suivante

            # 4. ÉTAT DE DÉFILEMENT (Scrolling)
            if self.scrolling > 0:
                self.scrolling -= 1
                self.view.scroll_upward()
                self.timer_before_next_char = self.delay_for_scrolling
                return  # Pendant que le texte monte, on n'affiche pas de nouvelles lettres

            # --- À partir d'ici, on sait avec certitude qu'on doit traiter du texte ---

            # 5. Si la phrase en cours est vide et qu'on n'a plus de mot sous la main
            if not self.current_word and not self.current_string:
                if self.text_list:
                    self.wait_a_press_for_next_text()
                else:
                    self.go_reset = True
                    self.over = True
                    self.wait_a_press()  # Gère self.pause = True et showing_cursor = True en interne
                return  # Sort de la boucle et de la fonction (en attente d'input)

            # 6. Si on a besoin d'un nouveau mot pour continuer
            if not self.current_word:
                self.current_word = self.cut_first_word()
                # Vérification de la place sur la ligne
                if self.current_word not in [" ",
                                             "\n"] and not self.is_there_room_for_current_word_on_the_current_row():
                    # Cas spécial : C'est un mot composé qu'on a la place de couper en deux
                    if self.is_the_current_word_a_compound_word() and self.is_there_room_for_first_part_of_current_compound_word():
                        self.keep_first_half_of_current_compound_word_and_returns_second_part_in_message()
                    # Sinon : Pas de place du tout, on passe à la ligne
                    else:
                        self.go_next_row()
                        # Si ce changement de ligne remplit la boîte et déclenche une pause :
                        if self.pause:
                            return
                        # Si on a un délai actif, on respecte le délai initial de 1 frame pour sauter une ligne
                        if self.delay_between_chars > 0:
                            return
                            # Sinon (délai = 0), on enchaîne tout de suite
                        continue

                        # 7. Affichage du mot en cours
            if self.current_word:
                self.display_word()

            # --- CONDITIONS DE FIN DE BOUCLE ---
            # Si le jeu s'est mis en pause suite à l'affichage (boîte pleine par ex.), on quitte
            if self.pause:
                return

            # Si un délai est paramétré (> 0), on casse la boucle pour ne traiter qu'une lettre par frame
            if self.delay_between_chars > 0:
                break

    def display_word(self):
        current_char = self.current_word[0]
        self.current_word = self.current_word[1:]
        if current_char == "\n":
            self.go_next_row()
            self.timer_before_next_char = self.delay_between_chars
        elif current_char == " ":
            # On imbrique la condition d'espace pour plus de clarté
            if self.is_there_room_for_this_word_on_the_current_row(current_char):
                self.display_a_character(current_char)
                # (Le timer n'est pas réinitialisé ici, l'espace s'affiche instantanément)
            else:
                self.go_next_row()
                self.timer_before_next_char = self.delay_between_chars
        else:
            self.display_a_character(current_char)
            self.timer_before_next_char = self.delay_between_chars

    def display_a_character(self, char):
        self.view.display_a_character((self.column, self.row), char)
        self.column += 1

    def go_next_row(self):
        if self.row < 2:
            self.row += 2
        else:
            self.wait_a_press()
        self.column = 0

    def cut_first_word(self):
        new_word = ""
        # La boucle tourne tant qu'il y a des caractères dans current_string
        while self.current_string:
            new_char = self.current_string[0]
            # Cas 1 : Espace ou retour à la ligne
            if new_char in [" ", "\n"]:
                if len(new_word) == 0:
                    new_word += new_char
                    self.current_string = self.current_string[1:]
                break  # On a trouvé la fin du mot, on sort de la boucle
            # Cas 2 : Le mot dépasse la taille de la boîte
            elif len(new_word) >= self.column_len:
                # On remet la dernière lettre lue dans current_string et on met un tiret
                self.current_string = new_word[-1] + self.current_string
                new_word = new_word[:-1] + "-"
                break  # Le mot est coupé, on sort de la boucle
            # Cas 3 : On ajoute la lettre au mot en cours
            else:
                new_word += new_char
                self.current_string = self.current_string[1:]
        return new_word

    def is_there_room_for_current_word_on_the_current_row(self):
        return self.is_there_room_for_this_word_on_the_current_row(self.current_word)

    def is_there_room_for_this_word_on_the_current_row(self, word):
        remaining_space = self.get_remaining_space_on_row()
        if remaining_space >= len(word):
            return True
        return False

    def get_remaining_space_on_row(self):
        return self.column_len - self.column

    def is_the_current_word_a_compound_word(self):
        if len(self.current_word) < 3:
            return False
        if "-" in self.current_word[1:-1]:
            return True
        return False

    def is_there_room_for_first_part_of_current_compound_word(self):
        part_1, part_2 = self.get_current_compound_word_split_in_two_part()
        return self.is_there_room_for_this_word_on_the_current_row(part_1)

    def keep_first_half_of_current_compound_word_and_returns_second_part_in_message(self):
        part_1, part_2 = self.get_current_compound_word_split_in_two_part()
        self.current_word = part_1
        self.current_string = part_2 + self.current_string

    def get_current_compound_word_split_in_two_part(self):
        reduced_word = self.current_word[1:-1]
        parts = reduced_word.split('-', 1)
        return self.current_word[0] + parts[0] + "-", parts[1] + self.current_word[-1]

# import pygame
# from settings import DELAY_BETWEEN_CHARS, DELAY_FOR_SCROLLING, AUTO_SCROLL_DELAY, AUTO_SCROLL
#
#
# class MessageBoxController:
#     def __init__(self, model, view, back):
#         self.model = model
#         self.view = view.message_box_view
#         self.back = back
#
#         self.text_list = []
#         self.current_string = None
#         self.current_word = None
#
#         self.column_len = self.view.column_len
#         self.row_len = self.view.row_len
#         self.column = 0
#         self.row = 0
#         self.scrolling = 0
#         self.delay_between_chars = DELAY_BETWEEN_CHARS
#         self.delay_for_scrolling = DELAY_FOR_SCROLLING
#         self.auto_scroll_delay = AUTO_SCROLL_DELAY
#         self.timer_before_next_char = self.delay_between_chars
#         self.timer_before_auto_scroll = self.auto_scroll_delay
#
#         self.column = 0
#         self.row = 1
#         self.scrolling = 0
#         self.go_reset = False
#         self.over = True
#         self.pause = False
#         self.auto_scroll = AUTO_SCROLL
#         self.view.showing_cursor = False
#
#     def show(self):
#         self.view.show()
#
#     def hide(self):
#         self.view.hide()
#         # self.back()
#
#     def load_text_list(self, text_list):
#         if text_list:
#             self.view.erase_all_lines()
#             self.text_list = text_list
#             self.current_string = self.text_list.pop(0)
#             self.over = False
#             self.pause = False
#             self.view.showing_cursor = False
#             self.view.visible = True
#
#     def reset_display(self):
#         self.view.erase_all_lines()
#         self.column = 0
#         self.row = 1
#         self.scrolling = 0
#         self.timer_before_next_char = self.delay_between_chars
#
#     def handle_input(self, events, keys):
#         self.update(keys)
#
#     def wait_a_press(self):
#         self.pause = True
#         if not self.auto_scroll:
#             self.view.showing_cursor = True # affiche le curseur si pas d'auto-scroll
#         # On réinitialise le timer d'auto-scroll à chaque nouvelle pause
#         self.timer_before_auto_scroll = self.auto_scroll_delay
#
#     def wait_a_press_for_next_text(self):
#         self.go_reset = True
#         self.current_string = self.text_list.pop(0)
#         self.wait_a_press()
#
#     def update(self, keys):
#         # 1. ÉTAT DE PAUSE : On attend une action du joueur (ou l'auto-scroll)
#         if self.pause:
#             # Par défaut, on valide si le joueur appuie sur Espace
#             validate_input = keys[pygame.K_SPACE]
#
#             # Si l'auto-scroll est actif, on décrémente le timer
#             if self.auto_scroll:
#                 self.timer_before_auto_scroll = max(self.timer_before_auto_scroll - 1, 0)
#                 # Si le timer est écoulé, on simule une validation
#                 if self.timer_before_auto_scroll <= 0:
#                     validate_input = True
#
#             # Si l'entrée est validée (par le joueur OU par l'auto-scroll)
#             if validate_input:
#                 if self.over:
#                     self.hide()
#                     self.back()
#                     self.pause = False
#                     self.view.showing_cursor = False
#                     return
#
#                 if self.go_reset:
#                     self.reset_display()
#                     self.go_reset = False
#
#                 self.pause = False
#                 self.view.showing_cursor = False
#                 self.scrolling = 2
#             return  # On bloque la suite du code tant qu'on est en pause
#
#         # 2. Si le dialogue est totalement terminé (et qu'on a déjà quitté la dernière pause)
#         if self.over:
#             return
#
#         # 3. ÉTAT D'ATTENTE : Gestion du délai entre chaque caractère
#         self.timer_before_next_char = max(self.timer_before_next_char - 1, 0)
#         if self.timer_before_next_char > 0:
#             return  # Le timer n'est pas à 0, on attend la frame suivante
#
#         # 4. ÉTAT DE DÉFILEMENT (Scrolling)
#         if self.scrolling > 0:
#             self.scrolling -= 1
#             self.view.scroll_upward()
#             self.timer_before_next_char = self.delay_for_scrolling
#             return  # Pendant que le texte monte, on n'affiche pas de nouvelles lettres
#
#         # --- À partir d'ici, on sait avec certitude qu'on doit traiter du texte ---
#
#         # 5. Si la phrase en cours est vide et qu'on n'a plus de mot sous la main
#         if not self.current_word and not self.current_string:
#             if self.text_list:
#                 self.wait_a_press_for_next_text()
#             else:
#                 self.go_reset = True
#                 self.over = True
#                 self.wait_a_press()  # Gère self.pause = True et showing_cursor = True en interne
#             return
#
#         # 6. Si on a besoin d'un nouveau mot pour continuer
#         if not self.current_word:
#             self.current_word = self.cut_first_word()
#             # Vérification de la place sur la ligne
#             if self.current_word not in [" ", "\n"] and not self.is_there_room_for_current_word_on_the_current_row():
#                 # Cas spécial : C'est un mot composé qu'on a la place de couper en deux
#                 if self.is_the_current_word_a_compound_word() and self.is_there_room_for_first_part_of_current_compound_word():
#                     self.keep_first_half_of_current_compound_word_and_returns_second_part_in_message()
#                 # Sinon : Pas de place du tout, on passe à la ligne
#                 else:
#                     self.go_next_row()
#                     return  # On coupe ici pour commencer l'affichage à la frame suivante
#
#         # 7. Affichage du mot en cours
#         if self.current_word:
#             self.display_word()
#
#     def display_word(self):
#         current_char = self.current_word[0]
#         self.current_word = self.current_word[1:]
#         if current_char == "\n":
#             self.go_next_row()
#             self.timer_before_next_char = self.delay_between_chars
#         elif current_char == " ":
#             # On imbrique la condition d'espace pour plus de clarté
#             if self.is_there_room_for_this_word_on_the_current_row(current_char):
#                 self.display_a_character(current_char)
#                 # (Le timer n'est pas réinitialisé ici, l'espace s'affiche instantanément)
#             else:
#                 self.go_next_row()
#                 self.timer_before_next_char = self.delay_between_chars
#         else:
#             self.display_a_character(current_char)
#             self.timer_before_next_char = self.delay_between_chars
#
#     def display_a_character(self, char):
#         self.view.display_a_character((self.column, self.row), char)
#         self.column += 1
#
#     def go_next_row(self):
#         if self.row < 2:
#             self.row += 2
#         else:
#             self.wait_a_press()
#         self.column = 0
#
#     def cut_first_word(self):
#         new_word = ""
#         # La boucle tourne tant qu'il y a des caractères dans current_string
#         while self.current_string:
#             new_char = self.current_string[0]
#             # Cas 1 : Espace ou retour à la ligne
#             if new_char in [" ", "\n"]:
#                 if len(new_word) == 0:
#                     new_word += new_char
#                     self.current_string = self.current_string[1:]
#                 break  # On a trouvé la fin du mot, on sort de la boucle
#             # Cas 2 : Le mot dépasse la taille de la boîte
#             elif len(new_word) >= self.column_len:
#                 # On remet la dernière lettre lue dans current_string et on met un tiret
#                 self.current_string = new_word[-1] + self.current_string
#                 new_word = new_word[:-1] + "-"
#                 break  # Le mot est coupé, on sort de la boucle
#             # Cas 3 : On ajoute la lettre au mot en cours
#             else:
#                 new_word += new_char
#                 self.current_string = self.current_string[1:]
#         return new_word
#
#     def is_there_room_for_current_word_on_the_current_row(self):
#         return self.is_there_room_for_this_word_on_the_current_row(self.current_word)
#
#     def is_there_room_for_this_word_on_the_current_row(self, word):
#         remaining_space = self.get_remaining_space_on_row()
#         if remaining_space >= len(word):
#             return True
#         return False
#
#     def get_remaining_space_on_row(self):
#         return self.column_len - self.column
#
#     def is_the_current_word_a_compound_word(self):
#         if len(self.current_word) < 3:
#             return False
#         if "-" in self.current_word[1:-1]:
#             return True
#         return False
#
#     def is_there_room_for_first_part_of_current_compound_word(self):
#         part_1, part_2 = self.get_current_compound_word_split_in_two_part()
#         return self.is_there_room_for_this_word_on_the_current_row(part_1)
#
#     def keep_first_half_of_current_compound_word_and_returns_second_part_in_message(self):
#         part_1, part_2 = self.get_current_compound_word_split_in_two_part()
#         self.current_word = part_1
#         self.current_string = part_2 + self.current_string
#
#     def get_current_compound_word_split_in_two_part(self):
#         reduced_word = self.current_word[1:-1]
#         parts = reduced_word.split('-', 1)
#         return self.current_word[0]+parts[0]+"-", parts[1]+self.current_word[-1]
