from typing import Any

from MessagersInterfaces import Listener, Notifier, T
from loguru import logger as lg


class ListenerLogger(Listener[Any]):
    def on_message(self, message: Any, notifier: Notifier[Any]):
        lg.info(f"New message from {notifier}: {message}")


class AnyToString(Listener[Any], Notifier[str]):
    def __init__(self, listener: Listener[str], last_char=''):
        self._listener = listener
        self._lastChar = last_char

    def on_message(self, message: Any, notifier: Notifier[Any]):
        s = str(message)
        if self._lastChar != '' and s[-1] != self._lastChar:
            s += self._lastChar
        self._listener(s, self)


class StringToByte(Listener[str], Notifier[bytes]):
    def __init__(self, listener: Listener[bytes]):
        self._listener = listener

    def on_message(self, message: str, notifier: Notifier[bytes]):
        self._listener(message.encode(), notifier)
