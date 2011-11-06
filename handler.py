from twisted.internet import reactor, protocol

import sys

from stats import Stats
import pickle

from netclient import TrotterSubFactory

from twisted.internet.task import LoopingCall

import random
from random import choice

import pygame
import colors
import map
import entity
from entity import Entity
from entity import is_boss, is_living, is_player, is_item, is_terrain, is_solid_terrain
import font
import sound
import viewport
import scores
import hud
import sprite

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
        pygame.mixer.pre_init(44100, -16, 2, 2048)
        self.titleMusic = sound.Sound("music/severedfifth_endofdays.ogg")
        self.titleMusic.play()

        musics = [
            "severedfifth_drilldown.ogg",
            "severedfifth_fightphilosophy.ogg",
            "severedfifth_machinesofwar.ogg",
            "severedfifth_repent.ogg",
            "severedfifth_endofdays.ogg",
            "severedfifth_foretoldrevelation.ogg",
            "severedfifth_theblackening.ogg",
            "severedfifth_fallout.ogg",
            "severedfifth_forgottenheroes.ogg",
            "severedfifth_politicold.ogg",
            "severedfifth_theyprey.ogg"
        ]

        self.gameMusic = pygame.mixer.Sound("music/"+choice(musics))
        self.attackSound = pygame.mixer.Sound("sounds/erdie__sword01.wav")
        self.ghastlySound = pygame.mixer.Sound("sounds/johnc__moan.wav")
        self.hurtSound = pygame.mixer.Sound("sounds/halleck__jacobsladdersingle2.mp3")

        self.lc = LoopingCall(self.titleevent)
        self.lc.start(0.1)

        self.hud = None
        # create an empty map for the server to fill in at the lobby
        self.map = map.Map(map.map_width, map.map_height)
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
                    self.gameMusic.play(-1)
                    print "DO A THING"
                    self.lc.stop()
                    self.lc = LoopingCall(self.lobbyevent)
                    self.lc.start(0.1)

                elif event.key == pygame.K_x:
                    pygame.event.post(pygame.event.Event(pygame.QUIT))

        self.screen.fill(colors.BLACK)
        self.screen.blit(self.title, self.titlerect)
        if self.counter == 0:
            self.drawText = not self.drawText
            self.counter = 5
        self.counter -= 1

        if self.drawText:
            self.fontDrawer.draw(400,450, "PRESS ENTER TO START")

        pygame.display.flip()

    def lobbyevent(self):
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

        self.screen.fill(colors.BLACK)
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
                if event.key == pygame.K_w or event.key == pygame.K_k:
                    moved = self.player_move_up()
                elif event.key == pygame.K_a or event.key == pygame.K_h:
                    moved = self.player_move_left()
                elif event.key == pygame.K_s or event.key == pygame.K_j:
                    moved = self.player_move_down()
                elif event.key == pygame.K_d or event.key == pygame.K_l:
                    moved = self.player_move_right()
                elif event.key == pygame.K_SPACE:
                    self.player_attack()
                elif event.key == pygame.K_ESCAPE:
                    pygame.event.post(pygame.event.Event(pygame.QUIT))

        if moved:
            self.viewport.update_view()
            self.pickup_item()

        self.map.update(self.viewport)
        if self.map.is_cleared() or self.player.stats.hp <= 0:
            self.lc.stop()
            self.lc = LoopingCall(self.gameoverevent)
            self.lc.start(0.1)
        else:
            # draw updated
            self.screen.fill(colors.BLACK)
            self.map.draw_within(self.viewport)
            self.hud.draw()
            pygame.display.flip()

    def gameoverevent(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                reactor.stop()

        self.screen.fill(colors.BLACK)
        self.fontDrawer.draw(400, 280, "GAME OVER")
        self.hud.draw()
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
            # the monster's not dead, so it's attacking. arrrgh
            if update.stats.hp > 0 and self.player:
                self.monster_attack(entity)

        elif is_player(update.enttype):
            entity = self.map.layers[2].getById(update.idnum)
            if entity is None:
                entity = Entity(update.stats, update.enttype,
                                       True, update.name, update.idnum)
                if self.player is None:
                    self.player = entity

                    x = pygame.display.get_surface().get_width()
                    y = pygame.display.get_surface().get_height()
                    self.hud = hud.HUD(self.player, x, y)
                    self.viewport = viewport.Viewport(self.player, int(x/32), int(y/32))
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

    def score_kill(self, entity):
        if is_boss(entity):
            self.player.stats.score += scores.BOSS
        elif is_player(entity):
            self.player.stats.score += scores.PLAYER
        else:
            self.player.stats.score += scores.GHOST

    def monster_attack(self, entity):
        entity_x = entity.stats.x
        entity_y = entity.stats.y
        player_x = self.player.stats.x
        player_y = self.player.stats.y

        dist = abs(entity_x - player_x) + abs(entity_y - player_y)
        if dist < 2:
            self.hurtSound.play()
            self.player.stats.hp -= 10
            self.f.transport.sendLine(pickle.dumps(self.player.getUpdate(),2))
        elif dist < 3:
            self.ghastlySound.play()

    def pickup_item(self):
        item = self.map.item_under_entity(self.player)
        if item:
            # set the hp to 0 to remove it in next map update
            item.stats.hp = 0
            self.player.stats.score += scores.POTION
            self.f.transport.sendLine(pickle.dumps(item.getUpdate(),2))
            # give the player a hitpoint boost
            self.player.stats.hp += random.randint(5, 25)
            self.f.transport.sendLine(pickle.dumps(self.player.getUpdate(),2))

    def player_attack(self):
        direction = self.player.sprite.direction
        x = self.player.stats.x
        y = self.player.stats.y
        if direction == sprite.LEFT:
            if self.map.is_entity_blocked_left(self.player):
                entity = self.map.layers[2].get(x-1, y)
                if entity:
                    self.attackSound.play()
                    entity.stats.hp -= 25
                    if entity.stats.hp <= 0:
                        self.score_kill(entity)
                    self.f.transport.sendLine(pickle.dumps(entity.getUpdate(),2))
        elif direction == sprite.RIGHT:
            if self.map.is_entity_blocked_right(self.player):
                entity = self.map.layers[2].get(x+1, y)
                if entity:
                    self.attackSound.play()
                    entity.stats.hp -= 25
                    if entity.stats.hp <= 0:
                        self.score_kill(entity)
                    self.f.transport.sendLine(pickle.dumps(entity.getUpdate(),2))
        elif direction == sprite.UP:
            if self.map.is_entity_blocked_up(self.player):
                entity = self.map.layers[2].get(x, y-1)
                if entity:
                    self.attackSound.play()
                    entity.stats.hp -= 25
                    if entity.stats.hp <= 0:
                        self.score_kill(entity)
                    self.f.transport.sendLine(pickle.dumps(entity.getUpdate(),2))
        elif direction == sprite.DOWN:
            if self.map.is_entity_blocked_down(self.player):
                entity = self.map.layers[2].get(x, y+1)
                if entity:
                    self.attackSound.play()
                    entity.stats.hp -= 25
                    if entity.stats.hp <= 0:
                        self.score_kill(entity)
                    self.f.transport.sendLine(pickle.dumps(entity.getUpdate(),2))

    def player_quit_game(self):
        # set the player's health to 0 "killing" it
        # update the server
        self.player.stats.hp = 0
        self.f.transport.sendLine(pickle.dumps(self.player.getUpdate(),2))

    def player_move_up(self):
        self.player.sprite.set_direction(sprite.UP)
        if not self.map.is_entity_blocked_up(self.player):
            # update player, send to server
            self.player.stats.y -= 1
            self.f.transport.sendLine(pickle.dumps(self.player.getUpdate(),2))
            return True
        return False

    def player_move_left(self):
        self.player.sprite.set_direction(sprite.LEFT)
        if not self.map.is_entity_blocked_left(self.player):
            # update player, send to server
            self.player.stats.x -= 1
            self.f.transport.sendLine(pickle.dumps(self.player.getUpdate(),2))
            return True
        return False

    def player_move_right(self):
        self.player.sprite.set_direction(sprite.RIGHT)
        if not self.map.is_entity_blocked_right(self.player):
            # update player, send to server
            self.player.stats.x += 1
            self.f.transport.sendLine(pickle.dumps(self.player.getUpdate(),2))
            return True
        return False

    def player_move_down(self):
        self.player.sprite.set_direction(sprite.DOWN)
        if not self.map.is_entity_blocked_down(self.player):
            # update player, send to server
            self.player.stats.y += 1
            self.f.transport.sendLine(pickle.dumps(self.player.getUpdate(),2))
            return True
        return False
