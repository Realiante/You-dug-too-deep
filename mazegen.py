import random
import colorama

__floor = 'f'
__start = 'start'
__wall = 'w'
__key = 'key'
__end = 'end'
__null = 'null'
__endPoint = None
__startPoint = None
__height = None
__width = None
__walls = []
maze = []


def __str__():
    global maze
    for i in range(0, __height):
        for j in range(0, __width):
            if maze[i][j] == __null:
                print(colorama.Fore.WHITE + '#', end=" ")
            elif maze[i][j] == __floor:
                print(colorama.Fore.GREEN + 'f', end=" ")
            elif maze[i][j] == [__floor, __start]:
                print(colorama.Fore.CYAN + 'o', end=" ")
            elif maze[i][j] == [__floor, __end]:
                print(colorama.Fore.CYAN + 'O', end=" ")
            else:
                print(colorama.Fore.RED + 'w', end=" ")

        print('\n')


def surrounding_cells(rand_wall):
    s_cells = 0
    if maze[rand_wall[0] - 1][rand_wall[1]] == __floor:
        s_cells += 1
    if maze[rand_wall[0] + 1][rand_wall[1]] == __floor:
        s_cells += 1
    if maze[rand_wall[0]][rand_wall[1] - 1] == __floor:
        s_cells += 1
    if maze[rand_wall[0]][rand_wall[1] + 1] == __floor:
        s_cells += 1

    return s_cells


def generate_maze(height, width):
    global __height, __width, maze, __walls
    __height = height
    __width = width
    for _ in range(0, height):
        line = []
        for _ in range(0, width):
            line.append(__null)
        maze.append(line)

    starting_height = int(random.random() * height)
    starting_width = int(random.random() * width)
    if starting_height == 0:
        starting_height += 1
    if starting_height == height - 1:
        starting_height -= 1
    if starting_width == 0:
        starting_width += 1
    if starting_width == width - 1:
        starting_width -= 1

    maze[starting_height][starting_width] = __floor
    __walls.append([starting_height - 1, starting_width])
    __walls.append([starting_height, starting_width - 1])
    __walls.append([starting_height, starting_width + 1])
    __walls.append([starting_height + 1, starting_width])

    # Denote walls in maze
    maze[starting_height - 1][starting_width] = __wall
    maze[starting_height][starting_width - 1] = __wall
    maze[starting_height][starting_width + 1] = __wall
    maze[starting_height + 1][starting_width] = __wall

    generate_path()


def check_left_wall(rand_wall):
    if (rand_wall[1] != 0) and (
            maze[rand_wall[0]][rand_wall[1] - 1] == __null and maze[rand_wall[0]][rand_wall[1] + 1] == __floor):
        # Find the number of surrounding cells
        s_cells = surrounding_cells(rand_wall)
        if s_cells < 2:
            # Denote the new path
            maze[rand_wall[0]][rand_wall[1]] = __floor

            # Mark the new walls
            # Upper cell
            upper_wall(rand_wall)
            # Bottom cell
            bottom_wall(rand_wall)
            # Leftmost cell
            left_wall(rand_wall)

        # Delete wall
        delete_wall(rand_wall)

        return True
    return False


def check_upper_wall(rand_wall):
    if (rand_wall[0] != 0) and (
            maze[rand_wall[0] - 1][rand_wall[1]] == __null and maze[rand_wall[0] + 1][rand_wall[1]] == __floor):

        s_cells = surrounding_cells(rand_wall)
        if s_cells < 2:
            # Denote the new path
            maze[rand_wall[0]][rand_wall[1]] = __floor

            # Mark the new walls
            # Upper cell
            upper_wall(rand_wall)

            # Leftmost cell
            left_wall(rand_wall)

            # Rightmost cell
            right_wall(rand_wall)

        # Delete wall
        delete_wall(rand_wall)

        return True
    return False


