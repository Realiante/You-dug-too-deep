from typing import List
import random
import resources
import pygame

pygame.init()  # todo: remove this line

floor_textures = resources.load_img_dir("floor")
wall_textures = resources.load_img_dir("wall")
key_texture = resources.load_img("tex/key.png")
door_texture = resources.load_img("tex/door.png")


def floor_img():
    return random.choice(floor_textures)


def wall_img():
    return random.choice(floor_textures)


def key_img():
    return key_texture


def door_img():
    return door_texture


img_dispatch = {
    'f': floor_img(),
    'start': floor_textures[0],
    'w': wall_img(),
    'key': key_img(),
    'end': door_img()
}


class Maze:

    def __init__(self, pattern: List[List[str]]):
        # todo
        pass
