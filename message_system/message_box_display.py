import pygame
from settings import MESSAGE_TILE_WIDTH, MESSAGE_TILE_HEIGHT
from message_system.character_display import CharDisplay

#TODO ajouter un effet d'apparition pour les char_display (alpha de 0 à 255 en x temps)


class MessageBox:
    def __init__(self, text_list, sprites_dict):
        grid_pos, grid_size = (0,12), (20,6)
        self.rect = pygame.Rect(grid_pos[0]*MESSAGE_TILE_WIDTH, grid_pos[1]*MESSAGE_TILE_HEIGHT, grid_size[0]*MESSAGE_TILE_WIDTH, grid_size[1]*MESSAGE_TILE_HEIGHT)
        self.sprite = pygame.image.load("assets/sprites/battle interface/message_box.png").convert()
        self.chars_display = [[CharDisplay(pygame.Rect(x, y, MESSAGE_TILE_WIDTH, MESSAGE_TILE_HEIGHT), sprites_dict, )
                               for x in range(self.rect.left+MESSAGE_TILE_WIDTH, self.rect.right-2*MESSAGE_TILE_WIDTH, MESSAGE_TILE_WIDTH)]
                              for y in range(self.rect.top+MESSAGE_TILE_HEIGHT, self.rect.bottom-MESSAGE_TILE_HEIGHT, MESSAGE_TILE_HEIGHT)]
        self.go_on_char = CharDisplay(pygame.Rect(self.rect.right-2*MESSAGE_TILE_WIDTH, self.rect.bottom-2*MESSAGE_TILE_HEIGHT, MESSAGE_TILE_WIDTH, MESSAGE_TILE_HEIGHT), sprites_dict, "^")

        self.text_list = text_list
        self.current_string = self.text_list.pop(0)
        self.current_word = None

        self.column_len = len(self.chars_display[0])
        self.row_len = len(self.chars_display)
        self.column = 0
        self.row = 1
        self.scrolling = 0
        self.delay_between_chars = 1
        self.delay_for_scrolling = 6
        self.auto_scroll_delay = 10
        self.blink_interval = 600
        self.timer_before_auto_scroll = self.auto_scroll_delay
        self.timer_before_next_char = self.delay_between_chars
        self.over = False
        self.pause = False
        self.go_reset = False
        self.auto_scroll = False
        self.visible = True

    def update(self, keys):
        if not self.over:
            if self.pause:
                if self.auto_scroll:
                    self.timer_before_auto_scroll = max(self.timer_before_auto_scroll - 1, 0)
                if keys[pygame.K_SPACE] or not self.timer_before_auto_scroll:
                    self.timer_before_auto_scroll = self.auto_scroll_delay
                    if self.go_reset:
                        self.reset_display()
                        self.go_reset = False
                    self.pause = False
                    self.scrolling = 2
            else:
                self.timer_before_next_char = max(self.timer_before_next_char - 1, 0)
                if self.timer_before_next_char <= 0:
                    if self.scrolling:
                        self.scrolling -= 1
                        self.scroll_upward()
                        self.timer_before_next_char = self.delay_for_scrolling
                    else:
                        if not self.current_word and not self.current_string:
                            if self.text_list:
                                self.wait_a_press_for_next_text()
                            else:
                                self.go_reset = True
                                self.wait_a_press()
                                self.over = True
                                self.pause = True
                        elif not self.current_word and self.current_string:
                            self.current_word = self.cut_first_word() # couper le 1er mot du message
                            if not self.current_word in [" ", "\n"] and not self.is_there_room_for_current_word_on_the_current_row(): # si "vrai" mot et pas la place sur la ligne
                                if self.is_the_current_word_a_compound_word():
                                    if self.is_there_room_for_first_part_of_current_compound_word():
                                        self.keep_first_half_of_current_compound_word_and_returns_second_part_in_message()
                                        self.display_word()
                                    else:
                                        self.go_next_row()
                                else:
                                    self.go_next_row()
                        elif self.current_word:
                            self.display_word()
            return self
        else:
            if keys[pygame.K_SPACE]:
                self.pause = False
                self.visible = False
                return None
            else:
                return self

    def display_word(self):
        current_char = self.current_word[0]
        self.current_word = self.current_word[1:]
        if current_char == "\n":
            self.go_next_row()
            self.timer_before_next_char = self.delay_between_chars
        elif current_char == " " and self.is_there_room_for_this_word_on_the_current_row(current_char):
            self.display_a_character(current_char)
        elif current_char == " " and not self.is_there_room_for_this_word_on_the_current_row(current_char):
            self.go_next_row()
            self.timer_before_next_char = self.delay_between_chars
        else:
            self.display_a_character(current_char)
            self.timer_before_next_char = self.delay_between_chars

    def display_a_character(self, char):
        self.chars_display[self.row][self.column].update(char)
        self.column += 1

    def wait_a_press(self):
        self.pause = True

    def go_next_row(self):
        if self.row < 2:
            self.row += 2
        else:
            self.wait_a_press()
        self.column = 0

    def wait_a_press_for_next_text(self):
        self.go_reset = True
        self.current_string = self.text_list.pop(0)
        self.wait_a_press()

    def scroll_upward(self):
        for y in range(1, self.row_len):
            for x in range(self.column_len):
                above_char = self.chars_display[y-1][x]
                below_char = self.chars_display[y][x]
                above_char.cut(below_char)

    def cut_first_word(self):
        # prélève une partie de la chaîne de caractère
        new_word = ""
        continuing = True
        while continuing:
            if self.current_string:
                new_char = self.current_string[0]
                if new_char in [" ", "\n"]: # si espace ou retour à la ligne
                    continuing = False # arrêt de la boucle
                    if len(new_word) == 0: # si mot en cours vide,
                        new_word += new_char # ajoute du caractère au nouveau mot
                        self.current_string = self.current_string[1:] # et le retire du message

                elif len(new_word) >= self.column_len: # sinon si mot a atteint la taille maximale d'une ligne
                    continuing = False # arrêt de la boucle
                    self.current_string = new_word[-1] + self.current_string # remettre le dernier caractère du mot en cours dans la liste
                    new_word = new_word[:-1] + "-" # et le remplacer par un tiret

                else: # sinon
                    new_word += new_char # ajout du caractère au mot en cours
                    self.current_string = self.current_string[1:] # et le retire du message
            else:
                continuing = False
        return new_word

    def is_there_room_for_current_word_on_the_current_row(self):
        return self.is_there_room_for_this_word_on_the_current_row(self.current_word)

    def is_there_room_for_this_word_on_the_current_row(self, word):
        remaining_space = self.get_remaining_space_on_row()
        if remaining_space >= len(word):
            return True
        return False

    def is_the_current_word_a_compound_word(self):
        if len(self.current_word) < 3:
            return False
        if "-" in self.current_word[1:-1]:
            return True
        return False

    def get_remaining_space_on_row(self):
        return self.column_len - self.column

    def is_there_room_for_first_part_of_current_compound_word(self):
        part_1, part_2 = self.get_current_compound_word_split_in_two_part()
        return self.is_there_room_for_this_word_on_the_current_row(part_1)

    def get_current_compound_word_split_in_two_part(self):
        reduced_word = self.current_word[1:-1]
        parts = reduced_word.split('-', 1)
        return self.current_word[0]+parts[0]+"-", parts[1]+self.current_word[-1]

    def keep_first_half_of_current_compound_word_and_returns_second_part_in_message(self):
        part_1, part_2 = self.get_current_compound_word_split_in_two_part()
        self.current_word = part_1
        self.current_string = part_2 + self.current_string

    def erase_all_lines(self):
        for i in range(len(self.chars_display)):
            self.erase_a_line(i)

    def erase_a_line(self, n):
        for char in self.chars_display[n]:
            char.update(None)

    def reset_display(self):
        self.erase_all_lines()
        self.column = 0
        self.row = 1

    def display(self, surface):
        if self.visible:
            surface.blit(self.sprite, self.rect)
            [[char.display(surface) for char in line] for line in self.chars_display]
            if self.pause:
                current_time = pygame.time.get_ticks()
                if int(current_time / self.blink_interval) % 2 == 0:
                    self.go_on_char.display(surface)
