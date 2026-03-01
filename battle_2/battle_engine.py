import pygame
from settings import GAME_BOY_RESOLUTION
from battle_2.battle_settings import SHOW_GRID, TILE_WIDTH, TILE_HEIGHT, BACKGROUND_COLOR
from battle_2.main_menu import MainMenuDisplay
from battle_2.status_display import BottomStatusHUD, TopStatusHUD
from battle_2.pokemon_display import PokemonDisplay
from battle_2.message_box_display import MessageBox



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
    def __init__(self, sprites_dict, trainer, wild_pokemon):
        self.rect = pygame.Rect((0,0),GAME_BOY_RESOLUTION)
        self.state = "MAIN_MENU"
        self.menus = ["MESSAGE_MENU", "MAIN_MENU"]
        self.menu_index = 1

        self.trainer_bottom = trainer
        self.wild_top_pokemon = wild_pokemon
        self.current_pokemon = self.trainer_bottom.get_current_pokemon()


        self.bottom_status_hud = BottomStatusHUD(sprites_dict)
        self.top_status_hud = TopStatusHUD(sprites_dict)
        self.message_box = MessageBox([], sprites_dict, True)
        self.top_pokemon_display = PokemonDisplay((12,0), sprites_dict)
        self.bottom_pokemon_display = PokemonDisplay((1,5), sprites_dict, None, True)
        self.main_menu_display = MainMenuDisplay((6,12), sprites_dict)
        self.update_status()
        self.update_sprites()

    def update_status(self):
        current_bottom_pokemon = self.trainer_bottom.get_current_pokemon()
        for pokemon, hud in zip([current_bottom_pokemon, self.wild_top_pokemon], [self.bottom_status_hud, self.top_status_hud]):
            hud.modify_name(pokemon.name)
            hud.modify_level(pokemon.stats['level'])
            hud.modify_life(pokemon.stats['hp'],pokemon.stats['max_hp'])

    def update_sprites(self):
        self.bottom_pokemon_display.modify_pokemon(self.trainer_bottom.get_current_pokemon())
        self.top_pokemon_display.modify_pokemon(self.wild_top_pokemon)

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
            choice = self.main_menu_display.update(events, self.current_pokemon)

        if choice:
            print(choice)

    def display(self, surface):
        surface.fill(BACKGROUND_COLOR)
        self.top_pokemon_display.display(surface)
        self.bottom_pokemon_display.display(surface)
        self.top_status_hud.display(surface)
        self.bottom_status_hud.display(surface)
        self.message_box.display(surface)
        if self.state == "MAIN_MENU":
            self.main_menu_display.display(surface)




