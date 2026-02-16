from settings import *
import math


def get_real_pos_from_grid_pos(grid_pos):
    return (grid_pos[0]) * TILE_SIZE[0], (grid_pos[1]) * TILE_SIZE[1]


def calculer_hauteur_saut(frame_actuelle: int, frames_max: int, hauteur_max: int) -> int:
    """
    Calcule la hauteur actuelle d'un saut en fonction de la frame en cours.

    Args:
        frame_actuelle: la frame actuelle (0 = début du saut, frames_max-1 = fin)
        frames_max: le nombre total de frames pour le saut complet (montée + descente)
        hauteur_max: la hauteur maximale du saut

    Returns:
        float: la hauteur actuelle du personnage
    """
    if frames_max <= 1:
        return hauteur_max

    # Normalisation de la frame entre 0 et 1
    t = frame_actuelle / (frames_max - 1)

    # Courbe parabolique (sinusoïdale pour un effet plus doux)
    # On utilise une sinusoïde pour que la montée et la descente soient symétriques et naturelles
    hauteur = int(hauteur_max * math.sin(t * math.pi))

    return hauteur


class Turn:
    def __init__(self, actor, direction, start_pos, end_pos):
        self.name = "turn"
        self.actor = actor
        self.actor.turn(direction)
        self.actor.get_new_animation()
        self.start_pos = start_pos
        self.end_pos = start_pos
        self.current_index = -1
        self.duration = 1

        self.over = False


    def update(self):
        if self.current_index < self.duration-1:
            t = max(0, min(1, (self.current_index+1) / self.duration))  # normaliser entre 0 et 1

            x = self.start_pos[0] + (self.end_pos[0] - self.start_pos[0]) * t
            y = self.start_pos[1] + (self.end_pos[1] - self.start_pos[1]) * t
            self.current_index += 1
            return x,y
        else:
            self.over = True
            return self.end_pos


class TurnUp(Turn):
    def __init__(self, actor):
        start_pos = actor.get_absolute_pos()
        end_pos = start_pos[0], start_pos[1]-TILE_SIZE[1]
        direction = "up"
        super().__init__(actor, direction, start_pos, end_pos)


class TurnDown(Turn):
    def __init__(self, actor):
        start_pos = actor.get_absolute_pos()
        end_pos = start_pos[0], start_pos[1]+TILE_SIZE[1]
        direction = "down"
        super().__init__(actor, direction, start_pos, end_pos)


class TurnLeft(Turn):
    def __init__(self, actor):
        start_pos = actor.get_absolute_pos()
        end_pos = start_pos[0]-TILE_SIZE[0], start_pos[1]
        direction = "left"
        super().__init__(actor, direction, start_pos, end_pos)


class TurnRight(Turn):
    def __init__(self, actor):
        start_pos = actor.get_absolute_pos()
        end_pos = start_pos[0]+TILE_SIZE[0], start_pos[1]
        direction = "right"
        super().__init__(actor, direction, start_pos, end_pos)


########################################################################################################################


class Move:
    def __init__(self, actor, direction, start_grid_pos, end_grid_pos, tile_map):
        self.name = "move"
        self.actor = actor
        self.start_grid_pos = start_grid_pos
        self.end_grid_pos = end_grid_pos
        self.start_pos = get_real_pos_from_grid_pos(self.start_grid_pos)
        self.end_pos = get_real_pos_from_grid_pos(self.end_grid_pos)

        if tile_map.is_move_possible_to_direction(actor, direction):
            self.over = False
            self.doable = True
            self.actor.turn(direction)
            self.actor.modify_state("walk")
            self.actor.get_new_animation()

        else:
            self.over = True
            self.doable = False
        self.current_index = -1
        self.duration = MOVE_DURATION_IN_FRAMES    # in frames

    def print_data(self):
        print(f"Move {self.current_index} ({self.duration}s)")


    def update(self):
        if self.current_index < self.duration-1 and not self.over:
            t = max(0, min(1, (self.current_index+1) / self.duration))  # normaliser entre 0 et 1

            x = self.start_pos[0] + (self.end_pos[0] - self.start_pos[0]) * t
            y = self.start_pos[1] + (self.end_pos[1] - self.start_pos[1]) * t
            self.current_index += 1
            self.actor.rect.topleft = x,y
        else:
            self.over = True
            if self.doable:
                self.actor.grid_pos = self.end_grid_pos

                self.actor.rect.topleft = self.end_pos


