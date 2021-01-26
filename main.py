import pygame
import pygame_widgets
from maze import maze
from enum import Enum

screenWidth = 1200
screenHeight = 900

menu_button_start: pygame_widgets.Button
menu_button_options: pygame_widgets.Button
menu_button_exit: pygame_widgets.Button

options_slider_volume: pygame_widgets.Slider
options_label_volume: pygame_widgets.Button
options_label_player1: pygame_widgets.Button
options_label_player2: pygame_widgets.Button
options_slider_items: pygame_widgets.Slider
options_label_items: pygame_widgets.Button
options_slider_speed: pygame_widgets.Slider
options_label_speed: pygame_widgets.Button
options_slider_protection: pygame_widgets.Slider
options_label_protection: pygame_widgets.Button
options_button_back: pygame_widgets.Button

pygame.init()

States = Enum('States', 'main_menu game_page options_menu')

state = None

screen = pygame.display.set_mode((screenWidth, screenHeight))

running = True

screen.fill(pygame.Color('gray16'))

print()


def exit():
    global running
    running = False


def draw_maze():
    global screenHeight, screenWidth, screen, state
    state = States.game_page
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
    global screenHeight, screenWidth, screen, state, menu_button_start, menu_button_exit, menu_button_options

    state = States.main_menu

    screen.fill(pygame.Color('gray16'))

    btnWidth = int(screenWidth / 5)
    btnHeight = int(screenHeight / 12)

    menu_button_start = pygame_widgets.Button(screen, int(screenWidth * 0.5 - btnWidth * 0.5),
                                              int(screenHeight * 0.25 - btnHeight * 0.5), btnWidth, btnHeight,
                                              text='Start',
                                              onClick=lambda: draw_maze())

    menu_button_options = pygame_widgets.Button(screen, int(screenWidth * 0.5 - btnWidth * 0.5),
                                                int(screenHeight * 0.5 - btnHeight * 0.5), btnWidth, btnHeight,
                                                text='Options',
                                                onClick=lambda: draw_options())

    menu_button_exit = pygame_widgets.Button(screen, int(screenWidth * 0.5 - btnWidth * 0.5),
                                             int(screenHeight * 0.75 - btnHeight * 0.5), btnWidth, btnHeight,
                                             text='Exist',
                                             onClick=lambda: exit())


