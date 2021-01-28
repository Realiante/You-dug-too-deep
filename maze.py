from typing import List
from random import choice
from character import Character
import resources
import pygame

pygame.init()

floor_textures = resources.load_img_dir("tex/floor")
wall_textures = resources.load_img_dir("tex/wall")
key_textures = (resources.load_img("tex/key.png"),)
door_textures = (resources.load_img("tex/door.png"),)
trap_textures = (resources.load_img("tex/trap.png"),)


class Maze:

    def __init__(self, pattern: List[List[List[str]]]):
        self.dirty = True  # does the algorithm need to recalculate a path for this maze
        self.key_pos = 0, 0
        self.end_pos = 0, 0
        self.player_pos = 0, 0
        draw_grid = []  # 3d collection with references to background images and layers.
        property_grid = []  # 2d collection where each element stores path costs and the tile's on_step effect
        y = -1
        for p_row in pattern:
            y += 1
            x = -1
            dg_row = []
            pg_row = []
            for p_tile in p_row:
                x += 1
                draw_tile = []
                grid_tile = [999, None]
                for p_layer in p_tile:
                    mapping = tile_dict.get(p_layer)
                    draw_tile.append(choice(mapping[0]))
                    grid_tile[0] = min(grid_tile[0], mapping[1])
                    if mapping[3] is not None:
                        mapping[3](self, None, y, x)
                    if mapping[2] is not None:
                        grid_tile[1] = mapping[2]
                dg_row.append(draw_tile)
                pg_row.append(grid_tile)
            draw_grid.append(dg_row)
            property_grid.append(pg_row)
        self.draw_grid = draw_grid
        self.property_grid = property_grid


def __effect_key(maze: Maze, character: Character, *args):
    character.can_exit = True
    maze.dirty = True


def __effect_win(maze: Maze, character: Character, *args):
    character.win = True


def __effect_damage_light(maze: Maze, character: Character, *args):
    character.take_damage(1)


def __effect_on_set_player(maze: Maze, character: Character, *args):
    maze.player_pos = args[0], args[1]


def __effect_on_set_key(maze: Maze, character: Character, *args):
    maze.key_pos = args[0], args[1]


def __effect_on_set_end(maze: Maze, character: Character, *args):
    maze.end_pos = args[0], args[1]


tile_dict = {
    # [0] collection of possible textures, [1] path cost mod (0 is regular, >10 is considered impassable) [2] tile on step, [3] tile on set
    'f': (floor_textures, 0, None, None),
    'start': (floor_textures, 0, None, __effect_on_set_player),
    'w': (wall_textures, 999, None, None),
    'key': (key_textures, 0, __effect_key, __effect_on_set_key),
    'end': (door_textures, 0, __effect_win, __effect_on_set_end),
    'trap': (door_textures, 2, __effect_damage_light, None)
}
