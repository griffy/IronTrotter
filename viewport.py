import pygame

# TODO: a position relative to the screen, ie the viewport is centered
class Viewport:
    # width and height is in tiles
    def __init__(self, player, width, height):
        self.player = player
        self.width = width
        self.height = height

    def within_view(self, entity):
        player_x = self.player.stats.x
        player_y = self.player.stats.y
        entity_x = entity.stats.x
        entity_y = entity.stats.y

        # FIXME: This assumes the player is always in the middle of the
        #        viewport
        if (abs(entity_x - player_x) <= (self.width / 2)) and \
           (abs(entity_y - player_y) <= (self.height / 2)):
            return True
        return False
