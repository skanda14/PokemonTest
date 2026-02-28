import pygame
import random
import sys
import math

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

# =====================================================================
# MOCK CLASSES (À remplacer par tes propres classes/bases de données)
# =====================================================================

# Les types qui utilisent la stat d'Attaque et de Défense dans la Gen 1
PHYSICAL_TYPES = ["Normal", "Fighting", "Flying", "Poison", "Ground", "Rock", "Bug", "Ghost"]

# Table d'efficacité des types simplifiée pour l'exemple
TYPE_CHART = {
    "Electric": {"Water": 2.0, "Grass": 0.5, "Ground": 0.0, "Electric": 0.5},
    "Grass": {"Water": 2.0, "Ground": 2.0, "Fire": 0.5, "Grass": 0.5, "Poison": 0.5},
    "Normal": {"Ghost": 0.0, "Rock": 0.5}
}


def get_type_effectiveness(move_type, defender_types):
    """Calcule le multiplicateur de type."""
    multiplier = 1.0
    if move_type in TYPE_CHART:
        for def_type in defender_types:
            if def_type in TYPE_CHART[move_type]:
                multiplier *= TYPE_CHART[move_type][def_type]
    return multiplier


class Move:
    def __init__(self, name, type_name, power, accuracy, pp):
        self.name = name
        self.type = type_name
        self.power = power
        self.accuracy = accuracy
        self.max_pp = pp
        self.pp = pp


class Item:
    def __init__(self, name, description, effect_type, effect_value, quantity):
        self.name = name
        self.description = description
        self.effect_type = effect_type  # ex: "heal"
        self.effect_value = effect_value  # ex: 20
        self.quantity = quantity


class Pokemon:
    def __init__(self, name, level, types, hp, attack, defense, special, speed, moves):
        self.name = name
        self.level = level
        self.types = types
        self.max_hp = hp
        self.hp = hp

        # Statistiques de la Gen 1 (Spécial est unique)
        self.attack = attack
        self.defense = defense
        self.special = special
        self.speed = speed
        self.base_speed = speed  # Utilisé pour les coups critiques

        self.moves = moves


# =====================================================================
# MOTEUR DE COMBAT GEN 1
# =====================================================================

def calculate_damage(attacker, defender, move):
    """
    Formule de dégâts fidèle à la Génération 1.
    """
    if move.power == 0:
        return 0, False, 1.0

    # 1. Vérifier si l'attaque est Physique ou Spéciale selon le type
    is_physical = move.type in PHYSICAL_TYPES

    atk_stat = attacker.attack if is_physical else attacker.special
    def_stat = defender.defense if is_physical else defender.special

    # 2. Coup Critique (Basé sur la vitesse de base dans la Gen 1)
    # Taux de critique Gen 1 : (Vitesse de base / 2) / 256
    crit_chance = (attacker.base_speed / 2.0) / 256.0
    is_crit = random.random() < crit_chance

    # Dans la Gen 1, le niveau est doublé lors d'un coup critique dans la formule
    level_calc = attacker.level * 2 if is_crit else attacker.level

    # 3. Calcul de base
    # Formule Gen 1: Damage = ((((2 * Level / 5) + 2) * Power * A / D) / 50) + 2
    base_damage = math.floor(math.floor(math.floor(2 * level_calc / 5 + 2) * move.power * atk_stat / def_stat) / 50) + 2

    # 4. STAB (Same Type Attack Bonus)
    if move.type in attacker.types:
        base_damage = math.floor(base_damage * 1.5)

    # 5. Efficacité des Types
    type_modifier = get_type_effectiveness(move.type, defender.types)
    base_damage = math.floor(base_damage * type_modifier)

    # 6. Random (Nombre entre 217 et 255 dans Gen 1)
    if base_damage > 0:
        random_factor = random.randint(217, 255)
        base_damage = math.floor((base_damage * random_factor) / 255)

    return max(1, base_damage), is_crit, type_modifier


def check_accuracy(move):
    """
    Reproduit le bug de précision de la Gen 1 (1 chance sur 256 de rater
    même avec 100% de précision).
    """
    # Génère un nombre entre 0 et 255
    rand = random.randint(0, 255)
    # L'attaque touche si rand est strictement inférieur à la précision
    # Précision convertie sur une base 255 (ex: 100% = 255)
    acc_255 = int((move.accuracy / 100.0) * 255)
    return rand < acc_255


