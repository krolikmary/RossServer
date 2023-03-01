import socket
import threading
import time
from loguru import logger as lg
from typing import List

import ServersExceptions
from MessagersInterfaces import Listener, T, Notifier


class TCPServer(Listener[bytes]):
    """
        Simple multithreading TCP server to send similar message to several clients on one port
    """
    # TODO implement repeat timer and repeat on new clients

    def __init__(self, host="127.0.0.1", port=8080):
        self._host = host
        self._port = port
        self._conListMutex = threading.Lock()
        self._hostMutex = threading.Lock()
        self._conList: List[socket.socket] = []
        self._stopEvent = threading.Event()
        self._timeToRepeat = -1
        self._repeatOnNew = False

    def start(self):
        """
            Starts the TCPSender.host in a new thread
        """
        threading.Thread(
            target=self.host
        ).start()

    def host(self):
        """
            Accepts new connections
        """
        self._stopEvent = threading.Event()
        if self._hostMutex.locked():
            raise ServersExceptions.ServerAlreadyStartedException()
        lg.info(f"started hosting at {self._host}:{self._port}")
        with self._hostMutex:
            with socket.socket() as sock:
                sock.setblocking(False)
                sock.bind((self._host, self._port))
                sock.listen()
                while not self._stopEvent.is_set():
                    try:
                        conn, addr = sock.accept()
                        with self._conListMutex:
                            lg.debug(f"new connection at {self._host}:{self._port} from {addr}")
                            self._conList.append(conn)
                    except socket.error:
                        pass
        lg.info(f"stopped hosting at {self._host}:{self._port}")

    def send_all(self, message: bytes):
        """
        send the message to all accepted clients

        :param message:
        :type message: bytes
        :return:
        """
        lg.debug(f"sending message by {self._host}:{self._port}: {message}")
        with self._conListMutex:
            for conn in list(self._conList):
                try:
                    conn.send(message)
                except socket.error:
                    lg.debug(f"{conn.getpeername()} disconnected from {self._host}:{self._port}")
                    conn.close()
                    self._conList.remove(conn)

    def on_message(self, message: bytes, notifier: Notifier[bytes]):
        self.send_all(message)

    def stop(self):
        """
        stops accepting new clients
        """
        lg.debug(f"request to stop at {self._host}:{self._port}")
        self._stopEvent.set()

    def clear_clients(self):
        """
        removes all clients
        """
        lg.info(f"requested to clear clients at {self._host}:{self._port}")
        with self._conListMutex:
            for conn in self._conList:
                conn.close()
            self._conList.clear()


if __name__ == "__main__":
    from UDPServer import UDPServer

    tcpServer = TCPServer("192.168.0.112")
    tcpServer.start()

    udpServer = UDPServer(tcpServer, "192.168.0.112", port=1337)
    udpServer.run()
