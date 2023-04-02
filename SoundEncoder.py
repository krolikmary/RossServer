import os.path
from typing import Any, Callable, Optional

from MessagersInterfaces import Listener, Notifier
from RossServer import RossEvent, RossState
import pygame


class SoundEncoder(Listener[RossEvent]):
    def __init__(self, directory="./sounds/", file_name_fun: Optional[Callable[[RossEvent], str]] = None):
        self._directory = directory
        self._get_file_name = file_name_fun
        self._mx = pygame.mixer
        self._mx.init()
        self._last_live = -1

    def get_file_name(self, event: RossEvent) -> str:
        if self._get_file_name:
            return self._get_file_name(event)
        else:
            return f"{event.camera_id}.mp3"

    def on_message(self, message: RossEvent, notifier: Notifier[RossEvent]):
        if (message.state == RossState.PGM or message.state == RossState.BOTH) and \
                message.camera_id != self._last_live:
            filename = self._directory + self.get_file_name(message)
            if not os.path.isfile(filename):
                return
            self._mx.music.stop()
            self._mx.music.load(self._directory + self.get_file_name(message))
            self._mx.music.play()
            self._last_live = message.camera_id
