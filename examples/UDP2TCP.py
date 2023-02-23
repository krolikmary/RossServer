if __name__ == "__main__":
    from UDPServer import UDPServer
    from TCPServer import TCPServer

    tcpServer = TCPServer(host="192.168.0.112", port=8080)
    tcpServer.start()
    udpServer = UDPServer(tcpServer, "192.168.0.112", port=1337)
    udpServer.run()