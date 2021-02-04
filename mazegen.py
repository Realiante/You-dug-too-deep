import random
import enum
import time
from colorama import init
from colorama import Fore, Back, Style

MazeObjects = enum.Enum('MazeObjects', 'wall floor null key')
floor = 'f'
start = 'start'
wall = 'w'
key = 'key'
end = 'end'
null = 'null'
endPoint = None
startPoint = None


def printMaze(maze):
    for i in range(0, height):
        for j in range(0, width):
            if maze[i][j] == null:
                print(Fore.WHITE + '#', end=" ")
            elif maze[i][j] == floor:
                print(Fore.GREEN + 'f', end=" ")
            elif maze[i][j] == [floor, start]:
                print(Fore.CYAN + 'o', end=" ")
            elif maze[i][j] == [floor, end]:
                print(Fore.CYAN + 'O', end=" ")
            else:
                print(Fore.RED + 'w', end=" ")

        print('\n')


def surroundingCells(rand_wall):
    s_cells = 0
    if (maze[rand_wall[0] - 1][rand_wall[1]] == floor):
        s_cells += 1
    if (maze[rand_wall[0] + 1][rand_wall[1]] == floor):
        s_cells += 1
    if (maze[rand_wall[0]][rand_wall[1] - 1] == floor):
        s_cells += 1
    if (maze[rand_wall[0]][rand_wall[1] + 1] == floor):
        s_cells += 1

    return s_cells


cell = floor
unvisited = null
height = 11
width = 27
maze = []

for i in range(0, height):
    line = []
    for j in range(0, width):
        line.append(unvisited)
    maze.append(line)

starting_height = int(random.random() * height)
starting_width = int(random.random() * width)
if (starting_height == 0):
    starting_height += 1
if (starting_height == height - 1):
    starting_height -= 1
if (starting_width == 0):
    starting_width += 1
if (starting_width == width - 1):
    starting_width -= 1

maze[starting_height][starting_width] = cell
walls = []
walls.append([starting_height - 1, starting_width])
walls.append([starting_height, starting_width - 1])
walls.append([starting_height, starting_width + 1])
walls.append([starting_height + 1, starting_width])

# Denote walls in maze
maze[starting_height - 1][starting_width] = wall
maze[starting_height][starting_width - 1] = wall
maze[starting_height][starting_width + 1] = wall
maze[starting_height + 1][starting_width] = wall

