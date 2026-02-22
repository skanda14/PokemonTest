import pygame


def get_sprite_dict(zoom):
    image = pygame.image.load("assets/sprites/battle interface/pokemon_police.png").convert_alpha()
    image = pygame.transform.scale_by(image, zoom)
    sprites = []
    for i in range(0, image.width, 8*zoom):
        # print(f"image {i}")
        new_image = image.copy().subsurface((i, 0, 8*zoom, 8*zoom))
        sprites.append(new_image)

    # sprites = [image.copy().subsurface((i * 8, 0, 8, 8)) for i in range(0, image.width, 8)]
    new_dict = {
        "numbers": {},
        "letters": {},
        "symbols": {},
        "all": {}
    }
    for i in range(len(sprites)):
        if i < 10:
            new_dict["numbers"][i] = sprites[i]
            new_dict["all"][str(i)] = sprites[i]
        elif i < 36:
            n = 65 + i - 10
            new_dict["letters"][chr(n)] = sprites[i]
            new_dict["all"][chr(n)] = sprites[i]
        elif i == 36:
            new_dict["symbols"]["/"] = sprites[i]
            new_dict["all"]["/"] = sprites[i]
        elif i == 37:
            new_dict["symbols"]["n"] = sprites[i]
            new_dict["all"]["n"] = sprites[i]
        elif i == 38:
            new_dict["symbols"][""] = sprites[i]
            new_dict["all"]["p"] = sprites[i]
        elif i == 39:
            new_dict["symbols"]["("] = sprites[i]
            new_dict["all"]["("] = sprites[i]
        elif i == 40:
            new_dict["symbols"]["="] = sprites[i]
            new_dict["all"]["="] = sprites[i]
        elif i == 41:
            new_dict["symbols"][")"] = sprites[i]
            new_dict["all"][")"] = sprites[i]
        elif i == 42:
            new_dict["symbols"][" "] = sprites[i]
            new_dict["all"][" "] = sprites[i]
    return new_dict
