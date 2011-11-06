import stats

TYPES = [
    "char.png",
    "grass.png",
    "wood.png"
]

CHAR = 0
GRASS = 1
WOOD = 2

TERRAIN = [
    GRASS,
    WOOD
]

entity_count = 0

def generate_entity(x, y):
    type = random.randint(len(TYPES))
    id = entity_count
    entity_count += 1
    stats = stats.Stats(x, y)

def generate_terrain_entity(x, y):
    type = random.randint(0, len(TERRAIN))
    id = entity_count
    entity_count += 1
    stats = stats.Stats(x, y)

class Entity:
    count = 0
    def __init__(self, id, stats, type, solid=False):
        self.id = id
        self.stats = stats
        self.type = type
        self.sprite = Sprite(TYPES[self.type])
        self.solid = solid
