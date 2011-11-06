import os
import random
import pygame
import spritesheet

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
    def __init__(self, image_url, x, y, width=32, height=32, animated=False):
        pygame.sprite.Sprite.__init__(self)
        self.image_url = image_url
        self.image = load_image(image_url)
        self.width = width
        self.height = height
        self.rect = self.image.get_rect()
        self.rect.topleft = (x*32,y*32)
        self.animated = animated

        if animated:
            self.images = []
            sprites = spritesheet.Spritesheet(os.path.join('images', image_url))
            for i in range(0,6):
                self.images.append(sprites.image_at((i*32,i*32,32,32)))
            self.image = self.images[0]
            self.frame = 0

    def update(self, stats):
        self.rect.topleft = (stats.x*32, stats.y*32)
        #self.rect.topleft = (self.rect.x + (random.randint(0,1) * -1) * 1, self.rect.y + (random.randint(0,1) * -1) * 1)
        if self.animated:
            self.frame = (self.frame + 1) % (len(self.images) - 1)
            self.image = self.images[self.frame]
