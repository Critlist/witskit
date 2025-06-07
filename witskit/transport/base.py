from abc import ABC, abstractmethod
from typing import Generator, Optional, Callable


class BaseTransport(ABC):
    """Base class for WITS transport implementations."""

    # Default WitsKit handshake packet with custom header
    # Uses TVD (Total Vertical Depth) symbol 0111 with dummy value -9999
    DEFAULT_HANDSHAKE_PACKET = b"&&\r\n1984WITSKIT\r\n0111-9999\r\n!!\r\n"
    DEFAULT_HANDSHAKE_INTERVAL = 30  # seconds, per industry standard

    def __init__(
        self,
        send_handshake: bool = True,
        handshake_interval: int = 30,
        custom_handshake: Optional[bytes] = None,
        on_error: Optional[Callable[[Exception], None]] = None,
    ):
        """Initialize base transport with handshaking configuration.

        Args:
            send_handshake: Whether to send automatic handshake packets (default: True)
            handshake_interval: Interval between handshakes in seconds (default: 30)
            custom_handshake: Custom handshake packet (default: uses WitsKit standard)
            on_error: Optional error callback function
        """
        self.send_handshake = send_handshake
        self.handshake_interval = handshake_interval
        self.handshake_packet = custom_handshake or self.DEFAULT_HANDSHAKE_PACKET
        self.on_error = on_error

    @abstractmethod
    def stream(self) -> Generator[str, None, None]:
        """
        Yields decoded WITS frames (as raw strings) from the source.
        """
        pass

    def close(self) -> None:
        """
        Optional cleanup, override if needed (e.g. closing sockets/ports).
        """
        pass
