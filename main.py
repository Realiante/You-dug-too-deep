import gui
from gui import *

running = True

gui.draw_startMenu()

gui.state = States.main_menu

while running:
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            running = False

    if gui.state == States.main_menu:
        gui.listen_startMenu(events)
        if gui.state == States.main_menu:
            gui.display_startMenu()
    elif gui.state == States.options_menu:
        gui.display_options()
    elif gui.state == States.game_page:
        display_maze()
    pygame.display.update()
