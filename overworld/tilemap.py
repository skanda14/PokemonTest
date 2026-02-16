import pygame
from utils.file_IO import get_dict_from_json_path
# from game_editor.game_editor_settings import TILE_SIZE
# from .tiles import StaticTile
from .tileset import Tileset



def get_existing_tilemap_table(size, tileset, data_table):
    overlay_tiles_pos_list = tileset.overlay_tiles_pos_list
    w,h = size
    new_table = []
    for y in range(h):
        new_line = []
        for x in range(w):
            tilemap_grid_pos = (x,y)
            tileset_grid_pos = data_table[y][x]
            new_tile = tileset.get_tile_copy(tileset_grid_pos, tilemap_grid_pos)
            if tileset_grid_pos in overlay_tiles_pos_list:
                new_tile.overlay = True
            new_line.append(new_tile)
        new_table.append(new_line)
    return new_table


class Tilemap:
    def __init__(self, file_path, characters=None):
        self.file_path = file_path
        data_dict = get_dict_from_json_path(self.file_path)
        self.name = data_dict['name']
        self.tileset = Tileset(data_dict['tileset_path'])
        self.map_size = data_dict['map_size']
        self.tile_size = data_dict["tile_size"]
        self.rect = pygame.Rect(0,0,self.map_size[0]*self.tile_size[0], self.map_size[1]*self.tile_size[1])
        self.tiles_table = get_existing_tilemap_table(self.map_size, self.tileset, data_dict["tiles_table"])
        self.characters = characters

    def get_effect_at_grid_pos(self, grid_pos):
        tile = self.get_tile(grid_pos)
        if tile:
            return tile.get_effect()
        return None

    def get_tile(self, grid_pos):
        x,y = grid_pos
        if 0 <= x < self.map_size[0] and 0 <= y < self.map_size[1]:
            return self.tiles_table[grid_pos[1]][grid_pos[0]]
        return None

    def is_move_possible_to_direction(self, actor, direction):
        start_grid_pos = actor.get_grid_pos()
        x,y = start_grid_pos
        match direction:
            case "up":
                y -= 1
            case "down":
                y += 1
            case "left":
                x -= 1
            case "right":
                x += 1
        target_grid_pos = x,y
        for char in self.characters:
            if actor != char:
                if char.get_grid_pos() == target_grid_pos:
                    return False
        tile = self.get_tile(target_grid_pos)
        if tile:
            if self.get_tile(target_grid_pos).can_be_accessed_from(start_grid_pos):
                return True
        return False

    def is_move_possible_to_grid_pos_from_move_direction(self, grid_pos, move_direction):
        match move_direction:
            case "up":
                arrival_direction = "down"
            case "down":
                arrival_direction = "up"
            case "left":
                arrival_direction = "right"
            case "right":
                arrival_direction = "left"
        target_grid_pos = grid_pos
        for char in self.characters:
            if char.get_grid_pos() == target_grid_pos:
                return False
        tile = self.get_tile(target_grid_pos)
        if tile:
            if self.get_tile(target_grid_pos).can_be_accessed_from_direction(arrival_direction):
                return True
        return False

    def get_size(self):
        return self.rect.size

    def update(self):
        for line in self.tiles_table:
            for tile in line:
                tile.update()

    def display(self, surface):
        x,y = 0,0
        for line in self.tiles_table:
            for tile in line:
                tile.display(surface, (x,y))

    def display_overlay(self, surface):
        x, y = 0, 0
        for line in self.tiles_table:
            for tile in line:
                if tile.overlay:
                    tile.display_overlay(surface, (x, y))

    # def display_overlay(self, surface, grid_pos):
    #     grid_x, grid_y = grid_pos
    #     x,y = 0,0
    #     self.tiles_table[grid_y][grid_x].display_overlay(surface, (x, y))


