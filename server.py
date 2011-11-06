from twisted.internet import reactor, protocol

from stats import Stats
import pickle

class TrotterPub(protocol.Protocol):
    def dataReceived(self, data):
        "As soon as any data is received, write it back."
        self.transport.write(pickle.dumps(Stats(1,2,3), 2))


def main():
    """This runs the protocol on port 8000"""
    factory = protocol.ServerFactory()
    factory.protocol = TrotterPub
    reactor.listenTCP(8000,factory)
    reactor.run()

# this only runs if the module was *not* imported
if __name__ == '__main__':
    main()
