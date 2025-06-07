from typing import Generator, Optional, Callable
import threading
import time
import serial
from .base import BaseTransport


class SerialReader(BaseTransport):
    def __init__(self, port: str, baudrate: int = 9600,
                 send_handshake: bool = True,
                 handshake_interval: int = 30,
                 custom_handshake: Optional[bytes] = None,
                 on_error: Optional[Callable[[Exception], None]] = None,
                 **serial_kwargs) -> None:
        """Initialize serial reader with handshaking support.
        
        Args:
            port: Serial port name (e.g., 'COM1', '/dev/ttyUSB0')
            baudrate: Serial communication baud rate (default: 9600)
            send_handshake: Whether to send automatic handshake packets (default: True)
            handshake_interval: Interval between handshakes in seconds (default: 30)
            custom_handshake: Custom handshake packet (default: uses WitsKit standard)
            on_error: Optional error callback function
            **serial_kwargs: Additional serial port configuration
        """
        super().__init__(send_handshake, handshake_interval, custom_handshake, on_error)
        self.port = port
        self.baudrate = baudrate
        self.serial_kwargs = serial_kwargs
        self.serial: Optional[serial.Serial] = None
        self._handshake_thread: Optional[threading.Thread] = None
        self._stop_handshake: threading.Event = threading.Event()
        self._connection_active: threading.Event = threading.Event()

    def _handshake_worker(self) -> None:
        """Background worker that sends handshake packets."""
        while not self._stop_handshake.wait(self.handshake_interval):
            if not self._connection_active.is_set():
                continue
                
            try:
                if self.serial and self.serial.is_open:
                    self.serial.write(self.handshake_packet)
                    self.serial.flush()
            except Exception as e:
                if self.on_error:
                    self.on_error(e)
                # Continue trying - connection might recover

    def stream(self) -> Generator[str, None, None]:
        """Stream WITS frames from serial connection with automatic handshaking."""
        try:
            self.serial = serial.Serial(
                port=self.port,
                baudrate=self.baudrate,
                timeout=1,
                **self.serial_kwargs
            )
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
                self.serial.write(self.handshake_packet)
                self.serial.flush()

            buffer: str = ""
            while True:
                if self.serial.in_waiting > 0:
                    chunk: bytes = self.serial.read(self.serial.in_waiting)
                    if chunk:
                        buffer += chunk.decode("utf-8", errors="ignore")
                        
                        while "&&" in buffer and "!!" in buffer:
                            start: int = buffer.index("&&")
                            end: int = buffer.index("!!") + 2
                            frame = buffer[start:end]
                            
                            # Filter out our own handshake packets
                            if not self._is_handshake_packet(frame):
                                yield frame
                                
                            buffer = buffer[end:]
                else:
                    # Small delay to prevent busy waiting
                    time.sleep(0.01)
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
        
        # Close serial connection
        if self.serial and self.serial.is_open:
            try:
                self.serial.close()
            except:
                pass
            self.serial = None

    def close(self) -> None:
        """Close the serial connection and stop handshaking."""
        self._cleanup()
