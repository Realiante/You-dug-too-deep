import pygame
import resources.images as images

bg_tex = images.load_weighted_images("tex/wall")
bgt_w, bgt_h = (*bg_tex.keys(),)[0].get_size()
bg_surface = pygame.Surface((0, 0))
dirty = True


def __refill(display_size):
    global bg_surface
    bg_surface = pygame.Surface(display_size).convert()
    screen_width, screen_height = display_size
    for height_index in range(0, screen_height, bgt_h):
        for width_index in range(0, screen_width, bgt_w):
            bg_surface.blit(images.choose_by_weight(bg_tex), (width_index, height_index))
            width_index += bgt_w
        height_index += bgt_h


def get(display_size):
    global dirty
    if dirty:
        __refill(display_size)
        dirty = False
    return bg_surface
