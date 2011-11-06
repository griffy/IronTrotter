import pickle
import StringIO

from twisted.internet import reactor, protocol

from stats import Stats

from update import Update

class TrotterSub(protocol.Protocol):
    #def __init__(self):
    #    self.factory.transport = self.transport

    def connectionMade(self):
        self.factory.transport = self.transport
        self.transport.write(pickle.dumps(self.factory.handler.player.getUpdate(), 2))

    def dataReceived(self, data):
        stringIO = StringIO.StringIO(data)
        up = pickle.Unpickler(stringIO)
        s = up.load()
        while s is not None:
            self.factory.handler.handleUpdate(s)
            try:
                s = up.load()
            except EOFError:
                print "EOF when reading from socket"
                break

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
