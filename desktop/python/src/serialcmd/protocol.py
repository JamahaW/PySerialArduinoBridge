from typing import Optional

from serialcmd.command import Command
from serialcmd.serializers import Serializer


class Protocol:
    """Протокол - набор команды для последовательной связи"""

    def __init__(self) -> None:
        pass

    def addCommand(self, name: str, signature: Optional[Serializer], returns: Optional[Serializer]) -> Command:
        """
        Добавить команду
        @param name Имя команды для отладки
        @param signature: Сигнатура (типы) входных аргументов
        @param returns: тип выходного значения
        """
        pass
