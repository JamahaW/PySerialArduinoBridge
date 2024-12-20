from dataclasses import dataclass
from typing import Optional

from serialcmd.core.result import Result
from serialcmd.errorenum import ErrorEnum
from serialcmd.serializers import Primitive
from serialcmd.serializers import Serializable
from serialcmd.serializers import Serializer
from serialcmd.streams.abc import Stream


@dataclass(frozen=True)
class RespondPolicy[E: ErrorEnum]:
    """Политика обработки ответа"""

    error_enum: type[E]
    """enum-класс ошибок (коды результата)"""

    error_primitive: Primitive
    """примитивный тип"""

    def read[R: Optional[Serializable]](self, stream: Stream, returns: Optional[Serializer[R]]) -> Result[R, E]:
        """Считать результат с потока (получить ответ)"""
        code = self.error_enum(self.error_primitive.read(stream))

        if code != self.error_enum.getOk():
            return Result.err(code)

        if returns is None:
            return Result.ok(None)

        return Result.ok(returns.read(stream))

    def toStr(self, ret: Serializer) -> str:
        """Получить строковое представление для отладки"""
        return f"({ret}, {self.error_enum.__name__}<{self.error_primitive}>)"


def _test():
    from serialcmd.streams.mock import MockStream
    from serialcmd.serializers import u8
    from serialcmd.serializers import u16
    from io import BytesIO

    class TestError(ErrorEnum):
        ok = 0x69
        bad = 0x42

        @classmethod
        def getOk(cls) -> ErrorEnum:
            return cls.ok

    stream = MockStream(input=BytesIO(b"\x69\x39\x30"), output=BytesIO())
    responder = RespondPolicy[TestError](TestError, u8)

    result = responder.read(stream, u16)

    try:
        print(f"{result.isOk()=}, {result.isErr()=}, {result.unwrap()=}")

    except ValueError as e:
        print(e)

    return


if __name__ == '__main__':
    _test()
