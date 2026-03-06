import pygame


class Animation:
    def __init__(self, name, frames, pos, frame_duration=0.05):
        """
        :param name: Le nom de l'animation (ex: "thunderbolt", "potion_sparkle")
        :param frames: Une liste de pygame.Surface (les images de l'animation)
        :param target_x: Position X où l'animation doit être jouée
        :param target_y: Position Y où l'animation doit être jouée
        :param frame_duration: Le temps en secondes que dure chaque image
        """
        self.name = name
        self.frames = frames
        self.x = pos[0]
        self.y = pos[1]
        self.frame_duration = frame_duration

        self.current_frame_index = 0
        self.timer = 0.0
        self.is_finished = False

    def update(self, dt):
        """Met à jour l'animation en fonction du temps écoulé."""
        if self.is_finished:
            return

        # On ajoute le temps écoulé (dt) au chronomètre interne
        self.timer += dt

        # Si le temps dépasse la durée d'une frame, on passe à la suivante
        if self.timer >= self.frame_duration:
            self.timer = 0.0  # On réinitialise le chrono
            self.current_frame_index += 1

            # Si on a dépassé la dernière image, l'animation est terminée
            if self.current_frame_index >= len(self.frames):
                self.is_finished = True
                self.current_frame_index = len(self.frames) - 1  # Reste sur la dernière frame (optionnel)

    def draw(self, surface):
        """Dessine l'image actuelle sur la surface principale."""
        if not self.is_finished and self.frames:
            current_image = self.frames[self.current_frame_index]

            # Optionnel : Centrer l'image sur les coordonnées x, y
            rect = current_image.get_rect(center=(self.x, self.y))
            surface.blit(current_image, rect)
