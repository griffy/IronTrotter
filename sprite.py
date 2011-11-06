import os
import random
import pygame
import spritesheet

NONE = -1
UP = 0
DOWN = 1
LEFT = 2
RIGHT = 3

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
    def __init__(self, image_url, x, y, width=32, height=32, animated=False, direction=NONE, image_urls = []):
        pygame.sprite.Sprite.__init__(self)
        self.image_url = image_url
        self.image = load_image(image_url)
        self.width = width
        self.height = height
        self.rect = self.image.get_rect()
        self.rect.topleft = (x*32,y*32)
        self.animated = animated
        self.direction = direction
        self.dir_images = []
        
        if direction != NONE:
            for url in image_urls:
                self.dir_images.append(load_image(url))

        if animated:
            self.images = []
            sprites = spritesheet.Spritesheet(os.path.join('images', image_url))
            for i in range(0,6):
                self.images.append(sprites.image_at((i*32,i*32,32,32)))
            self.image = self.images[0]
            self.frame = 0

    def set_direction(self, direction):
        self.direction = direction
        self.image = self.dir_images[self.direction]

    def update(self, stats, viewport):
        self.rect.topleft = (stats.x*32 - (viewport.x_offset*32), stats.y*32 - (viewport.y_offset*32))
        if self.animated:
            self.frame = (self.frame + 1) % (len(self.images) - 1)
            self.image = self.images[self.frame]
