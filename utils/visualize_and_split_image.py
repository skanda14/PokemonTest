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


def combine_images_from_list(image_list, n_cols):
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

def combine_images_from_table(image_table):
    if not image_table:
        return None

    # 1. On récupère les dimensions d'une tuile (on suppose qu'elles sont identiques)
    tile_w, tile_h = image_table[0][0].get_size()

    # 2. On calcule le nombre de lignes nécessaires
    n_rows = len(image_table)
    n_cols = len(image_table[0])

    # 3. On crée la surface de destination (le canevas)
    canvas_w = n_cols * tile_w
    canvas_h = n_rows * tile_h
    # SRCALPHA permet de conserver la transparence des sprites originaux
    combined_surface = pygame.Surface((canvas_w, canvas_h), pygame.SRCALPHA)

    # 4. On place chaque image à sa position (row, col)
    for row, image_row in enumerate(image_table):
        for col, tile in enumerate(image_row):
            x = col * tile_w
            y = row * tile_h
            combined_surface.blit(tile, (x, y))

    return combined_surface

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


def cut_font_image_image():
    path = "../image_test/Game Boy _ GBC - Pokemon Crystal - Miscellaneous - Font.png"
    surface = pygame.image.load(path).convert_alpha()
    color_key = surface.get_at((0,135))
    cut_area_rect = pygame.Rect(8, 136, 152-8, 208-136)
    tile_size = 8,8
    gap_size = 1,1
    return cut_surface_with_specific_settings(surface, cut_area_rect, tile_size, gap_size, color_key)


def cut_surface_with_specific_settings(surface, cut_area_rect, tile_size, gap_size, color_key=None):
    tile_width, tile_height = tile_size
    h_gap, v_gap = gap_size
    temp_surface = get_a_subsurface_from(surface, cut_area_rect)
    if color_key is not None:
        temp_surface.set_colorkey(color_key)
    subsurfaces_table = []
    for y in range(0, temp_surface.get_height(), tile_height+v_gap):
        new_line = []
        for x in range(0, temp_surface.get_width(), tile_width+h_gap):
            pos = x,y
            new_subsurface = get_a_subsurface_from(temp_surface, pygame.Rect(pos, tile_size))
            new_line.append(new_subsurface)
        subsurfaces_table.append(new_line)
    return subsurfaces_table

def display(screen, sprite):
    screen.fill((230, 210, 220))
    screen.blit(sprite, (0, 0))
    pygame.draw.rect(screen, (0, 255,0), (0, 0, 64, 64), 1)


def update(message_box, keys):
    message_box.update(keys)


def get_a_subsurface_from(surface, rect):
    return surface.copy().subsurface(rect).convert_alpha()


def get_list_with_element_at_front(input_list, index):
    if not (0 <= index < len(input_list)):
        return input_list[:]
    return [input_list[index]] + input_list[:index] + input_list[index + 1:]


def visualize_image_list(screen, sprites_list, combined_image=None, path_to_save_combined_image=None):
    clock = pygame.time.Clock()
    fps = 60
    zoom = 4


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
                    if combined_image:
                        export_surface(combined_image, path_to_save_combined_image)
                    else:
                        print("no combined image")

        display(screen, zoom_sprite)
        pygame.display.flip()

        pygame.display.set_caption(f"Pokemon Test (fps: {clock.get_fps(): .1f})")
        clock.tick(fps)


def test_cut_image():
    image_path = "../assets/sprites/battle/Game Boy _ GBC - Pokemon Red _ Blue - Miscellaneous - Pokemon Attacks.png"
    pos = 2, 201
    grid_size = 1,2
    gap_size = 0,0

    saved_file_name = "ice"


    pygame.init()
    resolution = 640,480
    screen = pygame.display.set_mode(resolution)



    image = pygame.image.load(image_path)

    tile_size = 8,8
    size = grid_size[0]*tile_size[0]+(grid_size[0]-1)*gap_size[0],grid_size[1]*tile_size[1]+(grid_size[1]-1)*gap_size[1]
    print("pos:", pos)
    print("size:",size)
    sprites_table = cut_surface_with_specific_settings(image, pygame.Rect(pos, size), tile_size, gap_size, None)
    save_path = "assets/sprites/battle_sprites/"
    save_file_extension = ".png"
    # i = -1  # index de l'image à mettre en 1ère place de la liste si -1 pas de changement
    # sprites_list = get_list_with_element_at_front(sprites_list, i)
    combined_image = combine_images_from_table(sprites_table)
    export_surface(combined_image, "../"+save_path+saved_file_name+save_file_extension)

    # visualize_image_list(screen, sprites_list, combined_image, "../"+save_path+saved_file_name+save_file_extension)


# test_cut_image()