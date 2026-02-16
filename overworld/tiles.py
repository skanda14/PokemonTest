import pygame
from overworld.action import JumpDown


def split_image_into_list(image, tile_size):
    new_line = []
    for y in range(0, image.get_height(), tile_size[1]):
        for x in range(0, image.get_width(), tile_size[0]):
            new_sprite = image.subsurface(((x, y), tile_size))
            new_line.append(new_sprite)
    return new_line


def get_overlaying_sprites(images):
    color_key = (255,255,255)
    new_sprites = []
    for image in images:
        new_image = image.copy()
        for y in range(4):
            for x in range(image.get_width()):
                new_image.set_at((x, y), color_key)
        new_image.set_colorkey(color_key)
        new_sprites.append(new_image)
    return new_sprites


class Tile:
    def __init__(self, grid_pos, size, image_list, access_tuple, color_key):
        self.grid_pos = grid_pos
        self.size = size
        self.rect = pygame.Rect((grid_pos[0]*size[0], grid_pos[1]*size[1]), size)
        self.color_key = color_key
        self.sprite = image_list
        self.sprites =  self.sprite.copy() # split_image_into_list(self.sprite, self.size)
        self.overlay_sprites = get_overlaying_sprites(self.sprites)
        self.access = access_tuple[0]
        self.four_dir_access_dict = access_tuple[1]
        self.overlay = False

    def get_effect(self):
        if self.access == 2:
            return JumpDown
        else:
            return None

    def can_be_accessed(self):
        if self.access == 1:
            return True
        return False

    def can_be_accessed_from(self, start_grid_pos):
        if self.access == 0:
            return False
        elif self.access == 1:
            return True
        else:
            tx,ty = self.grid_pos
            x,y = start_grid_pos
            if x < tx and self.four_dir_access_dict["left"] != 0:
                return True
            elif x > tx and self.four_dir_access_dict["right"] != 0:
                return True
            elif y < ty and self.four_dir_access_dict["up"] != 0:
                return True
            elif y > ty and self.four_dir_access_dict["down"] != 0:
                return True
            return False

    def can_be_accessed_from_direction(self, direction):
        if self.access == 0:
            return False
        elif self.access == 1:
            return True
        else:
            if direction == "left" and self.four_dir_access_dict["left"] != 0:
                return True
            elif direction == "right" and self.four_dir_access_dict["right"] != 0:
                return True
            elif direction == "up" and self.four_dir_access_dict["up"] != 0:
                return True
            elif direction == "down" and self.four_dir_access_dict["down"] != 0:
                return True
            return False

    def copy(self, tilemap_grid_pos):
        new_tile = Tile(tilemap_grid_pos, self.size, self.sprite, (self.access, self.four_dir_access_dict), self.color_key)
        return new_tile

    def update(self, game_speed=1):
        pass

    def get_tuple_access(self):
        return self.access, self.four_dir_access_dict

    def collide(self, pos):
        if self.rect.collidepoint(pos):
            return True
        return False

    def get_img(self):
        return self.sprites[0]

    def get_overlaying_sprite(self):
        return self.overlay_sprites[0]

    def display(self, surf, base_pos):
        pos = base_pos[0]+self.rect.left, base_pos[1]+self.rect.top
        surf.blit(self.get_img(), pos)

    def display_overlay(self, surf, base_pos):
        pos = base_pos[0]+self.rect.left, base_pos[1]+self.rect.top
        surf.blit(self.get_overlaying_sprite(), pos)


class StaticTile(Tile):
    def __init__(self, grid_pos, size, image, access_tuple, color_key):
        super().__init__(grid_pos, size, image, access_tuple, color_key)

    def copy(self, new_tilemap_grid_pos):
        new_tile = StaticTile(new_tilemap_grid_pos, self.size, self.sprite, (self.access, self.four_dir_access_dict), self.color_key)

        # new_tile = StaticTile(self.grid_pos, self.size, self.sprites, self.color_key, new_tilemap_grid_pos)
        return new_tile

    def update(self, game_speed=1):
        pass

    def get_img(self):
        return self.sprites[0]




class AnimatedTile(Tile):
    def __init__(self, grid_pos, size, image, access_tuple, color_key):
        super().__init__(grid_pos, size, image, access_tuple, color_key)
        self.speed = 1
        self.mode = "ping-pong"  # ping-pong / loop
        self.direction = 1
        self.img_duration = 30
        self.frame = -1
        self.max_frame = self.img_duration * len(self.sprites) - 1

    def copy(self, new_tilemap_grid_pos):
        new_tile = AnimatedTile(new_tilemap_grid_pos, self.size, self.sprite, (self.access, self.four_dir_access_dict), self.color_key)

        # new_tile = AnimatedTile(self.grid_pos, self.size, self.sprites, self.color_key, new_tilemap_grid_pos)
        return new_tile

    def update(self, game_speed=1):
        if self.frame == -1:
            self.frame = 0
        else:
            if self.mode == "loop":
                self.frame = (self.frame + game_speed) % (self.img_duration * len(self.sprites))
            elif self.mode == "ping-pong":
                self.frame += game_speed * self.direction
                if self.frame > self.max_frame:
                    gap = self.max_frame - self.frame
                    self.frame = self.max_frame - gap - self.img_duration
                    self.direction = -1
                elif self.frame < 0:
                    gap = -self.frame
                    self.frame = gap + self.img_duration
                    self.direction = 1
            else:
                self.frame = 0

    def get_img(self):
        return self.sprites[int(self.frame / self.img_duration)]

