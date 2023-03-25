from enum import Enum

from MessagersInterfaces import Listener, Notifier, T
from RossServer import *
from UMDDecoder import *


class RossEventToBin(Listener[RossEvent], Notifier[bytes]):
    def __init__(self, listener: Listener[bytes], num_of_cam=127):
        '''
        Creates "bytes" with lenght of 33
        1-st byte - lenght of "bytes"
        Others - camera's states
        '''
        self._listener = listener
        self._a = bytes()
        self._a = [0] * 33
        self._a[0] = 32

    def on_message(self, message: RossEvent, notifier: Notifier[RossEvent]):
        '''
        Fills the bytes with the corresponding state
        of the corresponding camera
        Param: RossState
        Returns: bytes
        '''
        multi = 0
        place = 0
        for i in range (1, self._a[1] + 1, 1):
            for k in range (1, 9, 1):
                place = i * multi + k
                if message.get_camera_id() == place:
                    self._a[place] += message.get_camera_state()
                    self._a[place] <<= 1
                else:
                    self._a[place] += 0
                    self._a[place] <<= 1
        self._listener(self._a, self)







'10001100 = 4 + 8 + 128 = 140' \
'01001100 = 4 + 8  + 64 = 76' \
'00001100 = 12' \
'11001100 = 4 + 8 + 64 + 128 = 204'