"""TCP transport reader for streaming WITS data with automatic handshaking."""

import socket
import threading
import time
from typing import Generator, Optional, Callable
from .base import BaseTransport


class TCPReader(BaseTransport):
    def __init__(self, host: str, port: int,
                 send_handshake: bool = True,
                 handshake_interval: int = 30,
                 custom_handshake: Optional[bytes] = None,
                 on_error: Optional[Callable[[Exception], None]] = None) -> None:
        """Initialize TCP reader with handshaking support.
        
        Args:
            host: The host to connect to
            port: The port to connect to
            send_handshake: Whether to send automatic handshake packets (default: True)
            handshake_interval: Interval between handshakes in seconds (default: 30)
            custom_handshake: Custom handshake packet (default: uses WitsKit standard)
            on_error: Optional error callback function
        """
        super().__init__(send_handshake, handshake_interval, custom_handshake, on_error)
        self.host: str = host
        self.port: int = port
        self.socket: Optional[socket.socket] = None
        self._handshake_thread: Optional[threading.Thread] = None
        self._stop_handshake: threading.Event = threading.Event()
        self._connection_active: threading.Event = threading.Event()

    def _handshake_worker(self) -> None:
        """Background worker that sends handshake packets."""
        while not self._stop_handshake.wait(self.handshake_interval):
            if not self._connection_active.is_set():
                continue
                
            try:
                if self.socket:
                    self.socket.send(self.handshake_packet)
            except Exception as e:
                if self.on_error:
                    self.on_error(e)
                # Continue trying - connection might recover

    def stream(self) -> Generator[str, None, None]:
        """Stream WITS frames from TCP connection with automatic handshaking."""
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect((self.host, self.port))
            self._connection_active.set()
            
            # Start handshake thread if enabled
            if self.send_handshake:
                self._stop_handshake.clear()
                self._handshake_thread = threading.Thread(
                    target=self._handshake_worker, 
                    daemon=True
                )
                self._handshake_thread.start()
                
                # Send initial handshake
                self.socket.send(self.handshake_packet)

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
                        frame = buffer[start:end]
                        
                        # Filter out our own handshake packets
                        if not self._is_handshake_packet(frame):
                            yield frame
                            
                        buffer = buffer[end:]
                except ConnectionResetError:
                    break
                except Exception as e:
                    if self.on_error:
                        self.on_error(e)
                    else:
                        print(f"TCP connection error: {e}")
                    break
        finally:
            self._cleanup()
    
    def _is_handshake_packet(self, frame: str) -> bool:
        """Check if frame is our own handshake packet."""
        return "1984WITSKIT" in frame and "0111-9999" in frame
    
    def _cleanup(self) -> None:
        """Clean up resources."""
        self._connection_active.clear()
        
        # Stop handshake thread
        if self._handshake_thread and self._handshake_thread.is_alive():
            self._stop_handshake.set()
            self._handshake_thread.join(timeout=2)
        
        # Close socket
        if self.socket:
            try:
                self.socket.close()
            except:
                pass
            self.socket = None

    def close(self) -> None:
        """Close the TCP connection and stop handshaking."""
        self._cleanup()
