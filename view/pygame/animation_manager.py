class AnimationManager:
    def __init__(self):
        """Initializes the manager with an empty list of active animations."""
        self.active_animations = []

    def add_animation(self, animation):
        """Adds a new animation to the active pool."""
        self.active_animations.append(animation)

    def update(self, dt):
        """
        Updates all active animations and removes the ones that are finished.
        Iterating over a copy of the list [:] prevents issues when removing items.
        """
        for anim in self.active_animations[:]:
            anim.update(dt)
            if anim.is_finished:
                self.active_animations.remove(anim)

    def draw(self, surface):
        """Draws all active animations to the screen."""
        for anim in self.active_animations:
            anim.draw(surface)

    def clear_all(self):
        """Instantly stops and removes all playing animations (useful for scene transitions)."""
        self.active_animations.clear()

    def is_playing(self, animation_name=None):
        """
        Checks if any animation (or a specific one) is currently playing.
        Useful to block player input while an attack animation is running.
        """
        if animation_name is None:
            return len(self.active_animations) > 0

        for anim in self.active_animations:
            if anim.name == animation_name:
                return True
        return False