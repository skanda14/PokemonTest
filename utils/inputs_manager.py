class InputsManager:
    def __init__(self):
        # État des touches à la frame actuelle
        self.current_keys = None
        # État des touches à la frame précédente
        self.previous_keys = None

    def update(self, key_state):
        """
        Met à jour l'état des touches. 
        À appeler à chaque frame en lui passant pygame.key.get_pressed().
        """
        # L'état actuel devient l'état précédent pour la prochaine vérification
        self.previous_keys = self.current_keys
        # On enregistre le nouvel état actuel
        self.current_keys = key_state

    def is_key_pressed(self, key_code):
        """
        Retourne True si la touche est maintenue enfoncée.
        """
        if self.current_keys is None:
            return False
        return self.current_keys[key_code]

    def is_key_just_pressed(self, key_code):
        """
        Retourne True UNIQUEMENT à la frame où la touche vient d'être pressée.
        (Elle est pressée maintenant, mais ne l'était pas à la frame précédente).
        """
        if self.current_keys is None or self.previous_keys is None:
            return False

        return self.current_keys[key_code] and not self.previous_keys[key_code]

    def is_key_just_released(self, key_code):
        """
        Retourne True UNIQUEMENT à la frame où la touche vient d'être relâchée.
        """
        if self.current_keys is None or self.previous_keys is None:
            return False

        return not self.current_keys[key_code] and self.previous_keys[key_code]
