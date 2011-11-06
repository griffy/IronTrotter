import os
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
    def __init__(self, image_url, width=32, height=32, x=0, y=0, animated=False):
        pygame.sprite.Sprite.__init__(self)
        self.image_url = image_url
        self.image = load_image(image_url)
        self.width = width
        self.height = height
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)
        self.animated = animated

        if animated:
            self.images = []
            sprites = spritesheet.Spritesheet(os.path.join('images', image_url))
            for i in range(0,6):
                self.images.append(sprites.image_at((i*32,i*32,32,32)))
            self.image = self.images[0]
            self.frame = 0

    def update(self):
        if self.animated:
            self.frame = (self.frame + 1) % (len(self.images) - 1)
            self.image = self.images[self.frame]           

    #def draw(self):
    #    screen = pygame.display.get_surface()
    #    screen.blit(self.image, self.rect)
