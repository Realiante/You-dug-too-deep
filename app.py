"""
@author: daniel.fedotov
@author: vel.krol
"""

import pygame
import thorpy
import gui

#  Initialisation script starts

pygame.init()
display = pygame.display.Info()
display_size = (display.current_w, display.current_h)
flags = pygame.HWSURFACE | pygame.DOUBLEBUF
application = thorpy.Application(size=display_size, caption="You-Dug-Too-Deep", center=True, flags=flags)
pygame.display.set_icon(pygame.image.load("ico.png"))

# Initialisation script ends

running = True

gui.init()
# Main game loop
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
# Main game loop

pygame.display.quit()
pygame.quit()
