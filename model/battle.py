import random
from dataclasses import dataclass
from model.action import Action
from model.battle_fun import who_has_highest_calculated_speed, who_has_highest_action_type_priority, who_has_highest_move_priority

@dataclass
class ChosenActions:
    player: tuple | None = None
    opponent: tuple | None = None

# Petite classe utilitaire pour générer des événements lisibles par le Controller
class BattleEvent:
    def __init__(self, event_type, **kwargs):
        self.type = event_type
        for key, value in kwargs.items():
            setattr(self, key, value)


class Battle:
    # Constantes pour les types d'actions
    ACTION_FIGHT = "FIGHT"
    ACTION_SWITCH = "SWITCH"
    ACTION_ITEM = "ITEM"
    ACTION_RUN = "RUN"
    # Constantes pour les phases du tour (Machine à états)
    PHASE_IDLE = "IDLE"
    PHASE_FIRST_ACTION = "FIRST_ACTION"
    PHASE_SECOND_ACTION = "SECOND_ACTION"
    PHASE_END_TURN = "END_TURN"
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
        self.chosen_actions = ChosenActions()

        # Variables pour le Ping-Pong
        self.current_phase = self.PHASE_IDLE
        self.first_action = None
        self.second_action = None
        self.step_queue = []  # Mini-file d'attente pour la phase en cours


    def add_player_action(self, action_data):
        if action_data:
            action_type, action, target = action_data
        else:
            action_type, action, target = None,None,None
        actor = self.active_player_pokemon
        self.add_action('player', action_type, action, actor, target)

    def add_opponent_action(self, action_data):
        if action_data:
            action_type, action, target = action_data
        else:
            action_type, action, target = None,None,None
        actor = self.active_opponent_pokemon
        self.add_action('opponent', action_type, action, actor, target)

    def add_opponent_random_move(self):
        moves = [self.active_opponent_pokemon.moves[key] for key in self.active_opponent_pokemon.moves if self.active_opponent_pokemon.moves[key]]
        move = random.choice(moves)
        new_data = ('FIGHT', move, None)
        print(f'{move.name} chosen by opponent!')
        self.add_opponent_action(new_data)

    def add_action(self, trainer, action_type, action, actor, target=None):
        new_action = Action(trainer, action_type, action, actor, target)
        if new_action.type == self.ACTION_FIGHT:
            if new_action.trainer == 'player':
                new_action.target = self.active_opponent_pokemon
            else:
                new_action.target = self.active_player_pokemon
        elif new_action.type == self.ACTION_SWITCH:
            if new_action.trainer == 'player':
                new_action.actor = self.active_player_pokemon
            else:
                new_action.actor = self.active_opponent_pokemon

        setattr(self.chosen_actions, trainer, new_action)

    def log_event(self, event_type, **kwargs):
        """Ajoute un événement que le Controller lira plus tard pour l'affichage."""
        event = {"type": event_type}
        event.update(kwargs)
        self.event_queue.append(event)

    # def execute_turn(self):
    #     """
    #     Résout un tour complet instantanément et remplit la file d'événements.
    #     player_action et enemy_action sont des dictionnaires, ex:
    #     {"type": ACTION_FIGHT, "move": "Thunderbolt"}
    #     """
    #     player_action, enemy_action = self.chosen_actions.player, self.chosen_actions.opponent
    #     self.turn_number += 1
    #     self.event_queue.clear()  # On vide les événements du tour précédent
    #
    #     # 1. Déterminer l'ordre de passage
    #     first_actor, first_action, second_actor, second_action = \
    #         self._determine_turn_order(player_action, enemy_action)
    #
    #     # 2. Le premier attaque
    #     self._process_action(first_actor, first_action, second_actor)
    #
    #     # 3. Vérifier si le combat continue avant de lancer la 2ème action
    #     if self._check_faint():
    #         return self.event_queue
    #
    #     # 4. Le second attaque
    #     self._process_action(second_actor, second_action, first_actor)
    #     self._check_faint()
    #
    #     # 5. Dégâts de fin de tour (Poison, Brûlure)
    #     if not self.is_over:
    #         self._apply_end_of_turn_effects()
    #
    #     return self.event_queue

    def prepare_turn(self):
        """
        Remplace execute_turn.
        Prépare l'ordre de passage, mais ne joue aucune action.
        """
        self.turn_number += 1
        self.add_opponent_random_move()

        # 1. Déterminer l'ordre de passage
        self.first_action, self.second_action = self._determine_turn_order(self.chosen_actions.player, self.chosen_actions.opponent)

        # 2. On initialise la machine à états sur la première action
        self.current_phase = self.PHASE_FIRST_ACTION
        self.step_queue = []

    def _determine_turn_order(self, p_action, e_action):
        """Détermine qui agit en premier (simplifié: basé sur la vitesse)."""
        # (Dans la vraie Gen 1, l'utilisation d'objet ou le switch est prioritaire)
        if not p_action.type:
            return e_action, p_action
        if not e_action.type:
            return p_action, e_action

        result = who_has_highest_action_type_priority(p_action, e_action, self.ACTION_RUN, self.ACTION_SWITCH, self.ACTION_ITEM)
        if result:
            return result

        result = who_has_highest_move_priority(p_action, e_action)
        if result:
            return result

        result = who_has_highest_calculated_speed(p_action, e_action)
        if result:
            return result

        # Speed tie (égalité) : aléatoire
        if random.choice([True, False]):
            return p_action, e_action
        else:
            return e_action, p_action

    def get_next_step(self):
        """
        C'est le PING du Controller. Renvoie l'événement suivant à afficher.
        """
        # 1. S'il reste des sous-événements dans la phase en cours, on les dépile un par un
        if len(self.step_queue) > 0:
            return self.step_queue.pop(0)

        # 2. Si la mini-file est vide, on calcule la phase suivante
        if self.current_phase == self.PHASE_FIRST_ACTION:
            self._execute_phase_action(self.first_action)
            self.current_phase = self.PHASE_SECOND_ACTION
            return self.get_next_step()  # Appel récursif pour envoyer le premier event généré

        elif self.current_phase == self.PHASE_SECOND_ACTION:
            # MAGIE DU PING PONG : Si le Pokémon est mort pendant l'action 1, son action est annulée !
            if self._can_execute_action(self.second_action):
                self._execute_phase_action(self.second_action)
            self.current_phase = self.PHASE_END_TURN
            return self.get_next_step()

        elif self.current_phase == self.PHASE_END_TURN:
            self._apply_end_of_turn_effects()
            self.current_phase = self.PHASE_IDLE
            return self.get_next_step()

        elif self.current_phase == self.PHASE_IDLE:
            # Plus de phases, plus d'événements : le tour est terminé
            return None

    def _execute_phase_action(self, action):
        """Calcule une action et remplit la mini-file (step_queue)."""
        if not action or not action.type:
            return

        # 1. On renvoie l'action originale pour l'affichage (ex: "Pikachu utilise Éclair")
        # self.step_queue.append(action)

        if action.type == self.ACTION_FIGHT:
            move = action.detail
            target_pokemon = action.target

            # 1. Le texte : "Pikachu utilise Éclair"
            self.step_queue.append(BattleEvent("FIGHT", actor=action.actor, detail=move, target=target_pokemon))

            # 2. NOUVEAU : L'animation visuelle
            target_side = "opponent" if action.actor == self.active_player_pokemon else "player"
            # On passe le nom du move en minuscules pour chercher l'animation correspondante
            self.step_queue.append(BattleEvent("ANIMATION", name='tackle', target=target_side)) #name=move.name.lower()

            # --- Calcul des dégâts ---
            damage = 10  # Simplifié

            target_pokemon.stats['hp'] = max(0, target_pokemon.stats['hp']-damage)
            # 2. On crée un événement pour l'animation/la barre de vie
            self.step_queue.append(
                BattleEvent("DAMAGE", target=target_pokemon, amount=damage, new_hp=target_pokemon.stats['hp']))

            # 3. On vérifie si cela a causé un K.O.
            self._check_faint()

        elif action.type == self.ACTION_SWITCH:
            # Logique de changement (Mettre à jour active_player_pokemon, etc.)
            pass
    #
    # def _process_action(self, action):
    #     if action.trainer == "player":
    #         target = self.active_opponent_pokemon
    #     else:
    #         target = self.active_player_pokemon
    #
    #     """Exécute l'action choisie."""
    #     actor_name = self.active_player_pokemon.name if actor == self.player else self.active_opponent_pokemon.name
    #
    #     if action["type"] == self.ACTION_FIGHT:
    #         move = action["move"]
    #         self.log_event("MESSAGE", text=f"{actor_name} used {move}!")
    #
    #         # Formule de dégâts très simplifiée pour l'exemple
    #         damage = 10
    #         target_pokemon = self.active_opponent_pokemon if actor == self.player else self.active_player_pokemon
    #
    #         target_pokemon.hp -= damage
    #         if target_pokemon.hp < 0:
    #             target_pokemon.hp = 0
    #
    #         self.log_event("DAMAGE", target="player" if actor == self.opponent else "opponent", amount=damage,
    #                        new_hp=target_pokemon.hp)
    #
    #     elif action["type"] == self.ACTION_SWITCH:
    #         # Logique de changement de Pokémon
    #         pass

    def _check_faint(self):
        """Vérifie si un Pokémon est K.O. et ajoute l'événement à la file."""
        if self.active_opponent_pokemon.stats['hp'] <= 0:
            self.step_queue.append(BattleEvent("FAINT", target=self.active_opponent_pokemon))

            if self.opponent.party.is_all_fainted():  # Ajuste "party" selon ta structure
                self.is_over = True
                self.winner = "PLAYER"
                self.step_queue.append(BattleEvent("BATTLE_END", winner="PLAYER"))

        if self.active_player_pokemon.stats['hp'] <= 0:
            self.step_queue.append(BattleEvent("FAINT", target=self.active_player_pokemon))

            if self.player.party.is_all_fainted():
                self.is_over = True
                self.winner = "OPPONENT"
                self.step_queue.append(BattleEvent("BATTLE_END", winner="OPPONENT"))

    def _can_execute_action(self, action):
        """Vérifie si l'acteur est toujours en état d'agir (pas mort, pas endormi, etc.)."""
        if not action or not action.actor:
            return False
        if action.actor.stats['hp'] <= 0:
            return False
        # Tu pourras ajouter plus tard : if action.actor.status == "SLEEP", etc.
        return True

    def _apply_end_of_turn_effects(self):
        """Gère les statuts comme le poison."""
        pass