from twisted.internet import reactor, protocol

import sys
import pygame

from handler import Handler


# this connects the protocol to a server runing on port 8000
def main():
    addr = "localhost"
    if len(sys.argv) > 1:
        addr = sys.argv[1]

    pygame.init()

    pygame.display.set_caption("Iron Trotter")
    pygame.display.set_icon(pygame.image.load("images/icon.png"))

    width, height = 0, 0
    screen = pygame.display.set_mode((width, height))

    h = Handler(screen)

    reactor.connectTCP(addr, 8000, h.f)
    reactor.run()


# this only runs if the module was *not* imported
if __name__ == '__main__':
    main()
