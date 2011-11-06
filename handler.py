from twisted.internet import reactor, protocol

import sys

from stats import Stats
import pickle

from netclient import TrotterSub

from twisted.internet.task import LoopingCall

import pygame
import colors
import map
import font
import sound

class Handler:
    def __init__(self, screen):
        self.title = pygame.image.load("images/titleScreen.png")
        self.titlerect = self.title.get_rect()

        self.screen = screen

        self.f = protocol.ClientFactory()
        self.f.protocol = TrotterSub

        self.fontDrawer = font.Font("font/youmurdererbb_reg.ttf", 100, colors.RED)

        self.counter = 5
        self.drawText = False

        pygame.mixer.init()
        self.titleMusic = sound.Sound("music/severedfifth_endofdays.ogg")
        self.titleMusic.play()

        self.lc = LoopingCall(self.titleevent)
        self.lc.start(0.1)

        self.map = map.generate_map(10,10)

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
       self.map.draw()
       pygame.display.flip()
