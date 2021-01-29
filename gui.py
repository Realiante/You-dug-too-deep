from enum import Enum

import pygame
import thorpy

menu_button_start: thorpy.make_button

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

States = Enum('States', 'main_menu game_page options_menu')
state = None

screenWidth = 1600
screenHeight = 900
screen = pygame.display.set_mode((screenWidth, screenHeight))
screen.fill(pygame.Color('gray16'))


def draw_maze():
    global screenHeight, screenWidth, screen, state
    state = States.game_page
    screen.fill(pygame.Color('gray16'))


def draw_start_menu():
    global screenHeight, screenWidth, screen, state, menu_button_start
    state = States.main_menu
    screen.fill(pygame.Color('gray16'))


def try_draw_start_menu(event, btn):
    if event.el == btn:
        draw_start_menu()


def draw_options():
    global screenHeight, screenWidth, screen, state, options_slider_volume, options_label_volume, \
        options_textbox_player1, options_label_player2, options_slider_items, options_label_items, \
        options_slider_speed, options_label_speed, options_slider_protection, options_label_protection, \
        options_button_back, options_label_player1, options_textbox_player2

    state = States.options_menu

    screen.fill(pygame.Color('gray16'))

    box_width = int(screenWidth / 5)

    options_slider_volume = thorpy.SliderX(length=box_width, limvals=(0, 100), text="", type_=int)
    options_label_volume = thorpy.make_text(text="Master Volume:")

    options_textbox_player1 = thorpy.Inserter(name="", value="Player 1")
    options_label_player1 = thorpy.make_text(text="Player 1 nickname:")
    options_textbox_player2 = thorpy.Inserter(name="", value="Player 2")
    options_label_player2 = thorpy.make_text(text="Player 2 nickname:")
    options_slider_items = thorpy.SliderX(length=box_width, limvals=(0, 8), text="", type_=int)
    options_label_items = thorpy.make_text(text="Starting items: ")
    options_slider_speed = thorpy.SliderX(length=box_width, limvals=(0, 3), text="", type_=int)
    options_label_speed = thorpy.make_text(text="Starting speed: ")
    options_slider_protection = thorpy.SliderX(length=box_width, limvals=(0, 2), text="", type_=int)
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
                            reac_func=try_draw_start_menu,
                            event_args={"id": thorpy.constants.EVENT_UNPRESS},
                            params={"btn": options_button_back},
                            reac_name="on click event")

    background.add_reaction(react)

    menu = thorpy.Menu(background)
    menu.play()

