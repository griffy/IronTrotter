from twisted.internet import reactor, protocol

from stats import Stats
import pickle

class TrotterPub(protocol.Protocol):
    def dataReceived(self, data):
        pickle.loads(data)

        #self.transport.write(pickle.dumps(Stats(1,2,3), 2))


class MyFactory(protocol.Factory):
    def __init__(self, glob):
        self.clients = []
        self.protocol = TrotterPub

    def clientConnectionMade(self, client):
        self.clients.append(client)

    def clientConnectionLost(self, client):
        self.clients.remove(client)


class ServerGlobals:
    def __init(self):
        pass

def main():
    """This runs the protocol on port 8000"""

    factory = MyFactory(ServerGlobals)

    reactor.listenTCP(8000,factory)
    reactor.run()

# this only runs if the module was *not* imported
if __name__ == '__main__':
    main()
