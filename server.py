from twisted.internet import reactor, protocol
from twisted.internet.task import LoopingCall

from stats import Stats
from update import Update
from random import choice
from sprite import UP, DOWN, LEFT, RIGHT
import pickle

import map
import entity
import pygame

class TrotterPub(protocol.Protocol):
    def __init__(self):
        self.first = True

    def dataReceived(self, data):
        up = pickle.loads(data)

        #self.factory.glob.update(up)

        if self.first == True:
            self.first = False
            for layer in self.factory.glob.map.layers:
                for ent in layer.entities:
                    self.transport.write(pickle.dumps(ent.getUpdate(), 2))

            #generate a player
            player = entity.Entity(Stats(0,0),0, "BOB")
            self.factory.glob.update(player)

            self.transport.write(pickle.dumps(player.getUpdate(),2))
        else:
            self.factory.glob.update(up)

            # send to all other clients
            for t in self.factory.transports:
                if t is not self.transport:
                    t.write(pickle.dumps(up,2))

    def connectionMade(self):
        self.factory.transports.append(self.transport)

class MyFactory(protocol.Factory):
    def __init__(self, glob):
        self.clients = []
        self.protocol = TrotterPub
        self.glob = glob
        self.transports = []

    def clientConnectionMade(self, client):
        self.clients.append(client)

    def clientConnectionLost(self, client):
        self.clients.remove(client)


class ServerGlobals:
    def __init__(self):
        self.map = map.generate_map(map.map_width,map.map_height)

    def update(self, up):
        if up.name != "":
            self.map.addPlayer(up)

def main():
    """This runs the protocol on port 8000"""

    pygame.init()

    screen = pygame.display.set_mode((1,1))

    glob = ServerGlobals()

    factory = MyFactory(glob)

    reactor.listenTCP(8000,factory)

    def move_enemy():
        if not glob.map.layers:
            return

        for entity in glob.map.layers[2].entities:         
            moves = []
            if glob.map.is_player_up(entity):
                moves.append(UP)
            if glob.map.is_player_down(entity):
                moves.append(DOWN)
            if glob.map.is_player_left(entity):                         
                moves.append(LEFT)
            if glob.map.is_player_right(entity):
                moves.append(RIGHT)
            
            if not moves:
                move = choice([UP, DOWN, LEFT, RIGHT])
            else:
                move = choice(moves)
            
            entity.sprite.set_direction(move)

            if move == UP:
                if not glob.map.is_entity_blocked_up(entity):
                    entity.stats.y -= 1
            elif move == DOWN:
                if not glob.map.is_entity_blocked_down(entity):
                    entity.stats.y += 1    
            elif move == LEFT:
                if not glob.map.is_entity_blocked_left(entity):
                    entity.stats.x -= 1
            else:
                if not glob.map.is_entity_blocked_right(entity):
                    entity.stats.x += 1

            # send updated postion information            

    self.lc = LoopingCall(move_enemy())
    self.lc.start(0.1)

    reactor.run()
    
# this only runs if the module was *not* imported
if __name__ == '__main__':
    main()
