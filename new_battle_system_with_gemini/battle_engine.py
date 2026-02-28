import pygame

# --- Moteur de combat (Brouillon à développer plus tard) ---

class BattleEngine:
    """
    Gère la logique entière du combat, l'affichage et les états.
    Basé sur la structure de 'engine/battle/core.asm'.
    """
    # Palette de couleurs style Game Boy
    COLOR_BG = (224, 248, 208)
    COLOR_LIGHT = (136, 192, 112)
    COLOR_DARK = (52, 104, 86)
    COLOR_BLACK = (8, 24, 32)

    def __init__(self, screen, player_trainer, enemy_pokemon):
        self.screen = screen
        self.player = player_trainer
        self.enemy = enemy_pokemon
        self.active_player_pokemon = self.player.party[0]

        # Police d'écriture (Idéalement on utiliserait une police bitmap Pokémon)
        self.font = pygame.font.SysFont("monospace", 28, bold=True)

        # Machine à états du combat
        # Etats possibles: 'INTRO', 'MAIN_MENU', 'MOVE_MENU', 'DIALOG'
        self.state = "INTRO"

        # Texte actuellement affiché dans la boîte de dialogue
        self.current_dialog = f"Un {self.enemy.name} sauvage apparait!"

        # Gestion des curseurs
        self.main_menu_cursor = 0  # 0: Haut-Gauche, 1: Bas-Gauche, 2: Haut-Droite, 3: Bas-Droite
        self.move_menu_cursor = 0  # 0 à 3 (Colonne verticale)

        # Constantes d'affichage (multipliées par 4 pour le scale)
        self.scale = 4
        self.screen_width = 160 * self.scale
        self.screen_height = 144 * self.scale

    def update(self, events):
        """Met à jour l'état du combat (logique, animations, inputs)."""
        for event in events:
            if event.type == pygame.KEYDOWN:
                # Touches d'action (A)
                if event.key in (pygame.K_SPACE, pygame.K_RETURN):
                    self._handle_action_button()
                # Touches d'annulation (B)
                elif event.key in (pygame.K_BACKSPACE, pygame.K_ESCAPE, pygame.K_x):
                    self._handle_back_button()
                # Touches directionnelles
                elif event.key == pygame.K_UP:
                    self._move_cursor('UP')
                elif event.key == pygame.K_DOWN:
                    self._move_cursor('DOWN')
                elif event.key == pygame.K_LEFT:
                    self._move_cursor('LEFT')
                elif event.key == pygame.K_RIGHT:
                    self._move_cursor('RIGHT')

    def _move_cursor(self, direction):
        """Gère le déplacement du curseur dans les grilles de menus."""
        if self.state == "MAIN_MENU":
            # Grille 2x2
            if direction in ('UP', 'DOWN'):
                self.main_menu_cursor ^= 1  # Alterne entre 0<->1 ou 2<->3
            elif direction in ('LEFT', 'RIGHT'):
                self.main_menu_cursor ^= 2  # Alterne entre 0<->2 ou 1<->3

        elif self.state == "MOVE_MENU":
            # Liste 1x4 (Colonne unique)
            moves_count = len(self.active_player_pokemon.moves)
            if direction == 'UP':
                self.move_menu_cursor = (self.move_menu_cursor - 1) % moves_count
            elif direction == 'DOWN':
                self.move_menu_cursor = (self.move_menu_cursor + 1) % moves_count

    def _handle_back_button(self):
        """Gère la touche de retour (B) pour annuler une action."""
        if self.state == "MOVE_MENU":
            self.state = "MAIN_MENU"

    def _handle_action_button(self):
        """Gère la touche d'action (A) selon l'état actuel."""
        if self.state == "INTRO":
            self.state = "MAIN_MENU"

        elif self.state == "MAIN_MENU":
            if self.main_menu_cursor == 0:  # ATTAQUE
                self.state = "MOVE_MENU"
                self.move_menu_cursor = 0
            elif self.main_menu_cursor == 1:  # OBJET
                self.current_dialog = "Les objets ne sont pas implementes."
                self.state = "DIALOG"
            elif self.main_menu_cursor == 2:  # POKEMON
                self.current_dialog = "Le menu POKeMON n'est pas implemente."
                self.state = "DIALOG"
            elif self.main_menu_cursor == 3:  # FUITE
                self.current_dialog = "Vous prenez la fuite !"
                self.state = "DIALOG"

        elif self.state == "MOVE_MENU":
            selected_move = self.active_player_pokemon.moves[self.move_menu_cursor]
            self.current_dialog = f"{self.active_player_pokemon.name} utilise {selected_move.name}!"
            self.state = "DIALOG"

        elif self.state == "DIALOG":
            # Pour l'instant, on boucle simplement vers le menu principal après un dialogue
            self.state = "MAIN_MENU"

    def display(self):
        """S'occupe de tout l'affichage à l'écran (Draw call)."""
        self.screen.fill(self.COLOR_BG)

        # 1. Dessiner les HUDs (Noms, Niveaux, Barres de PV)
        self._draw_enemy_hud()
        self._draw_player_hud()

        # 2. Dessiner les sprites (temporairement des rectangles)
        self._draw_sprites()

        # 3. Dessiner la boîte de texte / Menu en bas
        self._draw_bottom_box()

    def _draw_enemy_hud(self):
        """Dessine le HUD de l'ennemi en haut à gauche."""
        hud_x = 8 * self.scale
        hud_y = 8 * self.scale

        # Nom
        name_text = self.font.render(self.enemy.name, False, self.COLOR_BLACK)
        self.screen.blit(name_text, (hud_x, hud_y))

        # Niveau (Ex: :L5)
        level_text = self.font.render(f":L{self.enemy.level}", False, self.COLOR_BLACK)
        self.screen.blit(level_text, (hud_x + 48 * self.scale, hud_y + 8 * self.scale))

        # Barre de vie (HP)
        hp_label = self.font.render("HP:", False, self.COLOR_BLACK)
        self.screen.blit(hp_label, (hud_x + 8 * self.scale, hud_y + 18 * self.scale))

        # Calcul de la largeur de la barre (max 48 pixels * scale)
        hp_ratio = self.enemy.current_hp / self.enemy.stats['hp']
        bar_width = int(48 * self.scale * max(0, hp_ratio))

        pygame.draw.rect(self.screen, self.COLOR_BLACK,
                         (hud_x + 32 * self.scale, hud_y + 22 * self.scale, 48 * self.scale, 4 * self.scale), 2)
        pygame.draw.rect(self.screen, self.COLOR_DARK,
                         (hud_x + 32 * self.scale, hud_y + 22 * self.scale, bar_width, 4 * self.scale))

    def _draw_player_hud(self):
        """Dessine le HUD du joueur en bas à droite (au-dessus de la boîte de texte)."""
        hud_x = 72 * self.scale
        hud_y = 72 * self.scale

        # Nom
        name_text = self.font.render(self.active_player_pokemon.name, False, self.COLOR_BLACK)
        self.screen.blit(name_text, (hud_x, hud_y))

        # Niveau
        level_text = self.font.render(f":L{self.active_player_pokemon.level}", False, self.COLOR_BLACK)
        self.screen.blit(level_text, (hud_x + 48 * self.scale, hud_y + 8 * self.scale))

        # Barre de vie
        hp_label = self.font.render("HP:", False, self.COLOR_BLACK)
        self.screen.blit(hp_label, (hud_x + 8 * self.scale, hud_y + 18 * self.scale))

        hp_ratio = self.active_player_pokemon.current_hp / self.active_player_pokemon.stats['hp']
        bar_width = int(48 * self.scale * max(0, hp_ratio))

        pygame.draw.rect(self.screen, self.COLOR_BLACK,
                         (hud_x + 32 * self.scale, hud_y + 22 * self.scale, 48 * self.scale, 4 * self.scale), 2)
        pygame.draw.rect(self.screen, self.COLOR_DARK,
                         (hud_x + 32 * self.scale, hud_y + 22 * self.scale, bar_width, 4 * self.scale))

        # Affichage numérique des PV (spécifique au joueur dans Gen 1)
        hp_num_text = self.font.render(
            f"{self.active_player_pokemon.current_hp: >3}/ {self.active_player_pokemon.stats['hp']: >3}", False,
            self.COLOR_BLACK)
        self.screen.blit(hp_num_text, (hud_x + 24 * self.scale, hud_y + 28 * self.scale))

    def _draw_sprites(self):
        """Dessine les espaces réservés pour les sprites des Pokémon."""
        # Sprite Ennemi (Face) - 56x56 pixels typiquement, placé en haut à droite
        enemy_rect = (96 * self.scale, 8 * self.scale, 56 * self.scale, 56 * self.scale)
        pygame.draw.rect(self.screen, self.COLOR_LIGHT, enemy_rect)
        pygame.draw.rect(self.screen, self.COLOR_BLACK, enemy_rect, 2)

        # Sprite Joueur (Dos) - 56x56 pixels typiquement, placé en bas à gauche
        player_rect = (8 * self.scale, 48 * self.scale, 56 * self.scale, 56 * self.scale)
        pygame.draw.rect(self.screen, self.COLOR_LIGHT, player_rect)
        pygame.draw.rect(self.screen, self.COLOR_BLACK, player_rect, 2)

    def _draw_cursor(self, base_x, base_y):
        """Dessine un triangle (curseur classique Game Boy) aux coordonnées virtuelles."""
        points = [
            (base_x * self.scale, base_y * self.scale),
            ((base_x + 6) * self.scale, (base_y + 4) * self.scale),
            (base_x * self.scale, (base_y + 8) * self.scale)
        ]
        pygame.draw.polygon(self.screen, self.COLOR_BLACK, points)

    def _draw_bottom_box(self):
        """Dessine la zone de dialogue ou le menu en bas de l'écran."""
        box_rect = (0, 96 * self.scale, self.screen_width, 48 * self.scale)
        pygame.draw.rect(self.screen, self.COLOR_BG, box_rect)
        pygame.draw.rect(self.screen, self.COLOR_BLACK, box_rect, 4)

        if self.state in ["INTRO", "DIALOG"]:
            # Affichage du texte
            text_surface = self.font.render(self.current_dialog, False, self.COLOR_BLACK)
            self.screen.blit(text_surface, (8 * self.scale, 104 * self.scale))

        elif self.state == "MAIN_MENU":
            # Le texte du menu par défaut
            dialog_text = self.font.render(f"Que doit faire", False, self.COLOR_BLACK)
            dialog_text2 = self.font.render(f"{self.active_player_pokemon.name} ?", False, self.COLOR_BLACK)
            self.screen.blit(dialog_text, (8 * self.scale, 104 * self.scale))
            self.screen.blit(dialog_text2, (8 * self.scale, 120 * self.scale))

            # Dessin de la petite boîte du menu (ATTAQUE, OBJET, POKEMON, FUITE)
            menu_rect = (72 * self.scale, 96 * self.scale, 88 * self.scale, 48 * self.scale)
            pygame.draw.rect(self.screen, self.COLOR_BG, menu_rect)
            pygame.draw.rect(self.screen, self.COLOR_BLACK, menu_rect, 4)

            # Textes du menu
            atk_text = self.font.render("ATTAQUE", False, self.COLOR_BLACK)
            obj_text = self.font.render("OBJET", False, self.COLOR_BLACK)
            pkmn_text = self.font.render("POKéMON", False, self.COLOR_BLACK)
            run_text = self.font.render("FUITE", False, self.COLOR_BLACK)

            self.screen.blit(atk_text, (88 * self.scale, 104 * self.scale))
            self.screen.blit(obj_text, (88 * self.scale, 120 * self.scale))
            self.screen.blit(pkmn_text, (128 * self.scale, 104 * self.scale))
            self.screen.blit(run_text, (128 * self.scale, 120 * self.scale))

            # Dessin du curseur du Menu Principal
            cursor_positions = [(80, 108), (80, 124), (120, 108), (120, 124)]
            cx, cy = cursor_positions[self.main_menu_cursor]
            self._draw_cursor(cx, cy)

        elif self.state == "MOVE_MENU":
            # Dessin de la boîte d'infos (Type et PP) juste au-dessus à gauche
            info_rect = (0, 48 * self.scale, 88 * self.scale, 48 * self.scale)
            pygame.draw.rect(self.screen, self.COLOR_BG, info_rect)
            pygame.draw.rect(self.screen, self.COLOR_BLACK, info_rect, 4)

            # Affichage des infos de l'attaque sélectionnée
            selected_move = self.active_player_pokemon.moves[self.move_menu_cursor]
            type_label = self.font.render("TYPE/", False, self.COLOR_BLACK)
            type_text = self.font.render(selected_move.move_type, False, self.COLOR_BLACK)
            pp_text = self.font.render(f"PP {selected_move.current_pp: >2}/{selected_move.max_pp: >2}", False,
                                       self.COLOR_BLACK)

            self.screen.blit(type_label, (8 * self.scale, 52 * self.scale))
            self.screen.blit(type_text, (8 * self.scale, 64 * self.scale))
            self.screen.blit(pp_text, (8 * self.scale, 80 * self.scale))

            # Dessin du menu des attaques (1 colonne de 4 max) décalé vers la droite
            for i, move in enumerate(self.active_player_pokemon.moves):
                x_offset = 48
                # Espacement vertical régulier
                y_offset = 100 + (i * 10)
                move_text = self.font.render(move.name.upper(), False, self.COLOR_BLACK)
                self.screen.blit(move_text, (x_offset * self.scale, y_offset * self.scale))

            # Dessin du curseur du Menu des Attaques
            cx = 40
            cy = 104 + (self.move_menu_cursor * 10)
            self._draw_cursor(cx, cy)