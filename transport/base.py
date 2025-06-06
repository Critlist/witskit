from abc import ABC, abstractmethod
from typing import Generator

class BaseTransport(ABC):
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


