from dataclasses import dataclass

from serialcmd.errorenum import ErrorEnum
from serialcmd.core.result import Result
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

    def process[R: Serializable](self, stream: Stream, returns: Serializer[R]) -> Result[R, E]:
        """Считать результат с потока (получить ответ)"""
        code = self.error_enum(self.error_primitive.read(stream))

        if code != self.error_enum.getOk():
            return Result.err(code)

        return Result.ok(returns.read(stream))

    def toStr(self, ret: Serializer) -> str:
        """Получить строковое представление для отладки"""
        return f"({ret}, {self.error_enum.__name__}<{self.error_primitive}>)"
