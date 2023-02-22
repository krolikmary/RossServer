from __future__ import annotations

import socket
import threading
import time
from typing import Callable, Any
import TSLExceptions
from loguru import logger as lg


class UDPListener:
    """
    UDP multithreading server to notify listener about new messages
    """
    def __init__(self, listener: Callable[[bytes, Any, UDPListener], None], host="127.0.0.1", port=8080,
                 buffer_size=1024):
        """
        :param listener: function that will be called for each new message
        :param host: ip address of server
        :param port: port of server
        :param buffer_size: maximal length of message to read
        """
        self._bufferSize = buffer_size
        self._listener = listener
        self._host = host
        self._port = port
        self._hostMutex = threading.Lock()
        self._sendMutex = threading.Lock()
        self._stopEvent = threading.Event()

    def run(self):
        """
            Running host function in a new thread
        """
        threading.Thread(target=self.host).start()
        lg.info(f"UDPListener at {self._host}:{self._port} is running")

    def host(self):
        """
            Function to host the server
        """
        if self._hostMutex.locked():
            lg.warning(f"tried to host new UDPListener at {self._host}:{self._port}")
            raise TSLExceptions.ServerAlreadyStartedException()
        with self._hostMutex:
            with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
                sock.setblocking(False)
                sock.bind((self._host, self._port))
                lg.debug(f"UDPListener at {self._host}:{self._port} is hosting")
                while not self._stopEvent.is_set():
                    try:
                        message, address = sock.recvfrom(self._bufferSize)
                        self._listener(message, address, self)
                    except BlockingIOError:
                        pass

    def stop(self):
        """
            Stops the server
        """
        with self._sendMutex:
            lg.debug(f"UDPListener at {self._host}:{self._port} is stopping")
            self._stopEvent.set()


if __name__ == "__main__":
    udp_listener = UDPListener(lambda m, a, l: lg.info(f"Got message: {m} from {a}"), host="192.168.0.112")
    udp_listener.run()

    time.sleep(30)

    udp_listener.stop()