while (walls):
    # Pick a random wall
    rand_wall = walls[int(random.random() * len(walls)) - 1]

    # Check if it is a left wall
    if (rand_wall[1] != 0):
        if (maze[rand_wall[0]][rand_wall[1] - 1] == null and maze[rand_wall[0]][
            rand_wall[1] + 1] == floor):
            # Find the number of surrounding cells
            s_cells = surroundingCells(rand_wall)

            if (s_cells < 2):
                # Denote the new path
                maze[rand_wall[0]][rand_wall[1]] = floor

                # Mark the new walls
                # Upper cell
                if (rand_wall[0] != 0):
                    if (maze[rand_wall[0] - 1][rand_wall[1]] != floor):
                        maze[rand_wall[0] - 1][rand_wall[1]] = wall
                    if ([rand_wall[0] - 1, rand_wall[1]] not in walls):
                        walls.append([rand_wall[0] - 1, rand_wall[1]])

                # Bottom cell
                if (rand_wall[0] != height - 1):
                    if (maze[rand_wall[0] + 1][rand_wall[1]] != floor):
                        maze[rand_wall[0] + 1][rand_wall[1]] = wall
                    if ([rand_wall[0] + 1, rand_wall[1]] not in walls):
                        walls.append([rand_wall[0] + 1, rand_wall[1]])

                # Leftmost cell
                if (rand_wall[1] != 0):
                    if (maze[rand_wall[0]][rand_wall[1] - 1] != floor):
                        maze[rand_wall[0]][rand_wall[1] - 1] = wall
                    if ([rand_wall[0], rand_wall[1] - 1] not in walls):
                        walls.append([rand_wall[0], rand_wall[1] - 1])

            # Delete wall
            for wall in walls:
                if (wall[0] == rand_wall[0] and wall[1] == rand_wall[1]):
                    walls.remove(wall)

            continue

    # Check if it is an upper wall
    if (rand_wall[0] != 0):
        if (maze[rand_wall[0] - 1][rand_wall[1]] == null and maze[rand_wall[0] + 1][
            rand_wall[1]] == floor):

            s_cells = surroundingCells(rand_wall)
            if (s_cells < 2):
                # Denote the new path
                maze[rand_wall[0]][rand_wall[1]] = floor

                # Mark the new walls
                # Upper cell
                if (rand_wall[0] != 0):
                    if (maze[rand_wall[0] - 1][rand_wall[1]] != floor):
                        maze[rand_wall[0] - 1][rand_wall[1]] = wall
                    if ([rand_wall[0] - 1, rand_wall[1]] not in walls):
                        walls.append([rand_wall[0] - 1, rand_wall[1]])

                # Leftmost cell
                if (rand_wall[1] != 0):
                    if (maze[rand_wall[0]][rand_wall[1] - 1] != floor):
                        maze[rand_wall[0]][rand_wall[1] - 1] = wall
                    if ([rand_wall[0], rand_wall[1] - 1] not in walls):
                        walls.append([rand_wall[0], rand_wall[1] - 1])

                # Rightmost cell
                if (rand_wall[1] != width - 1):
                    if (maze[rand_wall[0]][rand_wall[1] + 1] != floor):
                        maze[rand_wall[0]][rand_wall[1] + 1] = wall
                    if ([rand_wall[0], rand_wall[1] + 1] not in walls):
                        walls.append([rand_wall[0], rand_wall[1] + 1])

            # Delete wall
            for wall in walls:
                if (wall[0] == rand_wall[0] and wall[1] == rand_wall[1]):
                    walls.remove(wall)

            continue

    # Check the bottom wall
    if (rand_wall[0] != height - 1):
        if (maze[rand_wall[0] + 1][rand_wall[1]] == null and maze[rand_wall[0] - 1][
            rand_wall[1]] == floor):

            s_cells = surroundingCells(rand_wall)
            if (s_cells < 2):
                # Denote the new path
                maze[rand_wall[0]][rand_wall[1]] = floor

                # Mark the new walls
                if (rand_wall[0] != height - 1):
                    if (maze[rand_wall[0] + 1][rand_wall[1]] != floor):
                        maze[rand_wall[0] + 1][rand_wall[1]] = wall
                    if ([rand_wall[0] + 1, rand_wall[1]] not in walls):
                        walls.append([rand_wall[0] + 1, rand_wall[1]])
                if (rand_wall[1] != 0):
                    if (maze[rand_wall[0]][rand_wall[1] - 1] != floor):
                        maze[rand_wall[0]][rand_wall[1] - 1] = wall
                    if ([rand_wall[0], rand_wall[1] - 1] not in walls):
                        walls.append([rand_wall[0], rand_wall[1] - 1])
                if (rand_wall[1] != width - 1):
                    if (maze[rand_wall[0]][rand_wall[1] + 1] != floor):
                        maze[rand_wall[0]][rand_wall[1] + 1] = wall
                    if ([rand_wall[0], rand_wall[1] + 1] not in walls):
                        walls.append([rand_wall[0], rand_wall[1] + 1])

            # Delete wall
            for wall in walls:
                if (wall[0] == rand_wall[0] and wall[1] == rand_wall[1]):
                    walls.remove(wall)

            continue

    # Check the right wall
    if (rand_wall[1] != width - 1):
        if (maze[rand_wall[0]][rand_wall[1] + 1] == null and maze[rand_wall[0]][
            rand_wall[1] - 1] == floor):

            s_cells = surroundingCells(rand_wall)
            if (s_cells < 2):
                # Denote the new path
                maze[rand_wall[0]][rand_wall[1]] = floor

                # Mark the new walls
                if (rand_wall[1] != width - 1):
                    if (maze[rand_wall[0]][rand_wall[1] + 1] != floor):
                        maze[rand_wall[0]][rand_wall[1] + 1] = wall
                    if ([rand_wall[0], rand_wall[1] + 1] not in walls):
                        walls.append([rand_wall[0], rand_wall[1] + 1])
                if (rand_wall[0] != height - 1):
                    if (maze[rand_wall[0] + 1][rand_wall[1]] != floor):
                        maze[rand_wall[0] + 1][rand_wall[1]] = wall
                    if ([rand_wall[0] + 1, rand_wall[1]] not in walls):
                        walls.append([rand_wall[0] + 1, rand_wall[1]])
                if (rand_wall[0] != 0):
                    if (maze[rand_wall[0] - 1][rand_wall[1]] != floor):
                        maze[rand_wall[0] - 1][rand_wall[1]] = wall
                    if ([rand_wall[0] - 1, rand_wall[1]] not in walls):
                        walls.append([rand_wall[0] - 1, rand_wall[1]])

            # Delete wall
            for wall in walls:
                if (wall[0] == rand_wall[0] and wall[1] == rand_wall[1]):
                    walls.remove(wall)

            continue

    # Delete the wall from the list anyway
    for wall in walls:
        if (wall[0] == rand_wall[0] and wall[1] == rand_wall[1]):
            walls.remove(wall)


for i in range(0, height):
    for j in range(0, width):
        if (maze[i][j] == null):
            maze[i][j] = wall


while True:
    i = random.randrange(width)
    if maze[1][i] == floor:
        maze[0][i] = [floor, end]
        endPoint = i
        break

while True:
    i = random.randrange(width)
    if maze[height - 2][i] == floor:
        maze[height - 1][i] = [floor, start]
        startPoint = i
        break

visitedStart = []
queueStart = []

visitedEnd = []
queueEnd = []




def bfs(visitedStep, queueStep, node):
    queue = [node]
    visited = [node]
    visitedStep.append([node[0], node[1], 0])
    queueStep.append([node[0], node[1], 0])
    while queue:
        s = queue.pop(0)
        q = queueStep.pop(0)
        print(s, end=" ")
        for neighbour in surroundingBfs(s):
            if neighbour not in visited:
                visited.append(neighbour)
                visitedStep.append([neighbour[0], neighbour[1], q[2] + 1])
                queue.append(neighbour)
                queueStep.append([neighbour[0], neighbour[1], q[2] + 1])


def surroundingBfs(node):
    lst = []
    print("?")
    if node[0] != 0:
        if maze[node[0] - 1][node[1]] == floor:
            lst.append([node[0] - 1, node[1]])
        print("?")
    if node[1] != 0:
        if maze[node[0]][node[1] - 1] == floor:
            lst.append([node[0], node[1] - 1])
        print("?")
    if node[0] != height - 1:
        if maze[node[0] + 1][node[1]] == floor:
            lst.append([node[0] + 1, node[1]])
        print("?")
    if node[1] != width - 1:
        if maze[node[0]][node[1] + 1] == floor:
            lst.append([node[0], node[1] + 1])
        print("?")
    return lst


bfs(visitedStart, queueStart, [0, startPoint])
bfs(visitedEnd, queueEnd, [height-1, endPoint])

# Print final maze
printMaze(maze)
