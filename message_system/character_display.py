class CharDisplay:
    def __init__(self, rect, sprites_dict, char=None):
        self.char = char
        self.rect = rect
        self.sprites_dict = sprites_dict

    def update(self, new_char):
        if new_char:
            if new_char in self.sprites_dict:
                self.char = new_char
            else:
                print(f"error: {new_char} not in sprites_dict")
                self.char = None
        else:
            self.char = None

    def erase(self):
        self.char = None

    def copy(self, other_char_display):
        self.char = other_char_display.get_char()

    def cut(self, other_char_display):
        self.char = other_char_display.get_char()
        other_char_display.erase()

    def get_char(self):
        return self.char

    def display(self, surface):
        if self.char: surface.blit(self.sprites_dict[self.char], self.rect)

