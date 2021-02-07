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

        self.grid = pattern.copy()
        self.__uniques = []

        y = 0
        for p_row in pattern:
            x = 0
            for p_tile in p_row:
                layer = 0
                base_claimed = False
                for p_layer in p_tile:
                    img, cost, on_step, on_add, base, unique = tile_objects.get(p_layer)

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


class MazeBuilder:
    __floor = 'f'
    __start = 'start'
    __wall = 'w'
    # __key = 'key' create a use for it in the future
    __end = 'end'
    __null = 'null'
    __walls = []
    end_point = None
    start_point = None
    height = None
    width = None
    maze = []

    def __init__(self, h, w):
        self.height = h
        self.width = w
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
        self.__walls.append([starting_height - 1, starting_width])
        self.__walls.append([starting_height, starting_width - 1])
        self.__walls.append([starting_height, starting_width + 1])
        self.__walls.append([starting_height + 1, starting_width])

        # Denote walls in maze
        self.maze[starting_height - 1][starting_width] = self.__wall
        self.maze[starting_height][starting_width - 1] = self.__wall
        self.maze[starting_height][starting_width + 1] = self.__wall
        self.maze[starting_height + 1][starting_width] = self.__wall

        self.generate_path()

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

    def surrounding_cells(self, rand_wall):
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

    def check_left_wall(self, rand_wall):
        if (rand_wall[1] != 0) and (
                self.maze[rand_wall[0]][rand_wall[1] - 1] == self.__null and self.maze[rand_wall[0]][
            rand_wall[1] + 1] == self.__floor):
            # Find the number of surrounding cells
            s_cells = self.surrounding_cells(rand_wall)
            if s_cells < 2:
                # Denote the new path
                self.maze[rand_wall[0]][rand_wall[1]] = self.__floor

                # Mark the new walls
                # Upper cell
                self.upper_wall(rand_wall)
                # Bottom cell
                self.bottom_wall(rand_wall)
                # Leftmost cell
                self.left_wall(rand_wall)

            # Delete wall
            self.delete_wall(rand_wall)

            return True
        return False

    def check_upper_wall(self, rand_wall):
        if (rand_wall[0] != 0) and (
                self.maze[rand_wall[0] - 1][rand_wall[1]] == self.__null and self.maze[rand_wall[0] + 1][
            rand_wall[1]] == self.__floor):

            s_cells = self.surrounding_cells(rand_wall)
            if s_cells < 2:
                # Denote the new path
                self.maze[rand_wall[0]][rand_wall[1]] = self.__floor

                # Mark the new walls
                # Upper cell
                self.upper_wall(rand_wall)

                # Leftmost cell
                self.left_wall(rand_wall)

                # Rightmost cell
                self.right_wall(rand_wall)

            # Delete wall
            self.delete_wall(rand_wall)

            return True
        return False

    def check_bottom_wall(self, rand_wall):
        if (rand_wall[0] != self.height - 1) and (
                self.maze[rand_wall[0] + 1][rand_wall[1]] == self.__null and self.maze[rand_wall[0] - 1][
            rand_wall[1]] == self.__floor):

            s_cells = self.surrounding_cells(rand_wall)
            if s_cells < 2:
                # Denote the new path
                self.maze[rand_wall[0]][rand_wall[1]] = self.__floor

                # Mark the new walls
                self.bottom_wall(rand_wall)
                self.left_wall(rand_wall)
                self.right_wall(rand_wall)

            # Delete wall
            self.delete_wall(rand_wall)

            return True
        return False

    def check_right_wall(self, rand_wall):
        if (rand_wall[1] != self.width - 1) and (
                self.maze[rand_wall[0]][rand_wall[1] + 1] == self.__null and self.maze[rand_wall[0]][
            rand_wall[1] - 1] == self.__floor):

            s_cells = self.surrounding_cells(rand_wall)
            if s_cells < 2:
                # Denote the new path
                self.maze[rand_wall[0]][rand_wall[1]] = self.__floor

                # Mark the new walls
                self.right_wall(rand_wall)
                self.bottom_wall(rand_wall)
                self.upper_wall(rand_wall)

            # Delete wall
            self.delete_wall(rand_wall)

            return True
        return False

    def upper_wall(self, rand_wall):
        if rand_wall[0] != 0:
            if self.maze[rand_wall[0] - 1][rand_wall[1]] != self.__floor:
                self.maze[rand_wall[0] - 1][rand_wall[1]] = self.__wall
            if [rand_wall[0] - 1, rand_wall[1]] not in self.__walls:
                self.__walls.append([rand_wall[0] - 1, rand_wall[1]])

    def bottom_wall(self, rand_wall):
        if rand_wall[0] != self.height - 1:
            if self.maze[rand_wall[0] + 1][rand_wall[1]] != self.__floor:
                self.maze[rand_wall[0] + 1][rand_wall[1]] = self.__wall
            if [rand_wall[0] + 1, rand_wall[1]] not in self.__walls:
                self.__walls.append([rand_wall[0] + 1, rand_wall[1]])

    def right_wall(self, rand_wall):
        if rand_wall[1] != self.width - 1:
            if self.maze[rand_wall[0]][rand_wall[1] + 1] != self.__floor:
                self.maze[rand_wall[0]][rand_wall[1] + 1] = self.__wall
            if [rand_wall[0], rand_wall[1] + 1] not in self.__walls:
                self.__walls.append([rand_wall[0], rand_wall[1] + 1])

    def left_wall(self, rand_wall):
        if rand_wall[1] != 0:
            if self.maze[rand_wall[0]][rand_wall[1] - 1] != self.__floor:
                self.maze[rand_wall[0]][rand_wall[1] - 1] = self.__wall
            if [rand_wall[0], rand_wall[1] - 1] not in self.__walls:
                self.__walls.append([rand_wall[0], rand_wall[1] - 1])

    def delete_wall(self, rand_wall):
        # Delete the wall from the list anyway
        for element in self.__walls:
            if element[0] == rand_wall[0] and element[1] == rand_wall[1]:
                self.__walls.remove(element)

    def generate_path(self):
        while self.__walls:
            # Pick a random wall
            rand_wall = self.__walls[int(random.random() * len(self.__walls)) - 1]
            if self.check_left_wall(rand_wall):
                continue
            if self.check_upper_wall(rand_wall):
                continue
            if self.check_bottom_wall(rand_wall):
                continue
            if self.check_right_wall(rand_wall):
                continue
            self.delete_wall(rand_wall)

        for i in range(0, self.height):
            for j in range(0, self.width):
                if self.maze[i][j] == self.__null:
                    self.maze[i][j] = self.__wall
        self.create_end()
        self.create_start()

    def create_end(self):
        while True:
            i = random.randrange(self.width)
            if self.maze[1][i] == self.__floor:
                self.maze[0][i] = [self.__floor, self.__end]
                self.end_point = i
                break

    def create_start(self):
        while True:
            i = random.randrange(self.width)
            if self.maze[self.height - 2][i] == self.__floor:
                self.maze[self.height - 1][i] = [self.__floor, self.__start]
                self.start_point = i
                break

    # Print final maze
