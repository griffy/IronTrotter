import sys
import pygame
import colors

pygame.init()

width, height = 800, 600

screen = pygame.display.set_mode((width, height))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    screen.fill(colors.BLACK)
    pygame.display.flip()
