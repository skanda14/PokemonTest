# import pygame
# import random
#
# # --- Constants mapping to ASM flags ---
# LINK_STATE_BATTLING = 1
# BATTLE_TYPE_NORMAL = 0
# BATTLE_TYPE_SAFARI = 1
#
#
# class Pokemon:
#     def __init__(self, species_name, max_hp, speed, attack, defense, moves):
#         self.species_name = species_name
#         self.max_hp = max_hp
#         self.current_hp = max_hp
#         self.speed = speed
#         self.attack = attack
#         self.defense = defense
#         self.moves = moves
#         self.status_conditions = []
#         self.is_fainted = False
#
#     def take_damage(self, amount):
#         self.current_hp -= amount
#         if self.current_hp <= 0:
#             self.current_hp = 0
#             self.is_fainted = True
#
#
# class BattleCore:
#     def __init__(self, screen_surface):
#         self.screen = screen_surface
#         self.player_mon = None
#         self.enemy_mon = None
#         self.battle_type = BATTLE_TYPE_NORMAL
#         self.is_trainer_battle = False
#
#         # Action states
#         self.player_selected_move = None
#         self.enemy_selected_move = None
#         self.escaped_from_battle = False
#
#     def slide_silhouettes_on_screen(self):
#         """
#         Translates: SlidePlayerAndEnemySilhouettesOnScreen
#         Handles the Pygame visual intro where silhouettes slide in.
#         """
#         self.screen.fill((255, 255, 255))  # Clear screen
#         # In a real Pygame app, you would load sprite images here
#         # and animate their X/Y coordinates in a loop with pygame.display.update()
#         print("Animating battle silhouettes...")
#         pygame.time.delay(1000)
#
#     def start_battle(self, player_team, enemy_team, is_trainer=False):
#         """
#         Translates: StartBattle
#         Initializes the battle variables and sends out the first Pokémon.
#         """
#         self.is_trainer_battle = is_trainer
#         self.slide_silhouettes_on_screen()
#
#         self.player_mon = self.get_first_alive_mon(player_team)
#         self.enemy_mon = self.get_first_alive_mon(enemy_team)
#
#         if not self.player_mon:
#             self.handle_player_black_out()
#             return
#
#         print(f"Go! {self.player_mon.species_name}!")
#         print(f"Enemy sent out {self.enemy_mon.species_name}!")
#
#         self.main_in_battle_loop()
#
#     def get_first_alive_mon(self, team):
#         for mon in team:
#             if not mon.is_fainted:
#                 return mon
#         return None
#
#     def main_in_battle_loop(self):
#         """
#         Translates: MainInBattleLoop
#         The core state machine of the Pokemon battle.
#         """
#         while not self.player_mon.is_fainted and not self.enemy_mon.is_fainted:
#             # 1. Player Turn Selection (Translates: DisplayBattleMenu)
#             player_action = self.display_battle_menu()
#             if player_action == "RUN":
#                 if self.try_running_from_battle():
#                     break
#                 else:
#                     self.player_selected_move = None  # Lost turn
#             else:
#                 self.player_selected_move = player_action
#
#             # 2. Enemy AI Turn Selection (Translates: SelectEnemyMove)
#             self.select_enemy_move()
#
#             # 3. Determine Speed & Execution Order (Translates: .compareSpeed)
#             player_goes_first = self.determine_turn_order()
#
#             if player_goes_first:
#                 self.execute_player_move()
#                 if self.escaped_from_battle or self.enemy_mon.is_fainted:
#                     break
#                 self.handle_residual_effects()  # Poison, Burn, Leech Seed
#
#                 if not self.player_mon.is_fainted:
#                     self.execute_enemy_move()
#                     self.handle_residual_effects()
#             else:
#                 self.execute_enemy_move()
#                 if self.escaped_from_battle or self.player_mon.is_fainted:
#                     break
#                 self.handle_residual_effects()
#
#                 if not self.enemy_mon.is_fainted:
#                     self.execute_player_move()
#                     self.handle_residual_effects()
#
#         # Handle faint outcomes
#         if self.player_mon.is_fainted:
#             self.handle_player_mon_fainted()
#         elif self.enemy_mon.is_fainted:
#             self.handle_enemy_mon_fainted()
#
#     def determine_turn_order(self):
#         """
#         Translates: .compareSpeed block inside MainInBattleLoop
#         Handles Quick Attack/Counter priority and speed ties.
#         """
#         # (Simplified priority logic for transcription clarity)
#         if self.player_selected_move == "QUICK_ATTACK" and self.enemy_selected_move != "QUICK_ATTACK":
#             return True
#         if self.enemy_selected_move == "QUICK_ATTACK" and self.player_selected_move != "QUICK_ATTACK":
#             return False
#
#         if self.player_mon.speed > self.enemy_mon.speed:
#             return True
#         elif self.player_mon.speed < self.enemy_mon.speed:
#             return False
#         else:
#             return random.choice([True, False])  # Speed tie (50/50)
#
#     def execute_player_move(self):
#         """Translates: ExecutePlayerMove"""
#         if not self.player_selected_move:
#             return
#
#         print(f"{self.player_mon.species_name} used {self.player_selected_move}!")
#         # Hook to CalculateDamage() logic here
#         damage = self.calculate_damage(self.player_mon, self.enemy_mon, 40)  # Placeholder 40 Base Power
#         self.enemy_mon.take_damage(damage)
#
#     def execute_enemy_move(self):
#         """Translates: ExecuteEnemyMove"""
#         if not self.enemy_selected_move:
#             return
#
#         print(f"Enemy {self.enemy_mon.species_name} used {self.enemy_selected_move}!")
#         damage = self.calculate_damage(self.enemy_mon, self.player_mon, 40)
#         self.player_mon.take_damage(damage)
#
#     def calculate_damage(self, attacker, defender, base_power):
#         """
#         Translates: CalculateDamage
#         Applies the classic Gen 1 damage formula.
#         """
#         level_calc = (2 * 50) / 5 + 2  # Assuming level 50 for simplicity
#         stat_ratio = attacker.attack / defender.defense
#         base_damage = ((level_calc * base_power * stat_ratio) / 50) + 2
#
#         # Add STAB, Weakness/Resistance, and Random variance here
#         variance = random.uniform(0.85, 1.0)
#         final_damage = int(base_damage * variance)
#         return max(1, final_damage)
#
#     def handle_residual_effects(self):
#         """Translates: HandlePoisonBurnLeechSeed"""
#         pass  # Handle HP drain here
#
#     def try_running_from_battle(self):
#         """Translates: TryRunningFromBattle"""
#         if self.is_trainer_battle:
#             print("No running from a trainer battle!")
#             return False
#
#         # Simplified escape formula
#         escape_odds = (self.player_mon.speed * 32) / (self.enemy_mon.speed / 4 % 256)
#         if escape_odds > 255 or random.randint(0, 255) < escape_odds:
#             print("Got away safely!")
#             self.escaped_from_battle = True
#             return True
#         else:
#             print("Can't escape!")
#             return False
#
#     def display_battle_menu(self):
#         # Stub for rendering Pygame UI and waiting for event loops
#         return "TACKLE"  # Mocking a user input
#
#     def select_enemy_move(self):
#         # Translates TrainerAI or Random Wild Move
#         self.enemy_selected_move = random.choice(self.enemy_mon.moves)
#
#     def handle_player_black_out(self):
#         print("Player is out of usable Pokémon! Player blacked out!")
#
#     def handle_enemy_mon_fainted(self):
#         print("Enemy fainted! You win!")
#
#     def handle_player_mon_fainted(self):
#         print("Your Pokémon fainted!")
#         # Logic to swap to next Pokémon would go here
#
#
#
#
# screen = pygame.display.set_mode((800, 600))
# BattleCore(screen).start_battle(None, None, None)

