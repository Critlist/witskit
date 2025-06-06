from typing import Generator, TextIO
from .base import BaseTransport


class FileReader(BaseTransport):
    """
    FileReader for reading WITS frames from a log file.
    Useful for testing and processing recorded WITS data.
    """
    
    def __init__(self, file_path: str) -> None:
        """
        Initialize FileReader with path to WITS log file.
        
        Args:
            file_path: Path to the .wits log file
        """
        self.file_path: str = file_path
        self._file: TextIO | None = None

    def stream(self) -> Generator[str, None, None]:
        """
        Stream WITS frames from the log file.
        
        Yields:
            Complete WITS frames as strings
        """
        if self._file is None:
            self._file = open(self.file_path, 'r', encoding='utf-8', errors='ignore')
        
        buffer: str = ""
        
        try:
            for line in self._file:
                buffer += line
                
                # Look for complete frames
                while "&&" in buffer and "!!" in buffer:
                    start: int = buffer.index("&&")
                    end: int = buffer.index("!!") + 2
                    frame: str = buffer[start:end]
                    yield frame
                    buffer = buffer[end:]
        finally:
            # Auto-close when generator is exhausted or an exception occurs
            self.close()

    def close(self) -> None:
        """Close the file if it's open."""
        if self._file:
            self._file.close()
            self._file = None 