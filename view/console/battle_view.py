import time


class ConsoleBattleView:
    def __init__(self):
        # Pour une vue console, l'affichage est instantané
        self._is_animating = False
        self._waiting_for_input = False

    # -----------------------------------------------------------------
    # Méthodes d'Affichage (Appelées par le Controller)
    # -----------------------------------------------------------------
    def display_text(self, text):
        """Affiche le message dans la console."""
        print(f"\n💬 {text}")

        # On simule un petit délai pour que le texte soit lisible
        # (Sinon la console affiche tout en 1 milliseconde)
        time.sleep(1)

    def display_main_menu(self, cursor_index):
        """Affiche le message dans la console."""
        string_list = [">"+string if i == cursor_index else string for i,string in enumerate(["Fight", "Pkmn", "Item", "Run"])]
        print(f"{string_list[0]} {string_list[1]}")
        print(f"{string_list[2]} {string_list[3]}")
        print("")
        time.sleep(1)


    def animate_hp_bar(self, target, new_hp):
        """Affiche la baisse des HP."""
        print(f"  [➔] {target.upper()}'s HP dropped to {new_hp}!")
        time.sleep(0.5)

    def animate_faint(self, target):
        """Affiche la mise K.O."""
        print(f"  [X] {target.upper()} collapsed!")
        time.sleep(1)

    # -----------------------------------------------------------------
    # Méthodes d'État (Interrogées par le Controller)
    # -----------------------------------------------------------------
    def is_busy(self):
        """
        Indique au Controller si une animation est en cours.
        Ici, comme on utilise time.sleep() pour ralentir, on n'est jamais 'busy'
        au sens de la boucle frame-par-frame.
        """
        return self._is_animating

    def needs_input_to_advance(self):
        """
        Indique si le jeu doit attendre que le joueur appuie sur une touche.
        Pour ce test console, on retourne False pour que le combat se déroule tout seul,
        mais on pourrait utiliser un input() classique ici.
        """
        return self._waiting_for_input

    def clear_message(self):
        """Efface le texte à l'écran (inutile en console, mais requis par le Controller)."""
        pass