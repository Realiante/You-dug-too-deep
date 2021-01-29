from enum import Enum

import pygame
import pygame_widgets
import thorpy

menu_button_start: thorpy.make_button

menu_button_start1: pygame_widgets.Button
menu_button_options: pygame_widgets.Button
menu_button_exit: pygame_widgets.Button

options_slider_volume: thorpy.SliderX
options_label_volume: thorpy.Element

options_textbox_player1: thorpy.make_textbox
options_label_player1: thorpy.Element
options_textbox_player2: thorpy.make_textbox
options_label_player2: thorpy.Element
options_slider_items: thorpy.SliderX
options_label_items: thorpy.Element
options_slider_speed: thorpy.SliderX
options_label_speed: thorpy.Element
options_slider_protection: thorpy.SliderX
options_label_protection: thorpy.Element
options_button_back: thorpy.Element

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
        maze_stack_player1_items[i] = pygame.Rect(50 + 100 * i, 750, 100, 100)
        maze_stack_player2_items[i] = pygame.Rect(850 + 100 * i, 750, 100, 100)


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
        pygame.draw.rect(screen, 'Gray60', maze_stack_player2_items[i])


def draw_startMenu():
    global screenHeight, screenWidth, screen, state, menu_button_start, menu_button_exit, menu_button_options

    state = States.main_menu

    screen.fill(pygame.Color('gray16'))

    btnWidth = int(screenWidth / 5)
    btnHeight = int(screenHeight / 12)

    # menu_button_start = thorpy.make_image_button('Start')  ========================================================================

    menu_button_options = pygame_widgets.Button(screen, int(screenWidth * 0.5 - btnWidth * 0.5),
                                                int(screenHeight * 0.5 - btnHeight * 0.5), btnWidth, btnHeight,
                                                text='Options',
                                                onClick=lambda: draw_options())

    menu_button_exit = pygame_widgets.Button(screen, int(screenWidth * 0.5 - btnWidth * 0.5),
                                             int(screenHeight * 0.75 - btnHeight * 0.5), btnWidth, btnHeight,
                                             text='Exist',
                                             onClick=lambda: exit())


def try_draw_startMenu(event, btn):
    if event.el == btn:
        draw_startMenu()


def draw_options():
    global screenHeight, screenWidth, screen, state, options_slider_volume, options_label_volume, \
        options_textbox_player1, options_label_player2, options_slider_items, options_label_items, \
        options_slider_speed, options_label_speed, options_slider_protection, options_label_protection, \
        options_button_back, options_label_player1, options_textbox_player2

    state = States.options_menu

    screen.fill(pygame.Color('gray16'))

    boxWidth = int(screenWidth / 5)
    boxHeight = int(screenHeight / 12)

    spacing = [0.13, 0.3, 0.45, 0.6, 0.7, 0.8, 0.9]
    # spacing for the different widgets by order, excluding volume due to its calculation.

    options_slider_volume = thorpy.SliderX(length=boxWidth, limvals=(0, 100), text="", type_=int)
    options_label_volume = thorpy.make_text(text="Master Volume:")

    options_textbox_player1 = thorpy.Inserter(name="", value="Player 1")
    options_label_player1 = thorpy.make_text(text="Player 1 nickname:")
    options_textbox_player2 = thorpy.Inserter(name="", value="Player 2")
    options_label_player2 = thorpy.make_text(text="Player 2 nickname:")
    options_slider_items = thorpy.SliderX(length=boxWidth, limvals=(0, 8), text="", type_=int)
    options_label_items = thorpy.make_text(text="Starting items: ")
    options_slider_speed = thorpy.SliderX(length=boxWidth, limvals=(0, 3), text="", type_=int)
    options_label_speed = thorpy.make_text(text="Starting speed: ")
    options_slider_protection = thorpy.SliderX(length=boxWidth, limvals=(0, 2), text="", type_=int)
    options_label_protection = thorpy.make_text(text="Starting protection: ")
    options_button_back = thorpy.make_button(text="Back")


draw_options()


def display_options():
    # options_slider_volume.draw()
    background = thorpy.Background(color=(200, 255, 255),
                                   elements=[options_slider_volume, options_textbox_player1, options_label_player1,
                                             options_label_volume, options_textbox_player2, options_label_player2,
                                             options_slider_items, options_label_items, options_slider_speed,
                                             options_label_speed, options_slider_protection, options_label_protection,
                                             options_button_back])

    thorpy.store(background,
                 [options_slider_volume, options_textbox_player1, options_textbox_player2, options_slider_items,
                  options_slider_speed, options_slider_protection, ],
                 align="left")
    thorpy.store(background, [options_label_volume, options_label_player1, options_label_player2, options_label_items,
                              options_label_speed, options_label_protection],
                 align="right")
    thorpy.store(background, [options_button_back], y=screenHeight * 3 / 4)

    react = thorpy.Reaction(reacts_to=thorpy.constants.THORPY_EVENT,
                            reac_func=try_draw_startMenu,
                            event_args={"id": thorpy.constants.EVENT_UNPRESS},
                            params={"btn": options_button_back},
                            reac_name="on click event")

    background.add_reaction(react)

    menu = thorpy.Menu(background)
    menu.play()


def display_startMenu():
    menu_button_options.draw()
    menu_button_exit.draw()


def listen_startMenu(events):
    # menu_reaction_start = thorpy.Reaction(reacts_to=thorpy.constants.THORPY_EVENT,
    #                           reac_func=draw_maze(),
    #                            event_args={"id": thorpy.constants.EVENT_UNPRESS},
    #                            params=None,
    #                            reac_name="click start reaction")

    # menu_button_start.listen(events)
    menu_button_options.listen(events)
    menu_button_exit.listen(events)
