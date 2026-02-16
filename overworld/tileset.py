import pygame
from .tiles import StaticTile, AnimatedTile
from utils.file_IO import get_dict_from_json_path


def split_image_into_tile_table(image, tile_size, tile_class, color_key, access_table):
    grid_y,grid_x = 0,0
    new_table = []
    if image:
        for y in range(0, image.get_height(), tile_size[1]):
            new_line = []
            for x in range(0, image.get_width(), tile_size[0]):
                new_sprite = image.subsurface(((x,y), tile_size)).convert_alpha()
                new_sprite.set_colorkey(color_key)
                access_data = access_table[grid_y][grid_x]
                new_tile = tile_class((grid_x,grid_y), tile_size, [new_sprite], access_data, color_key)
                new_line.append(new_tile)
                grid_x += 1
            new_table.append(new_line)
            grid_y += 1
            grid_x = 0
    return new_table


def split_image_into_animated_tile_list(image, tile_size, tile_class, color_key, animated_tiles_pos_table, access_table, tiles_table):
    grid_y,grid_x = len(tiles_table),0
    new_table = []

    for line in animated_tiles_pos_table:
        new_line = []
        for animated_pos_list in line:
            new_sprites = [image.subsurface(((image_pos[0]*tile_size[0], image_pos[1]*tile_size[1]), tile_size)).convert_alpha() for image_pos in animated_pos_list]
            access_data = access_table[grid_y][grid_x]
            new_tile = tile_class((grid_x, grid_y), tile_size, new_sprites, access_data, color_key)
            new_line.append(new_tile)
            grid_x += 1
        new_table.append(new_line)
        grid_y += 1
        grid_x = 0
    return new_table


def fuse_two_tables(table1, table2):
    new_table = []
    for line in table1:
        new_table.append(line)
    for line in table2:
        new_table.append(line)
    return new_table


class Tileset:
    def __init__(self, file_path):
        data_dict = get_dict_from_json_path(file_path)
        self.json_path = data_dict["file_path"]
        self.image_path = data_dict['image_path']
        self.image = pygame.image.load(self.image_path)
        self.name = data_dict['name']
        self.color_key = data_dict['color_key']
        self.tile_size = data_dict['tile_size']
        self.overlay_tiles_pos_list = data_dict['overlay_tiles_pos_list']
        self.animated_tiles_pos_table = data_dict['animated_tiles_pos_table']
        self.rect = pygame.Rect((0,0), self.image.get_size())
        # self.tiles_table = split_image_into_tile_table(self.image, self.tile_size, StaticTile, self.color_key, data_dict['access_table'])

        static_tiles_table = split_image_into_tile_table(self.image, self.tile_size, StaticTile, self.color_key, data_dict['access_table'])

        animated_tiles_table = split_image_into_animated_tile_list(self.image, self.tile_size, AnimatedTile, self.color_key,
                                                                   self.animated_tiles_pos_table, data_dict['access_table'], static_tiles_table)
        self.tiles_table = fuse_two_tables(static_tiles_table, animated_tiles_table)


    def coordinates_exist(self, coordinates):
        x, y = coordinates
        if 0 <= y < len(self.tiles_table) and 0 <= x < len(self.tiles_table[0]):
            return True
        return False

    def get_tile_copy(self, tileset_grid_pos, tilemap_grid_pos):
        x, y = tileset_grid_pos
        return self.tiles_table[y][x].copy(tilemap_grid_pos)

        # if self.coordinates_exist(tileset_grid_pos):
        #     x, y = tileset_grid_pos
        #     return self.tiles_table[y][x].copy(tilemap_grid_pos)
        # return self.tiles_table[0][0].copy(tilemap_grid_pos)
