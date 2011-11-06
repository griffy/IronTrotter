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
from entity import Entity
from entity import is_boss, is_living, is_player, is_item, is_terrain, is_solid_terrain
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
        self.map = map.Map(10, 10)
        self.player = None

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
        moved = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.player_quit_game()
                reactor.stop()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    moved = self.player_move_up()
                elif event.key == pygame.K_a:
                    moved =self.player_move_left()
                elif event.key == pygame.K_s:
                    moved = self.player_move_down()
                elif event.key == pygame.K_d:
                    moved = self.player_move_right()
        if moved:
            self.pickup_item()

        # draw updated
        self.map.draw_within(self.viewport)
        pygame.display.flip()

    # called when we receive Updates from the server
    def handleUpdate(self, update):
        if update.idnum == 0:
            return
        entity = None
        if is_living(update.enttype):
            entity = self.map.layers[2].getById(update.idnum)
            if entity is None:
                entity = Entity(update.stats, update.enttype,
                                       True, update.name, update.idnum)
                self.map.layers[2].add(entity)

        elif is_player(update.enttype):
            entity = self.map.layers[2].getById(update.idnum)
            if entity is None:
                entity = Entity(update.stats, update.enttype,
                                       True, update.name, update.idnum)
                if self.player is None:
                    self.player = entity
                    self.viewport = viewport.Viewport(self.player, 5, 5)
                self.map.layers[2].add(entity)

        elif is_item(update.enttype):
            entity = self.map.layers[1].getById(update.idnum)
            if entity is None:
                entity = Entity(update.stats, update.enttype,
                                       False, update.name, update.idnum)
                self.map.layers[1].add(entity)
        elif is_terrain(update.enttype):
            entity = self.map.layers[0].getById(update.idnum)
            if entity is None:
                entity = Entity(update.stats, update.enttype,
                                       is_solid_terrain(update.enttype),
                                       update.name, update.idnum)
                self.map.layers[0].add(entity)
        entity.stats = update.stats

    def pickup_item(self):
        item = self.map.item_under_entity(self.player)
        if item:
            item.stats.hp = 0
            self.f.transport.write(pickle.dumps(item.getUpdate()))
            # remove the item entity

    def player_quit_game(self):
        # set the player's health to 0 "killing" it
        # update the server
        self.player.stats.hp = 0
        self.f.transport.write(pickle.dumps(self.player.getUpdate()))

    def player_move_up(self):
        if not self.map.is_entity_blocked_up(self.player):
            # update player, send to server
            self.player.stats.y -= 1
            self.f.transport.write(pickle.dumps(self.player.getUpdate()))
            return True
        return False

    def player_move_left(self):
        if not self.map.is_entity_blocked_left(self.player):
            # update player, send to server
            self.player.stats.x -= 1
            self.f.transport.write(pickle.dumps(self.player.getUpdate()))
            return True
        return False

    def player_move_right(self):
        if not self.map.is_entity_blocked_right(self.player):
            # update player, send to server
            self.player.stats.x += 1
            self.f.transport.write(pickle.dumps(self.player.getUpdate()))
            return True
        return False

    def player_move_down(self):
        if not self.map.is_entity_blocked_down(self.player):
            # update player, send to server
            self.player.stats.y += 1
            self.f.transport.write(pickle.dumps(self.player.getUpdate()))
            return True
        return False
