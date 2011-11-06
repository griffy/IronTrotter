import pygame
import map

# TODO: a position relative to the screen, ie the viewport is centered
class Viewport:
    # width and height is in tiles
    def __init__(self, player, width, height):
        self.player = player

        self.width = width

        if width % 2 == 0:
            self.width +=1

        self.height = height

        if height % 2 == 0:
            self.height +=1


        self.halfW = (self.width -1) / 2
        self.halfH = (self.height -1) / 2
        self.x_offset = 0
        self.y_offset = 0


    def update_view(self):
        player_x = self.player.stats.x
        player_y = self.player.stats.y

        if player_x <= (self.halfW):
            self.x_offset = 0
        elif player_x >= (map.map_width - (self.halfW)):
            self.x_offset = map.map_width - self.width
        else:
            self.x_offset = player_x - (self.halfW)

        if player_y <= (self.halfH):
            self.y_offset = 0
        elif player_y >= (map.map_height - (self.halfH)):
            self.y_offset = map.map_height - self.height
        else:
            self.y_offset = player_y - (self.halfH)


    def within_view(self, entity):
        player_x = self.player.stats.x
        player_y = self.player.stats.y
        entity_x = entity.stats.x
        entity_y = entity.stats.y

        # FIXME: This assumes the player is always in the middle of the
        #        viewport
        if (entity_x >= self.x_offset and entity_x < (self.x_offset + self.width) and \
                entity_y >= self.y_offset and entity_y < (self.y_offset + self.height)):
            return True
        return False
