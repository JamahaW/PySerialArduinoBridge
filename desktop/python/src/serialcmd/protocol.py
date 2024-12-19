from typing import Iterable
from typing import Optional

from serialcmd.command import Command
from serialcmd.errorenum import ErrorEnum
from serialcmd.respond import RespondPolicy
from serialcmd.serializers import Primitive
from serialcmd.serializers import Serializable
from serialcmd.serializers import Serializer


class Protocol[E: ErrorEnum]:
    """Протокол - набор команды для последовательной связи"""

    def __init__(self, respond_policy: RespondPolicy[E], command_code_primitive: Primitive) -> None:
        """
        @param respond_policy: Политика обработки ответов
        @param command_code_primitive: Примитивный тип упаковки индексов команд
        """
        self._commands = list[Command]()
        self._respond_policy = respond_policy
        self._command_code_primitive = command_code_primitive

    def addCommand[S: Serializable, R: Serializable](self, name: str, signature: Optional[Serializer[S]], returns: Optional[Serializer[R]]) -> Command[S, R, E]:
        """
        Добавить команду
        @param name Имя команды для отладки
        @param signature: Сигнатура (типы) входных аргументов
        @param returns: тип выходного значения
        """
        ret = Command(
            code=self._getNextCommandCode(),
            signature=signature,
            returns=returns,
            respond_policy=self._respond_policy,
            name=name
        )

        self._commands.append(ret)
        return ret

    def getCommands(self) -> Iterable[Command]:
        """Получить список команд"""
        return self._commands

    def _getNextCommandCode(self) -> bytes:
        return self._command_code_primitive.pack(len(self._commands))
