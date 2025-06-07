import socket
from typing import Generator, Optional
from .base import BaseTransport


class TCPReader(BaseTransport):
    def __init__(self, host: str, port: int) -> None:
        self.host: str = host
        self.port: int = port
        self.socket: Optional[socket.socket] = None

    def stream(self) -> Generator[str, None, None]:
        """Stream WITS frames from TCP connection."""
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.host, self.port))

        buffer = ""
        while True:
            try:
                chunk: str = self.socket.recv(1024).decode("utf-8", errors="ignore")
                if not chunk:  # Connection closed
                    break

                buffer += chunk
                while "&&" in buffer and "!!" in buffer:
                    start: int = buffer.index("&&")
                    end: int = buffer.index("!!") + 2
                    yield buffer[start:end]
                    buffer: str = buffer[end:]
            except ConnectionResetError:
                break
            except Exception as e:
                print(f"TCP connection error: {e}")
                break

    def close(self) -> None:
        """Close the TCP connection."""
        if self.socket:
            self.socket.close()
            self.socket = None
