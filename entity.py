import random
from sprite import Sprite
from stats import Stats

TYPES = [
    "sprites/char.png",
    "tiles/grass.png",
    #"tiles/wood.png"
]

CHAR = 0
GRASS = 1
WOOD = 2

TERRAIN = [
    GRASS,
    #WOOD
]

SOLID_TERRAIN = { WOOD }

ITEMS = [

]

LIVING_ENTITIES = [
    CHAR
]

def generate_terrain_entity(x, y):
    type = TERRAIN[random.randint(0, len(TERRAIN)-1)]
    stats = Stats(x, y)
    solid = False
    if type in SOLID_TERRAIN:
        solid = True
    return Entity(stats, type, solid)

def generate_item_entity(x, y):
    type = ITEMS[random.randint(0, len(ITEMS)-1)]
    stats = Stats(x, y)
    solid = False
    return Entity(stats, type, solid)

def generate_living_entity(x, y):
    type = LIVING_ENTITIES[random.randint(0, len(LIVING_ENTITIES)-1)]
    stats = Stats(x, y)
    solid = True
    return Entity(stats, type, solid)

class Entity:
    count = 0
    def __init__(self, stats, type, solid, id=None):
        if not id:
            self.id = Entity.count
            Entity.count += 1
        else:
            self.id = id
        self.stats = stats
        self.type = type
        self.sprite = Sprite(TYPES[self.type])
        self.solid = solid
