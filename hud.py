import font
import colors

class HUD:
    def __init__(self, player, width, height):
        self.player = player
        self.width = width
        self.height = height
        self.heading_font = font.Font("font/youmurdererbb_reg.ttf",
                                    50,
                                    fgcolor=colors.WHITE,
                                    bgcolor=colors.CLEAR)
        self.stats_font = font.Font("font/youmurdererbb_reg.ttf",
                                    30,
                                    fgcolor=colors.RED,
                                    bgcolor=colors.CLEAR)

    def draw(self):
        # TODO: Actually replace with the map name if there is one,
        #       otherwise just leave the title
        self.heading_font.draw(self.width/2-35, 25, "Iron Trotter - Map 1")
        self.stats_font.draw(self.width-50, 30, "X: " + str(self.player.stats.x))
        self.stats_font.draw(self.width-50, 60, "Y: " + str(self.player.stats.y))
        self.stats_font.draw(self.width-50, 90, "HP: " + str(self.player.stats.hp))