def draw_options():
    global screenHeight, screenWidth, screen, state, options_slider_volume, options_label_volume, \
        options_label_player1, options_label_player2, options_slider_items, options_label_items, \
        options_slider_speed, options_label_speed, options_slider_protection, options_label_protection, \
        options_button_back

    state = States.options_menu

    screen.fill(pygame.Color('gray16'))

    boxWidth = int(screenWidth / 5)
    boxHeight = int(screenHeight / 12)

    spacing = [0.13, 0.3, 0.45, 0.6, 0.7, 0.8, 0.9]
    # spacing for the different widgets by order, excluding volume due to its calculation.

    options_slider_volume = pygame_widgets.Slider(screen, int(screenWidth * 0.5 - boxWidth * 0.5),
                                                  int(screenHeight * spacing[0] - boxHeight * 0.5), boxWidth,
                                                  int(boxHeight * 1.25),
                                                  min=0,
                                                  max=100, step=1, handleRadius=int(boxHeight * 0.45 * 1.25))
    options_label_volume = pygame_widgets.Button(screen, int(screenWidth * 0.2 - boxWidth * 0.5),
                                                 int(screenHeight * 0.14 - boxHeight * 0.5), boxWidth, boxHeight,
                                                 text='Master Volume: ' + str(options_slider_volume.getValue()),
                                                 onClick=lambda: {})
    options_label_player1 = pygame_widgets.Button(screen, int(screenWidth * 0.5 - boxWidth * 0.5),
                                                  int(screenHeight * spacing[1] - boxHeight * 0.5), boxWidth, boxHeight,
                                                  text='Player 1',
                                                  onClick=lambda: {})
    options_label_player2 = pygame_widgets.Button(screen, int(screenWidth * 0.5 - boxWidth * 0.5),
                                                  int(screenHeight * spacing[2] - boxHeight * 0.5), boxWidth, boxHeight,
                                                  text='Player 2',
                                                  onClick=lambda: {})
    options_slider_items = pygame_widgets.Slider(screen, int(screenWidth * 0.5 - boxWidth * 0.5),
                                                 int(screenHeight * spacing[3] - boxHeight * 0.5), boxWidth, boxHeight, min=0,
                                                 max=8, step=1, handleRadius=int(boxHeight * 0.45))
    options_label_items = pygame_widgets.Button(screen, int(screenWidth * 0.2 - boxWidth * 0.5),
                                                int(screenHeight * spacing[3] - boxHeight * 0.5), boxWidth, boxHeight,
                                                text='Starting Items: ' + str(options_slider_items.getValue()),
                                                onClick=lambda: {})
    options_slider_speed = pygame_widgets.Slider(screen, int(screenWidth * 0.5 - boxWidth * 0.5),
                                                 int(screenHeight * spacing[4] - boxHeight * 0.5), boxWidth, boxHeight, min=0,
                                                 max=3, step=1, handleRadius=int(boxHeight * 0.45))
    options_label_speed = pygame_widgets.Button(screen, int(screenWidth * 0.2 - boxWidth * 0.5),
                                                int(screenHeight * spacing[4] - boxHeight * 0.5), boxWidth, boxHeight,
                                                text='Starting Speed: ' + str(options_slider_speed.getValue()),
                                                onClick=lambda: {})
    options_slider_protection = pygame_widgets.Slider(screen, int(screenWidth * 0.5 - boxWidth * 0.5),
                                                      int(screenHeight * spacing[5] - boxHeight * 0.5), boxWidth, boxHeight,
                                                      min=0,
                                                      max=2, step=1, handleRadius=int(boxHeight * 0.45))
    options_label_protection = pygame_widgets.Button(screen, int(screenWidth * 0.2 - boxWidth * 0.5),
                                                     int(screenHeight * spacing[5] - boxHeight * 0.5), boxWidth, boxHeight,
                                                     text='Starting Protection: ' + str(
                                                         options_slider_protection.getValue()),
                                                     onClick=lambda: {})
    options_button_back = pygame_widgets.Button(screen, int(screenWidth * 0.5 - boxWidth * 0.5),
                                                int(screenHeight * spacing[6] - boxHeight * 0.5), boxWidth, boxHeight,
                                                text='Back',
                                                onClick=lambda: draw_startMenu())


def update_options():
    options_label_volume.text = options_label_volume.font.render(
        'Master Volume: ' + str(options_slider_volume.getValue()), True, (0, 0, 0))
    options_label_items.text = options_label_items.font.render(
        'Starting Items: ' + str(options_slider_items.getValue()), True, (0, 0, 0))
    options_label_speed.text = options_label_speed.font.render(
        'Starting Speed: ' + str(options_slider_speed.getValue()), True, (0, 0, 0))
    options_label_protection.text = options_label_protection.font.render(
        'Starting Protection: ' + str(options_slider_protection.getValue()), True, (0, 0, 0))


def display_options():
    update_options()
    options_slider_volume.draw()
    options_label_volume.draw()
    options_label_player1.draw()
    options_label_player2.draw()
    options_slider_items.draw()
    options_label_items.draw()
    options_slider_speed.draw()
    options_label_speed.draw()
    options_slider_protection.draw()
    options_label_protection.draw()
    options_button_back.draw()


def listen_options(events):
    options_slider_volume.listen(events)
    options_slider_items.listen(events)
    options_slider_speed.listen(events)
    options_slider_protection.listen(events)
    options_button_back.listen(events)


def display_startMenu():
    menu_button_start.draw()
    menu_button_options.draw()
    menu_button_exit.draw()


def listen_startMenu(events):
    menu_button_start.listen(events)
    menu_button_options.listen(events)
    menu_button_exit.listen(events)


draw_startMenu()
state = States.main_menu

while running:
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos

    if state == States.main_menu:
        listen_startMenu(events)
        if state == States.main_menu:
            display_startMenu()
    elif state == States.options_menu:
        listen_options(events)
        if state == States.options_menu:
            display_options()

    pygame.display.update()
