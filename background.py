from pygame import Surface
from random import choice
import resources

bg_tex = resources.load_img_dir("tex/wall")
bgt_w, bgt_h = bg_tex[0].get_size()
bg_surface = Surface((0, 0))
dirty = True


def __refill(display_size):
    global bg_surface
    bg_surface = Surface(display_size).convert()
    screen_width, screen_height = display_size
    for height_index in range(0, screen_height, bgt_h):
        for width_index in range(0, screen_width, bgt_w):
            bg_surface.blit(choice(bg_tex), (width_index, height_index))
            width_index += bgt_w
        height_index += bgt_h


def get(display_size):
    global dirty
    if dirty:
        __refill(display_size)
        dirty = False
    return bg_surface
