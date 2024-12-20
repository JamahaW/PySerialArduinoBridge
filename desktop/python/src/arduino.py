"""
Пример протокола для базовых функций Ардуино
"""

from serialcmd.core.respond import RespondPolicy
from serialcmd.core.result import Result
from serialcmd.errorenum import ErrorEnum
from serialcmd.protocol import Protocol
from serialcmd.serializers import Struct
from serialcmd.serializers import u32
from serialcmd.serializers import u8
from serialcmd.streams.abc import Stream


class ArduinoError(ErrorEnum):
    ok = 0x00
    """Команда выполнена успешно"""

    fail = 0x01
    """Произошла ошибка"""


class ArduinoProtocol(Protocol[ArduinoError, bool]):
    """Пример подключения к Arduino с минимальным набором команд"""

    def __init__(self, stream: Stream) -> None:
        super().__init__(RespondPolicy[ArduinoError](ArduinoError, u8), u8, stream, u8)
        self._pin_mode = self.addCommand("pinMode", Struct((u8, u8)), None)
        self._digital_write = self.addCommand("digitalWrite", Struct((u8, u8)), None)
        self._digital_read = self.addCommand("digitalRead", u8, u8)
        self._millis = self.addCommand("millis", None, u32)
        self._delay = self.addCommand("delay", u32, None)

    def pinMode(self, pin: int, mode: int) -> Result[None, ArduinoError]:
        """Установить режим пина"""
        return self._pin_mode.send((pin, mode))

    def digitalWrite(self, pin: int, mode: bool) -> Result[None, ArduinoError]:
        """Установить состояние пина"""
        return self._digital_write.send((pin, mode))

    def digitalRead(self, pin: int) -> Result[int, ArduinoError]:
        """Считать состояние пина"""
        return self._digital_read.send(pin)

    def millis(self) -> Result[int, ArduinoError]:
        """Получить время на плате в мс"""
        return self._millis.send(None)

    def delay(self, duration_ms: int) -> Result[None, ArduinoError]:
        """Оставить ведомое устройство ожидать заданное время"""
        return self._delay.send(duration_ms)


INPUT = 0x0
OUTPUT = 0x1
INPUT_PULLUP = 0x2
LED_BUILTIN = 13
