import pygame
import pygame.freetype
from classes.settings import *

if __name__ == '__main__':
    pygame.init()
    pygame.freetype.init()
    font1 = pygame.freetype.Font(None, 40)
    runing = False
    screen = pygame.display.set_mode([WIDHT, HEIGHT])
    while not runing:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                runing = True
        font1.render(screen, (200, 300), 'HELLLO', fgcolor=(250, 205, 204))
        pygame.display.flip()

    pygame.quit()
