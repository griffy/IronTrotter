import os
import pygame

def load_image(name):
    fullname = os.path.join('images', name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error, message:
        print 'Cannot load image:', name
        raise SystemExit, message
    image = image.convert_alpha()
    return image

class Sprite(pygame.sprite.Sprite):
    def __init__(self, image_url, width=32, height=32, x=0, y=0):
        self.image_url = image_url
        self.image = load_image(image_url)
        self.width = width
        self.height = height
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)

    def update(self):
        pass

    #def draw(self):
    #    screen = pygame.display.get_surface()
    #    screen.blit(self.image, self.rect)
