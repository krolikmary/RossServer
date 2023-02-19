import socket
import threading
import time

from loguru import logger as lg


class SenderAlreadyStartedException(Exception):
    pass


class TCPSender:
    """
        Simple multithreading TCP server to send similar message to several clients on one port
    """

    def __init__(self, host="127.0.0.1", port=8080):
        self._host = host
        self._port = port
        self._conListMutex = threading.Lock()
        self._hostMutex = threading.Lock()
        self._conList: list[socket.socket] = []
        self._stopEvent = threading.Event()

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
            raise SenderAlreadyStartedException()
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

    def sendAll(self, message: bytes):
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

    def stop(self):
        """
        stops accepting new clients
        """
        lg.debug(f"request to stop at {self._host}:{self._port}")
        self._stopEvent.set()

    def clearClients(self):
        """
        removes all clients
        """
        lg.info(f"requested to clear clients at {self._host}:{self._port}")
        with self._conListMutex:
            for conn in self._conList:
                conn.close()
            self._conList.clear()

if __name__ == "__main__":
    tcpServer = TCPSender("192.168.0.112")
    tcpServer.start()

    time.sleep(60)

    tcpServer.stop()