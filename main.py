import pygame
from maze import maze

screenWidth = 800
screenHeight = 600
button_start = None
button_exit = None
pygame.init()

screen = pygame.display.set_mode((screenWidth, screenHeight))

running = True

screen.fill(pygame.Color('gray16'))

print()


def draw_maze():
    global screenHeight, screenWidth, screen
    screen.fill(pygame.Color('gray16'))
    smth = int(screenHeight * 0.9 / len(maze))
    # give this a name lol
    for x in range(len(maze)):
        for y in range(len(maze[x])):
            if maze[y][x] == 1:
                pygame.draw.rect(screen, pygame.Color('black'),
                                 pygame.Rect(int(screenWidth * 0.15) + (x * smth),
                                             int(screenHeight * 0.05) + (y * smth), smth - 1, smth - 1))
            elif maze[y][x] == 0:
                pygame.draw.rect(screen, pygame.Color('white'),
                                 pygame.Rect(int(screenWidth * 0.15) + (x * smth),
                                             int(screenHeight * 0.05) + (y * smth), smth - 1, smth - 1))


def draw_startMenu():
    global screenHeight, screenWidth, screen, button_start, button_exit

    btnWidth = int(screenWidth/10)
    btnHeight = int(screenHeight / 10)

    button_start = pygame.Rect(int(screenWidth * 0.5 - btnWidth * 0.5), int(screenHeight * 0.33 - btnHeight * 0.5), btnWidth, btnHeight)
    button_exit = pygame.Rect(int(screenWidth * 0.5 - btnWidth * 0.5), int(screenHeight * 0.66 - btnHeight * 0.5), btnWidth, btnHeight)

    pygame.draw.rect(screen, pygame.Color('green'), button_start)
    pygame.draw.rect(screen, pygame.Color('red'), button_exit)

draw_startMenu()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos

            if button_start.collidepoint(mouse_pos):
                draw_maze()
            if button_exit.collidepoint(mouse_pos):
                running = False

    pygame.display.update()

