"""Pason-compliant serial transport reader for WITS data with handshaking support."""

import threading
import time
from typing import Generator, Optional, Callable
from .base import BaseTransport

try:
    import serial

    HAS_SERIAL = True
except ImportError:
    HAS_SERIAL = False


class PasonSerialReader(BaseTransport):
    """
    Serial reader that implements Pason EDR handshaking requirements.

    This reader automatically sends handshake packets every 30 seconds to maintain
    WITS communication with Pason EDR systems via serial connection.

    Key Pason Requirements Implemented:
    - Sends handshake packet every 30 seconds to prevent timeout
    - Uses recommended TVD WITS packet format: &&\r\n0111-9999\r\n!!\r\n
    - Supports full duplex communication over serial
    - Handles 1984PASON/EDR headers
    """

    # Recommended handshake packet as per Pason standards (Figure 11)
    HANDSHAKE_PACKET = b"&&\r\n0111-9999\r\n!!\r\n"
    HANDSHAKE_INTERVAL = 30  # seconds

    def __init__(
        self,
        port: str,
        baudrate: int = 9600,
        send_handshake: bool = True,
        handshake_interval: int = 30,
        custom_handshake: Optional[bytes] = None,
        on_error: Optional[Callable[[Exception], None]] = None,
        **serial_kwargs,
    ) -> None:
        """Initialize the Pason serial reader.

        Args:
            port: Serial port name (e.g., 'COM1', '/dev/ttyUSB0')
            baudrate: Serial communication baud rate (default: 9600)
            send_handshake: Whether to send automatic handshake packets (default: True)
            handshake_interval: Interval between handshakes in seconds (default: 30)
            custom_handshake: Custom handshake packet (default: uses Pason recommended)
            on_error: Optional error callback function
            **serial_kwargs: Additional serial port configuration
        """
        if not HAS_SERIAL:
            raise ImportError(
                "pyserial package is required for serial communication. Install with: pip install pyserial"
            )

        self.port: str = port
        self.baudrate: int = baudrate
        self.send_handshake: bool = send_handshake
        self.handshake_interval: int = handshake_interval
        self.handshake_packet: bytes = custom_handshake or self.HANDSHAKE_PACKET
        self.on_error: Optional[Callable[[Exception], None]] = on_error
        self.serial_kwargs = serial_kwargs

        self.serial_conn: Optional[serial.Serial] = None
        self._handshake_thread: Optional[threading.Thread] = None
        self._stop_handshake: threading.Event = threading.Event()
        self._connection_active: threading.Event = threading.Event()

    def _handshake_worker(self) -> None:
        """Background worker that sends handshake packets every 30 seconds."""
        while not self._stop_handshake.wait(self.handshake_interval):
            if not self._connection_active.is_set():
                continue

            try:
                if self.serial_conn and self.serial_conn.is_open:
                    self.serial_conn.write(self.handshake_packet)
                    self.serial_conn.flush()
                    # Optional: Log handshake activity
                    # print(f"DEBUG: Sent serial handshake at {time.strftime('%H:%M:%S')}")
            except Exception as e:
                if self.on_error:
                    self.on_error(e)
                # Continue trying - connection might recover

    def stream(self) -> Generator[str, None, None]:
        """Stream WITS frames from Pason EDR via serial with automatic handshaking."""
        try:
            # Establish serial connection
            self.serial_conn = serial.Serial(
                port=self.port,
                baudrate=self.baudrate,
                timeout=1,  # 1 second timeout for read operations
                **self.serial_kwargs,
            )
            self._connection_active.set()

            # Start handshake thread if enabled
            if self.send_handshake:
                self._stop_handshake.clear()
                self._handshake_thread = threading.Thread(
                    target=self._handshake_worker, daemon=True
                )
                self._handshake_thread.start()

            # Send initial handshake to establish communication
            if self.send_handshake:
                self.serial_conn.write(self.handshake_packet)
                self.serial_conn.flush()

            buffer: str = ""
            while True:
                try:
                    if self.serial_conn.in_waiting > 0:
                        chunk: bytes = self.serial_conn.read(
                            self.serial_conn.in_waiting
                        )
                        if chunk:
                            buffer += chunk.decode("utf-8", errors="ignore")

                            # Process complete WITS frames
                            while "&&" in buffer and "!!" in buffer:
                                start: int = buffer.index("&&")

                                # Find the matching end marker
                                end_search_start = start + 2
                                end_pos = buffer.find("!!", end_search_start)
                                if end_pos == -1:
                                    break  # Incomplete frame

                                end: int = end_pos + 2
                                frame = buffer[start:end]

                                # Handle Pason EDR header filtering
                                processed_frame = self._process_pason_frame(frame)
                                if processed_frame:
                                    yield processed_frame

                                buffer = buffer[end:]
                    else:
                        # Small delay to prevent busy waiting
                        time.sleep(0.01)

                except Exception as e:
                    if self.on_error:
                        self.on_error(e)
                    break

        except Exception as e:
            if self.on_error:
                self.on_error(e)
            raise
        finally:
            self._cleanup()

    def _process_pason_frame(self, frame: str) -> Optional[str]:
        """
        Process Pason EDR frame and handle 1984PASON/EDR headers.

        Args:
            frame: Raw WITS frame from EDR

        Returns:
            Processed frame or None if frame should be filtered
        """
        lines = frame.strip().split("\n")
        processed_lines = []

        for line in lines:
            line = line.strip()
            if not line:
                continue

            # Check for 1984PASON/EDR header and handle appropriately
            if line.startswith("1984") and "PASON" in line:
                # This is the Pason EDR header - keep for now but mark it
                # In a production system, you might want to filter this based on configuration
                processed_lines.append(line)
            else:
                processed_lines.append(line)

        if processed_lines:
            return "\n".join(processed_lines)
        return None

    def _cleanup(self) -> None:
        """Clean up resources."""
        self._connection_active.clear()

        # Stop handshake thread
        if self._handshake_thread and self._handshake_thread.is_alive():
            self._stop_handshake.set()
            self._handshake_thread.join(timeout=2)

        # Close serial connection
        if self.serial_conn and self.serial_conn.is_open:
            try:
                self.serial_conn.close()
            except:
                pass
            self.serial_conn = None

    def close(self) -> None:
        """Close the serial connection and stop handshaking."""
        self._cleanup()

    def __enter__(self):
        """Context manager entry."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()
