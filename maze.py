"""
@author: daniel.fedotov, vel.krol

@structure and multiple path hack: daniel.fedotov
@maze generation: vel.krol
"""

from typing import List
from random import choice
from tilescript import dictionary as tile_objects
import math
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
    __trap = 'trap'
    __key = 'key'
    __end = 'end'
    __null = 'null'

    def __init__(self, h, w):
        self.end_point = None
        self.start_point = None
        self.height = h
        self.width = w
        self.__walls = []
        self.maze = []  # so interpreter will know maze is a list
        self.generate_maze()

    def generate_maze(self):
        self.maze = []  # Clearing the maze
        for _ in range(0, self.height):
            line = []
            for _ in range(0, self.width):
                line.append(MazeBuilder.__null)
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

        self.maze[starting_height][starting_width] = MazeBuilder.__floor
        self.__walls.append([starting_height - 1, starting_width])
        self.__walls.append([starting_height, starting_width - 1])
        self.__walls.append([starting_height, starting_width + 1])
        self.__walls.append([starting_height + 1, starting_width])

        # Denote walls in maze
        self.maze[starting_height - 1][starting_width] = MazeBuilder.__wall
        self.maze[starting_height][starting_width - 1] = MazeBuilder.__wall
        self.maze[starting_height][starting_width + 1] = MazeBuilder.__wall
        self.maze[starting_height + 1][starting_width] = MazeBuilder.__wall
        self.__generate_path()
        self.__create_new_paths()
        self.__create_new_traps()
        self.__create_key()

    def __str__(self):
        mz_str = ""
        for i in range(0, self.height):
            for j in range(0, self.width):
                if self.maze[i][j] == MazeBuilder.__null:
                    mz_str += colorama.Fore.WHITE + '#' + " "
                elif self.maze[i][j] == MazeBuilder.__floor:
                    mz_str += colorama.Fore.GREEN + 'f' + " "
                elif self.maze[i][j] == MazeBuilder.__start:
                    mz_str += colorama.Fore.CYAN + 'o' + " "
                elif self.maze[i][j] == MazeBuilder.__end:
                    mz_str += colorama.Fore.CYAN + 'O' + " "
                elif self.maze[i][j] == MazeBuilder.__key:
                    mz_str += colorama.Fore.WHITE + 'K' + " "
                elif self.maze[i][j] == MazeBuilder.__trap:
                    mz_str += colorama.Fore.MAGENTA + 'T' + " "
                else:
                    mz_str += colorama.Fore.RED + 'w' + " "
            mz_str += '\n'
        return mz_str

    def __surrounding_cells(self, rand_wall):
        s_cells = 0
        y, x = rand_wall
        if self.maze[y - 1][x] == MazeBuilder.__floor:
            s_cells += 1
        if self.maze[y + 1][x] == MazeBuilder.__floor:
            s_cells += 1
        if self.maze[y][x - 1] == MazeBuilder.__floor:
            s_cells += 1
        if self.maze[y][x + 1] == MazeBuilder.__floor:
            s_cells += 1

        return s_cells

    def __check_left_wall(self, rand_wall):
        if (rand_wall[1] != 0) and (self.maze[rand_wall[0]][rand_wall[1] - 1] == MazeBuilder.__null
                                    and self.maze[rand_wall[0]][rand_wall[1] + 1] == MazeBuilder.__floor):
            # Find the number of surrounding cells
            s_cells = self.__surrounding_cells(rand_wall)
            if s_cells < 2:
                # Denote the new path
                self.maze[rand_wall[0]][rand_wall[1]] = MazeBuilder.__floor

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
        if (rand_wall[0] != 0) and (self.maze[rand_wall[0] - 1][rand_wall[1]] == MazeBuilder.__null
                                    and self.maze[rand_wall[0] + 1][rand_wall[1]] == MazeBuilder.__floor):
            s_cells = self.__surrounding_cells(rand_wall)
            if s_cells < 2:
                # Denote the new path
                self.maze[rand_wall[0]][rand_wall[1]] = MazeBuilder.__floor

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
        if (rand_wall[0] != self.height - 1) and (self.maze[rand_wall[0] + 1][rand_wall[1]] == MazeBuilder.__null
                                                  and self.maze[rand_wall[0] - 1][rand_wall[1]] == MazeBuilder.__floor):

            s_cells = self.__surrounding_cells(rand_wall)
            if s_cells < 2:
                # Denote the new path
                self.maze[rand_wall[0]][rand_wall[1]] = MazeBuilder.__floor

                # Mark the new walls
                self.__bottom_wall(rand_wall)
                self.__left_wall(rand_wall)
                self.__right_wall(rand_wall)

            # Delete wall
            self.__delete_wall(rand_wall)

            return True
        return False

    def __check_right_wall(self, rand_wall):
        if (rand_wall[1] != self.width - 1) and (self.maze[rand_wall[0]][rand_wall[1] + 1] == MazeBuilder.__null
                                                 and self.maze[rand_wall[0]][rand_wall[1] - 1] == MazeBuilder.__floor):

            s_cells = self.__surrounding_cells(rand_wall)
            if s_cells < 2:
                # Denote the new path
                self.maze[rand_wall[0]][rand_wall[1]] = MazeBuilder.__floor

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
            if self.maze[rand_wall[0] - 1][rand_wall[1]] != MazeBuilder.__floor:
                self.maze[rand_wall[0] - 1][rand_wall[1]] = MazeBuilder.__wall
            if [rand_wall[0] - 1, rand_wall[1]] not in self.__walls:
                self.__walls.append([rand_wall[0] - 1, rand_wall[1]])

    def __bottom_wall(self, rand_wall):
        if rand_wall[0] != self.height - 1:
            if self.maze[rand_wall[0] + 1][rand_wall[1]] != MazeBuilder.__floor:
                self.maze[rand_wall[0] + 1][rand_wall[1]] = MazeBuilder.__wall
            if [rand_wall[0] + 1, rand_wall[1]] not in self.__walls:
                self.__walls.append([rand_wall[0] + 1, rand_wall[1]])

    def __right_wall(self, rand_wall):
        if rand_wall[1] != self.width - 1:
            if self.maze[rand_wall[0]][rand_wall[1] + 1] != MazeBuilder.__floor:
                self.maze[rand_wall[0]][rand_wall[1] + 1] = MazeBuilder.__wall
            if [rand_wall[0], rand_wall[1] + 1] not in self.__walls:
                self.__walls.append([rand_wall[0], rand_wall[1] + 1])

    def __left_wall(self, rand_wall):
        if rand_wall[1] != 0:
            if self.maze[rand_wall[0]][rand_wall[1] - 1] != MazeBuilder.__floor:
                self.maze[rand_wall[0]][rand_wall[1] - 1] = MazeBuilder.__wall
            if [rand_wall[0], rand_wall[1] - 1] not in self.__walls:
                self.__walls.append([rand_wall[0], rand_wall[1] - 1])

    def __delete_wall(self, rand_wall):
        # Delete the wall from the list anyway
        for element in self.__walls:
            if element[0] == rand_wall[0] and element[1] == rand_wall[1]:
                self.__walls.remove(element)

    def __generate_path(self):
        while self.__walls:
            # Pick a random wall
            rand_wall = self.__walls[int(random.random() * len(self.__walls)) - 1]
            #
            if self.__check_left_wall(rand_wall) \
                    or self.__check_upper_wall(rand_wall) \
                    or self.__check_bottom_wall(rand_wall) \
                    or self.__check_right_wall(rand_wall):
                continue
            self.__delete_wall(rand_wall)

        for i in range(0, self.height):
            for j in range(0, self.width):
                if self.maze[i][j] == MazeBuilder.__null:
                    self.maze[i][j] = MazeBuilder.__wall
        self.__create_end()
        self.__create_start()

    def __create_end(self):
        for i in range(self.width - 1, 0, -1):
            if self.maze[1][i] == MazeBuilder.__floor:
                self.maze[0][i] = MazeBuilder.__end
                self.end_point = i

                break

    def __create_start(self):
        for i in range(self.width):
            if self.maze[self.height - 2][i] == MazeBuilder.__floor:
                self.maze[self.height - 1][i] = MazeBuilder.__start
                self.start_point = i
                break

    def __opposite_floors(self, pos: tuple):
        y, x = pos
        opp_horizontal = self.maze[y][x - 1] == MazeBuilder.__floor and self.maze[y][x + 1] == MazeBuilder.__floor
        opp_vertical = self.maze[y - 1][x] == MazeBuilder.__floor and self.maze[y + 1][x] == MazeBuilder.__floor
        return opp_vertical or opp_horizontal

    def __create_new_paths(self):
        potential_breaches = []
        for y in range(1, self.height - 1):
            for x in range(1, self.width - 1):
                if self.maze[y][x] == MazeBuilder.__wall:
                    surround = self.__surrounding_cells((y, x))
                    if surround == 2 and self.__opposite_floors((y, x)):
                        # while currently the corners are ignored, maybe some time they can be appended too,
                        # appending corners produced an interesting room generation effect, but was not pretty.
                        potential_breaches.append((y, x))
        self.__generate_breaches(potential_breaches, 40, 0, False)

    def __generate_breaches(self, potential_breaches: list, percent: int, count: int, reverse_step: bool):
        if potential_breaches:
            if reverse_step:
                potential_breach = potential_breaches[-1]
            else:
                potential_breach = potential_breaches[0]
            y, x = potential_breach
            rv = random.randrange(100)
            if rv < percent:
                self.maze[y][x] = MazeBuilder.__floor  # todo: should be any walkable surface
                percent -= 40 + count / math.sqrt(self.width * self.height)
            potential_breaches.remove(potential_breach)
            self.__generate_breaches(potential_breaches, percent + 20, count + 1, not reverse_step)

    def __create_new_traps(self):
        potential_breaches = []
        for y in range(1, self.height - 1):
            for x in range(1, self.width - 1):
                if self.maze[y][x] == MazeBuilder.__floor:
                    surround = self.__surrounding_cells((y, x))
                    if surround == 2:
                        potential_breaches.append((y, x))
        self.__generate_traps(potential_breaches, 40, 0, False)

    def __mod_opposite_traps(self, pos: tuple):
        y, x = pos
        opp_horizontal = self.maze[y][x - 1] == MazeBuilder.__trap and self.maze[y][x + 1] == MazeBuilder.__trap
        opp_vertical = self.maze[y - 1][x] == MazeBuilder.__trap and self.maze[y + 1][x] == MazeBuilder.__trap
        if opp_vertical or opp_horizontal:
            return 0
        return 50

    def __generate_traps(self, potential_breaches: list, percent: int, count: int, reverse_step: bool):
        if potential_breaches:
            if reverse_step:
                potential_breach = potential_breaches[-1]
            else:
                potential_breach = potential_breaches[0]
            y, x = potential_breach
            rv = random.randrange(100)
            if rv - 50 < percent and not self.__is_surrounding_traps(y, x):
                mod = self.__mod_opposite_traps(potential_breach)
                if rv + mod < percent:
                    self.maze[y][x] = MazeBuilder.__trap
                    percent = 0
            potential_breaches.remove(potential_breach)
            self.__generate_traps(potential_breaches, percent + 10, count + 1, not reverse_step)

    def __is_surrounding_traps(self, y, x):  # returns True if there's a trap and False if there are no traps
        for i in range(-1, 1):  # i for x
            for j in range(-1, 1):  # j for y
                if 1 < x + i < self.width - 2 and 1 < y + j < self.height - 2 \
                        and self.maze[y + j][x + i] == MazeBuilder.__trap:
                    return True
        return False

    def __create_key(self):
        from_start = []
        steps_from_start = []
        from_end = []
        steps_from_end = []

        self.__bfs_steps(from_start, steps_from_start, [self.height - 1, self.start_point])
        self.__bfs_steps(from_end, steps_from_end, [0, self.end_point])

        max_size = 0
        max_node = []
        for i in range(len(from_start)):
            temp = from_end.index(from_start[i])
            if steps_from_start[i][2] + steps_from_end[temp][2] > max_size:
                max_size = steps_from_start[i][2] + steps_from_end[temp][2]
                max_node = from_start[i]

        self.maze[max_node[0]][max_node[1]] = MazeBuilder.__key

    def __bfs_steps(self, visited: list, visited_steps: list, node: list):
        queue = [node]
        visited.append(node)
        queue_steps = [[node[0], node[1], 0]]
        visited_steps.append([node[0], node[1], 0])

        while queue:
            s = queue.pop(0)
            q = queue_steps.pop(0)
            graph = self.__get_surround(s)
            for neighbour in graph:
                if neighbour not in visited:
                    visited.append(neighbour)
                    visited_steps.append([neighbour[0], neighbour[1], q[2] + 1])
                    queue.append(neighbour)
                    queue_steps.append([neighbour[0], neighbour[1], q[2] + 1])
        visited.pop(0)
        visited_steps.pop(0)

    def __get_surround(self, node):
        lst = []
        if node[0] > 1 and self.__is_walkable([node[0] - 1, node[1]]):
            lst.append([node[0] - 1, node[1]])
        if node[0] < self.height - 2 and self.__is_walkable([node[0] + 1, node[1]]):
            lst.append([node[0] + 1, node[1]])
        if node[1] > 1 and self.__is_walkable([node[0], node[1] - 1]):
            lst.append([node[0], node[1] - 1])
        if node[1] < self.width - 2 and self.__is_walkable([node[0], node[1] + 1]):
            lst.append([node[0], node[1] + 1])
        return lst

    def __is_walkable(self, node):
        if self.maze[node[0]][node[1]] == MazeBuilder.__floor or self.maze[node[0]][node[1]] == MazeBuilder.__trap \
                or self.maze[node[0]][node[1]] == MazeBuilder.__key:
            return True
        return False

    def get_type(self, x, y):
        return self.maze[y][x]
