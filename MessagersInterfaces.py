from __future__ import annotations

from typing import TypeVar, Generic, Dict

from ServerDescriptor import Descriptor

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
