"""
An example of passing messages using observer (Notifier[T] -> Listener[T]) pattern

Scheme:
                          bytes               TSLEvent                RossEvent
socket - - - > UDPServer -------> UMDDecoder ----------> RossDecoder -----------> SoundEncoder - - - > sound
"""

if __name__ == "__main__":
    import sys

    sys.path.append('../')
    from UDPServer import UDPServer
    from UMDDecoder import UMDDecoder
    from RossServer import RossDecoder
    from SoundEncoder import SoundEncoder
    soundEncoder = SoundEncoder('../sounds/')
    rossDecoder = RossDecoder(soundEncoder)
    umdDecoder = UMDDecoder(rossDecoder)
    udpServer = UDPServer(umdDecoder, host="0.0.0.0", port=1337)
    udpServer.run()