import random
import math


class Pokemon:
    def __init__(self, name, types, stats, level, moves):
        self.name = name
        self.types = types
        self.level = level
        self.base_stats = stats  # [HP, ATK, DEF, SPD, SPC]
        self.moves = moves

        # Calcul des stats réelles (approximation sans IV/EV pour l'exemple)
        self.max_hp = self._calc_stat(stats[0], level, is_hp=True)
        self.current_hp = self.max_hp
        self.attack = self._calc_stat(stats[1], level)
        self.defense = self._calc_stat(stats[2], level)
        self.speed = self._calc_stat(stats[3], level)
        self.special = self._calc_stat(stats[4], level)

    def _calc_stat(self, base, level, is_hp=False):
        if is_hp:
            return math.floor((base * 2 * level) / 100) + level + 10
        return math.floor((base * 2 * level) / 100) + 5


def calculate_damage(attacker, defender, move, is_critical=False):
    """
    Reproduit la formule de dégâts de la Gen 1.
    Réf: engine/battle/core.asm (DamageCalc)
    """
    # Dans la Gen 1, le critique dépend de la vitesse de base / 512
    level = attacker.level * (2 if is_critical else 1)

    # Choix entre Attaque/Défense ou Spécial/Spécial (Gen 1 n'avait qu'une stat Spécial)
    if move['category'] == 'Physical':
        atk = attacker.attack
        dfn = defender.defense
    else:
        atk = attacker.special
        dfn = defender.special

    # Formule de base
    damage = math.floor(math.floor(math.floor(2 * level / 5 + 2) * move['power'] * atk / dfn) / 50) + 2

    # Multiplicateurs (STAB, Type)
    if move['type'] in attacker.types:
        damage = math.floor(damage * 1.5)

    # Le facteur aléatoire (entre 217 et 255) / 255
    random_factor = random.randint(217, 255)
    damage = math.floor(damage * random_factor / 255)

    return max(1, damage)


