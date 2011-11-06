from twisted.internet import reactor, protocol

import sys

from stats import Stats
import pickle

from netclient import TrotterSubFactory

from twisted.internet.task import LoopingCall

import pygame
import colors
import map
import entity
from entity import is_boss, is_living, is_item, is_terrain
import font
import sound
import viewport

class Handler:
    def __init__(self, screen):
        self.title = pygame.image.load("images/titleScreen.png")
        self.titlerect = self.title.get_rect()

        self.screen = screen

        self.f = TrotterSubFactory(self)

        self.fontDrawer = font.Font("font/youmurdererbb_reg.ttf", 100, colors.RED)

        self.counter = 5
        self.drawText = False

        pygame.mixer.init()
        self.titleMusic = sound.Sound("music/severedfifth_endofdays.ogg")
        self.titleMusic.play()

        self.lc = LoopingCall(self.titleevent)
        self.lc.start(0.1)

        # create an empty map for the server to fill in at the lobby
        self.map = map.Map(800, 640)
        # ditto for player
        self.player = None
        # and viewport
        self.viewport = None

    def titleevent(self):
        global counter
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                reactor.stop()
            elif event.type == pygame.KEYDOWN:
                # --- KEY handlers go HERE ---
                if event.key == pygame.K_m:
                    print "c"
                elif event.key == pygame.K_RETURN:
                    self.titleMusic.stop()
                    print "DO A THING"
                    self.lc.stop()
                    self.lc = LoopingCall(self.lobbyevent)
                    self.lc.start(0.1)

                elif event.key == pygame.K_x:
                    pygame.event.post(pygame.event.Event(pygame.QUIT))

        self.screen.blit(self.title, self.titlerect)
        if self.counter == 0:
            self.drawText = not self.drawText
            self.counter = 5
        self.counter -= 1

        if self.drawText:
            self.fontDrawer.draw(400,450, "PRESS ENTER TO START")

        pygame.display.flip()

    def lobbyevent(self):
        # TODO: the below should be set after the server responds with updates
        #self.player = entity.Entity(Stats(0,0), entity.LIVING_ENTITIES[0], True, "Bob")
        #self.viewport = viewport.Viewport(self.player, 5, 5)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                reactor.stop()
            elif event.type == pygame.KEYDOWN:
                # --- KEY handlers go HERE ---
                if event.key == pygame.K_RETURN:
                    self.lc.stop()
                    self.lc = LoopingCall(self.gameevent)
                    self.lc.start(0.1)

                elif event.key == pygame.K_x:
                    pygame.event.post(pygame.event.Event(pygame.QUIT))

        self.screen.blit(self.title, self.titlerect)
        if self.counter == 0:
            self.drawText = not self.drawText
            self.counter = 5
        self.counter -= 1

        if self.drawText:
            self.fontDrawer.draw(400,450, "PRESS ENTER TO START")

        pygame.display.flip()

    def gameevent(self):
        # get user input and send to server
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.player_quit_game()
                reactor.stop()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    self.player_move_up()
                elif event.key == pygame.K_a:
                    self.player_move_left()
                elif event.key == pygame.K_s:
                    self.player_move_down()
                elif event.key == pygame.K_d:
                    self.player_move_right()
        # get server updates
        # apply them
        # for update in updates: handleUpdate(update)
        # draw updated
        self.map.draw_within(self.viewport)
        pygame.display.flip()

    def handleUpdate(self, update):
        entity = None
        if is_living(enttype) or name != "":
            entity = self.map.layers[2].getById(update.idnum)
        elif is_item(enttype):
            entity = self.map.layers[1].getById(update.idnum)
        elif is_terrain(enttype):
            entity = self.map.layers[0].getById(update.idnum)
        entity.stat = stat

    def player_quit_game(self):
        pass

    def player_move_up(self):
        if not self.map.is_entity_blocked_up(self.player):
            # update player, send to server
            self.player.stats.y -= 1
            self.f.transport.write(pickle.dumps(self.player.getUpdate()))

    def player_move_left(self):
        if not self.map.is_entity_blocked_left(self.player):
            # update player, send to server
            self.player.stats.x -= 1
            self.f.transport.write(pickle.dumps(self.player.getUpdate()))

    def player_move_right(self):
        if not self.map.is_entity_blocked_right(self.player):
            # update player, send to server
            self.player.stats.x += 1
            self.f.transport.write(pickle.dumps(self.player.getUpdate()))

    def player_move_down(self):
        if not self.map.is_entity_blocked_down(self.player):
            # update player, send to server
            self.player.stats.y += 1
            self.f.transport.write(pickle.dumps(self.player.getUpdate()))
