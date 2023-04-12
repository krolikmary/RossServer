from enum import Enum

from typing import List, Dict

from RossEventMultiplexor import Multiplexor
from JSONEncoder import RossEventToJson
from MessagersInterfaces import Listener, Notifier
from RossServer import RossEvent
from TCPServer import TCPServer
from TSLUMDEncoder import RossEventToTSLUMD


class OutputProto(Enum):
    SOUND = 0
    TSLUMD = 1
    JSON = 2
    BIN = 3


class OutputServer(Listener[RossEvent]):
    def start(self):
        raise NotImplementedError()

    def stop(self):
        raise NotImplementedError()

    def get_proto(self) -> OutputProto:
        raise NotImplementedError()


class NetworkTransport(Enum):
    UDP = 0
    TCP = 1


class NetworkOutputServer(OutputServer):
    def get_ip(self) -> str:
        raise NotImplementedError()

    def get_port(self) -> int:
        raise NotImplementedError()

    def get_transport(self) -> NetworkTransport:
        raise NotImplementedError()


class TSLTCPServer(NetworkOutputServer):
    def __init__(self, ip: str, port: int, repeat_for_new=False):
        self._tcp_server = TCPServer(str, port, repeat_for_new)
        self._ross_event_to_tsl_umd = RossEventToTSLUMD(self._tcp_server)

    def get_ip(self) -> str:
        return self._tcp_server.get_ip()

    def get_port(self) -> int:
        return self._tcp_server.get_port()

    def get_transport(self) -> NetworkTransport:
        return NetworkTransport.TCP

    def get_proto(self) -> OutputProto:
        return OutputProto.TSLUMD

    def start(self):
        self._tcp_server.start()

    def stop(self):
        self._tcp_server.stop()

    def on_message(self, message: RossEvent, notifier: Notifier[RossEvent]):
        self._ross_event_to_tsl_umd(message, notifier)


class JsonTCPServer(NetworkOutputServer):
    def __init__(self, ip: str, port: int, repeat_for_new=False):
        self._tcp_server = TCPServer(str, port, repeat_for_new)
        self._json_encoder = RossEventToJson(self._tcp_server)

    def get_ip(self) -> str:
        return self._tcp_server.get_ip()

    def get_port(self) -> int:
        return self._tcp_server.get_port()

    def get_transport(self) -> NetworkTransport:
        return NetworkTransport.TCP

    def start(self):
        self._tcp_server.start()

    def stop(self):
        self._tcp_server.stop()

    def get_proto(self) -> OutputProto:
        return OutputProto.JSON

    def on_message(self, message: RossEvent, notifier: Notifier[RossEvent]):
        self._json_encoder(message, notifier)


class ServersModel:
    def __init__(self, multiplexor: Multiplexor):
        self._multiplexor: Multiplexor = multiplexor

    def get_descriptors(self) -> Dict[int, Listener[RossEvent]]:
        return self._multiplexor.get_listeners()

