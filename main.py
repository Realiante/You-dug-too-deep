import gui
from gui import *

running = True

draw_startMenu()

gui.state = States.main_menu

while running:
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos

    if gui.state == States.main_menu:
        gui.listen_startMenu(events)
        if gui.state == States.main_menu:
            gui.display_startMenu()
    elif gui.state == States.options_menu:
        gui.listen_options(events)
        if gui.state == States.options_menu:
            gui.display_options()

    pygame.display.update()
