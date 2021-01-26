import math
from enum import Enum

import pygame
import pygame_widgets

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

maze_label_player1_speed: pygame_widgets.Button
maze_label_player2_speed: pygame_widgets.Button
maze_label_player1_protection: pygame_widgets.Button
maze_label_player2_protection: pygame_widgets.Button
maze_label_player1_health: pygame_widgets.Button
maze_label_player2_health: pygame_widgets.Button
maze_rect_player1_gameCover: pygame.Rect
maze_rect_player2_gameCover: pygame.Rect
maze_stack_player1_items = [None] * 7
maze_stack_player2_items = [None] * 7

pygame.init()

States = Enum('States', 'main_menu game_page options_menu')

state = None

screenWidth = 1600
screenHeight = 900

screen = pygame.display.set_mode((screenWidth, screenHeight))

screen.fill(pygame.Color('gray16'))


def draw_maze():
    global screenHeight, screenWidth, screen, state, maze_label_player1_speed, maze_label_player2_speed, \
        maze_label_player1_protection, maze_label_player2_protection, maze_label_player1_health, \
        maze_label_player2_health, maze_rect_player1_gameCover, maze_rect_player2_gameCover, maze_stack_player1_items, \
        maze_stack_player2_items

    state = States.game_page

    screen.fill(pygame.Color('gray16'))

    spacing = [0.1, 0.6]

    maze_label_player1_speed = pygame_widgets.Button(screen, 50, 50, 150, 150,
                                                     text='SPD: ' + str(options_slider_speed.getValue()),
                                                     radius=100,
                                                     onClick=lambda: {})
    maze_label_player2_speed = pygame_widgets.Button(screen, 850, 50, 150, 150,
                                                     text='SPD: ' + str(options_slider_speed.getValue()),
                                                     radius=100,
                                                     onClick=lambda: {})
    maze_label_player1_protection = pygame_widgets.Button(screen, 200, 50, 150, 150,
                                                          text='DEF: ' + str(options_slider_protection.getValue()),
                                                          radius=100,
                                                          onClick=lambda: {})
    maze_label_player2_protection = pygame_widgets.Button(screen, 1000, 50, 150, 150,
                                                          text='DEF: ' + str(options_slider_protection.getValue()),
                                                          radius=100,
                                                          onClick=lambda: {})
    maze_label_player1_health = pygame_widgets.Button(screen, 350, 50, 400, 150,
                                                      text='Player 1 HP',
                                                      inactiveColour='DarkGreen',
                                                      onClick=lambda: {})
    maze_label_player2_health = pygame_widgets.Button(screen, 1150, 50, 400, 150,
                                                      text='Player 2 HP',
                                                      inactiveColour='DarkGreen',
                                                      onClick=lambda: {})
    maze_rect_player1_gameCover = pygame.Rect(50, 200, 700, 550)
    maze_rect_player2_gameCover = pygame.Rect(850, 200, 700, 550)
    for i in range(7):
        maze_stack_player1_items[i] = pygame.Rect(50+100*i, 750, 100, 100)
        maze_stack_player2_items[i] = pygame.Rect(850+100*i, 750, 100, 100)


def display_maze():
    maze_label_player1_speed.draw()
    maze_label_player2_speed.draw()
    maze_label_player1_protection.draw()
    maze_label_player2_protection.draw()
    maze_label_player1_health.draw()
    maze_label_player2_health.draw()
    pygame.draw.rect(screen, 'Gray80', maze_rect_player1_gameCover)
    pygame.draw.rect(screen, 'Gray80', maze_rect_player2_gameCover)
    for i in range(7):
        pygame.draw.rect(screen, 'Gray60', maze_stack_player1_items[i])
        pygame.draw.line()
        pygame.draw.rect(screen, 'Gray60', maze_stack_player2_items[i])


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
                                                 int(screenHeight * spacing[3] - boxHeight * 0.5), boxWidth, boxHeight,
                                                 min=0,
                                                 max=8, step=1, handleRadius=int(boxHeight * 0.45))
    options_label_items = pygame_widgets.Button(screen, int(screenWidth * 0.2 - boxWidth * 0.5),
                                                int(screenHeight * spacing[3] - boxHeight * 0.5), boxWidth, boxHeight,
                                                text='Starting Items: ' + str(options_slider_items.getValue()),
                                                onClick=lambda: {})
    options_slider_speed = pygame_widgets.Slider(screen, int(screenWidth * 0.5 - boxWidth * 0.5),
                                                 int(screenHeight * spacing[4] - boxHeight * 0.5), boxWidth, boxHeight,
                                                 min=0,
                                                 max=3, step=1, handleRadius=int(boxHeight * 0.45))
    options_label_speed = pygame_widgets.Button(screen, int(screenWidth * 0.2 - boxWidth * 0.5),
                                                int(screenHeight * spacing[4] - boxHeight * 0.5), boxWidth, boxHeight,
                                                text='Starting Speed: ' + str(options_slider_speed.getValue()),
                                                onClick=lambda: {})
    options_slider_protection = pygame_widgets.Slider(screen, int(screenWidth * 0.5 - boxWidth * 0.5),
                                                      int(screenHeight * spacing[5] - boxHeight * 0.5), boxWidth,
                                                      boxHeight,
                                                      min=0,
                                                      max=2, step=1, handleRadius=int(boxHeight * 0.45))
    options_label_protection = pygame_widgets.Button(screen, int(screenWidth * 0.2 - boxWidth * 0.5),
                                                     int(screenHeight * spacing[5] - boxHeight * 0.5), boxWidth,
                                                     boxHeight,
                                                     text='Starting Protection: ' + str(
                                                         options_slider_protection.getValue()),
                                                     onClick=lambda: {})
    options_button_back = pygame_widgets.Button(screen, int(screenWidth * 0.5 - boxWidth * 0.5),
                                                int(screenHeight * spacing[6] - boxHeight * 0.5), boxWidth, boxHeight,
                                                text='Back',
                                                onClick=lambda: draw_startMenu())


draw_options()


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
