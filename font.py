import pygame
import colors

class Font:
    def __init__(self, font_url, font_size, fgcolor=colors.BLACK,
                 bgcolor=colors.CLEAR):
        self.font = pygame.font.Font(font_url, font_size)
        self.fgcolor = fgcolor
        self.bgcolor = bgcolor

    def draw(self, x, y, text):
        if self.bgcolor != colors.CLEAR:
            text_surf = self.font.render(text, True, self.fgcolor, self.bgcolor)
        else:
            text_surf = self.font.render(text, True, self.fgcolor)

        text_rect = text_surf.get_rect()
        text_rect.centerx = x
        text_rect.centery = y
        screen = pygame.display.get_surface()
        screen.blit(text_surf, text_rect)
