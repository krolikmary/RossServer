"""
An example of passing messages using observer (Notifier[T] -> Listener[T]) pattern

Scheme:
                        bytes               RossEvent          RossEvent                 str                 bytes
socket - - > UDPServer -------> UMDDecoder ----------> Filter ----------->  AnyToString -----> StringToByte -------> TCPServer - - > socket
"""

if __name__ == "__main__":
    import sys

    sys.path.append('../')

    from UDPServer import UDPServer
    from TCPServer import TCPServer
    from UtilityDecoders import AnyToString, StringToByte
    from UMDDecoder import UMDDecoder
    from RossServer import RossDecoder
    from Filter import Filter

    tcpServer = TCPServer(host="0.0.0.0", port=8080, repeat_for_new=True)
    tcpServer.start()
    udpServer = UDPServer(
        UMDDecoder(
            RossDecoder(
                Filter(
                    AnyToString(
                        StringToByte(tcpServer),
                        last_char='\n',
                    ),
                    {1, 2}
                )

            )
        ),
        host="0.0.0.0",
        port=1337
    )
    udpServer.run()
