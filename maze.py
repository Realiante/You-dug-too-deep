"""
@author: daniel.fedotov
"""

from typing import List
from random import choice
from tilescript import dictionary as tile_objects
import random
import colorama


class MazeData:

    def __init__(self, pattern: List[List[List[str]]]):
        self.dirty = True  # does the algorithm need to recalculate a path for this maze
        self.key_pos = 0, 0
        self.end_pos = 0, 0
        self.player_pos = 0, 0
        self.max_cell_depth = 0
        self.grid = pattern.copy()
        self.__uniques = []

        y = 0
        for p_row in pattern:
            x = 0
            for p_tile in p_row:
                layer = 0
                base_claimed = False
                for p_layer in p_tile:
                    img, cost, on_step, on_add, base, unique = tile_objects[p_layer]

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
                self.max_cell_depth = max(self.max_cell_depth, layer)
                x += 1
            y += 1


class MazeBuilder:
    __floor = 'f'
    __start = 'start'
    __wall = 'w'
    # todo: __key = 'key' create a use for it in the future
    __end = 'end'
    __null = 'null'

    def __init__(self, h, w):
        self.end_point = None
        self.start_point = None
        self.height = h
        self.width = w
        self.walls = []
        self.maze = []  # So interpreter will know maze is a list
        self.generate_maze()

    def generate_maze(self):
        self.maze = []  # Clearing the maze
        for _ in range(0, self.height):
            line = []
            for _ in range(0, self.width):
                line.append(self.__null)
            self.maze.append(line)
        starting_height = int(random.random() * self.height)
        starting_width = int(random.random() * self.width)
        if starting_height == 0:
            starting_height += 1
        if starting_height == self.height - 1:
            starting_height -= 1
        if starting_width == 0:
            starting_width += 1
        if starting_width == self.width - 1:
            starting_width -= 1

        self.maze[starting_height][starting_width] = self.__floor
        self.walls.append([starting_height - 1, starting_width])
        self.walls.append([starting_height, starting_width - 1])
        self.walls.append([starting_height, starting_width + 1])
        self.walls.append([starting_height + 1, starting_width])

        # Denote walls in maze
        self.maze[starting_height - 1][starting_width] = self.__wall
        self.maze[starting_height][starting_width - 1] = self.__wall
        self.maze[starting_height][starting_width + 1] = self.__wall
        self.maze[starting_height + 1][starting_width] = self.__wall
        self.__generate_path()

    def __str__(self):
        mz_str = ""
        for i in range(0, self.height):
            for j in range(0, self.width):
                if self.maze[i][j] == self.__null:
                    mz_str += colorama.Fore.WHITE + '#' + " "
                elif self.maze[i][j] == self.__floor:
                    mz_str += colorama.Fore.GREEN + 'f' + " "
                elif self.maze[i][j] == [self.__floor, self.__start]:
                    mz_str += colorama.Fore.CYAN + 'o' + " "
                elif self.maze[i][j] == [self.__floor, self.__end]:
                    mz_str += colorama.Fore.CYAN + 'O' + " "
                else:
                    mz_str += colorama.Fore.RED + 'w' + " "
            mz_str += '\n'
        return mz_str

    def __surrounding_cells(self, rand_wall):
        s_cells = 0
        if self.maze[rand_wall[0] - 1][rand_wall[1]] == self.__floor:
            s_cells += 1
        if self.maze[rand_wall[0] + 1][rand_wall[1]] == self.__floor:
            s_cells += 1
        if self.maze[rand_wall[0]][rand_wall[1] - 1] == self.__floor:
            s_cells += 1
        if self.maze[rand_wall[0]][rand_wall[1] + 1] == self.__floor:
            s_cells += 1

        return s_cells

    def __check_left_wall(self, rand_wall):
        if (rand_wall[1] != 0) and (self.maze[rand_wall[0]][rand_wall[1] - 1] == self.__null
                                    and self.maze[rand_wall[0]][rand_wall[1] + 1] == self.__floor):
            # Find the number of surrounding cells
            s_cells = self.__surrounding_cells(rand_wall)
            if s_cells < 2:
                # Denote the new path
                self.maze[rand_wall[0]][rand_wall[1]] = self.__floor

                # Mark the new walls
                # Upper cell
                self.__upper_wall(rand_wall)
                # Bottom cell
                self.__bottom_wall(rand_wall)
                # Leftmost cell
                self.__left_wall(rand_wall)

            # Delete wall
            self.__delete_wall(rand_wall)

            return True
        return False

    def __check_upper_wall(self, rand_wall):
        if (rand_wall[0] != 0) and (self.maze[rand_wall[0] - 1][rand_wall[1]] == self.__null
                                    and self.maze[rand_wall[0] + 1][rand_wall[1]] == self.__floor):
            s_cells = self.__surrounding_cells(rand_wall)
            if s_cells < 2:
                # Denote the new path
                self.maze[rand_wall[0]][rand_wall[1]] = self.__floor

                # Mark the new walls
                # Upper cell
                self.__upper_wall(rand_wall)

                # Leftmost cell
                self.__left_wall(rand_wall)

                # Rightmost cell
                self.__right_wall(rand_wall)

            # Delete wall
            self.__delete_wall(rand_wall)

            return True
        return False

    def __check_bottom_wall(self, rand_wall):
        if (rand_wall[0] != self.height - 1) and (self.maze[rand_wall[0] + 1][rand_wall[1]] == self.__null
                                                  and self.maze[rand_wall[0] - 1][rand_wall[1]] == self.__floor):

            s_cells = self.__surrounding_cells(rand_wall)
            if s_cells < 2:
                # Denote the new path
                self.maze[rand_wall[0]][rand_wall[1]] = self.__floor

                # Mark the new walls
                self.__bottom_wall(rand_wall)
                self.__left_wall(rand_wall)
                self.__right_wall(rand_wall)

            # Delete wall
            self.__delete_wall(rand_wall)

            return True
        return False

    def __check_right_wall(self, rand_wall):
        if (rand_wall[1] != self.width - 1) and (self.maze[rand_wall[0]][rand_wall[1] + 1] == self.__null
                                                 and self.maze[rand_wall[0]][rand_wall[1] - 1] == self.__floor):

            s_cells = self.__surrounding_cells(rand_wall)
            if s_cells < 2:
                # Denote the new path
                self.maze[rand_wall[0]][rand_wall[1]] = self.__floor

                # Mark the new walls
                self.__right_wall(rand_wall)
                self.__bottom_wall(rand_wall)
                self.__upper_wall(rand_wall)

            # Delete wall
            self.__delete_wall(rand_wall)

            return True
        return False

    def __upper_wall(self, rand_wall):
        if rand_wall[0] != 0:
            if self.maze[rand_wall[0] - 1][rand_wall[1]] != self.__floor:
                self.maze[rand_wall[0] - 1][rand_wall[1]] = self.__wall
            if [rand_wall[0] - 1, rand_wall[1]] not in self.walls:
                self.walls.append([rand_wall[0] - 1, rand_wall[1]])

    def __bottom_wall(self, rand_wall):
        if rand_wall[0] != self.height - 1:
            if self.maze[rand_wall[0] + 1][rand_wall[1]] != self.__floor:
                self.maze[rand_wall[0] + 1][rand_wall[1]] = self.__wall
            if [rand_wall[0] + 1, rand_wall[1]] not in self.walls:
                self.walls.append([rand_wall[0] + 1, rand_wall[1]])

    def __right_wall(self, rand_wall):
        if rand_wall[1] != self.width - 1:
            if self.maze[rand_wall[0]][rand_wall[1] + 1] != self.__floor:
                self.maze[rand_wall[0]][rand_wall[1] + 1] = self.__wall
            if [rand_wall[0], rand_wall[1] + 1] not in self.walls:
                self.walls.append([rand_wall[0], rand_wall[1] + 1])

    def __left_wall(self, rand_wall):
        if rand_wall[1] != 0:
            if self.maze[rand_wall[0]][rand_wall[1] - 1] != self.__floor:
                self.maze[rand_wall[0]][rand_wall[1] - 1] = self.__wall
            if [rand_wall[0], rand_wall[1] - 1] not in self.walls:
                self.walls.append([rand_wall[0], rand_wall[1] - 1])

    def __delete_wall(self, rand_wall):
        # Delete the wall from the list anyway
        for element in self.walls:
            if element[0] == rand_wall[0] and element[1] == rand_wall[1]:
                self.walls.remove(element)

    def __generate_path(self):
        while self.walls:
            # Pick a random wall
            rand_wall = self.walls[int(random.random() * len(self.walls)) - 1]
            #
            if self.__check_left_wall(rand_wall) \
                    or self.__check_upper_wall(rand_wall) \
                    or self.__check_bottom_wall(rand_wall) \
                    or self.__check_right_wall(rand_wall):
                continue
            self.__delete_wall(rand_wall)

        for i in range(0, self.height):
            for j in range(0, self.width):
                if self.maze[i][j] == self.__null:
                    self.maze[i][j] = self.__wall
        self.__create_end()
        self.__create_start()

    def __create_end(self):
        while True:
            i = random.randrange(self.width)
            if self.maze[1][i] == self.__floor:
                self.maze[0][i] = [self.__floor, self.__end]
                self.end_point = i
                break

    def __create_start(self):
        while True:
            i = random.randrange(self.width)
            if self.maze[self.height - 2][i] == self.__floor:
                self.maze[self.height - 1][i] = [self.__floor, self.__start]
                self.start_point = i
                break

    # Print final maze
