import pygame
import map

# TODO: a position relative to the screen, ie the viewport is centered
class Viewport:
    # width and height is in tiles
    def __init__(self, player, width, height):
        self.player = player

        self.width = width
        self.height = height
        self.x_offset = 0
        self.y_offset = 0


    def update_view(self):
        player_x = self.player.stats.x
        player_y = self.player.stats.y

        if player_x <= (self.width / 2):
            self.x_offset = 0
        elif player_x > (map.map_width - (self.width / 2)):
            self.x_offset = map.map_width - self.width
        else:
            self.x_offset = player_x - (self.width / 2)

        if player_y <= (self.height / 2):
            self.y_offset = 0
        elif player_y > (map.map_height - (self.height / 2)):
            self.y_offset = map.map_height - self.height
        else:
            self.y_offset = player_y - (self.height / 2)


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
