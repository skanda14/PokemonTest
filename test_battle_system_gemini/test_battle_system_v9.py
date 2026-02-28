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
MESSAGE_DURATION = 1500  # Durée d'affichage d'un message (ms)
HP_DRAIN_SPEED = 0.5  # Vitesse de descente de la barre (PV par frame)

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
# MOCK CLASSES
# =====================================================================

PHYSICAL_TYPES = ["Normal", "Fighting", "Flying", "Poison", "Ground", "Rock", "Bug", "Ghost"]

TYPE_CHART = {
    "Electric": {"Water": 2.0, "Grass": 0.5, "Ground": 0.0, "Electric": 0.5},
    "Grass": {"Water": 2.0, "Ground": 2.0, "Fire": 0.5, "Grass": 0.5, "Poison": 0.5},
    "Normal": {"Ghost": 0.0, "Rock": 0.5},
    "Fire": {"Grass": 2.0, "Water": 0.5, "Fire": 0.5},
    "Water": {"Fire": 2.0, "Grass": 0.5, "Water": 0.5, "Ground": 2.0}
}


def get_type_effectiveness(move_type, defender_types):
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
        self.effect_type = effect_type
        self.effect_value = effect_value
        self.quantity = quantity


class Pokemon:
    def __init__(self, name, level, types, hp, attack, defense, special, speed, moves):
        self.name = name
        self.level = level
        self.types = types
        self.max_hp = hp
        self.hp = hp
        self.visual_hp = float(hp)  # Pour l'animation de la barre
        self.attack = attack
        self.defense = defense
        self.special = special
        self.speed = speed
        self.base_speed = speed
        self.moves = moves


# =====================================================================
# LOGIQUE DE COMBAT
# =====================================================================

def calculate_damage(attacker, defender, move):
    if move.power == 0: return 0, False, 1.0
    is_physical = move.type in PHYSICAL_TYPES
    atk_stat = attacker.attack if is_physical else attacker.special
    def_stat = defender.defense if is_physical else defender.special
    crit_chance = (attacker.base_speed / 2.0) / 256.0
    is_crit = random.random() < crit_chance
    level_calc = attacker.level * 2 if is_crit else attacker.level
    base_damage = math.floor(math.floor(math.floor(2 * level_calc / 5 + 2) * move.power * atk_stat / def_stat) / 50) + 2
    if move.type in attacker.types: base_damage = math.floor(base_damage * 1.5)
    type_modifier = get_type_effectiveness(move.type, defender.types)
    base_damage = math.floor(base_damage * type_modifier)
    if base_damage > 0:
        random_factor = random.randint(217, 255)
        base_damage = math.floor((base_damage * random_factor) / 255)
    return max(1, base_damage), is_crit, type_modifier


def check_accuracy(move):
    rand = random.randint(0, 255)
    acc_255 = int((move.accuracy / 100.0) * 255)
    return rand < acc_255


def try_capture(target, ball_rate):
    chance = ((target.max_hp * 3 - target.hp * 2) * ball_rate) / (target.max_hp * 3)
    roll = random.random()
    return roll < (chance / 100.0)


# =====================================================================
# MOTEUR DE COMBAT
# =====================================================================

