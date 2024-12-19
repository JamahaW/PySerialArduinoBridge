from enum import IntEnum
from typing import Final
from typing import Iterable
from typing import Optional
from typing import Sequence

from serialcmd.commands import Command
from serialcmd.commands import ReadHelper
from serialcmd.primitives import Primitive


class Protocol[ResultType: IntEnum]:

    def __init__(self, command_code_primitive: Primitive, result: ReadHelper[ResultType]) -> None:
        self._command_code_primitive: Final[Primitive] = command_code_primitive
        self._current_command_code = 0
        self._result = result
        self._commands = list[Command[ResultType, ResultType]]()

    def addCommand[ReturnType](self, signature: Optional[Sequence[Primitive]], return_type: Optional[Primitive] = None) -> Command[ReturnType, ResultType]:
        command = Command[ReturnType, ResultType](
            self._result,
            self._command_code_primitive.pack(self._current_command_code),
            signature,
            return_type
        )
        self._commands.append(command)
        self._current_command_code += 1
        return command

    def getCommands(self) -> Iterable[Command]:
        return self._commands


if __name__ == '__main__':
    class ExampleResult(IntEnum):
        OK = 0x00


    protocol = Protocol(Primitive.u16, ReadHelper(ExampleResult, ExampleResult.OK, Primitive.u16))

    protocol.addCommand((Primitive.u8, Primitive.u32), Primitive.u16)
    protocol.addCommand(None, Primitive.f32)
    protocol.addCommand(None, None)
    protocol.addCommand((Primitive.u8,), None)

    print("\n".join(map(str, protocol.getCommands())))
