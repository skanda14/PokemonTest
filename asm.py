import pygame
import random

# Configuration de l'écran Game Boy
GB_WIDTH, GB_HEIGHT = 160, 144
SCALE = 4  # Pour voir quelque chose sur nos écrans modernes


class BattleEngine:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((GB_WIDTH * SCALE, GB_HEIGHT * SCALE))
        self.clock = pygame.time.Clock()

        # Registres et Mémoire simulés
        self.h_scx = 0  # Scroll X
        self.h_scy = 0  # Scroll Y
        self.shadow_oam = [{"x": 160, "y": 0} for _ in range(40)]
        self.w_player_hp = 100
        self.w_enemy_hp = 100
        self.is_in_battle = 1  # 1: Sauvage, 2: Dresseur

    def slide_player_head_left(self):
        """Simulation de SlidePlayerHeadLeft (Déplacement des Sprites OAM)"""
        # En assembleur: dec [hl] x2 pour 21 entrées OAM
        for i in range(21):
            self.shadow_oam[i]["x"] -= 2

    def run_battle_logic(self):
        """Boucle principale basée sur MainInBattleLoop"""
        running = True
        while running:
            # Check HP (HandlePlayerMonFainted / HandleEnemyMonFainted)
            if self.w_player_hp <= 0:
                self.handle_player_black_out()
                break
            if self.w_enemy_hp <= 0:
                self.handle_enemy_mon_fainted()
                # En combat sauvage, la victoire arrête la boucle
                if self.is_in_battle == 1: break

            # Gestion des priorités (Quick Attack / Speed)
            # Cette partie simule la logique de décision du tour
            player_speed = 50
            enemy_speed = 45

            # Détermination de qui attaque en premier
            # Note: Le code original gère ici Quick Attack et Counter
            if player_speed >= enemy_speed:
                self.execute_turn("PLAYER")
            else:
                self.execute_turn("ENEMY")

            pygame.display.flip()
            self.clock.tick(60)

    def handle_poison_burn_leech_seed(self, target):
        """Simulation du bug Leech Seed / Toxic"""
        # Le code original multiplie les dégâts de Vampigraine
        # par le compteur Toxic si BADLY_POISONED est actif.
        damage = target.max_hp // 16
        if target.status == "BADLY_POISONED":
            target.toxic_counter += 1
            damage *= target.toxic_counter

        target.hp -= damage
        print(f"Residual damage: {damage}")

    def faint_enemy_pokemon(self):
        """Simulation de FaintEnemyPokemon"""
        # Simulation du bug mentionné dans l'ASM:
        # Seul le high byte de Bide est effacé (AccumulatedDamage % 256)
        # self.player_bide_damage &= 0x00FF

        print("Enemy fainted! Playing SFX_FAINT_FALL")
        self.play_sound("FAINT_THUD")

    def slide_silhouettes(self):
        """Animation initiale des silhouettes"""
        scx_offset = 0x90
        while scx_offset > 0:
            scx_offset -= 2
            self.h_scx = scx_offset
            self.slide_player_head_left()
            self.draw_frame()
            self.clock.tick(60)

    def draw_frame(self):
        """Rendu visuel simplifié"""
        self.screen.fill((255, 255, 255))  # Fond blanc (Game Boy)
        # Ici on dessinerait les surfaces Pygame pour le BG et les Sprites
        pygame.display.update()

    def play_sound(self, effect_name):
        print(f"Playing sound: {effect_name}")


# --- Point d'entrée ---
if __name__ == "__main__":
    game = BattleEngine()
    print("Start Battle: Initializing Silhouettes...")
    game.slide_silhouettes()
    print("Entering Main Battle Loop...")
    game.run_battle_logic()