class MoveUp(Move):
    def __init__(self, actor, tile_map):
        start_pos = actor.get_grid_pos()
        end_pos = start_pos[0], start_pos[1]-1
        direction = "up"
        super().__init__(actor, direction, start_pos, end_pos, tile_map)


class MoveDown(Move):
    def __init__(self, actor, tile_map):
        start_pos = actor.get_grid_pos()
        end_pos = start_pos[0], start_pos[1]+1
        direction = "down"
        super().__init__(actor, direction, start_pos, end_pos, tile_map)


class MoveLeft(Move):
    def __init__(self, actor, tile_map):
        start_pos = actor.get_grid_pos()
        end_pos = start_pos[0]-1, start_pos[1]
        direction = "left"
        super().__init__(actor, direction, start_pos, end_pos, tile_map)


class MoveRight(Move):
    def __init__(self, actor, tile_map):
        start_pos = actor.get_grid_pos()
        end_pos = start_pos[0]+1, start_pos[1]
        direction = "right"
        super().__init__(actor, direction, start_pos, end_pos, tile_map)


########################################################################################################################


class Jump:
    def __init__(self, actor, direction, start_grid_pos, end_grid_pos, tile_map):
        self.over = False
        match direction:
            case "up":
                arrival_direction = "down"
            case "down":
                arrival_direction = "up"
            case "left":
                arrival_direction = "right"
            case "right":
                arrival_direction = "left"
        if not tile_map.is_move_possible_to_grid_pos_from_move_direction(end_grid_pos, arrival_direction):
            self.over = True
        self.name = "jump"
        self.actor = actor
        self.actor.turn(direction)
        self.actor.modify_state("walk")
        self.actor.get_new_animation()
        self.actor.show_shadow()
        self.actor.grid_pos = end_grid_pos
        self.start_grid_pos = start_grid_pos
        self.end_grid_pos = end_grid_pos
        self.start_pos = get_real_pos_from_grid_pos(self.start_grid_pos)
        self.end_pos = get_real_pos_from_grid_pos(self.end_grid_pos)
        self.current_index = -1
        self.jump_height = 10
        self.duration = MOVE_DURATION_IN_FRAMES*2    # in frames

    def print_data(self):
        print(f"Move {self.current_index} ({self.duration}s)")


    def update(self):
        if self.current_index < self.duration-1 and not self.over:
            t = max(0, min(1, (self.current_index+1) / self.duration))  # normaliser entre 0 et 1
            x = self.start_pos[0] + (self.end_pos[0] - self.start_pos[0]) * t
            y = self.start_pos[1] + (self.end_pos[1] - self.start_pos[1]) * t
            self.current_index += 1
            self.actor.rect.topleft = x,y
            self.actor. z = calculer_hauteur_saut(self.current_index, self.duration, self.jump_height)
        else:
            self.actor.hide_shadow()
            self.over = True
            self.actor.z = 0
            self.actor.rect.topleft = self.end_pos


class JumpUp(Jump):
    def __init__(self, actor, tile_map):
        start_pos = actor.get_grid_pos()
        end_pos = start_pos[0], start_pos[1]-2
        direction = "up"
        super().__init__(actor, direction, start_pos, end_pos, tile_map)


class JumpDown(Jump):
    def __init__(self, actor, tile_map):
        start_pos = actor.get_grid_pos()
        end_pos = start_pos[0], start_pos[1]+2
        direction = "down"
        super().__init__(actor, direction, start_pos, end_pos, tile_map)


class JumpLeft(Jump):
    def __init__(self, actor, tile_map):
        start_pos = actor.get_grid_pos()
        end_pos = start_pos[0]-2, start_pos[1]
        direction = "left"
        super().__init__(actor, direction, start_pos, end_pos, tile_map)


class JumpRight(Jump):
    def __init__(self, actor, tile_map):
        start_pos = actor.get_grid_pos()
        end_pos = start_pos[0]+2, start_pos[1]
        direction = "right"
        super().__init__(actor, direction, start_pos, end_pos, tile_map)
