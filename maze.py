"""
@author: daniel.fedotov
"""

from typing import List
from random import choice
from tilescript import dictionary as tile_objects


class MazeData:

    def __init__(self, pattern: List[List[List[str]]]):
        self.dirty = True  # does the algorithm need to recalculate a path for this maze
        self.key_pos = 0, 0
        self.end_pos = 0, 0
        self.player_pos = 0, 0

        self.grid = pattern.copy()
        self.__uniques = []

        y = 0
        for p_row in pattern:
            x = 0
            for p_tile in p_row:
                layer = 0
                base_claimed = False
                for p_layer in p_tile:
                    img, cost, on_step, on_add, base, unique = tile_objects.update(p_layer)

                    # base check
                    if base:
                        if base_claimed or layer != 0:
                            self.grid[y][x].remove(p_layer)
                            break
                        base_claimed = True

                    # uniqueness check
                    if unique:
                        if p_layer in self.__uniques:
                            self.grid[y][x].remove(p_layer)
                            break
                        self.__uniques.append(p_layer)

                    if on_add is not None:
                        on_add(self, None, (x, y))
                    layer += 1
                x += 1
            y += 1
