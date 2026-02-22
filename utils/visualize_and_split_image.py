import pygame
import os

def export_surface(surface, filename):
    """
    Enregistre une surface Pygame au format PNG.
    Le nom du fichier doit inclure l'extension .png.
    """
    # 1. Vérifier si le dossier de destination existe
    directory = os.path.dirname(filename)
    if directory and not os.path.exists(directory):
        os.makedirs(directory)
        print(f"Created directory: {directory}")

    # 2. Enregistrer l'image
    try:
        pygame.image.save(surface, filename)
        print(f"Successfully saved to: {filename}")
    except pygame.error as e:
        print(f"Failed to save image: {e}")


def combine_images(image_list, n_cols):
    if not image_list:
        return None

    # 1. On récupère les dimensions d'une tuile (on suppose qu'elles sont identiques)
    tile_w, tile_h = image_list[0].get_size()

    # 2. On calcule le nombre de lignes nécessaires
    # On utilise divmod pour voir s'il y a un reste et ajouter une ligne si besoin
    n_rows, remainder = divmod(len(image_list), n_cols)
    if remainder > 0:
        n_rows += 1

    # 3. On crée la surface de destination (le canevas)
    canvas_w = n_cols * tile_w
    canvas_h = n_rows * tile_h
    # SRCALPHA permet de conserver la transparence des sprites originaux
    combined_surface = pygame.Surface((canvas_w, canvas_h), pygame.SRCALPHA)

    # 4. On place chaque image à sa position (row, col)
    for i, img in enumerate(image_list):
        row, col = divmod(i, n_cols)
        x = col * tile_w
        y = row * tile_h
        combined_surface.blit(img, (x, y))

    return combined_surface


def get_empty_index():
    line_len = 16
    new_list = ([(i+4*line_len) for i in range(13,14+1)]+
                [(i+5*line_len) for i in range(0,3+1)]+
                [(5+6*line_len)]+
                [(10+6*line_len)]+
                [(2*7*line_len)])
    return int(13+4*line_len)


def images_are_the_same(image_a, image_b):
    if not image_a or not image_b:
        return False
    if image_a.get_width() != image_b.get_width():
        return False
    if image_a.get_height() != image_b.get_height():
        return False
    for y in range(image_a.get_height()):
        for x in range(image_a.get_width()):
            if image_a.get_at((x, y)) != image_b.get_at((x, y)):
                return False
    return True


def image_exist_in_list(new_image, image_list):
    for image in image_list:
        if images_are_the_same(image, new_image):
            return True
    return False


def cut_image(path):
    images = []
    image = pygame.image.load(path).convert_alpha()
    color_key = image.get_at((0,135))
    image.set_colorkey(color_key)
    empty_index = get_empty_index()
    i = 0
    for y in range(136, 208, 9):
        for x in range(8, 152, 9):
            if i == empty_index:
                sub_image = image.copy().subsurface(x, y, 8, 8).convert_alpha()
                images = [sub_image]+images
            else:
                sub_image = image.copy().subsurface(x, y, 8, 8).convert_alpha()
                if not image_exist_in_list(sub_image, images):
                    images.append(sub_image)
            i += 1
    return images



def display(screen, sprite):
    screen.fill((230, 210, 220))
    screen.blit(sprite, (0, 0))
    pygame.draw.rect(screen, (0, 255,0), (0, 0, 64, 64), 1)


def update(message_box, keys):
    message_box.update(keys)


def test():
    pygame.init()
    clock = pygame.time.Clock()
    fps = 60
    resolution = 640,480
    zoom = 4

    screen = pygame.display.set_mode(resolution)

    image_path = "../image_test/Game Boy _ GBC - Pokemon Crystal - Miscellaneous - Font.png"
    sprites_list = cut_image(image_path)

    combined_image = combine_images(sprites_list, 12)
    sprites_list = [combined_image]

    index = 0
    max_index = len(sprites_list)

    zoom_sprite = pygame.transform.scale_by(sprites_list[index], zoom)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    print("right")
                    index += 1
                    index = index % max_index
                    print(f"index: {index}")
                    zoom_sprite = pygame.transform.scale_by(sprites_list[index], zoom)

                elif event.key == pygame.K_LEFT:
                    index -= 1
                    index = index % max_index
                    zoom_sprite = pygame.transform.scale_by(sprites_list[index], zoom)

                elif event.key == pygame.K_s:
                    export_surface(combined_image, "../image_test/pokemon_font.png")

        display(screen, zoom_sprite)
        pygame.display.flip()

        pygame.display.set_caption(f"Pokemon Test (fps: {clock.get_fps(): .1f})")
        clock.tick(fps)


# test()