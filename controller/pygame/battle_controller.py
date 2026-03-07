import pygame
from controller.pygame.main_menu_controller import MainMenuController
from controller.pygame.fight_menu_controller import FightMenuController
from controller.pygame.switch_menu_controller import SwitchMenuController
from controller.pygame.switch_sub_menu_controller import SwitchSubMenuController
from controller.pygame.item_menu_controller import ItemMenuController
from controller.pygame.item_target_selection_menu_controller import ItemTargetMenuController
from controller.pygame.stats_menu_controller import StatsMenuController
from controller.pygame.message_box_controller import MessageBoxController

# Les différents états du contrôleur
STATE_BATTLE_INTRODUCTION = "STATE_BATTLE_INTRODUCTION"
STATE_WAITING_FOR_INPUT = "WAITING_FOR_INPUT"
STATE_RESOLVING_TURN = "STATE_RESOLVING_TURN"
STATE_BATTLE_OVER = "BATTLE_OVER"
STATE_FORCED_SWITCH = "STATE_FORCED_SWITCH"


class BattleController:
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.state = STATE_BATTLE_INTRODUCTION
        self.main_menu = MainMenuController(model=self.model, view=self.view, go_message_box=self.open_message_box, on_fight_chosen=self.open_fight_menu, on_switch_chosen=self.open_switch_menu, on_item_chosen=self.open_item_menu, on_run_chosen=self.run_chosen)

        self.fight_menu = FightMenuController(model=self.model, view=self.view, go_message_box=self.open_message_box, move_chosen=self.move_chosen, cancel_chosen=self.cancel_chosen)

        self.switch_menu = SwitchMenuController(model=self.model, view=self.view, go_message_box=self.open_message_box, pokemon_chosen=self.open_switch_sub_menu, cancel_chosen=self.cancel_chosen)
        self.switch_sub_menu = SwitchSubMenuController(model=self.model, view=self.view, go_message_box=self.open_message_box, item_chosen=self.switch_pokemon_chosen, stats_chosen=self.stats_chosen, cancel_chosen=self.cancel_chosen)
        self.stats_menu = StatsMenuController(model=self.model, view=self.view, id=1, go_message_box=self.open_message_box, go_next=self.open_stats_2_menu)
        self.stats_2_menu = StatsMenuController(model=self.model, view=self.view, id=2, go_message_box=self.open_message_box, go_next=self.cancel_chosen)

        self.item_menu = ItemMenuController(model=self.model, view=self.view, go_message_box=self.open_message_box, item_chosen=self.item_chosen, cancel_chosen=self.cancel_chosen)
        self.item_target_selection_menu = ItemTargetMenuController(model=self.model, view=self.view, go_message_box=self.open_message_box, pokemon_chosen=self.item_target_chosen, cancel_chosen=self.cancel_chosen)

        self.message_box = MessageBoxController(model=self.model, view=self.view, back=self.cancel_chosen)

        self.current_menu = None
        self.previous_menus = []


        # Copie de la file d'événements générée par le modèle
        self.event_queue = []
        self.current_event = None

    # -----------------------------------------------------------------
    # --- Les Callbacks de navigation ---
    # -----------------------------------------------------------------

    def cancel_chosen(self, item=None):
        if self.current_menu == self.switch_menu and self.state == STATE_FORCED_SWITCH:
            print("Vous devez choisir un Pokémon !")
            return

        self.current_menu.hide()
        self.current_menu = None
        if self.previous_menus:
            self.current_menu = self.previous_menus[-1]
            self.previous_menus = self.previous_menus[:-1]
            self.current_menu.show()
            print(f'Back to {self.current_menu}')

    def run_chosen(self):
        new_action_data = ('RUN', None, None)
        print("Run chosen!")
        self.end_player_choice_phase(new_action_data)

    def move_chosen(self, move):
        self.fight_menu.hide()
        new_action_data = ('FIGHT', move, None)
        print(f'{move.name} chosen !')
        self.end_player_choice_phase(new_action_data)

    def switch_pokemon_chosen(self, pokemon):
        self.switch_menu.hide()
        self.switch_sub_menu.hide()

        if self.state == STATE_FORCED_SWITCH:
            print(f'Remplacement forcé par {pokemon.name} !')
            self.model.execute_forced_switch("player", pokemon)
            self.previous_menus = []
            self.view.hide_all_menus()
            # On relance le Ping-Pong
            self.current_menu = None
            self.state = STATE_RESOLVING_TURN
            self.current_event = None
        else:
            # Comportement normal d'un switch classique
            new_action_data = ('SWITCH', None, pokemon)
            print(f'Switch to {pokemon.name} !')
            self.end_player_choice_phase(new_action_data)

    def stats_chosen(self, pokemon):
        self.open_stats_menu(pokemon)
        print(f'Pokemon {pokemon.name} stats')

    def item_chosen(self, item):
        self.open_item_target_selection_menu(item)

    def item_target_chosen(self, pokemon, item):
        self.item_target_selection_menu.hide()
        self.item_menu.hide()
        new_action_data = ('ITEM', item, pokemon)
        print(f'{item.item_name} use on {pokemon.name} !')
        self.end_player_choice_phase(new_action_data)

    def open_switch_sub_menu(self, pokemon):
        self.save_current_menu_to_previous_menus()
        self.current_menu = self.switch_sub_menu
        self.switch_sub_menu.pokemon = pokemon
        self.current_menu.show()

    def open_stats_menu(self, pokemon):
        self.stats_menu.pokemon = pokemon
        self.stats_menu.update_items(pokemon)
        self.current_menu = self.stats_menu
        self.current_menu.show()

    def open_stats_2_menu(self, pokemon):
        self.stats_2_menu.pokemon = pokemon
        self.stats_2_menu.update_items(pokemon)
        self.current_menu = self.stats_2_menu
        self.current_menu.show()

    def open_item_target_selection_menu(self, chosen_item):
        self.save_current_menu_to_previous_menus()
        self.current_menu = self.item_target_selection_menu
        self.current_menu.update_consommable(chosen_item)
        self.current_menu.update_items(self._get_pokemons())
        self.current_menu.show()

    def open_fight_menu(self):
        self.save_current_menu_to_previous_menus()
        self.current_menu = self.fight_menu
        self.current_menu.update_items(self._get_current_pokemon_moves())
        self.current_menu.show()

    def open_switch_menu(self):
        self.save_current_menu_to_previous_menus()
        self.current_menu = self.switch_menu
        self.current_menu.update_items(self._get_pokemons())
        self.current_menu.show()

    def open_item_menu(self):
        self.save_current_menu_to_previous_menus()
        self.current_menu = self.item_menu
        self.current_menu.update_items(self._get_current_items())
        self.current_menu.show()

    def open_message_box(self, text_list):
        self.save_current_menu_to_previous_menus()
        self.message_box.reset_display()
        self.current_menu = self.message_box
        self.current_menu.show()
        self.current_menu.load_text_list(text_list)

    def open_main_menu(self):
        self.previous_menus = []
        self.current_menu = self.main_menu
        self.current_menu.show()

    def save_current_menu_to_previous_menus(self):
        if self.current_menu:
            self.previous_menus.append(self.current_menu)

    def start_player_choice_phase(self):
        self.view.hide_all_menus()  # Sécurité visuelle garantie
        self.previous_menus = []
        self.current_menu = None
        self.state = STATE_WAITING_FOR_INPUT
        print(f"\nGO STATE_WAITING_FOR_INPUT {self.model.turn_number}\n")

    def end_player_choice_phase(self, player_action):
        self.current_menu = None
        self.previous_menus = []
        self.view.hide_all_menus()
        self.model.add_player_action(player_action)
        # self.model.add_opponent_action(None)
        self.model.prepare_turn()
        self.state = STATE_RESOLVING_TURN
        self.current_event = None
        print("\nGO STATE_RESOLVING_TURN\n")


    def update(self, dt, events, keys):
        self.view.update(dt)

        """Traite les touches pressées par le joueur selon l'état actuel."""
        # if self.state == STATE_BATTLE_INTRODUCTION:
        #     self.start_player_choice_phase()

        if self.state in [STATE_WAITING_FOR_INPUT, STATE_FORCED_SWITCH]:
            if not self.current_menu:
                self.open_main_menu()
            if self.current_menu:
                self.current_menu.handle_input(events, keys)
        elif self.state in [STATE_BATTLE_INTRODUCTION, STATE_RESOLVING_TURN]:
            # 1. PING: On demande l'étape suivante au Model
            if self.current_event is None:
                self.current_event = self.model.get_next_step()
                if self.current_event is None:

                    # Le tour est fini, retour au choix du joueur
                    if self.model.is_over:
                        self.state = STATE_BATTLE_OVER
                        print(f"FIN DU COMBAT ! Vainqueur : {self.model.winner}")
                        # Ici tu pourras gérer le retour à la carte, l'écran de Game Over, etc.
                        return

                        # Sinon, le tour classique est fini, retour au choix du joueur
                    self.start_player_choice_phase()
                    return

                # On lance l'événement (ex: ouvrir une message_box, lancer une animation)
                self.execute_event(self.current_event)
            # 2. PONG : On vérifie si l'événement en cours est terminé visuellement
            if self.current_event is not None:

                # Si l'événement nécessite une interaction (ex: fermer une message_box)
                # il faut passer les events/keys à l'interface active.
                if self.current_menu:
                    self.current_menu.handle_input(events, keys)
                is_finished = self._is_event_finished()
                if is_finished:
                    # L'action est terminée à l'écran, on remet à None pour redéclencher le PING
                    self.current_event = None

    def execute_event(self, event):
        """Traite l'événement et met à jour l'interface graphique."""
        text_to_display = ""
        if event.type == "MESSAGE":
            text_to_display = event.text
        elif event.type == "FIGHT":
            text_to_display = f"{event.actor.name} utilise {event.detail.name} sur {event.target.name}!"
        elif event.type == "ITEM":
            text_to_display = f"{event.trainer} utilise {event.detail.item_name} sur {event.target.name}!"
        # elif event.type == "SWITCH":
        #     text_to_display = f"{event.trainer}: Reviens {event.actor.name}, go {event.target.name}!"
        elif event.type == "RUN":
            if getattr(event, 'success', True):
                text_to_display = "Vous prenez la fuite en toute sécurité !"
            else:
                text_to_display = "Vous ne pouvez pas fuir un combat de dresseur !"
        elif event.type == "SWITCH_OUT":
            if event.trainer == "player":
                text_to_display = f"{event.pokemon.name}!! Reviens!"
            else:
                if getattr(event, 'wild_encounter', False):
                    text_to_display = f"Le {event.pokemon.name.upper()} sauvage disparaît!"
                else:
                    text_to_display = f"L'adversaire retire {event.pokemon.name.upper()}!"
        elif event.type == "SWITCH_IN":
            if event.trainer == "player":
                text_to_display = f"En avant! {event.pokemon.name}!"
            else:
                if getattr(event, 'wild_encounter', False):
                    text_to_display = f"Un {event.pokemon.name.upper()} sauvage apparaît!"
                else:
                    text_to_display = f"TRAINER fait appel à...\n{event.pokemon.name.upper()}!"
                    # text_to_display = f"L'adversaire envoie {event.pokemon.name.upper()}!"

        elif event.type == "SWITCH_SPRITE":
            self.view.update_active_pokemon(event.side, event.new_pokemon)
            print(f"Mise à jour visuelle : {event.new_pokemon.name} entre sur le terrain")

        elif event.type == "FORCE_SWITCH":
            if event.trainer == "player":
                # On met le tour en pause et on force l'ouverture du menu Pokémon
                self.state = STATE_FORCED_SWITCH
                self.open_switch_menu()
                print("Switch forcé pour le joueur !")
            else:
                # L'IA choisit automatiquement le premier Pokémon vivant
                # (Assure-toi d'avoir une méthode get_first_available() ou similaire dans ta classe Party)
                new_pokemon = next(p for p in self.model.opponent.party.members if p.stats['hp'] > 0)
                self.model.execute_forced_switch("opponent", new_pokemon)
                print(f"L'adversaire remplace son Pokémon K.O. par {new_pokemon.name}")

        elif event.type in ["DAMAGE", "HEAL"]:
            # On ne fait pas de texte, on lance juste l'animation !
            self.view.animate_hp(event.new_hp, event.target)
            action_name = "Dégâts" if event.type == "DAMAGE" else "Soin"
            print(f"Animation de {action_name} sur {event.target.name} vers {event.new_hp} HP")
            print(event.target.name,':' ,event.target.stats['hp'], '/',event.target.stats['max_hp'])
        elif event.type == "ANIMATION":
            self.view.play_animation(event.name, event.target)
            print(f"Playing animation: {event.name} on {event.target}")
        elif event.type == "FAINT":
            text_to_display = f"{event.target.name} est K.O.!"
            # Plus tard, tu pourras aussi appeler la View ici pour cacher le sprite
            # ex: self.view.hide_pokemon(event.target) ou lancer une animation 'faint'
        elif event.type == "BATTLE_END":
            if event.winner == "PLAYER":
                text_to_display = "Vous avez remporté le combat !"
            elif event.winner == "OPPONENT":
                text_to_display = "Vous n'avez plus de Pokémon en état de se battre... Vous êtes hors-jeu."
            # Si le winner est ESCAPE, on ne met pas de texte ici car l'événement RUN s'en est déjà chargé !

        # Au lieu du print, on ouvre la boîte de dialogue avec le texte généré
        if text_to_display:
            print(text_to_display)  # Gardé pour ton debug console
            self.open_message_box([text_to_display])

    def _is_event_finished(self):
        """Vérifie si l'événement visuel en cours est terminé."""
        if not self.current_event:
            return True

        event_type = self.current_event.type
        # Exemple 1 : Événement texte
        if event_type in ["BATTLE_END", "MESSAGE", "FIGHT", "ITEM", "SWITCH_IN", "SWITCH_OUT", "RUN", "FAINT"]:
            # L'événement est fini si la message_box n'est plus le menu actif
            # (Cela implique que execute_event a ouvert la message_box, et que le joueur l'a fermée)
            if self.current_menu != self.message_box:
                return True
            return False
        elif event_type == "ANIMATION":
            # On demande directement à la vue si l'animation joue encore
            return not self.view.is_animation_playing()
        elif event_type in ["DAMAGE", "HEAL"]:
            # Le Controller "bloque" (renvoie False) tant que la barre bouge !
            # Dès que view.is_hp_animating() devient False, le Controller fera son prochain PING.
            return not self.view.is_hp_animating()
        elif event_type == "SWITCH_SPRITE":
            return True

        return True


    def _get_pokemons(self):
        pokemons = self.model.player.party.members
        return pokemons

    def _get_current_pokemon_moves(self):
        pokemon = self.model.active_player_pokemon
        moves = [pokemon.moves[key] for key in pokemon.moves if pokemon.moves[key]]
        return moves

    def _get_current_items(self):
        bag = self.model.player.bag
        items = [slot for slot in bag.slots.copy()]
        return items