# =====================================================================
# INTERFACE PYGAME
# =====================================================================

class BattleEngine:
    def __init__(self, screen, player_party, enemy_pkmn, inventory):
        self.screen = screen
        self.player_party = player_party
        self.player = player_party[0]  # Le premier Pokémon de l'équipe est envoyé au combat
        self.enemy = enemy_pkmn
        self.inventory = inventory

        # États du jeu: "MAIN_MENU", "MOVE_MENU", "PARTY_MENU", "ITEM_MENU", "ITEM_TARGET_MENU", "RESOLVING", "END"
        self.state = "MAIN_MENU"
        self.return_state = None  # Permet de revenir au bon menu après un message
        self.force_switch = False  # Devient True quand le Pokémon actif est K.O.
        self.message_queue = ["Un combat Pokémon commence !", f"Un {self.enemy.name} sauvage apparaît !"]
        self.current_message = ""
        self.action_queue = []  # Stocke les actions (dictionnaires) à résoudre
        self.pending_item = None  # Stocke l'objet en cours d'utilisation avant le choix de la cible

        self.main_options = ["FIGHT", "PKMN", "ITEM", "RUN"]
        self.selected_main_index = 0
        self.selected_move_index = 0
        self.selected_party_index = 0
        self.selected_item_index = 0

    def draw_health_bar(self, x, y, hp, max_hp, name, level):
        """Dessine une barre de vie style Gen 1 simplifiée."""
        pygame.draw.rect(self.screen, COLOR_BLACK, (x, y, 200, 50), 2)
        pygame.draw.rect(self.screen, COLOR_WHITE, (x + 2, y + 2, 196, 46))

        # Texte
        name_text = font.render(name, True, COLOR_BLACK)
        level_text = font_small.render(f"Nv{level}", True, COLOR_BLACK)
        self.screen.blit(name_text, (x + 5, y + 5))
        self.screen.blit(level_text, (x + 150, y + 8))

        # Barre
        bar_width = 150
        hp_ratio = max(0.0, hp / max_hp)
        current_bar_width = int(bar_width * hp_ratio)

        pygame.draw.rect(self.screen, COLOR_BLACK, (x + 20, y + 30, bar_width + 4, 14))
        pygame.draw.rect(self.screen, COLOR_WHITE, (x + 22, y + 32, bar_width, 10))

        # Couleur de la barre de vie
        hp_color = COLOR_GREEN
        if hp_ratio < 0.2:
            hp_color = COLOR_RED
        elif hp_ratio < 0.5:
            hp_color = (200, 200, 50)  # Jaune

        if current_bar_width > 0:
            pygame.draw.rect(self.screen, hp_color, (x + 22, y + 32, current_bar_width, 10))

    def draw_main_menu(self):
        """Dessine le menu principal (FIGHT, PKMN, ITEM, RUN)."""
        # Boîte de dialogue de gauche (Que va faire X ?)
        prompt_rect = pygame.Rect(0, SCREEN_HEIGHT - 100, SCREEN_WIDTH - 250, 100)
        pygame.draw.rect(self.screen, COLOR_WHITE, prompt_rect)
        pygame.draw.rect(self.screen, COLOR_BLACK, prompt_rect, 3)

        prompt_text1 = font.render("Que doit faire", True, COLOR_BLACK)
        prompt_text2 = font.render(f"{self.player.name} ?", True, COLOR_BLACK)
        self.screen.blit(prompt_text1, (20, SCREEN_HEIGHT - 80))
        self.screen.blit(prompt_text2, (20, SCREEN_HEIGHT - 50))

        # Boîte de menu de droite
        menu_rect = pygame.Rect(SCREEN_WIDTH - 250, SCREEN_HEIGHT - 100, 250, 100)
        pygame.draw.rect(self.screen, COLOR_WHITE, menu_rect)
        pygame.draw.rect(self.screen, COLOR_BLACK, menu_rect, 3)

        for i, option in enumerate(self.main_options):
            x = SCREEN_WIDTH - 230 + (i % 2) * 110
            y = SCREEN_HEIGHT - 80 + (i // 2) * 40

            color = COLOR_BLACK
            prefix = " "
            if i == self.selected_main_index:
                color = COLOR_RED
                prefix = ">"

            text = font.render(f"{prefix} {option}", True, color)
            self.screen.blit(text, (x, y))

    def draw_move_menu(self):
        """Dessine le menu de sélection des attaques avec les PP."""
        menu_rect = pygame.Rect(0, SCREEN_HEIGHT - 100, SCREEN_WIDTH, 100)
        pygame.draw.rect(self.screen, COLOR_WHITE, menu_rect)
        pygame.draw.rect(self.screen, COLOR_BLACK, menu_rect, 3)

        for i, move in enumerate(self.player.moves):
            # Positionnement sur une grille 2x2
            x = 50 + (i % 2) * 250
            y = SCREEN_HEIGHT - 85 + (i // 2) * 45

            color = COLOR_BLACK
            prefix = " "
            if i == self.selected_move_index:
                color = COLOR_RED  # Indique la sélection
                prefix = ">"

            text = font.render(f"{prefix} {move.name}", True, color)
            pp_text = font_small.render(f"PP {move.pp}/{move.max_pp}", True, color)

            self.screen.blit(text, (x, y))
            self.screen.blit(pp_text, (x + 20, y + 20))

    def draw_party_menu(self):
        """Dessine le menu de l'équipe Pokémon."""
        menu_rect = pygame.Rect(50, 30, 500, 250)
        pygame.draw.rect(self.screen, COLOR_WHITE, menu_rect)
        pygame.draw.rect(self.screen, COLOR_BLACK, menu_rect, 3)

        if self.state == "ITEM_TARGET_MENU":
            title = font.render("Utiliser sur qui ?", True, COLOR_BLACK)
        else:
            title = font.render("Choisissez un POKéMON", True, COLOR_BLACK)

        self.screen.blit(title, (70, 40))

        for i, pkmn in enumerate(self.player_party):
            y = 80 + i * 50
            color = COLOR_BLACK
            prefix = " "
            if i == self.selected_party_index:
                color = COLOR_RED
                prefix = ">"

            text = font.render(f"{prefix} {pkmn.name}", True, color)
            lvl_text = font_small.render(f"Nv{pkmn.level}", True, color)

            hp_color = COLOR_BLACK
            if pkmn.hp == 0:
                hp_color = COLOR_RED

            hp_text = font_small.render(f"HP {pkmn.hp}/{pkmn.max_hp}", True, hp_color)

            self.screen.blit(text, (70, y))
            self.screen.blit(lvl_text, (250, y + 4))
            self.screen.blit(hp_text, (350, y + 4))

    def draw_item_menu(self):
        """Dessine le menu des objets (inventaire)."""
        menu_rect = pygame.Rect(50, 30, 500, 250)
        pygame.draw.rect(self.screen, COLOR_WHITE, menu_rect)
        pygame.draw.rect(self.screen, COLOR_BLACK, menu_rect, 3)

        title = font.render("OBJETS", True, COLOR_BLACK)
        self.screen.blit(title, (70, 40))

        # On ajoute une option "RETOUR" virtuelle à la fin de la liste
        display_items = self.inventory + [{"name": "RETOUR", "quantity": ""}]

        for i, item in enumerate(display_items):
            y = 80 + i * 40
            color = COLOR_BLACK
            prefix = " "
            if i == self.selected_item_index:
                color = COLOR_RED
                prefix = ">"

            if isinstance(item, dict):  # C'est le bouton RETOUR
                text = font.render(f"{prefix} {item['name']}", True, color)
                self.screen.blit(text, (70, y))
            else:
                text = font.render(f"{prefix} {item.name}", True, color)
                # Griser la quantité si on en a plus
                qty_color = color if item.quantity > 0 else COLOR_GRAY
                qty_text = font.render(f"x{item.quantity}", True, qty_color)
                self.screen.blit(text, (70, y))
                self.screen.blit(qty_text, (400, y))

    def draw_message_box(self):
        """Dessine la boîte de dialogue en bas de l'écran."""
        box_rect = pygame.Rect(0, SCREEN_HEIGHT - 100, SCREEN_WIDTH, 100)
        pygame.draw.rect(self.screen, COLOR_WHITE, box_rect)
        pygame.draw.rect(self.screen, COLOR_BLACK, box_rect, 3)

        if self.current_message:
            text = font.render(self.current_message, True, COLOR_BLACK)
            self.screen.blit(text, (20, SCREEN_HEIGHT - 60))

            # Indicateur "Appuyez sur espace"
            indicator = font_small.render("Appuyez sur ESPACE", True, COLOR_GRAY)
            self.screen.blit(indicator, (SCREEN_WIDTH - 150, SCREEN_HEIGHT - 25))

    def execute_move(self, attacker, defender, move):
        """Logique de résolution d'une attaque."""
        move.pp -= 1
        self.message_queue.append(f"{attacker.name} utilise {move.name} !")

        if not check_accuracy(move):
            self.message_queue.append("Mais l'attaque échoue ! (Bug 1/256 ou esquive)")
            return

        damage, is_crit, type_mod = calculate_damage(attacker, defender, move)
        defender.hp -= damage

        if is_crit:
            self.message_queue.append("Coup Critique !")

        if type_mod > 1.0:
            self.message_queue.append("C'est super efficace !")
        elif type_mod < 1.0 and type_mod > 0.0:
            self.message_queue.append("Ce n'est pas très efficace...")
        elif type_mod == 0.0:
            self.message_queue.append(f"Cela n'affecte pas {defender.name}...")

        if defender.hp <= 0:
            defender.hp = 0
            self.message_queue.append(f"{defender.name} est K.O. !")

    def process_next_action(self):
        """Exécute la prochaine action dans la file d'attente (gestion séquentielle)."""
        if not self.action_queue:
            return

        action = self.action_queue.pop(0)

        if action["type"] == "switch":
            old_name = self.player.name
            self.player = action["data"]
            self.message_queue.append(f"Reviens {old_name} !")
            self.message_queue.append(f"Go ! {self.player.name} !")
            self.advance_message()
            return

        elif action["type"] == "item":
            item_data = action["data"]
            item = item_data["item"]
            target = item_data["target"]

            item.quantity -= 1
            self.message_queue.append(f"Vous utilisez {item.name} sur {target.name} !")

            if item.effect_type == "heal":
                healed_amount = min(item.effect_value, target.max_hp - target.hp)
                target.hp += healed_amount
                self.message_queue.append(f"{target.name} récupère {healed_amount} PV !")

            self.advance_message()
            return

        elif action["type"] == "attack":
            is_player = (action["actor"] == "player")
            attacker = self.player if is_player else self.enemy
            defender = self.enemy if is_player else self.player
            move = action["data"]

            # Si l'attaquant a été mis K.O. avant de pouvoir attaquer
            if attacker.hp <= 0:
                self.process_next_action()
                return

            if move is None:
                self.message_queue.append(f"{attacker.name} n'a plus d'attaques !")
            else:
                self.execute_move(attacker, defender, move)

            self.advance_message()

    def resolve_turn(self, action_type, action_data):
        """Organise l'ordre des actions, gère le switch et la vitesse."""
        # Sélection pour l'ennemi (IA très basique, on vérifie qu'il a des PP)
        available_enemy_moves = [m for m in self.enemy.moves if m.pp > 0]
        enemy_move = random.choice(available_enemy_moves) if available_enemy_moves else None

        if action_type == "switch":
            # Le switch est prioritaire sur les attaques
            self.action_queue = [
                {"actor": "player", "type": "switch", "data": action_data},
                {"actor": "enemy", "type": "attack", "data": enemy_move}
            ]
        elif action_type == "item":
            # L'utilisation d'un objet est également prioritaire
            self.action_queue = [
                {"actor": "player", "type": "item", "data": action_data},
                {"actor": "enemy", "type": "attack", "data": enemy_move}
            ]
        elif action_type == "attack":
            player_move = action_data
            # Déterminer l'ordre avec la Vitesse
            if self.player.speed >= self.enemy.speed:
                self.action_queue = [
                    {"actor": "player", "type": "attack", "data": player_move},
                    {"actor": "enemy", "type": "attack", "data": enemy_move}
                ]
            else:
                self.action_queue = [
                    {"actor": "enemy", "type": "attack", "data": enemy_move},
                    {"actor": "player", "type": "attack", "data": player_move}
                ]

        # On lance l'exécution de la première action
        self.process_next_action()

    def advance_message(self):
        """Passe au message suivant dans la file d'attente ou déclenche l'action suivante."""
        if self.message_queue:
            self.current_message = self.message_queue.pop(0)
            self.state = "RESOLVING"
        else:
            self.current_message = ""
            if self.enemy.hp <= 0:
                self.state = "END"
                self.current_message = "Vous avez gagné !"
            elif self.player.hp <= 0:
                # Vérifie s'il reste des Pokémon en vie dans l'équipe
                if any(p.hp > 0 for p in self.player_party):
                    self.force_switch = True
                    self.state = "PARTY_MENU"
                else:
                    self.state = "END"
                    self.current_message = "Vous n'avez plus de Pokémon en état de combattre..."
            elif self.action_queue:
                # S'il reste des actions à résoudre ce tour-ci (la 2ème attaque)
                self.process_next_action()
            else:
                # Retour au menu normal, ou au menu des attaques si on a reçu l'avertissement "Plus de PP"
                if getattr(self, "return_state", None):
                    self.state = self.return_state
                    self.return_state = None
                else:
                    self.state = "MAIN_MENU"

    def update(self, screen):
        screen.fill(COLOR_WHITE)

        # Affichage des barres de vie
        self.draw_health_bar(50, 50, self.enemy.hp, self.enemy.max_hp, self.enemy.name, self.enemy.level)
        self.draw_health_bar(350, 200, self.player.hp, self.player.max_hp, self.player.name, self.player.level)

        # Sprites factices (Rectangles)
        pygame.draw.rect(screen, COLOR_RED, (380, 50, 100, 100))  # Sprite Ennemi
        pygame.draw.rect(screen, COLOR_GREEN, (100, 200, 100, 100))  # Sprite Joueur

        if self.state == "MAIN_MENU":
            if not self.message_queue:
                self.draw_main_menu()
            else:
                self.draw_message_box()
        elif self.state == "MOVE_MENU":
            self.draw_move_menu()
        elif self.state == "PARTY_MENU":
            self.draw_party_menu()
            if self.message_queue:
                self.draw_message_box()
        elif self.state == "ITEM_MENU":
            self.draw_item_menu()
            if self.message_queue:
                self.draw_message_box()
        elif self.state == "ITEM_TARGET_MENU":
            self.draw_party_menu()
            if self.message_queue:
                self.draw_message_box()
        elif self.state == "RESOLVING" or self.state == "END":
            self.draw_message_box()

    def handle_event(self, event):
        if self.state == "MAIN_MENU" and not self.message_queue:
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
                    elif selected_option == "PKMN":
                        self.state = "PARTY_MENU"
                        self.selected_party_index = 0
                    elif selected_option == "ITEM":
                        self.state = "ITEM_MENU"
                        self.selected_item_index = 0
                    elif selected_option == "RUN":
                        self.message_queue.append("Vous prenez la fuite !")
                        self.enemy.hp = 0  # Astuce pour finir le combat proprement
                        self.advance_message()

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
                    if selected_move.pp > 0:
                        self.resolve_turn("attack", selected_move)
                    else:
                        # Gestion des attaques à 0 PP
                        self.message_queue.append("Il n'y a plus de PP pour cette attaque !")
                        self.return_state = "MOVE_MENU"
                        self.advance_message()

        elif self.state == "PARTY_MENU":
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE or event.key == pygame.K_BACKSPACE:
                    if not getattr(self, "force_switch", False):
                        self.state = "MAIN_MENU"  # Retour annulé (uniquement si non forcé)
                elif event.key == pygame.K_DOWN:
                    if self.selected_party_index + 1 < len(self.player_party):
                        self.selected_party_index += 1
                elif event.key == pygame.K_UP:
                    if self.selected_party_index > 0:
                        self.selected_party_index -= 1
                elif event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                    selected_pkmn = self.player_party[self.selected_party_index]
                    if selected_pkmn.hp <= 0:
                        self.message_queue.append(f"{selected_pkmn.name} est K.O. !")
                        self.return_state = "PARTY_MENU"
                        self.advance_message()
                    elif selected_pkmn == self.player and not getattr(self, "force_switch", False):
                        self.message_queue.append(f"{selected_pkmn.name} est déjà au combat !")
                        self.return_state = "PARTY_MENU"
                        self.advance_message()
                    else:
                        # Remplacement valide
                        if getattr(self, "force_switch", False):
                            self.force_switch = False
                            self.player = selected_pkmn
                            self.message_queue.append(f"Go ! {self.player.name} !")
                            self.action_queue = []  # On annule les éventuelles actions résiduelles (fin de tour)
                            self.advance_message()
                        else:
                            self.resolve_turn("switch", selected_pkmn)

        elif self.state == "ITEM_MENU":
            if event.type == pygame.KEYDOWN:
                display_items_count = len(self.inventory) + 1  # +1 pour le bouton RETOUR

                if event.key == pygame.K_ESCAPE or event.key == pygame.K_BACKSPACE:
                    self.state = "MAIN_MENU"
                elif event.key == pygame.K_DOWN:
                    if self.selected_item_index + 1 < display_items_count:
                        self.selected_item_index += 1
                elif event.key == pygame.K_UP:
                    if self.selected_item_index > 0:
                        self.selected_item_index -= 1
                elif event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                    if self.selected_item_index == len(self.inventory):
                        # Option RETOUR sélectionnée
                        self.state = "MAIN_MENU"
                    else:
                        selected_item = self.inventory[self.selected_item_index]
                        if selected_item.quantity <= 0:
                            self.message_queue.append("Vous n'en avez plus !")
                            self.return_state = "ITEM_MENU"
                            self.advance_message()
                        else:
                            # Au lieu de l'utiliser tout de suite, on passe à la sélection de la cible
                            self.pending_item = selected_item
                            self.state = "ITEM_TARGET_MENU"
                            self.selected_party_index = 0

        elif self.state == "ITEM_TARGET_MENU":
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE or event.key == pygame.K_BACKSPACE:
                    self.state = "ITEM_MENU"  # Retour à l'inventaire
                elif event.key == pygame.K_DOWN:
                    if self.selected_party_index + 1 < len(self.player_party):
                        self.selected_party_index += 1
                elif event.key == pygame.K_UP:
                    if self.selected_party_index > 0:
                        self.selected_party_index -= 1
                elif event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                    selected_pkmn = self.player_party[self.selected_party_index]

                    # Vérifications avant d'utiliser l'objet sur la cible
                    if self.pending_item.effect_type == "heal" and selected_pkmn.hp == selected_pkmn.max_hp:
                        self.message_queue.append(f"{selected_pkmn.name} a déjà tous ses PV !")
                        self.return_state = "ITEM_TARGET_MENU"
                        self.advance_message()
                    elif self.pending_item.effect_type == "heal" and selected_pkmn.hp <= 0:
                        self.message_queue.append(f"{selected_pkmn.name} est K.O. !")
                        self.return_state = "ITEM_TARGET_MENU"
                        self.advance_message()
                    else:
                        # Utilisation valide sur la cible sélectionnée
                        action_data = {"item": self.pending_item, "target": selected_pkmn}
                        self.resolve_turn("item", action_data)

        elif self.state == "RESOLVING" or (self.state == "MAIN_MENU" and self.message_queue):
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.advance_message()


# =====================================================================
# INITIALISATION DES DONNÉES ET BOUCLE PRINCIPALE
# =====================================================================

def main():
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Pokémon Gen 1 Battle System")
    clock = pygame.time.Clock()

    # Création des Pokémon avec leurs attaques instanciées directement
    pikachu = Pokemon("Pikachu", 5, ["Electric"], 20, attack=11, defense=9, special=11, speed=15, moves=[
        Move("Thunder Shock", "Electric", 40, 100, 30),
        Move("Quick Attack", "Normal", 40, 100, 30)
    ])

    charmander = Pokemon("Charmander", 5, ["Fire"], 19, attack=11, defense=9, special=11, speed=13, moves=[
        Move("Ember", "Fire", 40, 100, 25),
        Move("Scratch", "Normal", 40, 100, 35)
    ])

    squirtle = Pokemon("Squirtle", 5, ["Water"], 20, attack=10, defense=13, special=10, speed=10, moves=[
        Move("Bubble", "Water", 20, 100, 30),
        Move("Tackle", "Normal", 35, 95, 35)
    ])

    # Création de l'équipe du joueur
    player_party = [pikachu, charmander, squirtle]

    # Création de l'inventaire
    potion = Item("Potion", "Restaure 20 PV", "heal", 20, 3)
    super_potion = Item("Super Potion", "Restaure 50 PV", "heal", 50, 1)
    inventory = [potion, super_potion]

    bulbasaur = Pokemon("Bulbasaur", 5, ["Grass", "Poison"], 21, attack=10, defense=10, special=12, speed=10, moves=[
        Move("Vine Whip", "Grass", 45, 100, 25),
        Move("Tackle", "Normal", 35, 95, 35)
    ])

    # Initialisation du moteur avec la liste de l'équipe et l'inventaire
    engine = BattleEngine(screen, player_party, bulbasaur, inventory)

    # Lancement du premier message
    engine.advance_message()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            else:
                engine.handle_event(event)

        engine.update(screen)
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()