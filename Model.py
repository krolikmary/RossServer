from __future__ import annotations

from typing import Dict, Optional, Callable

from RossEventMultiplexor import Multiplexor
from JSONEncoder import RossEventToJson
from MessagersInterfaces import Notifier, OutputServer, NetworkOutputServer
from RossServer import RossDecoder
from RossEvent import RossEvent
from ServerDescriptor import Descriptor, OutputProto, NetworkTransport
from TCPServer import TCPServer
from TSLUMDEncoder import RossEventToTSLUMD
from UDPServer import UDPServer
from UMDDecoder import UMDDecoder
from SoundEncoder import SoundEncoder


class TSLTCPServer(NetworkOutputServer):
    def __init__(self, ip: str, port: int, repeat_for_new=False):
        self._tcp_server = TCPServer(ip, port, repeat_for_new)
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
        self._tcp_server = TCPServer(ip, port, repeat_for_new)
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
    def __init__(self, ip: str, listener_port=1337):
        self._multiplexor: Multiplexor = Multiplexor()
        ross_decoder = RossDecoder(self._multiplexor)
        umd_decoder = UMDDecoder(ross_decoder)
        self._udp_server = UDPServer(umd_decoder, host=ip, port=listener_port)
        self._ip = ip
        self._listener_port = listener_port

    def run(self):
        """
            starts a listening for incoming packets
        """
        self._udp_server.run()

    def get_descriptors(self) -> Dict[int, Descriptor]:
        """
            returns dict from id of server to its descriptor
        """
        return dict((k, v.get_descriptor()) for k, v in self._multiplexor.get_listeners().items())

    def delete_server(self, listener_id: int):
        """
            deletes listener by its id
            the listener will be stopped (if possible)
            and it will not get any new messages from the model
        """
        listener = self._multiplexor.delete_listener(listener_id)
        if issubclass(type(listener), OutputServer):
            listener.stop()

    def add_tslumd(self, port, repeat_for_new=False) -> int:
        """
            creates and starts a new TSLTCPServer
        """
        server = TSLTCPServer(self._ip, port, repeat_for_new)
        server.start()
        return self._multiplexor.add_listener(server)

    def add_sound(self, sound_directory ="./sounds/", file_name_fun: Optional[Callable[[RossEvent], str]] = None) -> int:
        """
            creates and starts a new SoundServer (SoundEncoder)
        """
        server = SoundEncoder(sound_directory)
        server.start()
        return self._multiplexor.add_listener(server)

    def add_json(self, port, repeat_for_new=False) -> int:
        """
            creates and starts a new JsonTCPServer
        """
        server = JsonTCPServer(self._ip, port, repeat_for_new)
        server.start()
        return self._multiplexor.add_listener(server)
