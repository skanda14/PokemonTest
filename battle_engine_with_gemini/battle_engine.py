import pygame
import random
from battle_engine.battle_fun import check_accuracy, calculate_damage
from battle_engine.types import PHYSICAL_TYPES
from battle_engine.type_chart import TYPE_CHART
from debug import Debug


# Initialisation de Pygame
pygame.init()

# Constantes d'affichage
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 400
FPS = 30

# Couleurs
COLOR_WHITE = (255, 255, 255)
COLOR_BLACK = (0, 0, 0)
COLOR_GREEN = (100, 200, 100)
COLOR_RED = (200, 100, 100)
COLOR_GRAY = (200, 200, 200)

# Polices
font = pygame.font.SysFont("Arial", 20, bold=True)
font_small = pygame.font.SysFont("Arial", 16)


class BattleEngine:
    def __init__(self, screen, player_pkmn, enemy_pkmn):
        # self.screen = screen
        self.player = player_pkmn
        self.enemy = enemy_pkmn

        # États du jeu: "MAIN_MENU", "MOVE_MENU", "RESOLVING", "END"
        self.state = "MAIN_MENU"
        self.message_queue = ["Un combat Pokémon commence !", f"Un {self.enemy.name} sauvage apparaît !"]
        self.current_message = ""
        self.action_queue = []  # Stocke les actions à résoudre pendant le tour

        self.main_options = ["FIGHT", "PKMN", "ITEM", "RUN"]
        self.selected_main_index = 0
        self.selected_move_index = 0

    def update(self):
        pass

    def handle_event(self, event):
        if self.message_queue and not self.current_message:
            self.current_message = self.message_queue.pop(0)

        # elif self.message_queue or self.current_message:
        #     if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
        #         print("space")
        #         self.advance_message()

        elif self.action_queue:
            self.execute_move(self.action_queue.pop(0))

        elif self.state == "MAIN_MENU":
            if event.type == pygame.KEYDOWN:
                # Navigation stricte en grille 2x2
                if event.key == pygame.K_RIGHT:
                    if self.selected_main_index % 2 == 0: self.selected_main_index += 1
                elif event.key == pygame.K_LEFT:
                    if self.selected_main_index % 2 != 0: self.selected_main_index -= 1
                elif event.key == pygame.K_DOWN:
                    if self.selected_main_index < 2: self.selected_main_index += 2
                elif event.key == pygame.K_UP:
                    if self.selected_main_index >= 2: self.selected_main_index -= 2
                elif event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                    selected_option = self.main_options[self.selected_main_index]

                    if selected_option == "FIGHT":
                        self.state = "MOVE_MENU"
                        self.selected_move_index = 0
                    elif selected_option == "RUN":
                        self.message_queue.append("Vous prenez la fuite !")
                        self.enemy.hp = 0  # Astuce pour finir le combat proprement
                        # self.advance_message()
                    else:
                        # PKMN et ITEM ne sont pas encore programmés
                        self.message_queue.append(f"{selected_option} n'est pas encore implémenté !")
                        # self.advance_message()

        elif self.state == "MOVE_MENU":
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE or event.key == pygame.K_BACKSPACE:
                    self.state = "MAIN_MENU"  # Retour en arrière
                elif event.key == pygame.K_RIGHT:
                    if self.selected_move_index % 2 == 0 and self.selected_move_index + 1 < len(self.player.moves):
                        self.selected_move_index += 1
                elif event.key == pygame.K_LEFT:
                    if self.selected_move_index % 2 != 0:
                        self.selected_move_index -= 1
                elif event.key == pygame.K_DOWN:
                    if self.selected_move_index + 2 < len(self.player.moves):
                        self.selected_move_index += 2
                elif event.key == pygame.K_UP:
                    if self.selected_move_index >= 2:
                        self.selected_move_index -= 2
                elif event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                    selected_move = self.player.moves[self.selected_move_index]
                    self.resolve_turn(selected_move)
                    self.state = "MAIN MENU"


    def resolve_turn(self, player_move):
        """Organise l'ordre d'attaque basé sur la vitesse."""
        # Sélection aléatoire pour l'ennemi (IA très basique)
        enemy_move = random.choice(self.enemy.moves)

        # Déterminer l'ordre avec la Vitesse
        if self.player.speed >= self.enemy.speed:
            first, second = self.player, self.enemy
            move_first, move_second = player_move, enemy_move
        else:
            first, second = self.enemy, self.player
            move_first, move_second = enemy_move, player_move

        # On simule les actions
        self.action_queue.append((first, second, move_first))
        self.action_queue.append((second, first, move_second))

        # self.advance_message()

    def execute_move(self, action):
        attacker, defender, move = action
        if attacker.hp < 0 or defender.hp < 0:
            return

        """Logique de résolution d'une attaque."""
        self.message_queue.append(f"{attacker.name} utilise {move.name} !")

        if not check_accuracy(move):
            self.message_queue.append("Mais l'attaque échoue ! (Bug 1/256 ou esquive)")
            return

        damage, is_crit, type_mod = calculate_damage(attacker, defender, move, PHYSICAL_TYPES, TYPE_CHART)
        defender.hp -= damage

        if is_crit:
            self.message_queue.append("Coup Critique !")

        if type_mod == 0.0:
            self.message_queue.append(f"Cela n'affecte pas {defender.name}...")
        elif type_mod > 1.0:
            self.message_queue.append("C'est super efficace !")
        elif type_mod < 1.0:
            self.message_queue.append("Ce n'est pas très efficace...")

        if defender.hp <= 0:
            defender.hp = 0
            self.message_queue.append(f"{defender.name} est K.O. !")
        # self.advance_message()


    def advance_message(self):
        print("advance message")
        """Passe au message suivant dans la file d'attente."""
        if self.message_queue:
            self.current_message = self.message_queue.pop(0)
        else:
            self.current_message = ""
            if self.player.hp <= 0 or self.enemy.hp <= 0:
                self.state = "END"
                self.current_message = "Le combat est terminé."
            elif self.action_queue:
                self.state = "EXECUTION"
            else:
                self.state = "MAIN_MENU"


    # =====================================================================
    # DRAWING METHODS
    # =====================================================================

    def draw(self, screen):
        screen.fill(COLOR_WHITE)

        # Affichage des barres de vie
        self.draw_health_bar(screen, 50, 50, self.enemy.hp, self.enemy.max_hp, self.enemy.name, self.enemy.level)
        self.draw_health_bar(screen, 350, 200, self.player.hp, self.player.max_hp, self.player.name, self.player.level)

        # Sprites factices (Rectangles)
        pygame.draw.rect(screen, COLOR_RED, (380, 50, 100, 100))  # Sprite Ennemi
        pygame.draw.rect(screen, COLOR_GREEN, (100, 200, 100, 100))  # Sprite Joueur

        if self.state == "MAIN_MENU":
            if not self.message_queue:
                self.draw_main_menu(screen)
            else:
                self.draw_message_box(screen)
        elif self.state == "MOVE_MENU":
            self.draw_move_menu(screen)
        elif self.state == "RESOLVING" or self.state == "END":
            self.draw_message_box(screen)


    def draw_health_bar(self,screen,  x, y, hp, max_hp, name, level):
        """Dessine une barre de vie style Gen 1 simplifiée."""
        pygame.draw.rect(screen, COLOR_BLACK, (x, y, 200, 50), 2)
        pygame.draw.rect(screen, COLOR_WHITE, (x + 2, y + 2, 196, 46))

        # Texte
        name_text = font.render(name, True, COLOR_BLACK)
        level_text = font_small.render(f"Nv{level}", True, COLOR_BLACK)
        screen.blit(name_text, (x + 5, y + 5))
        screen.blit(level_text, (x + 150, y + 8))

        # Barre
        bar_width = 150
        hp_ratio = max(0.0, hp / max_hp)
        current_bar_width = int(bar_width * hp_ratio)

        pygame.draw.rect(screen, COLOR_BLACK, (x + 20, y + 30, bar_width + 4, 14))
        pygame.draw.rect(screen, COLOR_WHITE, (x + 22, y + 32, bar_width, 10))

        # Couleur de la barre de vie
        hp_color = COLOR_GREEN
        if hp_ratio < 0.2:
            hp_color = COLOR_RED
        elif hp_ratio < 0.5:
            hp_color = (200, 200, 50)  # Jaune

        if current_bar_width > 0:
            pygame.draw.rect(screen, hp_color, (x + 22, y + 32, current_bar_width, 10))

    def draw_main_menu(self, screen, ):
        """Dessine le menu principal (FIGHT, PKMN, ITEM, RUN)."""
        # Boîte de dialogue de gauche (Que va faire X ?)
        prompt_rect = pygame.Rect(0, SCREEN_HEIGHT - 100, SCREEN_WIDTH - 250, 100)
        pygame.draw.rect(screen, COLOR_WHITE, prompt_rect)
        pygame.draw.rect(screen, COLOR_BLACK, prompt_rect, 3)

        prompt_text1 = font.render("Que doit faire", True, COLOR_BLACK)
        prompt_text2 = font.render(f"{self.player.name} ?", True, COLOR_BLACK)
        screen.blit(prompt_text1, (20, SCREEN_HEIGHT - 80))
        screen.blit(prompt_text2, (20, SCREEN_HEIGHT - 50))

        # Boîte de menu de droite
        menu_rect = pygame.Rect(SCREEN_WIDTH - 250, SCREEN_HEIGHT - 100, 250, 100)
        pygame.draw.rect(screen, COLOR_WHITE, menu_rect)
        pygame.draw.rect(screen, COLOR_BLACK, menu_rect, 3)

        for i, option in enumerate(self.main_options):
            x = SCREEN_WIDTH - 230 + (i % 2) * 110
            y = SCREEN_HEIGHT - 80 + (i // 2) * 40

            color = COLOR_BLACK
            prefix = " "
            if i == self.selected_main_index:
                color = COLOR_RED
                prefix = ">"

            text = font.render(f"{prefix} {option}", True, color)
            screen.blit(text, (x, y))

    def draw_move_menu(self, screen) :
        """Dessine le menu de sélection des attaques."""
        menu_rect = pygame.Rect(0, SCREEN_HEIGHT - 100, SCREEN_WIDTH, 100)
        pygame.draw.rect(screen, COLOR_WHITE, menu_rect)
        pygame.draw.rect(screen, COLOR_BLACK, menu_rect, 3)

        for i, move in enumerate(self.player.moves):
            # Positionnement sur une grille 2x2
            x = 50 + (i % 2) * 250
            y = SCREEN_HEIGHT - 80 + (i // 2) * 40

            color = COLOR_BLACK
            prefix = " "
            if i == self.selected_move_index:
                color = COLOR_RED  # Indique la sélection
                prefix = ">"

            text = font.render(f"{prefix} {move.name}", True, color)
            screen.blit(text, (x, y))

    def draw_message_box(self, screen, ):
        """Dessine la boîte de dialogue en bas de l'écran."""
        box_rect = pygame.Rect(0, SCREEN_HEIGHT - 100, SCREEN_WIDTH, 100)
        pygame.draw.rect(screen, COLOR_WHITE, box_rect)
        pygame.draw.rect(screen, COLOR_BLACK, box_rect, 3)

        if self.current_message:
            text = font.render(self.current_message, True, COLOR_BLACK)
            screen.blit(text, (20, SCREEN_HEIGHT - 60))

            # Indicateur "Appuyez sur espace"
            indicator = font_small.render("Appuyez sur ESPACE", True, COLOR_GRAY)
            screen.blit(indicator, (SCREEN_WIDTH - 150, SCREEN_HEIGHT - 25))
