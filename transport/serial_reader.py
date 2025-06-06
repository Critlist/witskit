
from typing import Any, Generator, Literal, NoReturn
import serial
from .base import BaseTransport

class SerialReader(BaseTransport):
    def __init__(self, port: str, baudrate: int = 9600) -> None:
        self.serial = serial.Serial(port, baudrate=baudrate, timeout=1)

    def stream(self) -> Generator[str, Any, NoReturn]:
        buffer= ""
        while True:
            chunk: str = self.serial.read(1024).decode("utf-8", errors="ignore")
            buffer += chunk
            while "&&" in buffer and "!!" in buffer:
                start: int = buffer.index("&&")
                end: int = buffer.index("!!") + 2
                yield buffer[start:end]
                buffer: str = buffer[end:]

    def close(self) -> None:
        self.serial.close()
