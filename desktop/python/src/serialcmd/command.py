"""Команда"""
from dataclasses import dataclass
from enum import IntEnum
from typing import Optional

from serialcmd.result import Result
from serialcmd.serializers import Serializable
from serialcmd.serializers import Serializer
from serialcmd.stream import Stream


@dataclass
class Command[S: Serializable, R: Serializable, E: IntEnum]:
    """Команда"""

    code: bytes
    """Уникальный идентификатор команды"""
    signature: Optional[Serializer[S]]
    """Входные аргументы"""
    returns: Optional[Serializer[R]]
    """Возвращаемое значение"""
    name: str
    """Имя команды для отладки"""

    def pack(self, value: S) -> bytes:
        """Компилировать команду в байты"""
        if self.signature is None:
            return self.code

        return self.code + self.signature.pack(value)

    def send(self, stream: Stream, value: S) -> Result[R, E]:
        """Отправить команду в поток"""

        stream.write(self.pack(value))

        n = NotImplemented

        respond = stream.read(n)

        returns = stream.read(self.returns.getSize())

        return Result.ok(self.returns.unpack(returns))
