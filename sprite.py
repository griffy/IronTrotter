import os
import random
import pygame
import spritesheet

NONE = -1
UP = 0
DOWN = 1
LEFT = 2
RIGHT = 3

UP_ANIMATE = 4
DOWN_ANIMATE = 5
LEFT_ANIMATE = 6
RIGHT_ANIMATE = 7

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
        self.image_urls = image_urls
        self.animate = False
        
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

    def do_animate(self):
        if self.direction == UP:
            self.direction = UP_ANIMATE
        elif self.direction == DOWN:
            self.direction = DOWN_ANIMATE
        elif self.direction == LEFT:
            self.direction = LEFT_ANIMATE
        else:
            self.direction = RIGHT_ANIMATE
        self.animate = True
        self.frame = 0

    def set_direction(self, direction):
        self.direction = direction
        self.image = self.dir_images[self.direction]

    def update(self, stats, viewport):
        self.rect.topleft = (stats.x*32 - (viewport.x_offset*32), stats.y*32 - (viewport.y_offset*32))
        if self.animate:
            sheet = spritesheet.Spritesheet("images/" + self.image_urls[self.direction])
            
            self.image = sheet.image_at((self.frame*32,0,32,32))
            self.frame += 1
            if self.frame > 6:
                self.animate = False
