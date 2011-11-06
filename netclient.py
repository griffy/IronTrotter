import pickle
from twisted.internet import reactor, protocol

from stats import Stats

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
