from dataclasses import dataclass
from typing import Optional

from serialcmd.errorenum import ErrorEnum
from serialcmd.respond import RespondPolicy
from serialcmd.result import Result
from serialcmd.serializers import Serializable
from serialcmd.serializers import Serializer
from serialcmd.stream import Stream


@dataclass(frozen=True)
class Command[S: Serializable, R: Serializable, E: ErrorEnum]:
    """Команда"""

    code: bytes
    """Уникальный идентификатор команды"""
    signature: Optional[Serializer[S]]
    """Входные аргументы"""
    returns: Optional[Serializer[R]]
    """Возвращаемое значение"""
    respond_policy: RespondPolicy[E]
    """Обработчик ответа"""
    name: str
    """Имя команды для отладки"""

    def send(self, stream: Stream, value: S) -> Result[R, E]:
        """Отправить команду в поток"""
        stream.write(self.code)

        if self.signature is not None:
            self.signature.write(stream, value)

        return self.respond_policy.process(stream, self.returns)

    def __str__(self) -> str:
        return f"{self.name}<{self.code.hex().upper()}>({self.signature}) -> {self.respond_policy.toStr(self.returns)}"


def _test():
    from serialcmd.serializers import Struct
    from serialcmd.serializers import f64
    from serialcmd.serializers import u32

    from serialcmd.serializers import i8

    class TestErr(ErrorEnum):
        bad = 0x69
        ok = 0x00

        def getOk(self) -> ErrorEnum:
            return self.ok

    c = Command(b"\xFF", Struct((u32, f64)), i8, RespondPolicy(TestErr, u32), "test")
    print(c)


if __name__ == '__main__':
    _test()
