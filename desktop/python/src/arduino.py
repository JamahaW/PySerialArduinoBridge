from serialcmd.core.errorenum import ErrorEnum
from serialcmd.protocol import Protocol


class ArduinoError(ErrorEnum):
    ok = 0x00
    fail = 0x01


class ArduinoProtocol(Protocol[ArduinoError]):
    """Пример подключения к Arduino с минимальным набором команд"""

    pass


INPUT = 0x0
OUTPUT = 0x1
INPUT_PULLUP = 0x2
LED_BUILTIN = 13

# Подключение к Arduino, скорость повышенная
# arduino = ArduinoProtocol(Serial("COM10", 115200))

# Ожидание пока вся инициализация slave платы пройдёт ...

# Закрытие порта
