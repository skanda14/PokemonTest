import pygame


class Animation:
    def __init__(self, name, anim_data, sprites_dict, pos):
        """
        :param name: The name of the animation (e.g., "thunderbolt")
        :param anim_data: The dictionary loaded from the exported JSON
        :param sprites_dict: The global dictionary containing Pygame surfaces
        :param pos: Tuple (X, Y) defining the base position of the animation on screen
        """
        self.name = name
        self.anim_data = anim_data
        self.sprites_dict = sprites_dict
        self.base_x = pos[0]
        self.base_y = pos[1]

        # Extract settings directly from the exported data
        self.fps = self.anim_data.get("fps", 12)
        self.is_looping = self.anim_data.get("loop", False)

        # Calculate how long one frame should last in seconds
        self.frame_duration = 1.0 / self.fps if self.fps > 0 else 0.1
        self.frames = self.anim_data.get("frames", [])

        self.current_frame_index = 0
        self.timer = 0.0
        self.is_finished = False

    def update(self, dt):
        """Updates the animation state based on delta time."""
        if self.is_finished or not self.frames:
            return

        self.timer += dt

        if self.timer >= self.frame_duration:
            # Handle potential frame skipping if dt is very large
            frames_to_advance = int(self.timer // self.frame_duration)
            self.timer -= frames_to_advance * self.frame_duration

            self.current_frame_index += frames_to_advance

            if self.current_frame_index >= len(self.frames):
                if self.is_looping:
                    self.current_frame_index %= len(self.frames)
                else:
                    self.is_finished = True
                    self.current_frame_index = len(self.frames) - 1

    def draw(self, surface):
        """Draws all elements of the current frame."""
        if not self.frames:
            return

        # Get the list of sprites to draw for the current frame
        current_frame_data = self.frames[self.current_frame_index]

        # Sort elements by Z-order so background elements are drawn first
        sorted_elements = sorted(current_frame_data, key=lambda item: item.get("z", 0))

        for element in sorted_elements:
            sprite_key = element.get("sprite_key")

            # Verify if the sprite is loaded in the game dictionary
            if sprite_key in self.sprites_dict:
                image = self.sprites_dict[sprite_key]

                # Calculate final position: Base Game Coordinates + Editor Offsets
                final_x = self.base_x + element.get("x", 0)
                final_y = self.base_y + element.get("y", 0)

                surface.blit(image, (final_x, final_y))


# class Animation:
#     def __init__(self, name, frames, pos, frame_duration=0.05):
#         """
#         :param name: Le nom de l'animation (ex: "thunderbolt", "potion_sparkle")
#         :param frames: Une liste de pygame.Surface (les images de l'animation)
#         :param target_x: Position X où l'animation doit être jouée
#         :param target_y: Position Y où l'animation doit être jouée
#         :param frame_duration: Le temps en secondes que dure chaque image
#         """
#         self.name = name
#         self.frames = frames
#         self.x = pos[0]
#         self.y = pos[1]
#         self.frame_duration = frame_duration
#
#         self.current_frame_index = 0
#         self.timer = 0.0
#         self.is_finished = False
#
#     def update(self, dt):
#         """Met à jour l'animation en fonction du temps écoulé."""
#         if self.is_finished:
#             return
#
#         # On ajoute le temps écoulé (dt) au chronomètre interne
#         self.timer += dt
#
#         # Si le temps dépasse la durée d'une frame, on passe à la suivante
#         if self.timer >= self.frame_duration:
#             self.timer = 0.0  # On réinitialise le chrono
#             self.current_frame_index += 1
#
#             # Si on a dépassé la dernière image, l'animation est terminée
#             if self.current_frame_index >= len(self.frames):
#                 self.is_finished = True
#                 self.current_frame_index = len(self.frames) - 1  # Reste sur la dernière frame (optionnel)
#
#     def draw(self, surface):
#         """Dessine l'image actuelle sur la surface principale."""
#         if not self.is_finished and self.frames:
#             current_image = self.frames[self.current_frame_index]
#
#             # Optionnel : Centrer l'image sur les coordonnées x, y
#             rect = current_image.get_rect(center=(self.x, self.y))
#             surface.blit(current_image, rect)
