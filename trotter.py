from twisted.internet import reactor, protocol

import sys

from stats import Stats
import pickle

from twisted.internet.task import LoopingCall

import pygame
import colors
import map
import font

class TrotterSub(protocol.Protocol):
    """Once connected, send a message, then print the result."""

    def connectionMade(self):
        self.transport.write("hello, world!")

    def dataReceived(self, data):
        "As soon as any data is received, write it back."
        s = pickle.loads(data)
        print "Server said:", s.x, s.y, s.hp

    def connectionLost(self, reason):
        print "connection lost"


class Handler:
    title = pygame.image.load("images/titleScreen.png")
    titlerect = title.get_rect()

    width, height = 800, 600
    screen = pygame.display.set_mode((width, height))

    f = protocol.ClientFactory()
    f.protocol = TrotterSub

    counter = 100
    drawText = True


    def pyevent(self):
        global counter
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                reactor.stop()
            elif event.type == pygame.KEYDOWN:
                # --- KEY handlers go HERE ---
                if event.key == pygame.K_m:
                    print "c"
                elif event.key == pygame.K_x:
                    pygame.event.post(pygame.event.Event(pygame.QUIT))

        fontDrawer = font.Font("font/youmurdererbb_reg.ttf", 100, colors.RED)

        self.screen.blit(self.title, self.titlerect)
        if self.counter == 0:
            self.drawText = not self.drawText
            self.counter = 100
        self.counter -= 1

        if self.drawText:
            fontDrawer.draw(400,450, "PRESS ENTER TO START")

        pygame.display.flip()



# this connects the protocol to a server runing on port 8000
def main():
    addr = "localhost"
    if len(sys.argv) > 1:
        addr = sys.argv[1]

    pygame.init()

    pygame.display.set_caption("Iron Trotter")

    h = Handler()

    lc = LoopingCall(h.pyevent)
    lc.start(0.1)

    reactor.connectTCP(addr, 8000, h.f)
    reactor.run()


# this only runs if the module was *not* imported
if __name__ == '__main__':
    main()
