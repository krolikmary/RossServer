if __name__ == "__main__":
    from UDPServer import UDPServer
    from UMDDecoder import UMDDecoder
    from UtilityDecoders import ListenerLogger

    listenerLogger = ListenerLogger()
    umdDecoder = UMDDecoder(listenerLogger)
    udpServer = UDPServer(umdDecoder, host="192.168.0.112", port=1337)
    udpServer.run()