class BattleEngine:
    def __init__(self, screen, player_party, enemy_pkmn, inventory):
        self.screen = screen
        self.player_party = player_party
        self.player = player_party[0]
        self.enemy = enemy_pkmn
        self.inventory = inventory

        self.state = "MAIN_MENU"
        self.return_state = None
        self.force_switch = False
        self.message_queue = ["Un combat Pokémon commence !", f"Un {self.enemy.name} sauvage apparaît !"]
        self.current_message = ""
        self.action_queue = []
        self.pending_item = None

        self.message_timer = 0
        self.is_hp_animating = False  # Nouveau flag pour bloquer les messages

        self.main_options = ["FIGHT", "PKMN", "ITEM", "RUN"]
        self.selected_main_index = 0
        self.selected_move_index = 0
        self.selected_party_index = 0
        self.selected_item_index = 0

    def draw_health_bar(self, x, y, visual_hp, max_hp, name, level):
        pygame.draw.rect(self.screen, COLOR_BLACK, (x, y, 200, 50), 2)
        pygame.draw.rect(self.screen, COLOR_WHITE, (x + 2, y + 2, 196, 46))
        name_text = font.render(name, True, COLOR_BLACK)
        level_text = font_small.render(f"Nv{level}", True, COLOR_BLACK)
        self.screen.blit(name_text, (x + 5, y + 5))
        self.screen.blit(level_text, (x + 150, y + 8))

        bar_width = 150
        hp_ratio = max(0.0, visual_hp / max_hp)
        current_bar_width = int(bar_width * hp_ratio)

        pygame.draw.rect(self.screen, COLOR_BLACK, (x + 20, y + 30, bar_width + 4, 14))
        pygame.draw.rect(self.screen, COLOR_WHITE, (x + 22, y + 32, bar_width, 10))

        hp_color = COLOR_GREEN
        if hp_ratio < 0.2:
            hp_color = COLOR_RED
        elif hp_ratio < 0.5:
            hp_color = (200, 200, 50)

        if current_bar_width > 0:
            pygame.draw.rect(self.screen, hp_color, (x + 22, y + 32, current_bar_width, 10))

    def draw_message_box(self):
        box_rect = pygame.Rect(0, SCREEN_HEIGHT - 100, SCREEN_WIDTH, 100)
        pygame.draw.rect(self.screen, COLOR_WHITE, box_rect)
        pygame.draw.rect(self.screen, COLOR_BLACK, box_rect, 3)
        if self.current_message:
            text = font.render(self.current_message, True, COLOR_BLACK)
            self.screen.blit(text, (20, SCREEN_HEIGHT - 60))

    def execute_move(self, attacker, defender, move):
        move.pp -= 1
        self.message_queue.append(f"{attacker.name} utilise {move.name} !")

        if not check_accuracy(move):
            self.message_queue.append("Mais l'attaque échoue !")
            return

        damage, is_crit, type_mod = calculate_damage(attacker, defender, move)
        defender.hp -= damage

        # Flag pour indiquer que le prochain message doit attendre la fin de l'animation HP
        self.is_hp_animating = True

        if is_crit: self.message_queue.append("Coup Critique !")
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
        if not self.action_queue: return
        action = self.action_queue.pop(0)

        if action["type"] == "switch":
            old_name = self.player.name
            self.player = action["data"]
            self.message_queue.append(f"Reviens {old_name} !")
            self.message_queue.append(f"Go ! {self.player.name} !")
            self.advance_message()

        elif action["type"] == "item":
            item_data = action["data"]
            item = item_data["item"]
            if item.effect_type == "heal":
                target = item_data["target"]
                item.quantity -= 1
                self.message_queue.append(f"Vous utilisez {item.name} sur {target.name} !")
                target.hp = min(target.max_hp, target.hp + item.effect_value)
                self.is_hp_animating = True  # Animation aussi pour le soin
                self.advance_message()
            elif item.effect_type == "capture":
                item.quantity -= 1
                self.message_queue.append(f"Vous lancez une {item.name} !")
                if try_capture(self.enemy, item.effect_value):
                    self.message_queue.append(f"Et hop ! {self.enemy.name} est capturé !")
                    if len(self.player_party) < 6: self.player_party.append(self.enemy)
                    self.enemy.hp = 0
                    self.is_hp_animating = True
                    self.action_queue = []
                else:
                    self.message_queue.append(f"Zut ! {self.enemy.name} s'est libéré !")
                self.advance_message()

        elif action["type"] == "attack":
            is_player = (action["actor"] == "player")
            attacker = self.player if is_player else self.enemy
            defender = self.enemy if is_player else self.player
            move = action["data"]
            if attacker.hp <= 0:
                self.process_next_action()
                return
            if move is None:
                self.message_queue.append(f"{attacker.name} n'a plus d'attaques !")
            else:
                self.execute_move(attacker, defender, move)
            self.advance_message()

    def resolve_turn(self, action_type, action_data):
        available_enemy_moves = [m for m in self.enemy.moves if m.pp > 0]
        enemy_move = random.choice(available_enemy_moves) if available_enemy_moves else None

        if action_type == "switch" or action_type == "item":
            self.action_queue = [
                {"actor": "player", "type": action_type, "data": action_data},
                {"actor": "enemy", "type": "attack", "data": enemy_move}
            ]
        elif action_type == "attack":
            if self.player.speed >= self.enemy.speed:
                self.action_queue = [
                    {"actor": "player", "type": "attack", "data": action_data},
                    {"actor": "enemy", "type": "attack", "data": enemy_move}
                ]
            else:
                self.action_queue = [
                    {"actor": "enemy", "type": "attack", "data": enemy_move},
                    {"actor": "player", "type": "attack", "data": action_data}
                ]
        self.process_next_action()

    def advance_message(self):
        self.message_timer = pygame.time.get_ticks()

        if self.message_queue:
            self.current_message = self.message_queue.pop(0)
            self.state = "RESOLVING"
        else:
            self.current_message = ""
            if self.enemy.hp <= 0:
                self.state = "END"
                self.current_message = f"{self.enemy.name} a rejoint votre équipe !" if self.enemy in self.player_party else "Vous avez gagné !"
            elif self.player.hp <= 0:
                if any(p.hp > 0 for p in self.player_party):
                    self.force_switch = True
                    self.state = "PARTY_MENU"
                else:
                    self.state = "END"
                    self.current_message = "Vous n'avez plus de Pokémon..."
            elif self.action_queue:
                self.process_next_action()
            else:
                if getattr(self, "return_state", None):
                    self.state = self.return_state
                    self.return_state = None
                else:
                    self.state = "MAIN_MENU"

    def update_visual_hp(self, pkmn):
        """Fait tendre visual_hp vers hp graduellement."""
        if abs(pkmn.visual_hp - pkmn.hp) < HP_DRAIN_SPEED:
            pkmn.visual_hp = float(pkmn.hp)
            return False  # Animation terminée
        else:
            if pkmn.visual_hp > pkmn.hp:
                pkmn.visual_hp -= HP_DRAIN_SPEED
            else:
                pkmn.visual_hp += HP_DRAIN_SPEED
            return True  # Toujours en cours

    def update(self, screen):
        # Gestion des barres de vie
        anim_enemy = self.update_visual_hp(self.enemy)
        anim_player = self.update_visual_hp(self.player)

        # On ne bloque le message que si on a explicitement demandé une animation HP
        # et que l'animation n'est pas encore finie.
        if self.is_hp_animating:
            if not anim_enemy and not anim_player:
                self.is_hp_animating = False
                # Optionnel : On peut reset le timer ici si on veut que le message
                # reste un peu après la fin de la barre de vie
                # self.message_timer = pygame.time.get_ticks()

        # Gestion du timer automatique pour les messages (bloqué si animation HP en cours)
        if self.current_message and self.state in ["RESOLVING", "END", "MAIN_MENU"]:
            if not self.is_hp_animating:
                if pygame.time.get_ticks() - self.message_timer > MESSAGE_DURATION:
                    self.advance_message()

        screen.fill(COLOR_WHITE)
        self.draw_health_bar(50, 50, self.enemy.visual_hp, self.enemy.max_hp, self.enemy.name, self.enemy.level)
        self.draw_health_bar(350, 200, self.player.visual_hp, self.player.max_hp, self.player.name, self.player.level)

        # Sprites placeholders
        pygame.draw.rect(screen, COLOR_RED, (380, 50, 100, 100))
        pygame.draw.rect(screen, COLOR_GREEN, (100, 200, 100, 100))

        if self.state == "MAIN_MENU":
            if not self.message_queue and not self.current_message:
                self.draw_main_menu()
            else:
                self.draw_message_box()
        elif self.state == "MOVE_MENU":
            self.draw_move_menu()
        elif self.state in ["PARTY_MENU", "ITEM_TARGET_MENU"]:
            self.draw_party_menu()
        elif self.state == "ITEM_MENU":
            self.draw_item_menu()
        elif self.state in ["RESOLVING", "END"]:
            self.draw_message_box()

    # Les autres méthodes d'affichage restent identiques (draw_main_menu, etc.)
    def draw_main_menu(self):
        prompt_rect = pygame.Rect(0, SCREEN_HEIGHT - 100, SCREEN_WIDTH - 250, 100)
        pygame.draw.rect(self.screen, COLOR_WHITE, prompt_rect)
        pygame.draw.rect(self.screen, COLOR_BLACK, prompt_rect, 3)
        prompt_text1 = font.render("Que doit faire", True, COLOR_BLACK)
        prompt_text2 = font.render(f"{self.player.name} ?", True, COLOR_BLACK)
        self.screen.blit(prompt_text1, (20, SCREEN_HEIGHT - 80))
        self.screen.blit(prompt_text2, (20, SCREEN_HEIGHT - 50))
        menu_rect = pygame.Rect(SCREEN_WIDTH - 250, SCREEN_HEIGHT - 100, 250, 100)
        pygame.draw.rect(self.screen, COLOR_WHITE, menu_rect)
        pygame.draw.rect(self.screen, COLOR_BLACK, menu_rect, 3)
        for i, option in enumerate(self.main_options):
            x = SCREEN_WIDTH - 230 + (i % 2) * 110
            y = SCREEN_HEIGHT - 80 + (i // 2) * 40
            color = COLOR_RED if i == self.selected_main_index else COLOR_BLACK
            prefix = ">" if i == self.selected_main_index else " "
            text = font.render(f"{prefix} {option}", True, color)
            self.screen.blit(text, (x, y))

    def draw_move_menu(self):
        menu_rect = pygame.Rect(0, SCREEN_HEIGHT - 100, SCREEN_WIDTH, 100)
        pygame.draw.rect(self.screen, COLOR_WHITE, menu_rect)
        pygame.draw.rect(self.screen, COLOR_BLACK, menu_rect, 3)
        for i, move in enumerate(self.player.moves):
            x = 50 + (i % 2) * 250
            y = SCREEN_HEIGHT - 85 + (i // 2) * 45
            color = COLOR_RED if i == self.selected_move_index else COLOR_BLACK
            prefix = ">" if i == self.selected_move_index else " "
            text = font.render(f"{prefix} {move.name}", True, color)
            pp_text = font_small.render(f"PP {move.pp}/{move.max_pp}", True, color)
            self.screen.blit(text, (x, y))
            self.screen.blit(pp_text, (x + 20, y + 20))

    def draw_party_menu(self):
        menu_rect = pygame.Rect(50, 30, 500, 250)
        pygame.draw.rect(self.screen, COLOR_WHITE, menu_rect)
        pygame.draw.rect(self.screen, COLOR_BLACK, menu_rect, 3)
        title_str = "Utiliser sur qui ?" if self.state == "ITEM_TARGET_MENU" else "Choisissez un POKéMON"
        title = font.render(title_str, True, COLOR_BLACK)
        self.screen.blit(title, (70, 40))
        for i, pkmn in enumerate(self.player_party):
            y = 80 + i * 50
            color = COLOR_RED if i == self.selected_party_index else COLOR_BLACK
            prefix = ">" if i == self.selected_party_index else " "
            text = font.render(f"{prefix} {pkmn.name}", True, color)
            lvl_text = font_small.render(f"Nv{pkmn.level}", True, color)
            hp_color = COLOR_RED if pkmn.hp == 0 else COLOR_BLACK
            hp_text = font_small.render(f"HP {int(pkmn.visual_hp)}/{pkmn.max_hp}", True, hp_color)
            self.screen.blit(text, (70, y))
            self.screen.blit(lvl_text, (250, y + 4))
            self.screen.blit(hp_text, (350, y + 4))

    def draw_item_menu(self):
        menu_rect = pygame.Rect(50, 30, 500, 250)
        pygame.draw.rect(self.screen, COLOR_WHITE, menu_rect)
        pygame.draw.rect(self.screen, COLOR_BLACK, menu_rect, 3)
        title = font.render("OBJETS", True, COLOR_BLACK)
        self.screen.blit(title, (70, 40))
        display_items = self.inventory + [{"name": "RETOUR", "quantity": ""}]
        for i, item in enumerate(display_items):
            y = 80 + i * 40
            color = COLOR_RED if i == self.selected_item_index else COLOR_BLACK
            prefix = ">" if i == self.selected_item_index else " "
            if isinstance(item, dict):
                text = font.render(f"{prefix} {item['name']}", True, color)
                self.screen.blit(text, (70, y))
            else:
                text = font.render(f"{prefix} {item.name}", True, color)
                qty_color = color if item.quantity > 0 else COLOR_GRAY
                qty_text = font.render(f"x{item.quantity}", True, qty_color)
                self.screen.blit(text, (70, y))
                self.screen.blit(qty_text, (400, y))

    def handle_event(self, event):
        if event.type != pygame.KEYDOWN: return
        if (self.state in ["RESOLVING", "END"] or (self.state == "MAIN_MENU" and self.current_message)):
            if event.key == pygame.K_SPACE and not self.is_hp_animating:
                self.advance_message()
                return
        if self.state == "MAIN_MENU" and not self.message_queue and not self.current_message:
            if event.key == pygame.K_RIGHT:
                self.selected_main_index = (self.selected_main_index + 1) % 4
            elif event.key == pygame.K_LEFT:
                self.selected_main_index = (self.selected_main_index - 1) % 4
            elif event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                opt = self.main_options[self.selected_main_index]
                if opt == "FIGHT":
                    self.state = "MOVE_MENU"
                elif opt == "PKMN":
                    self.state = "PARTY_MENU"
                elif opt == "ITEM":
                    self.state = "ITEM_MENU"
                elif opt == "RUN":
                    self.message_queue.append("Vous prenez la fuite !")
                    self.enemy.hp = 0
                    self.advance_message()
        elif self.state == "MOVE_MENU":
            if event.key in [pygame.K_ESCAPE, pygame.K_BACKSPACE]:
                self.state = "MAIN_MENU"
            elif event.key == pygame.K_RIGHT:
                self.selected_move_index = (self.selected_move_index + 1) % len(self.player.moves)
            elif event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                move = self.player.moves[self.selected_move_index]
                if move.pp > 0:
                    self.resolve_turn("attack", move)
                else:
                    self.message_queue.append("Plus de PP !")
                    self.return_state = "MOVE_MENU"
                    self.advance_message()
        elif self.state == "PARTY_MENU":
            if event.key in [pygame.K_ESCAPE, pygame.K_BACKSPACE] and not self.force_switch:
                self.state = "MAIN_MENU"
            elif event.key == pygame.K_DOWN:
                self.selected_party_index = (self.selected_party_index + 1) % len(self.player_party)
            elif event.key == pygame.K_UP:
                self.selected_party_index = (self.selected_party_index - 1) % len(self.player_party)
            elif event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                pk = self.player_party[self.selected_party_index]
                if pk.hp <= 0:
                    self.message_queue.append(f"{pk.name} est K.O. !")
                    self.advance_message()
                elif pk == self.player and not self.force_switch:
                    self.message_queue.append("Déjà au combat !")
                    self.advance_message()
                else:
                    if self.force_switch:
                        self.force_switch = False
                        self.player = pk
                        self.message_queue.append(f"Go ! {pk.name} !")
                        self.advance_message()
                    else:
                        self.resolve_turn("switch", pk)
        elif self.state == "ITEM_MENU":
            if event.key in [pygame.K_ESCAPE, pygame.K_BACKSPACE]:
                self.state = "MAIN_MENU"
            elif event.key == pygame.K_DOWN:
                self.selected_item_index = (self.selected_item_index + 1) % (len(self.inventory) + 1)
            elif event.key == pygame.K_UP:
                self.selected_item_index = (self.selected_item_index - 1) % (len(self.inventory) + 1)
            elif event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                if self.selected_item_index == len(self.inventory):
                    self.state = "MAIN_MENU"
                else:
                    item = self.inventory[self.selected_item_index]
                    if item.quantity <= 0:
                        self.message_queue.append("Plus d'exemplaires !")
                        self.advance_message()
                    elif item.effect_type == "heal":
                        self.pending_item = item
                        self.state = "ITEM_TARGET_MENU"
                    elif item.effect_type == "capture":
                        self.resolve_turn("item", {"item": item})
        elif self.state == "ITEM_TARGET_MENU":
            if event.key in [pygame.K_ESCAPE, pygame.K_BACKSPACE]:
                self.state = "ITEM_MENU"
            elif event.key == pygame.K_DOWN:
                self.selected_party_index = (self.selected_party_index + 1) % len(self.player_party)
            elif event.key == pygame.K_UP:
                self.selected_party_index = (self.selected_party_index - 1) % len(self.player_party)
            elif event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                pk = self.player_party[self.selected_party_index]
                if self.pending_item.effect_type == "heal" and (pk.hp >= pk.max_hp or pk.hp <= 0):
                    self.message_queue.append("Impossible !")
                    self.advance_message()
                else:
                    self.resolve_turn("item", {"item": self.pending_item, "target": pk})


# =====================================================================
# MAIN
# =====================================================================

def main():
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Pokémon Gen 1 Battle System")
    clock = pygame.time.Clock()

    pikachu = Pokemon("Pikachu", 5, ["Electric"], 20, 11, 9, 11, 15, [
        Move("Thunder Shock", "Electric", 40, 100, 30),
        Move("Quick Attack", "Normal", 40, 100, 30)
    ])
    charmander = Pokemon("Charmander", 5, ["Fire"], 19, 11, 9, 11, 13, [
        Move("Ember", "Fire", 40, 100, 25)
    ])

    player_party = [pikachu, charmander]
    inventory = [
        Item("Potion", "Soin 20PV", "heal", 20, 3),
        Item("Poke Ball", "Capture", "capture", 100, 5)
    ]

    bulbasaur = Pokemon("Bulbasaur", 5, ["Grass", "Poison"], 21, 10, 10, 12, 10, [
        Move("Vine Whip", "Grass", 45, 100, 25),
        Move("Tackle", "Normal", 35, 95, 35)
    ])

    engine = BattleEngine(screen, player_party, bulbasaur, inventory)
    engine.advance_message()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(); sys.exit()
            engine.handle_event(event)
        engine.update(screen)
        pygame.display.flip()
        clock.tick(FPS)


if __name__ == "__main__":
    main()