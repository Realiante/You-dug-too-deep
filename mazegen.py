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


visitedStartStep = []
visitedStart = []
queueStart = []

visitedEndStep = []
visitedEnd = []
queueEnd = []


def bfs(visited_step, visited, queue_step, node):
    queue = [node]
    visited.append(node)
    visited_step.append([node[0], node[1], 0])
    queue_step.append([node[0], node[1], 0])
    while queue:
        s = queue.pop(0)
        q = queue_step.pop(0)
        for neighbour in surrounding_bfs(s):
            if neighbour not in visited:
                visited.append(neighbour)
                visited_step.append([neighbour[0], neighbour[1], q[2] + 1])
                queue.append(neighbour)
                queue_step.append([neighbour[0], neighbour[1], q[2] + 1])
    visited.pop(0)
    visited_step.pop(0)


def surrounding_bfs(node):
    lst = []
    if node[0] != 0 and maze[node[0] - 1][node[1]] == __floor:
        lst.append([node[0] - 1, node[1]])
    if node[1] != 0 and maze[node[0]][node[1] - 1] == __floor:
        lst.append([node[0], node[1] - 1])
    if node[0] != __height - 1 and maze[node[0] + 1][node[1]] == __floor:
        lst.append([node[0] + 1, node[1]])
    if node[1] != __width - 1 and maze[node[0]][node[1] + 1] == __floor:
        lst.append([node[0], node[1] + 1])
    return lst


def remove_wall_around(node):
    if node[0] > 1:
        if maze[node[0] - 1][node[1]] == __wall and maze[node[0] - 2][node[1]] == __floor:
            maze[node[0] - 1][node[1]] = __null
            return
    if node[0] < __height - 2:
        if maze[node[0] + 1][node[1]] == __wall and maze[node[0] + 2][node[1]] == __floor:
            maze[node[0] + 1][node[1]] = __null
            return
    if node[1] > 1:
        if maze[node[0]][node[1] - 1] == __wall and maze[node[0]][node[1] - 2] == __floor:
            maze[node[0]][node[1] - 1] = __null
            return
    if node[1] < __width - 2:
        if maze[node[0]][node[1] + 1] == __wall and maze[node[0]][node[1] + 2] == __floor:
            maze[node[0]][node[1] + 1] = __null


generate_maze(5, 8)

bfs(visitedStartStep, visitedStart, queueStart, [__height - 1, __startPoint])
bfs(visitedEndStep, visitedEnd, queueEnd, [0, __endPoint])

closeEnd = []
closeStart = []

for i in range(len(visitedStart)):
    temp = visitedEnd.index(visitedStart[i])
    print(visitedStartStep[i][2], " ", visitedEndStep[temp][2])
    if visitedStartStep[i][2] > visitedEndStep[temp][2]:
        closeEnd.append(visitedEndStep[temp])
    else:
        closeStart.append(visitedStartStep[i])

__str__()

# Print final maze
