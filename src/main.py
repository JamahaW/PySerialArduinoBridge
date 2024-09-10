from time import sleep
from timeit import timeit

from serial import Serial

from pyserialbridge.commands import CacheableCommand
from pyserialbridge.commands import Command
from pyserialbridge.primitives import Primitives

INPUT = 0x0
OUTPUT = 0x1
INPUT_PULLUP = 0x2
LED_BUILTIN = 13


class ArduinoConnection:
    """Пример подключения к Arduino с минимальным набором команд"""

    def __init__(self, serial: Serial) -> None:
        self.serial = serial

        # Команды этого устройства
        self._pin_mode = Command(0x10, (Primitives.u8, Primitives.u8))
        self._digital_write = Command(0x11, (Primitives.u8, Primitives.u8))
        self._digital_read = Command(0x12, (Primitives.u8,))
        self._delay_ms = Command(0x13, (Primitives.u32,))

    # Обёртки над командами ниже, чтобы сразу компилировать и отправлять их в порт

    def pinMode(self, pin: int, mode: int) -> None:
        self.serial.write(self._pin_mode.pack(pin, mode))

    def digitalWrite(self, pin: int, state: bool | int) -> None:
        self.serial.write(self._digital_write.pack(pin, state))

    def digitalRead(self, pin: int) -> bool:
        self.serial.write(self._digital_read.pack(pin))  # Отправляем запрос для чтения пина
        response = self.serial.read()  # Ждём и получаем ответ (bytes)
        return Primitives.u8.unpack(response)  # получаем распакованное значение

    def delay(self, milliseconds: int) -> None:
        self.serial.write(self._delay_ms.pack(milliseconds))
        # Код будет спать вместе с Arduino
        sleep(0.001 * milliseconds)


def main() -> None:
    # Подключение к Arduino, скорость повышенная
    arduino = ArduinoConnection(Serial("COM10", 115200))

    # Ожидание пока вся инициализация slave платы пройдёт ...
    sleep(2)

    # Стандартный блинк
    arduino.digitalWrite(LED_BUILTIN, 1)
    arduino.delay(1000)
    arduino.digitalWrite(LED_BUILTIN, 0)
    arduino.delay(1000)

    # Закрытие порта
    arduino.serial.close()


def test() -> None:
    from random import randint

    cmd = Command(0x69, (Primitives.u8,))
    h_cmd = CacheableCommand(0x69, (Primitives.u8,))

    def rand():
        return randint(0, 255)

    pack_no_cache = timeit(lambda: cmd.pack(rand()))
    pack_cached = timeit(lambda: h_cmd.pack(rand()))

    print(f"{pack_no_cache=}\n{pack_cached=}\n({pack_no_cache / pack_cached})")


if __name__ == '__main__':
    main()
    # test()
