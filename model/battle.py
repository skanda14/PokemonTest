import random


class Battle:
    # Constantes pour les types d'actions
    ACTION_FIGHT = "FIGHT"
    ACTION_SWITCH = "SWITCH"
    ACTION_ITEM = "ITEM"
    ACTION_RUN = "RUN"

    def __init__(self, player, opponent, is_wild_encounter=False):
        self.player = player
        self.opponent = opponent
        self.is_wild_encounter = is_wild_encounter

        # Références aux Pokémon actuellement sur le terrain
        self.active_player_pokemon = self.player.party.get_first_member()
        self.active_opponent_pokemon = self.opponent.party.get_first_member()

        # État du combat
        self.turn_number = 0
        self.is_over = False
        self.winner = None  # Peut être "PLAYER", "OPPONENT", ou "DRAW"
        self.escape_attempts = 0

        # La file d'événements pour communiquer avec le Controller
        self.event_queue = []

    def log_event(self, event_type, **kwargs):
        """Ajoute un événement que le Controller lira plus tard pour l'affichage."""
        event = {"type": event_type}
        event.update(kwargs)
        self.event_queue.append(event)

    def execute_turn(self, player_action, enemy_action):
        """
        Résout un tour complet instantanément et remplit la file d'événements.
        player_action et enemy_action sont des dictionnaires, ex:
        {"type": ACTION_FIGHT, "move": "Thunderbolt"}
        """
        self.turn_number += 1
        self.event_queue.clear()  # On vide les événements du tour précédent

        # 1. Déterminer l'ordre de passage
        first_actor, first_action, second_actor, second_action = \
            self._determine_turn_order(player_action, enemy_action)

        # 2. Le premier attaque
        self._process_action(first_actor, first_action, second_actor)

        # 3. Vérifier si le combat continue avant de lancer la 2ème action
        if self._check_faint():
            return self.event_queue

        # 4. Le second attaque
        self._process_action(second_actor, second_action, first_actor)
        self._check_faint()

        # 5. Dégâts de fin de tour (Poison, Brûlure)
        if not self.is_over:
            self._apply_end_of_turn_effects()

        return self.event_queue

    def _determine_turn_order(self, p_action, e_action):
        """Détermine qui agit en premier (simplifié: basé sur la vitesse)."""
        # (Dans la vraie Gen 1, l'utilisation d'objet ou le switch est prioritaire)
        if p_action["type"] in [self.ACTION_SWITCH, self.ACTION_ITEM, self.ACTION_RUN]:
            return self.player, p_action, self.opponent, e_action

        p_speed = self.active_player_pokemon.stats["speed"]
        e_speed = self.active_opponent_pokemon.stats["speed"]

        if p_speed > e_speed:
            return self.player, p_action, self.opponent, e_action
        elif e_speed > p_speed:
            return self.opponent, e_action, self.player, p_action
        else:
            # Speed tie (égalité) : aléatoire
            if random.choice([True, False]):
                return self.player, p_action, self.opponent, e_action
            else:
                return self.opponent, e_action, self.player, p_action

    def _process_action(self, actor, action, target_actor):
        """Exécute l'action choisie."""
        actor_name = self.active_player_pokemon.name if actor == self.player else self.active_opponent_pokemon.name

        if action["type"] == self.ACTION_FIGHT:
            move = action["move"]
            self.log_event("MESSAGE", text=f"{actor_name} used {move}!")

            # Formule de dégâts très simplifiée pour l'exemple
            damage = 10
            target_pokemon = self.active_opponent_pokemon if actor == self.player else self.active_player_pokemon

            target_pokemon.hp -= damage
            if target_pokemon.hp < 0:
                target_pokemon.hp = 0

            self.log_event("DAMAGE", target="player" if actor == self.opponent else "opponent", amount=damage,
                           new_hp=target_pokemon.hp)

        elif action["type"] == self.ACTION_SWITCH:
            # Logique de changement de Pokémon
            pass

    def _check_faint(self):
        """Vérifie si un Pokémon est K.O. et met à jour l'état du combat."""
        if self.active_opponent_pokemon.hp <= 0:
            self.log_event("MESSAGE", text=f"Enemy {self.active_opponent_pokemon.name} fainted!")
            self.log_event("FAINT", target="opponent")

            if self.opponent.team.is_all_fainted():
                self.is_over = True
                self.winner = "PLAYER"
                self.log_event("BATTLE_END", winner="PLAYER")
            return True

        if self.active_player_pokemon.hp <= 0:
            self.log_event("MESSAGE", text=f"{self.active_player_pokemon.name} fainted!")
            self.log_event("FAINT", target="player")

            if self.player.team.is_all_fainted():
                self.is_over = True
                self.winner = "OPPONENT"
                self.log_event("BATTLE_END", winner="OPPONENT")
            return True

        return False

    def _apply_end_of_turn_effects(self):
        """Gère les statuts comme le poison."""
        pass