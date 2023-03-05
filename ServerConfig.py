from enum import Enum


class Protocols(Enum):
    LOGGER = -1
    UNKNOWN = 0
    TSLUMD = 1


class ServerConfig:
    def __init__(self):
        self.ip: str = '127.0.0.1'
        self.port: int = -1
        self.protocol: Protocols = Protocols.UNKNOWN
        self.repeatTimer: int = -1
        self.repeatOnNew: bool = False
