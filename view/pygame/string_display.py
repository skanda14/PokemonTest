from view.pygame.battle_display_fun import get_convert_rect_from_grid_rect, get_rect, get_relative_pos_from_rect
from view.pygame.character_display import CharDisplay


class StringDisplay:
    def __init__(self, grid_pos, grid_size, sprites_dict, data=None):
        self.grid_rect = get_rect(grid_pos, grid_size)
        self.rect = get_convert_rect_from_grid_rect(grid_pos, grid_size)
        self.sprite_dict = sprites_dict
        self.chars_display = [CharDisplay(get_relative_pos_from_rect((i,0), self.grid_rect), sprites_dict) for i in range(grid_size[0])]
        self.modify(data)
        self.visible = True

    def show(self):
        self.visible = True

    def hide(self):
        self.visible = False

    def modify(self, data):
        if data is not None:
            string = str(data)
            max_chars = int(len(self.chars_display))
            formatted_string = f"{string[:max_chars]:<{max_chars}}"
            for char, char_display in zip(formatted_string, self.chars_display):
                char_display.update(char)

    def display(self, surface):
        if self.visible:
            for char in self.chars_display:
                char.display(surface)
