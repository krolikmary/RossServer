if __name__ == "__main__":
    from UDPServer import UDPServer
    from TCPServer import TCPServer
    from UtilityDecoders import AnyToString, StringToByte
    from UMDDecoder import UMDDecoder

    tcpServer = TCPServer(host="192.168.0.112", port=8080)
    tcpServer.start()
    udpServer = UDPServer(UMDDecoder(AnyToString(StringToByte(tcpServer), last_char='\n')), host="192.168.0.112", port=1337)
    udpServer.run()

