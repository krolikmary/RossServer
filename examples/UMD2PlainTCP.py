"""
An example of passing messages using observer (Notifier[T] -> Listener[T]) pattern

Scheme:
                        bytes               TSLEvent                str                 bytes
socket - - > UDPServer -------> UMDDecoder ----------> AnyToString -----> StringToByte -------> TCPServer - - > socket
"""

if __name__ == "__main__":
    import sys

    sys.path.append('../')

    from UDPServer import UDPServer
    from TCPServer import TCPServer
    from UtilityDecoders import AnyToString, StringToByte
    from UMDDecoder import UMDDecoder
    from RossServer import RossDecoder

    tcpServer = TCPServer(host="0.0.0.0", port=8080, repeat_for_new=True)
    tcpServer.start()
    udpServer = UDPServer(
        UMDDecoder(
            RossDecoder(
                AnyToString(
                    StringToByte(tcpServer),
                    last_char='\n'
                )
            )
        ),
        host="0.0.0.0",
        port=1337
    )
    udpServer.run()
