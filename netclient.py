import pickle
import StringIO

from twisted.internet import reactor, protocol

from twisted.protocols.basic import LineReceiver

from stats import Stats

from update import Update, nullUpdate

class TrotterSub(LineReceiver):
    #def __init__(self):
    #    self.factory.transport = self.transport

    def connectionMade(self):
        self.factory.transport = self
        self.sendLine(pickle.dumps(nullUpdate, 2))

    def lineReceived(self, data):
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
