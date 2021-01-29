import gui
from gui import States
import pygame

pygame.init()

running = True
gui.draw_start_menu()
gui.state = States.main_menu

while running:
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            running = False

    if gui.state == States.main_menu:
        gui.listen_start_menu(events)
        if gui.state == States.main_menu:
            gui.display_start_menu()
    elif gui.state == States.options_menu:
        gui.display_options()
    elif gui.state == States.game_page:
        gui.display_maze()
    pygame.display.update()
