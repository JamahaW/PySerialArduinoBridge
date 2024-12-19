from enum import IntEnum
from time import sleep
from typing import Tuple

from serial import Serial

from serialcmd.commands import ReadHelper
from serialcmd.primitives import Primitive
from serialcmd.protocol import Protocol


class ArduinoErrors(IntEnum):
    OK = 0
    FAIL = 1


class ArduinoProtocol(Protocol[ArduinoErrors]):
    """Пример подключения к Arduino с минимальным набором команд"""

    def __init__(self, serial: Serial) -> None:
        super().__init__(Primitive.u8, ReadHelper(ArduinoErrors, ArduinoErrors.OK, Primitive.u8))

        self.serial = serial

        # Команды этого устройства
        self._pin_mode = self.addCommand((Primitive.u8, Primitive.u8))
        self._digital_write = self.addCommand((Primitive.u8, Primitive.u8))
        self._digital_read = self.addCommand((Primitive.u8,))
        self._delay_ms = self.addCommand((Primitive.u32,))

    def pinMode(self, pin: int, mode: int) -> Tuple[ArduinoErrors, None]:
        return self._pin_mode.send(self.serial, pin, mode)

    def digitalWrite(self, pin: int, state: bool | int) -> Tuple[ArduinoErrors, None]:
        return self._pin_mode.send(self.serial, pin, state)

    def digitalRead(self, pin: int) -> Tuple[ArduinoErrors, bool | None]:
        return self._digital_read.send(self.serial, pin)

    def delay(self, milliseconds: int) -> Tuple[ArduinoErrors, None]:
        return self._delay_ms.send(self.serial, milliseconds)


def main() -> None:
    INPUT = 0x0
    OUTPUT = 0x1
    INPUT_PULLUP = 0x2
    LED_BUILTIN = 13

    # Подключение к Arduino, скорость повышенная
    arduino = ArduinoProtocol(Serial("COM10", 115200))

    # Ожидание пока вся инициализация slave платы пройдёт ...
    sleep(2)

    # Стандартный блинк
    arduino.digitalWrite(LED_BUILTIN, 1)
    arduino.delay(1000)
    arduino.digitalWrite(LED_BUILTIN, 0)
    arduino.delay(1000)

    # Закрытие порта
    arduino.serial.close()


if __name__ == '__main__':
    main()
