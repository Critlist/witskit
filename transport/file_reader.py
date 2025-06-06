from io import TextIOWrapper
from typing import Generator, Literal, LiteralString
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
        self._file = None

    def stream(self) -> Generator[str, None, None]:
        """
        Stream WITS frames from the log file.
        
        Yields:
            Complete WITS frames as strings
        """
        with open(self.file_path, 'r', encoding='utf-8', errors='ignore') as file:
            self._file: TextIOWrapper[_WrappedBuffer] = file
            buffer: Literal[''] = ""
            
            for line in file:
                buffer += line
                
                # Look for complete frames
                while "&&" in buffer and "!!" in buffer:
                    start: int = buffer.index("&&")
                    end: int = buffer.index("!!") + 2
                    frame: LiteralString = buffer[start:end]
                    yield frame
                    buffer = buffer[end:]

    def close(self) -> None:
        """Close the file if it's open."""
        if self._file:
            self._file.close()
            self._file = None 