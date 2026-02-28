import pygame
from battle.battle_settings import SHOW_GRID, TILE_WIDTH, TILE_HEIGHT, BACKGROUND_COLOR
from battle.item_menu_display import ItemMenuDisplay
from battle.main_menu import MainMenuDisplay
from battle.move_data_menu_display import MoveDataMenuDisplay
from battle.move_menu_display import MoveMenuDisplay
from settings import GAME_BOY_RESOLUTION
from battle.status_display import BottomStatusHUD, TopStatusHUD
from battle.pokemon_display import PokemonDisplay
from message_system.message_box_display import MessageBox
from battle.switch_menu_display import SwitchMenuDisplay
from battle.item_target_choice_menu_display import ItemTargetChoiceMenuDisplay
from battle.switch_sub_menu_display import SwitchSubMenuDisplay
from battle.pokemon_stats_display import PokemonStatsDisplay


#TODO Finir la pokemon_stats_display (avec 2ème page)
#TODO adapter la message box
#TODO changer la machine state par un nesting ?
#TODO ajouter la logique de tour par tour et relier avec le display
#TODO alimenter la database via API
#TODO ajouter vraies données dans le display (sprite, move, etc)
#TODO réfléchir à l'implémentation des status malus (poison, sleep, burn etc...)
#TODO mettre animation des moves (avec sfx)
#TODO mettre en place animation d'introduction et de fin
#TODO mettre musique
#TODO ajouter combat contre trainer
#TODO système de palette de couleur pour passer de la couleur au NB (gb pocket), NB verdatre (gb), ou monocouleur (comme pkmn rouge et bleu sur gbc)
#TODO implémenter un mode 2J


texts = [
    "Bien le bonjour!\nBienvenue dans le monde magique des POKéMON!",
    "Mon nom est CHEN!\nLes gens souvent m'appellent le PROF POKéMON!",
    "Ce monde est peuplé de créatures du nom de POKéMON!",
]

class BattleEngine:
    def __init__(self, sprites_dict):
        self.rect = pygame.Rect((0,0),GAME_BOY_RESOLUTION)
        self.state = "MAIN_MENU"
        self.menus = ["MESSAGE_MENU", "MAIN_MENU", "MOVE_MENU", "ITEM_MENU", "SWITCH_MENU", "ITEM_TARGET_MENU", "SWITCH_SUB_MENU", "STATS_MENU"]
        self.menu_index = 1

        self.bottom_status_hud = BottomStatusHUD(sprites_dict)
        self.top_status_hud = TopStatusHUD(sprites_dict)
        self.message_box = MessageBox([], sprites_dict, True)
        self.top_pokemon_display = PokemonDisplay((12,0), sprites_dict)
        self.bottom_pokemon_display = PokemonDisplay((1,5), sprites_dict)
        self.main_menu_display = MainMenuDisplay((6,12), sprites_dict)
        self.move_data_menu_display = MoveDataMenuDisplay((0,8), sprites_dict)
        self.move_menu_display = MoveMenuDisplay((4,12), self.move_data_menu_display, sprites_dict)
        self.item_target_menu_display = ItemTargetChoiceMenuDisplay((0,0), sprites_dict)
        self.item_menu_display = ItemMenuDisplay((4,2), sprites_dict, self.item_target_menu_display)
        self.switch_menu_display = SwitchMenuDisplay((0,0), sprites_dict)
        self.switch_sub_menu_display = SwitchSubMenuDisplay((11,11), sprites_dict)
        self.pokemon_stats_display = PokemonStatsDisplay((0,0), sprites_dict)

    def update(self, events, keys):
        # self.state = self.menus[self.menu_index]
        for event in events:
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    self.message_box.load_text_list(texts.copy())
                elif event.key == pygame.K_n:
                    self.menu_index = (self.menu_index + 1) % len(self.menus)
                    self.state = self.menus[self.menu_index]
                elif event.key == pygame.K_b:
                    self.menu_index = (self.menu_index - 1) % len(self.menus)
                    self.state = self.menus[self.menu_index]

        choice = None

        if self.state == "MESSAGE_MENU":
            self.message_box.update(keys)
        elif self.state == "MAIN_MENU":
            choice = self.main_menu_display.update(events)
        elif self.state == "MOVE_MENU":
            choice = self.move_menu_display.update(events)
            self.move_data_menu_display.update()
        elif self.state == "ITEM_MENU":
            choice = self.item_menu_display.update(events)
        elif self.state == "ITEM_TARGET_MENU":
            choice = self.item_target_menu_display.update(events)
        elif self.state == "SWITCH_MENU":
            choice = self.switch_menu_display.update(events)
        elif self.state == "SWITCH_SUB_MENU":
            choice = self.switch_sub_menu_display.update(events)
        elif self.state == "STATS_MENU":
            choice = self.pokemon_stats_display.update(events)

        if choice:
            match choice:
                case menu if menu in self.menus:
                    self.state = choice
                case "FUITE":
                    print("Run !")
                case _:
                    print(choice)

    def display(self, surface):
        surface.fill(BACKGROUND_COLOR)
        self.top_pokemon_display.display(surface)
        self.bottom_pokemon_display.display(surface)
        self.bottom_status_hud.display(surface)
        self.top_status_hud.display(surface)
        self.message_box.display(surface)
        if self.state == "MAIN_MENU":
            self.main_menu_display.display(surface)
        elif self.state == "MOVE_MENU":
            self.move_menu_display.display(surface)
            self.move_data_menu_display.display(surface)
        elif self.state == "ITEM_MENU":
            self.item_menu_display.display(surface)
        elif self.state == "ITEM_TARGET_MENU":
            self.item_target_menu_display.display(surface)
        elif self.state == "SWITCH_MENU":
            self.switch_menu_display.display(surface)
        elif self.state == "SWITCH_SUB_MENU":
            self.switch_menu_display.display(surface)
            self.switch_sub_menu_display.display(surface)
        elif self.state == "STATS_MENU":
            self.pokemon_stats_display.display(surface)



