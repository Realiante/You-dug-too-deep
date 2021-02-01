import background
import pygame

#  Initialisation script starts
pygame.init()
display = pygame.display.Info()
pygame.display.set_icon(pygame.image.load("ico.png"))
pygame.display.set_caption("You-Dug-Too-Deep")
display_size = (display.current_w, display.current_h)
screen = pygame.display.set_mode(display_size)
pygame.draw.rect(screen, (78, 203, 245), (0, 0, 250, 500), 5)

# Initialisation script ends

dirty = True  # does the screen need to be updated
running = True

# Main game loop
while running:
    if dirty:
        screen.blit(background.get(display_size), (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    pygame.display.flip()
    pygame.display.update()
# Main game loop

pygame.quit()
