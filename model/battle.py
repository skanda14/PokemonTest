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
    PHASE_INTRO = "INTRO"
    PHASE_IDLE = "IDLE"
    PHASE_FIRST_ACTION = "FIRST_ACTION"
    PHASE_SECOND_ACTION = "SECOND_ACTION"
    PHASE_END_TURN = "END_TURN"
    def __init__(self, player, opponent, is_wild_encounter=True):
        self.player = player
        self.opponent = opponent
        self.is_wild_encounter = is_wild_encounter

        # Références aux Pokémon actuellement sur le terrain
        self.active_player_pokemon = None
        self.active_opponent_pokemon = None

        # État du combat
        self.turn_number = 0
        self.is_over = False
        self.winner = None  # Peut être "PLAYER", "OPPONENT", ou "DRAW"
        self.escape_attempts = 0
        self.chosen_actions = ChosenActions()

        # Variables pour le Ping-Pong
        self.current_phase = self.PHASE_INTRO
        self.first_action = None
        self.second_action = None
        self.step_queue = []  # Mini-file d'attente pour la phase en cours
        self._build_intro()

    def _build_intro(self):
        """Prépare les événements d'introduction du combat."""
        self.step_queue.append(
            BattleEvent("MESSAGE", text=f"Début du combat!"))

        # if self.is_wild_encounter:
        #     self._build_wild_encounter_intro()
        # else:
        #     self._build_trainer_battle_intro()
        self._temp_build_intro()

    def _temp_build_intro(self):
        """Prépare les événements d'introduction du combat."""
        # 1. Apparition de l'adversaire
        trainer_side = "opponent"
        new_pokemon = self.opponent.party.get_first_member()

        self.step_queue.append(BattleEvent("ANIMATION", name='tackle', target=trainer_side)) # name='send_out'
        self.step_queue.append(BattleEvent("SWITCH_SPRITE", side=trainer_side, new_pokemon=new_pokemon))
        self.step_queue.append(BattleEvent("SWITCH_IN", trainer=trainer_side, pokemon=new_pokemon, wild_encounter=self.is_wild_encounter))
        self.active_opponent_pokemon = new_pokemon
        # 2. Envoi du Pokémon du joueur
        trainer_side = "player"
        new_pokemon = self.player.party.get_first_member()
        self.step_queue.append(BattleEvent("SWITCH_IN", trainer=trainer_side, pokemon=new_pokemon))
        self.step_queue.append(BattleEvent("ANIMATION", name='tackle', target=trainer_side)) # name='send_out'
        self.step_queue.append(BattleEvent("SWITCH_SPRITE", side=trainer_side, new_pokemon=new_pokemon))
        self.active_player_pokemon = new_pokemon

    def _build_trainer_battle_intro(self):
        # animation apparition des 2 trainers
        # affichage des sprites fixe des trainers
        # affichage Hud pokeballs des trainers
        # affichage message "TRAINER veut se battre!"
        # arrêt affichage hud pokeballs des trainers
        # arrêt affichage sprite fixe du opponent trainer
        # animation disparition opponent trainer
        # message "TRAINER fait appel à... EVOLI!"
        # animation apparition pokemon adverse
        # affichage du sprite fixe du pokemon adverse
        # affichage hud opponent pokemon stats
        # arrêt affichage player trainer sprite
        # animation disparition player trainer
        # message "En avant! PIKACHU!"
        # affichage hud player pokemon stats
        # animation apparition du player trainer pokemon
        # affichage sprite fixe player trainer pokemon
        pass

    def _build_wild_encounter_intro(self):
        # animation apparition wild pokemon et apparition player trainer
        # affichage sprite fixe wild pokemon et sprite fixe player trainer
        # affichage hud player pokeball
        # message "Un RATTATA sauvage apparaît!"
        # arrêt affichage hud player pokeball
        # affichage hud wild pokemon stats
        # arrêt affichage du sprite du player trainer
        # animation disparition player trainer
        # message "En avant! PIKACHU!"
        # affichage hud player pokemon stats
        # animation apparition player pokemon
        # apparition sprite fixe player pokemon
        pass

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

    # def log_event(self, event_type, **kwargs):
    #     """Ajoute un événement que le Controller lira plus tard pour l'affichage."""
    #     event = {"type": event_type}
    #     event.update(kwargs)
    #     self.event_queue.append(event)

    def prepare_turn(self):
        """Prépare l'ordre de passage, mais ne joue aucune action."""
        self.add_opponent_random_move()
        self.turn_number += 1
        print(f'Turn number: {self.turn_number}')

        # 1. Déterminer l'ordre de passage
        self.first_action, self.second_action = self._determine_turn_order(self.chosen_actions.player, self.chosen_actions.opponent)

        # 2. On initialise la machine à états sur la première action
        self.current_phase = self.PHASE_FIRST_ACTION
        self.step_queue = []

    def _determine_turn_order(self, p_action, e_action):
        """Détermine qui agit en premier"""
        if not p_action.type:
            return e_action, p_action
        if not e_action.type:
            return p_action, e_action

        # Détermine la priorité parmi le type d'action: Run > Switch > Item > Fight
        result = who_has_highest_action_type_priority(p_action, e_action, self.ACTION_RUN, self.ACTION_SWITCH, self.ACTION_ITEM)
        if result:
            return result

        # Sinon détermine la priorité en fonction du move (Fight)
        result = who_has_highest_move_priority(p_action, e_action)
        if result:
            return result

        # Sinon détermine la priorité en fonction de la vitesse
        result = who_has_highest_calculated_speed(p_action, e_action)
        if result:
            return result

        # Sinon Speed tie (égalité) : aléatoire
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

        # Si une action précédente (Fuite ou K.O. du dernier Pokémon)
        # a mis fin au combat, on annule toutes les phases suivantes !
        if self.is_over:
            self.current_phase = self.PHASE_IDLE
            return None

        # 2. Si la mini-file est vide, on calcule la phase suivante
        if self.current_phase == self.PHASE_INTRO:
            self.current_phase = self.PHASE_IDLE
            return None  # Renvoie None pour dire au Controller que l'action (l'intro) est finie
        elif self.current_phase == self.PHASE_FIRST_ACTION:
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
        if action.type == self.ACTION_FIGHT:
            self._execute_fight_action(action)
        elif action.type == self.ACTION_ITEM:
            self._execute_item_action(action)
        elif action.type == self.ACTION_SWITCH:
            self._execute_switch_action(action)
        elif action.type == self.ACTION_RUN:
            self._execute_run_action(action)

    def _execute_run_action(self, action):
        if action.trainer == "player":
            # Simplification : 100% de réussite contre les Pokémon sauvages
            if self.is_wild_encounter:
                self.step_queue.append(BattleEvent("RUN", success=True))
                self.is_over = True
                self.winner = "ESCAPE"
                self.step_queue.append(BattleEvent("BATTLE_END", winner="ESCAPE"))
            else:
                self.step_queue.append(BattleEvent("RUN", success=False))

    def _execute_fight_action(self, action):
        move = action.detail
        target_pokemon = action.target
        if action.trainer == "player":
            current_actor = self.active_player_pokemon
            current_target = self.active_opponent_pokemon
        else:
            current_actor = self.active_opponent_pokemon
            current_target = self.active_player_pokemon
        # 1. Le texte : "Pikachu utilise Éclair"
        self.step_queue.append(BattleEvent("FIGHT", actor=current_actor, detail=move, target=current_target))
        # 2. L'animation visuelle
        target_side = "opponent" if action.actor == self.active_player_pokemon else "player"
        # On passe le nom du move en minuscules pour chercher l'animation correspondante
        self.step_queue.append(BattleEvent("ANIMATION", name='tackle', target=target_side))  # name=move.name.lower()
        damage = 10  # Calcul des dégâts simplifié
        current_target.stats['hp'] = max(0, current_target.stats['hp'] - damage)
        # 3. On crée un événement pour l'animation/la barre de vie
        self.step_queue.append(
            BattleEvent("DAMAGE", target=current_target, amount=damage, new_hp=current_target.stats['hp']))
        # 4. On vérifie si cela a causé un K.O.
        self._check_faint()

        # 5. (Optionnel) Consommer un PP du move
        move.modify_current_pp()

    def _execute_item_action(self, action):
        inventory_slot = action.detail
        target_pokemon = action.target

        # 1. Le texte : "Player utilise Potion sur Pikachu!"
        self.step_queue.append(
            BattleEvent("ITEM", trainer=action.trainer, detail=inventory_slot, target=target_pokemon))

        # 2. L'animation visuelle (ex: des petites étincelles de soin)
        target_side = "player" if target_pokemon in self.player.party.members else "opponent"
        self.step_queue.append(BattleEvent("ANIMATION", name='tackle', target=target_side))  # name='potion'

        # 3. Logique de l'objet (Soin simplifié pour l'exemple)
        heal_amount = 20
        # Idéalement, ton objet devrait avoir une méthode item.apply(target_pokemon)
        # On s'assure de ne pas dépasser les HP maximums (à adapter selon ta structure)
        max_hp = target_pokemon.stats.get('max_hp', 100)
        target_pokemon.stats['hp'] = min(max_hp, target_pokemon.stats['hp'] + heal_amount)

        # 4. On crée un événement pour faire remonter la barre de vie
        # On utilise un nouveau type d'événement "HEAL" pour être sémantiquement clair
        self.step_queue.append(
            BattleEvent("HEAL", target=target_pokemon, amount=heal_amount, new_hp=target_pokemon.stats['hp']))

        # 5. (Optionnel) Consommer l'objet du sac
        inventory_slot.modify_quantity(-1)
        # self.player.bag.remove_item(item)

    def _execute_switch_action(self, action):
        actor_pokemon = action.actor
        new_pokemon = action.target
        trainer_side = "player" if action.trainer == 'player' else "opponent"

        # 1. Événement logique de retrait
        self.step_queue.append(BattleEvent("SWITCH_OUT", trainer=action.trainer, pokemon=actor_pokemon, wild_encounter=self.is_wild_encounter))
        # 2. Animation de retrait
        self.step_queue.append(BattleEvent("ANIMATION", name='tackle', target=trainer_side)) # name='withdraw'
        # 3. Logique : Changement du Pokémon actif dans le Model
        if trainer_side == "player":
            self.active_player_pokemon = new_pokemon
        else:
            self.active_opponent_pokemon = new_pokemon

        # 4. Événement logique d'entrée
        self.step_queue.append(BattleEvent("SWITCH_IN", trainer=action.trainer, pokemon=new_pokemon, wild_encounter=self.is_wild_encounter))
        # 5. Animation d'envoi
        self.step_queue.append(BattleEvent("ANIMATION", name='tackle', target=trainer_side)) # name='send_out'
        # 6. Événement pour la vue : changer le sprite et le HUD
        self.step_queue.append(BattleEvent("SWITCH_SPRITE", side=trainer_side, new_pokemon=new_pokemon))



    def _check_faint(self):
        """Vérifie si un Pokémon est K.O. et ajoute l'événement à la file."""
        if self.active_opponent_pokemon.stats['hp'] <= 0:
            self.step_queue.append(BattleEvent("FAINT", target=self.active_opponent_pokemon))

            if self.opponent.party.is_all_fainted():  # Ajuste "party" selon ta structure
                self.is_over = True
                self.winner = "PLAYER"
                self.step_queue.append(BattleEvent("BATTLE_END", winner="PLAYER"))
            else:
                self.step_queue.append(BattleEvent("FORCE_SWITCH", trainer="opponent"))

        if self.active_player_pokemon.stats['hp'] <= 0:
            self.step_queue.append(BattleEvent("FAINT", target=self.active_player_pokemon))

            if self.player.party.is_all_fainted():
                self.is_over = True
                self.winner = "OPPONENT"
                self.step_queue.append(BattleEvent("BATTLE_END", winner="OPPONENT"))
            else:
                self.step_queue.append(BattleEvent("FORCE_SWITCH", trainer="player"))

    def execute_forced_switch(self, trainer, new_pokemon):
        """Résout un changement de Pokémon forcé au milieu d'un tour."""
        trainer_side = "player" if trainer == "player" else "opponent"

        # 1. Mise à jour de la logique
        if trainer == "player":
            self.active_player_pokemon = new_pokemon
        else:
            self.active_opponent_pokemon = new_pokemon

        # 2. On crée les événements visuels du remplacement
        switch_events = [
            BattleEvent("SWITCH_SPRITE", side=trainer_side, new_pokemon=new_pokemon),
            BattleEvent("SWITCH_IN", trainer=trainer_side, pokemon=new_pokemon,
                        wild_encounter=self.is_wild_encounter if trainer_side == "opponent" else False),
            BattleEvent("ANIMATION", name='tackle', target=trainer_side)  # name='send_out'
        ]

        # 3. MAGIE : On insère ces événements TOUT AU DÉBUT de la file d'attente en cours
        self.step_queue = switch_events # + self.step_queue

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
