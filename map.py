import random
import pygame
from entity import generate_item_entity
from entity import generate_living_entity
from entity import generate_terrain_entity
from entity import generate_player_entity
from entity import Entity
from entity import is_living

map_height = 35
map_width = 45


def makeMapFromFile(url):
    pass

# width and height are in tiles
def generate_map(width, height):
    print "generating terrain"
    terrain_layer = _generate_terrain_layer(width, height)
    print "generating items"
    items_layer = _generate_items_layer(terrain_layer)
    print "generating entities"
    entities_layer = _generate_living_entities_layer(terrain_layer,
                                                     items_layer)
    return Map(width, height, [terrain_layer, items_layer, entities_layer])

def _generate_terrain_layer(width, height):
    terrain_layer = MapLayer(width, height)

    # figure out the map and floor tiles that we will be using
    maptype = random.randint(0,2)
    floor = 0
    if maptype == 2:
       floor = random.randint(0,8)

    for x in range(width):
        for y in range(height):
            entity = generate_terrain_entity(x, y, maptype, floor)
            terrain_layer.add(entity)
    return terrain_layer

def _generate_items_layer(terrain_layer):
    width = terrain_layer.width
    height = terrain_layer.height
    items_layer = MapLayer(width, height)
    for x in range(width):
        for y in range(height):
            if not terrain_layer.get(x, y).solid:
                if random.randint(1, 10) == 1:
                    entity = generate_item_entity(x, y)
                    items_layer.add(entity)
    return items_layer

def _generate_living_entities_layer(terrain_layer, items_layer):
    width = terrain_layer.width
    height = terrain_layer.height
    entities_layer = MapLayer(width, height)

    # TODO: based this on the number of players
    player_count = 0

    for x in range(width):
        for y in range(height):
            if not items_layer.get(x, y) and not terrain_layer.get(x, y).solid:
                if random.randint(1, 10) == 1:
                    entity = generate_living_entity(x, y)
                    entities_layer.add(entity)
                elif random.randint(1, 10) == 1 and player_count > 0:
                    entity = generate_player_entity(x, y)
                    entities_layer.add(entity)
                    player_count -= 1
    return entities_layer


class MapLayer:
    def __init__(self, width, height, map_url=None):
        self.width = width
        self.height = height
        self.group = pygame.sprite.Group()
        self.entities = []
        if map_url:
            self.load(map_url)

    def update(self, viewport):
        to_kill = []
        for i, entity in enumerate(self.entities):
            if entity.stats.hp <= 0:
                to_kill.append(i)
            else:
                entity.update(viewport)
        to_kill.reverse()
        for i in to_kill:
            self.entities[i].sprite.kill()
            self.entities.pop(i)

    def draw(self):
        self.group.draw(pygame.display.get_surface())

    def draw_within(self, viewport):
        visible_group = pygame.sprite.Group()
        for entity in self.entities:
            if viewport.within_view(entity):
                visible_group.add(entity.sprite)
        visible_group.draw(pygame.display.get_surface())

    def add(self, entity):
        self.group.add(entity.sprite)
        self.entities.append(entity)

    def get(self, x, y):
        for entity in self.entities:
            if entity.stats.x == x and entity.stats.y == y:
                return entity
        return None

    def getById(self, id_num):
        for entity in self.entities:
            if entity.id_num == id_num:
                return entity
        return None

    def has(self, entity):
        return self.group.has(entity.sprite)

class Map:
    def __init__(self, width, height, layers=None):
        self.width = width
        self.height = height
        self.layers = layers
        self.player_list = []
        if not layers:
            self.layers = [MapLayer(width, height),
                           MapLayer(width, height),
                           MapLayer(width, height)]

    def update(self, viewport):
        for layer in self.layers:
            layer.update(viewport)

    def draw(self):
        for layer in self.layers:
            layer.draw()

    def draw_within(self, viewport):
        for layer in self.layers:
            layer.draw_within(viewport)

    def save(self):
        pass

    def load(self, url):
        pass

    def get(self, x, y):
        for layer in self.layers:
            ent = layer.get(x, y)
            if ent != None:
                return ent
        return None

    def getById(self, id_num):
        for layer in self.layers:
            ent = layer.getById(id_num)
            if ent != None:
                return ent
        return None

    def item_under_entity(self, entity):
        for item in self.layers[1].entities:
            if item.stats.x == entity.stats.x and item.stats.y == entity.stats.y:
                return item
        return None

    def is_entity_blocked(self, new_x, new_y):
        terrain = self.layers[0].get(new_x, new_y)
        if terrain and terrain.solid:
            return True
        living = self.layers[2].get(new_x, new_y)
        if living and living.solid:
            return True
        return False

    def is_player_up(self, entity):
        for player in self.player_list:
            if player.stats.y < entity.stats.y:
                return True
        return False

    def is_player_down(self,entity):
        for player in self.player_list:
            if player.stats.y > entity.stats.y:
                return True
        return False

    def is_player_left(self, entity):
        for player in self.player_list:
            if player.stats.x < entity.stats.y:
                return True
        return False

    def is_player_right(self,entity):
        for player in self.player_list:
            if player.stats.x > entity.stats.y:
                return True
        return False

    def is_entity_blocked_up(self, entity):
        new_x = entity.stats.x
        new_y = entity.stats.y-1
        if new_y < 0:
            return True
        return self.is_entity_blocked(new_x, new_y)

    def is_entity_blocked_left(self, entity):
        new_x = entity.stats.x-1
        new_y = entity.stats.y
        if new_x < 0:
            return True
        return self.is_entity_blocked(new_x, new_y)

    def is_entity_blocked_right(self, entity):
        new_x = entity.stats.x+1
        new_y = entity.stats.y
        if new_x >= self.width:
            return True
        return self.is_entity_blocked(new_x, new_y)

    def is_entity_blocked_down(self, entity):
        new_x = entity.stats.x
        new_y = entity.stats.y+1
        if new_y >= self.height:
            return True
        return self.is_entity_blocked(new_x, new_y)

    def is_cleared(self):
        if len(self.layers[1].entities) > 0:
            return False
        for entity in self.layers[2].entities:
            if is_living(entity):
                return False
        return True

    def addPlayer(self, up):
        ent = Entity(up.stats,up.enttype,True,up.name,up.idnum)
        player_list.append(ent)
