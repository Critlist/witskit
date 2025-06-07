"""Requesting TCP transport reader for streaming WITS data from request/response servers."""

import socket
from typing import Generator, Optional, Callable
from .base import BaseTransport


class RequestingTCPReader(BaseTransport):
    """TCP reader that sends an initial request to trigger data streaming.
    
    Some WITS servers operate in request/response mode and wait for a client
    to send a request before they start streaming data.
    """

    def __init__(self, host: str, port: int, 
                 request_data: Optional[bytes] = None,
                 send_handshake: bool = True,
                 handshake_interval: int = 30,
                 custom_handshake: Optional[bytes] = None,
                 on_error: Optional[Callable[[Exception], None]] = None) -> None:
        """Initialize the requesting TCP reader.
        
        Args:
            host: The host to connect to
            port: The port to connect to
            request_data: The initial request to send (default: uses handshake packet)
            send_handshake: Whether to send automatic handshake packets (default: True)
            handshake_interval: Interval between handshakes in seconds (default: 30)
            custom_handshake: Custom handshake packet (default: uses WitsKit standard)
            on_error: Optional error callback function
        """
        super().__init__(send_handshake, handshake_interval, custom_handshake, on_error)
        self.host: str = host
        self.port: int = port
        # Use handshake packet as default request if none provided
        self.request_data: bytes = request_data or self.handshake_packet
        self.socket: Optional[socket.socket] = None

    def stream(self) -> Generator[str, None, None]:
        """Stream WITS frames from TCP connection with initial request."""
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.host, self.port))
        
        # Send initial request to trigger streaming
        self.socket.send(self.request_data)

        buffer: str = ""
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
                    buffer = buffer[end:]
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