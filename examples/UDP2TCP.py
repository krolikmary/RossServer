"""
An example of passing messages using observer (Notifier[T] -> Listener[T]) pattern

Scheme:
                          bytes
socket - - - > UDPServer -------> TCPServer - - - > socket
"""

if __name__ == "__main__":
    import sys

    sys.path.append('../')
    from UDPServer import UDPServer
    from TCPServer import TCPServer

    tcpServer = TCPServer(host="127.0.0.1", port=8080)
    tcpServer.start()
    udpServer = UDPServer(tcpServer, "127.0.0.1", port=1337)
    udpServer.run()