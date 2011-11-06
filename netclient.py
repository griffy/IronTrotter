import pickle
from twisted.internet import reactor, protocol

from stats import Stats

from update import Update

class TrotterSub(protocol.Protocol):
    #def __init__(self):
    #    self.h = self.factory.handler

    def connectionMade(self):
        self.transport.write(pickle.dumps(self.factory.handler.player.getUpdate()))

    def dataReceived(self, data):
        s = pickle.loads(data)
        self.factory.handler.handleUpdate(s)

    def connectionLost(self, reason):
        print "connection lost"

class TrotterSubFactory(protocol.ClientFactory):
    protocol = TrotterSub

    def __init__(self, handler):
        self.handler = handler

    def clientConnectionFailed(self, connector, reason):
        print "Connection failed - goodbye!"
        reactor.stop()

    def clientConnectionLost(self, connector, reason):
        print "Connection lost - goodbye!"
        reactor.stop()
