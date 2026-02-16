import pygame
from utils.file_IO import get_dict_from_json_path
from settings import TILE_SIZE
from .animation import Animation
# from .move import Move
from collections import deque


def get_image(path):
    if path:
        return pygame.image.load(path)
    else:
        return None


def load_player_sprites(image_path, color_key):
    image = get_image(image_path)
    w,h = TILE_SIZE
    gap = 1
    sprites = []
    if image:
        for y in range(0, image.get_height() - 1, h+gap):
            for x in range(0, image.get_width()-1, w+gap):
                new_sprite = image.subsurface((x+gap,y+gap, w, h))
                new_sprite.set_colorkey(color_key)
                sprites.append(new_sprite)
    return sprites


def get_animation_dict(sprites):
    new_dict = {
        "idle": {
            "down": Animation("idle down", [sprites[1]], loop=True),
            "up": Animation("idle up", [sprites[4]], loop=True),
            "left": Animation("idle left", [sprites[6]], loop=True),
            "right": Animation("idle right", [sprites[8]], loop=True),
        },
        "walk": {
            "down": Animation("walk down", [ sprites[1], sprites[0], sprites[1], sprites[2]], loop=True),
            "up": Animation("walk up", [sprites[4], sprites[3], sprites[4], sprites[5]], loop=True),
            "left": Animation("walk left", [sprites[6], sprites[7], sprites[6], sprites[7]], loop=True),
            "right": Animation("walk right", [sprites[8], sprites[9], sprites[8], sprites[9]], loop=True),
        },
    }
    return new_dict


def get_shadow_sprite():
    new_image = pygame.image.load("assets/sprites/character_shadow.png").convert_alpha()
    new_image.set_colorkey(new_image.get_at((0,0)))
    return new_image


class Character:
    def __init__(self, file_path):
        data_dict = get_dict_from_json_path(file_path)
        self.grid_pos = (0,0)
        self.name = data_dict["name"]
        self.rect = pygame.Rect((0, 0), TILE_SIZE)
        self.z = 0
        self.direction = "down"
        self.state_name = "idle"
        self.sprites = load_player_sprites(data_dict["image_path"], data_dict["color_key"])
        self.shadow_sprite = get_shadow_sprite()
        self.animations_dict = get_animation_dict(self.sprites)
        self.current_action = None
        self.current_animation = None
        self.shadow_visibility = False
        self.shadow_y_shift = 2
        self.tilemap = None
        self.action_queue = deque()
        # self.current_animation = self.animations_dict["walk"][self.orientation]

    def show_shadow(self):
        self.shadow_visibility = True

    def hide_shadow(self):
        self.shadow_visibility = False

    def get_grid_pos(self):
        # real_x, real_y = self.rect.topleft
        # grid_pos = (real_x//TILE_SIZE[0], real_y//TILE_SIZE[1])
        return self.grid_pos

    def get_targeted_grid_pos(self):
        x,y = self.grid_pos
        if self.state_name == "walk":
            match self.direction:
                case "down":
                    y += 1
                case "up":
                    y -= 1
                case "left":
                    x -= 1
                case "right":
                    x += 1
            return x,y
        else:
            return None

    def reset_animation(self):
        self.modify_state("idle")
        # self.current_animation = None
        self.get_new_animation()

    def get_absolute_pos(self):
        return self.rect.topleft

    def modify_state(self, new_state):
        if self.state_name != new_state:
            self.state_name = new_state

    def turn(self, direction):
        if self.direction != direction:
            self.direction = direction

    def get_new_move(self, new_move_class):
        if not self.current_action:
            self.current_action = new_move_class(self, self.tilemap)

    # def get_new_move(self, move_dir):
    #     if not self.current_move:
    #         if move_dir[0] > 0:
    #             self.direction = "right"
    #         elif move_dir[0] < 0:
    #             self.direction = "left"
    #         elif move_dir[1] > 0:
    #             self.direction = "down"
    #         elif move_dir[1] < 0:
    #             self.direction = "up"
    #         tile_w,tile_h = TILE_SIZE
    #         start_pos = self.rect.topleft
    #         end_pos = start_pos[0] + move_dir[0]*tile_w, start_pos[1] + move_dir[1]*tile_h
    #         new_move = Move(self, start_pos, end_pos)
    #         self.current_move = new_move
    #         # self.state_name = "walk"
    #         # self.get_new_animation()

    def is_free_to_act(self):
        if not self.current_action and not self.action_queue:
            return True
        return False

    def load_animation(self, new_animation):
        # print("Loading animation " + new_animation.name)
        self.current_animation = new_animation

    def get_new_animation(self):
        new_animation = self.animations_dict[self.state_name][self.direction].copy()
        if not self.current_animation:
            self.load_animation(new_animation)
        elif self.current_animation.name != new_animation.name:
            self.load_animation(new_animation)

    def update(self):
        if self.current_action:
            # print(f"{self.current_move}: {self.current_move.current_index}/{self.current_move.duration}")
            self.current_action.update()
            if self.current_action.over:
                self.current_action = None

        else:
            if self.action_queue:
                self.get_new_move(self.action_queue.popleft())
                # self.current_action = self.action_queue.popleft()
            else:
                # print("")
                # self.modify_state("idle")
                self.reset_animation()

        if self.current_animation:
            if not self.current_animation.update():
                pass
                # self.reset_animation()
        else:
            pass
            # self.current_animation = self.animations_dict[self.state_name][self.direction]

    def display(self, screen):
        if self.shadow_visibility:
            screen.blit(self.shadow_sprite, (self.rect.left, self.rect.top+self.shadow_y_shift-4))
        if self.current_animation:
            image = self.current_animation.img()
            screen.blit(image, (self.rect.left, self.rect.top-self.z-4))
        # pygame.draw.rect(screen, (255,255,255), self.rect)

    def overlay_display(self, screen):
        if self.current_animation:
            image = self.current_animation.img()
            cropped_image = image.subsurface((0,0, 16, 8)).convert_alpha()
            # cropped_image.set_colorkey(image.colorkey)
            screen.blit(cropped_image, (self.rect.left, self.rect.top-self.z-4))