import pygame
import sys

# Configuration Pygame
WIDTH, HEIGHT = 480, 400
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
font = pygame.font.SysFont("monospace", 24)


def draw_battle_scene(player, enemy, message=""):
    screen.fill(WHITE)

    # Dessiner les rectangles de combat (simplifiés)
    pygame.draw.rect(screen, BLACK, (50, 50, 150, 100), 2)  # Cadre Ennemi
    pygame.draw.rect(screen, BLACK, (280, 200, 150, 100), 2)  # Cadre Joueur

    # Stats
    enemy_txt = font.render(f"{enemy.name} L{enemy.level}", True, BLACK)
    player_txt = font.render(f"{player.name} L{player.level}", True, BLACK)
    screen.blit(enemy_txt, (60, 60))
    screen.blit(player_txt, (290, 210))

    # Barres de vie (HP)
    pygame.draw.rect(screen, (0, 255, 0), (60, 90, (enemy.current_hp / enemy.max_hp) * 100, 10))
    pygame.draw.rect(screen, (0, 255, 0), (290, 240, (player.current_hp / player.max_hp) * 100, 10))

    # Zone de texte
    pygame.draw.rect(screen, BLACK, (0, 300, WIDTH, 100), 3)
    msg_txt = font.render(message, True, BLACK)
    screen.blit(msg_txt, (20, 320))

    pygame.display.flip()


def main():
    # Initialisation data (Stats basées sur les fichiers .asm)
    # Pikachu: types=[ELECTRIC], stats=[35, 55, 30, 90, 50]
    player = Pokemon("PIKACHU", ["Electric"], [35, 55, 30, 90, 50], 5, [])
    # Salameche: stats=[39, 52, 43, 65, 50]
    enemy = Pokemon("CHARMANDER", ["Fire"], [39, 52, 43, 65, 50], 5, [])

    move_charge = {'name': 'CHARGE', 'power': 40, 'type': 'Normal', 'category': 'Physical'}

    message = "Un SALAMECHE sauvage!"

    while True:
        draw_battle_scene(player, enemy, message)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit();
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:  # Simuler une attaque
                    dmg = calculate_damage(player, enemy, move_charge)
                    enemy.current_hp = max(0, enemy.current_hp - dmg)
                    message = f"PIKACHU utilise CHARGE! -{dmg}"


if __name__ == "__main__":
    main()