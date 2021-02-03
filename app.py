import background
import pygame

#  Initialisation script starts
pygame.init()
display = pygame.display.Info()
pygame.display.set_icon(pygame.image.load("ico.png"))
pygame.display.set_caption("You-Dug-Too-Deep")
display_size = (display.current_w, display.current_h)
flags = pygame.HWSURFACE | pygame.DOUBLEBUF
screen = pygame.display.set_mode(size=display_size, flags=flags)

# Initialisation script ends

dirty = True  # does the screen need to be updated
running = True

# Main game loop
while running:
    if dirty:
        screen.fill((0, 155, 0))
        screen.blit(background.get(display_size), (0, 0))
        pygame.display.flip()
        dirty = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
# Main game loop

pygame.quit()