def check_bottom_wall(rand_wall):
    if (rand_wall[0] != __height - 1) and (
            maze[rand_wall[0] + 1][rand_wall[1]] == __null and maze[rand_wall[0] - 1][rand_wall[1]] == __floor):

        s_cells = surrounding_cells(rand_wall)
        if s_cells < 2:
            # Denote the new path
            maze[rand_wall[0]][rand_wall[1]] = __floor

            # Mark the new walls
            bottom_wall(rand_wall)
            left_wall(rand_wall)
            right_wall(rand_wall)

        # Delete wall
        delete_wall(rand_wall)

        return True
    return False


def check_right_wall(rand_wall):
    if (rand_wall[1] != __width - 1) and (
            maze[rand_wall[0]][rand_wall[1] + 1] == __null and maze[rand_wall[0]][rand_wall[1] - 1] == __floor):

        s_cells = surrounding_cells(rand_wall)
        if s_cells < 2:
            # Denote the new path
            maze[rand_wall[0]][rand_wall[1]] = __floor

            # Mark the new walls
            right_wall(rand_wall)
            bottom_wall(rand_wall)
            upper_wall(rand_wall)

        # Delete wall
        delete_wall(rand_wall)

        return True
    return False


def upper_wall(rand_wall):
    if rand_wall[0] != 0:
        if maze[rand_wall[0] - 1][rand_wall[1]] != __floor:
            maze[rand_wall[0] - 1][rand_wall[1]] = __wall
        if [rand_wall[0] - 1, rand_wall[1]] not in __walls:
            __walls.append([rand_wall[0] - 1, rand_wall[1]])


def bottom_wall(rand_wall):
    if rand_wall[0] != __height - 1:
        if maze[rand_wall[0] + 1][rand_wall[1]] != __floor:
            maze[rand_wall[0] + 1][rand_wall[1]] = __wall
        if [rand_wall[0] + 1, rand_wall[1]] not in __walls:
            __walls.append([rand_wall[0] + 1, rand_wall[1]])


def right_wall(rand_wall):
    if rand_wall[1] != __width - 1:
        if maze[rand_wall[0]][rand_wall[1] + 1] != __floor:
            maze[rand_wall[0]][rand_wall[1] + 1] = __wall
        if [rand_wall[0], rand_wall[1] + 1] not in __walls:
            __walls.append([rand_wall[0], rand_wall[1] + 1])


def left_wall(rand_wall):
    if rand_wall[1] != 0:
        if maze[rand_wall[0]][rand_wall[1] - 1] != __floor:
            maze[rand_wall[0]][rand_wall[1] - 1] = __wall
        if [rand_wall[0], rand_wall[1] - 1] not in __walls:
            __walls.append([rand_wall[0], rand_wall[1] - 1])


def delete_wall(rand_wall):
    # Delete the wall from the list anyway
    for wall in __walls:
        if wall[0] == rand_wall[0] and wall[1] == rand_wall[1]:
            __walls.remove(wall)


def generate_path():
    while __walls:
        # Pick a random wall
        rand_wall = __walls[int(random.random() * len(__walls)) - 1]
        if check_left_wall(rand_wall):
            continue
        if check_upper_wall(rand_wall):
            continue
        if check_bottom_wall(rand_wall):
            continue
        if check_right_wall(rand_wall):
            continue
        delete_wall(rand_wall)

    for i in range(0, __height):
        for j in range(0, __width):
            if maze[i][j] == __null:
                maze[i][j] = __wall
    create_end()
    create_start()


def create_end():
    global __endPoint
    while True:
        i = random.randrange(__width)
        if maze[1][i] == __floor:
            maze[0][i] = [__floor, __end]
            __endPoint = i
            break


def create_start():
    global __startPoint
    while True:
        i = random.randrange(__width)
        if maze[__height - 2][i] == __floor:
            maze[__height - 1][i] = [__floor, __start]
            __startPoint = i
            break


generate_maze(8, 16)

__str__()

# Print final maze
