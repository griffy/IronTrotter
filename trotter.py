import sys
import pygame
import colors

pygame.init()

width, height = 800, 600

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Iron Trotter")
title = pygame.image.load("images/titleScreen.png")
titlerect = title.get_rect()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
	
	screen.blit(title, titlerect)
    pygame.display.flip()
	
