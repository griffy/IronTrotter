import pygame
import entity

def makeMapFromFile(url):
    pass

# width and height are in tiles
def generate_map(width, height):
    terrain_layer = _generate_terrain_layer(width, height)
    items_layer = _generate_items_layer(terrain_layer)
    entities_layer = _generate_living_entities_layer(terrain_layer,
                                                     items_layer)
    return Map(width, height, [terrain_layer, items_layer, entities_layer])

def _generate_terrain_layer(width, height):
    terrain_layer = MapLayer(width, height)
    for x in range(width):
        for y in range(height):
            entity = entity.generate_terrain_entity(x, y)
            terrain_layer.add(entity)
    return terrain_layer

def _generate_items_layer(terrain_layer):
    items_layer = MapLayer(width, height)
    for x in range(width):
        for y in range(height):
            if not terrain_layer.get(x, y).solid:
                if random.randint(1, 10) == 1:
                    entity = entity.generate_item_entity(x, y)
                    items_layer.add(entity)
    return items_layer

def _generate_living_entities_layer(terrain_layer, items_layer):
    entities_layer = MapLayer(width, height)
    for x in range(width):
        for y in range(height):
            if not items_layer.get(x, y) and not terrain_layer.get(x, y).solid:
                if random.randint(1, 10) == 1:
                    entity = entity.generate_living_entity(x, y)
                    entities_layer.add(entity)
    return entities_layer


class MapLayer:
    def __init__(self, width, height, map_url=None):
        self.width = width
        self.height = height
        self.group = pygame.sprite.Group()
        if map_url:
            self.load(map_url)

    def draw(self):
        self.group.draw(pygame.display.get_surface())

    def add(self, entity):
        entity.sprite.add(self.group)

    def get(self, x, y):
        for entity in group:
                if entity.sprite.rect.center == (x,y):
                    return entity
        return None

class Map:
    def __init__(self, width, height, layers):
        self.layers = layers

    def draw(self):
        for layer in layers:
            layer.draw()

    def save(self):
        pass

    def load(self, url):
        pass
