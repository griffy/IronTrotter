def makeMapFromFile(url):

def generate():
    pass

def _generate_terrain():
    pass

class MapLayer:
    def __init__(self, sprites):
        self.group = pygame.sprite.Group()
        for sprite in sprites:
            sprite.add(self.group)
        #self.visible_group =

    def draw(self):
        pass
    def add(self, sprite):
        pass

class Map:
    def __init__(self, groups):
        self.groups = groups

    def draw(self):
        pass
    def save(self):
        pass
    def load(self, url):
        pass
