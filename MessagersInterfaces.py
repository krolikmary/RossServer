from __future__ import annotations

from typing import TypeVar, Generic, Dict

from RossEvent import RossEvent
from ServerDescriptor import Descriptor, OutputProto, NetworkTransport

T = TypeVar('T')


class Notifier(Generic[T]):
    """
    an interface of class that send messages of type T
    """
    pass


class Listener(Generic[T]):
    """
    an interface of class that get messages of type T
    """

    def on_message(self, message: T, notifier: Notifier[T]):
        raise NotImplementedError()

    def __call__(self, message: T, notifier: Notifier[T]):
        self.on_message(message, notifier)

    def get_descriptor(self) -> Descriptor:
        return Descriptor()


class OutputServer(Listener[RossEvent]):
    def start(self):
        """
            begins a work of server
            if your server doesnt require to be started before sending messages
            you can just write pass in body
        """
        raise NotImplementedError()

    def stop(self):
        """
            stop a work of server
            if your server doesnt require to be stopped when it's useless anymore
            you can just write pass in body
        """
        raise NotImplementedError()

    def get_proto(self) -> OutputProto:
        """
            returns an OutputProto that describes which protocol it uses
            used to generate a Descriptor
        """
        raise NotImplementedError()

    def get_descriptor(self) -> Descriptor:
        """
            returns a Descriptor that describes a server
        """
        ans = Descriptor()
        ans.protocol = self.get_proto()
        return ans


class NetworkOutputServer(OutputServer):
    def get_ip(self) -> str:
        """
            returns an ip of the hostname it uses
        """
        raise NotImplementedError()

    def get_port(self) -> int:
        """
            returns a port which the server is listening
        """
        raise NotImplementedError()

    def get_transport(self) -> NetworkTransport:
        """
            returns a transport the server is using
        """
        raise NotImplementedError()

    def get_descriptor(self) -> Descriptor:
        ans = super().get_descriptor()
        ans.ip = self.get_ip()
        ans.port = self.get_port()
        ans.transport = self.get_transport()
        return ans
