import pygame
from settings import *
from overworld.tilemap import Tilemap
from overworld.action import MoveUp, MoveDown, MoveLeft, MoveRight, TurnDown


class Overworld:
    def __init__(self, current_tilemap, chars, screen=None):
        self.name = "Test"
        if not screen:
            screen = pygame.display.set_mode(RESOLUTION)
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.fps = FPS
        self.rect = self.screen.get_rect()

        self.characters = chars
        self.tilemap = current_tilemap
        self.events = []

        self.surface = None
        self.zoom = ZOOM
        self.surface_pos = 0,0
        self.map_name = ""
        self.running = False

    def initialization(self):
        self.map_name = self.tilemap.name
        for char in self.characters:
            char.tilemap = self.tilemap

        self.surface = pygame.Surface(self.tilemap.get_size())
        self.surface_pos = self.rect.width/2 - self.surface.get_width()/2*self.zoom, self.rect.height/2 - self.surface.get_height()/2*self.zoom
        self.place_player_at_grid_pos(self.characters[0], (10,0))
        self.place_player_at_grid_pos(self.characters[1], (6,10))

        self.update_surface_pos()

    def place_player_at_grid_pos(self, character, grid_pos):
        character.grid_pos = grid_pos
        real_pos = (grid_pos[0])*TILE_SIZE[0], (grid_pos[1])*TILE_SIZE[1]
        character.rect.topleft = real_pos

    def run(self):
        self.initialization()
        player = self.characters[0]
        self.running = True
        while self.running:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.running = False
                    elif event.key == pygame.K_KP2:
                        character = self.characters[1]
                        character.action_queue.append(MoveDown)
                    elif event.key == pygame.K_KP4:
                        character = self.characters[1]
                        character.action_queue.append(MoveLeft)
                    elif event.key == pygame.K_KP6:
                        character = self.characters[1]
                        character.action_queue.append(MoveRight)
                    elif event.key == pygame.K_KP8:
                        character = self.characters[1]
                        character.action_queue.append(MoveUp)

            mouse_pos = pygame.mouse.get_pos()
            pressed_keys = pygame.key.get_pressed()
            self.update(mouse_pos, pressed_keys, events)
            self.display()
            pygame.display.flip()
            pygame.display.set_caption(f"{self.name} {self.map_name} (fps: {self.clock.get_fps(): .1f})")
            self.clock.tick(self.fps)
            # if player.current_animation:
            #     player.current_animation.print_data()
            # if player.current_move:
            #     player.current_move.print_data()
            #     running = True
            #     while running:
            #         events = pygame.event.get()
            #         for event in events:
            #             if event.type == pygame.KEYDOWN:
            #                 if event.key == pygame.K_SPACE:
            #                     running = False

    # def move_character(self, character, direction):
    #     if character.is_free_to_act():
    #         if self.tilemap.is_move_possible_to_direction(character, direction):
    #             if character.direction == direction:
    #                 x,y = character.get_grid_pos()
    #                 next_grid_pos = None
    #                 move = None
    #                 match direction:
    #                     case "left":
    #                         move = MoveLeft
    #                         next_grid_pos = x-1,y
    #                     case "right":
    #                         move = MoveRight
    #                         next_grid_pos = x+1,y
    #                     case "up":
    #                         move = MoveUp
    #                         next_grid_pos = x,y-1
    #                     case "down":
    #                         move = MoveDown
    #                         next_grid_pos = x, y+1
    #                 next_effect = self.tilemap.get_effect_at_grid_pos(next_grid_pos)
    #                 if next_effect:
    #                     character.action_queue.append(next_effect)
    #                 else:
    #                     character.get_new_move(move)
    #             else:
    #                 character.direction = direction
    #         else:
    #             character.direction = direction

    def move_character(self, character, direction):
        if character.is_free_to_act():

            if character.direction == direction:
                x,y = character.get_grid_pos()
                next_grid_pos = None
                move = None
                match direction:
                    case "left":
                        move = MoveLeft
                        next_grid_pos = x-1,y
                        grid_pos_to_jump = x-2, y
                    case "right":
                        move = MoveRight
                        next_grid_pos = x+1,y
                        grid_pos_to_jump = x + 2, y
                    case "up":
                        move = MoveUp
                        next_grid_pos = x,y-1
                        grid_pos_to_jump = x, y-2
                    case "down":
                        move = MoveDown
                        next_grid_pos = x, y+1
                        grid_pos_to_jump = x, y+2
                if self.tilemap.is_move_possible_to_grid_pos_from_move_direction(next_grid_pos, direction):
                    next_effect = self.tilemap.get_effect_at_grid_pos(next_grid_pos)
                    if next_effect:
                        if self.tilemap.is_move_possible_to_grid_pos_from_move_direction(grid_pos_to_jump, direction):
                            character.action_queue.append(next_effect)
                    else:
                        character.get_new_move(move)
            else:
                character.direction = direction


    def move_character_up(self, character):
        character.get_new_move(MoveUp)

    def move_character_down(self, character):
        character.get_new_move(MoveDown)

    def move_character_left(self, character):
        character.get_new_move(MoveLeft)

    def move_character_right(self, character):
        character.get_new_move(MoveRight)

    def update(self, mouse_pos, pressed_keys, events):
        self.interactions(mouse_pos, pressed_keys, events)
        if self.tilemap:
            self.tilemap.update()
        for event in self.events:
            event.update(0)
        for character in self.characters:
            character.update()

    def interactions(self, mouse_pos, pressed_keys, events):
        if pressed_keys[pygame.K_UP]:
            self.move_character(self.characters[0], "up")
        elif pressed_keys[pygame.K_DOWN]:
            self.move_character(self.characters[0], "down")
        elif pressed_keys[pygame.K_LEFT]:
            self.move_character(self.characters[0], "left")
        elif pressed_keys[pygame.K_RIGHT]:
            self.move_character(self.characters[0], "right")

        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    print("go")
                    self.characters[0].action_queue.append(MoveDown)
                    self.characters[0].action_queue.append(MoveDown)
                    self.characters[0].action_queue.append(MoveLeft)
                    self.characters[0].action_queue.append(MoveLeft)
                    self.characters[0].action_queue.append(MoveUp)
                    self.characters[0].action_queue.append(MoveUp)
                    self.characters[0].action_queue.append(MoveRight)
                    self.characters[0].action_queue.append(MoveRight)
                    self.characters[0].action_queue.append(TurnDown)

    def update_surface_pos(self):
        px,py = self.characters[0].rect.topleft
        pw,ph = self.characters[0].rect.size
        sx,sy = self.rect.center
        x = sx - pw*self.zoom - px*self.zoom  # sx - pw/2*self.zoom - px*self.zoom
        y = sy - ph/2*self.zoom - py*self.zoom
        self.surface_pos = x,y

    def display(self):
        self.screen.fill((0,0,0))
        self.draw_surface()
        zoomed_surf = pygame.transform.scale_by(self.surface, self.zoom)
        self.update_surface_pos()

        self.screen.blit(zoomed_surf, self.surface_pos)
        # if self.debug:
        #     if self.debug.is_visible():
        #         self.debug.display(self.screen)

    def draw_surface(self):
        self.surface.fill(BACKGROUND_COLOR)
        self.draw_parts(self.surface)
        # self.draw_grid(self.surface)

    def draw_parts(self, surf):
        if self.tilemap:
            self.tilemap.display(surf)
        for character in self.characters:
            character.display(surf)
        if self.tilemap:
            self.tilemap.display_overlay(surf)
        for character in self.characters:
            character.overlay_display(surf)

    def draw_grid(self, surf):
        for y in range(0, surf.get_height(), TILE_SIZE[1]):
            for x in range(0, surf.get_width(), TILE_SIZE[0]):
                pygame.draw.rect(surf, (255,255,255), (x, y, TILE_SIZE[0], TILE_SIZE[1]), 1)
