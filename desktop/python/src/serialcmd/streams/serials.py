from dataclasses import dataclass
from typing import Iterable

import serial.tools.list_ports
from serial import Serial as SerialPort

from serialcmd.streams.abc import Stream


@dataclass
class Serial(Stream):
    """Стрим по последовательному порту"""

    def __init__(self, port: str, baud: int) -> None:
        self._serial_port = SerialPort(port=port, baudrate=baud)

    def read(self, size: int = 1) -> bytes:
        return self._serial_port.read(size)

    def write(self, data: bytes) -> None:
        self._serial_port.write(data)

    @staticmethod
    def getPorts(keywords: Iterable[str] = ("Arduino", "CH340", "USB-SERIAL")) -> list[str]:
        """
        Находит порты, содержащие указанные ключевые слова в описании устройства.
        @param keywords: Список ключевых слов для поиска (по умолчанию ищет Arduino).
        """
        return [
            port.device for port in serial.tools.list_ports.comports()
            if any(keyword in port.description for keyword in keywords)
        ]

    def __str__(self) -> str:
        return f"{self.__class__.__name__}<{self._serial_port.port}>"


def _test():
    ports = Serial.getPorts()
    print(ports)

    stream = Serial(ports[0], 115200)

    buf = stream.read(7)

    from serialcmd.serializers import Struct
    from serialcmd.serializers import u8
    from serialcmd.serializers import u16
    from serialcmd.serializers import u32

    print(buf)

    a, b, c, = Struct((u32, u16, u8)).unpack(buf)

    print(f"{a:X}, {b:X}, {c:X}")

    return


if __name__ == '__main__':
    _test()
