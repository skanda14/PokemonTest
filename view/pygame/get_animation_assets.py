import pygame


def get_animation_assets():
    tackle_sprites = [pygame.Surface((16, 16)) for _ in range(20)]
    for sprite in tackle_sprites:
        sprite.fill((255, 0, 0))
    new_animation_assets = {
        "thunderbolt": [pygame.Surface((50, 50)) for _ in range(5)],  # 5 frames
        "potion": [pygame.Surface((30, 30)) for _ in range(3)],  # 3 frames
        "tackle": tackle_sprites  # 4 frames
    }
    return new_animation_assets