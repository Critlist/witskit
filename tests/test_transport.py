"""
Unit tests for transport layer components.
"""

import pytest
from unittest.mock import Mock, patch, mock_open
from io import StringIO
import socket
from typing import Generator, NoReturn, Optional

from witskit.transport.base import BaseTransport
from witskit.transport.tcp_reader import TCPReader
from witskit.transport.serial_reader import SerialReader
from witskit.transport.file_reader import FileReader


class MockTransport(BaseTransport):
    """Mock transport for testing."""
    
    def __init__(self, frames: Optional[list[str]] = None) -> None:
        self.frames: list[str] = frames if frames is not None else []
        self.closed = False
    
    def stream(self) -> Generator[str, None, None]:
        """Yield mock WITS frames."""
        for frame in self.frames:
            yield frame
    
    def close(self) -> None:
        """Mark as closed."""
        self.closed = True


class TestBaseTransport:
    """Test the BaseTransport abstract base class."""
    
    def test_mock_transport_streams_frames(self) -> None:
        """Test that mock transport yields frames correctly."""
        test_frames = [
            "&&0101WELL001\n0108650.40\n!!",
            "&&0101WELL001\n0108651.50\n!!"
        ]
        
        transport = MockTransport(test_frames)
        streamed_frames = list(transport.stream())
        
        assert len(streamed_frames) == 2
        assert streamed_frames[0] == test_frames[0]
        assert streamed_frames[1] == test_frames[1]
    
    def test_mock_transport_close(self) -> None:
        """Test that transport can be closed."""
        transport = MockTransport()
        assert not transport.closed
        
        transport.close()
        assert transport.closed


class TestTCPReader:
    """Test the TCPReader implementation."""
    
    @patch('socket.socket')
    def test_tcp_reader_connection(self, mock_socket_class) -> None:
        """Test TCP connection setup."""
        mock_socket = Mock()
        mock_socket_class.return_value = mock_socket
        
        reader = TCPReader("localhost", 1234)
        
        # Start streaming to trigger connection
        stream_gen: Generator[str, None, None] = reader.stream()
        
        # Setup mock to return data then close
        mock_socket.recv.side_effect = [b"", ]  # Empty data to close connection
        
        frames = list(stream_gen)
        
        # Verify connection was attempted
        mock_socket_class.assert_called_once_with(socket.AF_INET, socket.SOCK_STREAM)
        mock_socket.connect.assert_called_once_with(("localhost", 1234))
        assert frames == []
    
    @patch('socket.socket')
    def test_tcp_reader_receives_frames(self, mock_socket_class) -> None:
        """Test TCP reader processes WITS frames correctly."""
        mock_socket = Mock()
        mock_socket_class.return_value = mock_socket
        
        # Mock data chunks that form complete WITS frames
        test_data: list[bytes] = [
            b"&&0101WELL001\n0108650.40\n!!&&0101",
            b"WELL001\n0108651.50\n!!",
            b""  # End connection
        ]
        mock_socket.recv.side_effect = test_data
        
        reader = TCPReader("localhost", 1234)
        frames = list(reader.stream())
        
        assert len(frames) == 2
        assert "&&0101WELL001" in frames[0]
        assert "0108650.40" in frames[0]
        assert frames[0].endswith("!!")
    
    @patch('socket.socket')
    def test_tcp_reader_handles_connection_error(self, mock_socket_class) -> None:
        """Test TCP reader handles connection errors gracefully."""
        mock_socket = Mock()
        mock_socket_class.return_value = mock_socket
        mock_socket.recv.side_effect = ConnectionResetError("Connection lost")
        
        reader = TCPReader("localhost", 1234)
        frames = list(reader.stream())
        
        assert frames == []
    
    def test_tcp_reader_close(self) -> None:
        """Test TCP reader close functionality."""
        reader = TCPReader("localhost", 1234)
        mock_socket = Mock()
        reader.socket = mock_socket
        
        reader.close()
        
        mock_socket.close.assert_called_once()
        assert reader.socket is None


class TestFileReader:
    """Test the FileReader implementation."""
    
    def test_file_reader_streams_frames(self) -> None:
        """Test file reader processes WITS frames from file."""
        test_content = """&&0101WELL001
0108650.40
!!
&&0101WELL001
0108651.50
!!"""
        
        with patch("builtins.open", mock_open(read_data=test_content)):
            reader = FileReader("test.wits")
            frames = list(reader.stream())
        
        assert len(frames) == 2
        assert "&&0101WELL001" in frames[0]
        assert "0108650.40" in frames[0]
        assert frames[0].endswith("!!")
    
    def test_file_reader_handles_partial_frames(self) -> None:
        """Test file reader handles incomplete frames."""
        test_content = """&&0101WELL001
0108650.40
!!
&&0101INCOMPLETE"""
        
        with patch("builtins.open", mock_open(read_data=test_content)):
            reader = FileReader("test.wits")
            frames = list(reader.stream())
        
        # Should only get the complete frame
        assert len(frames) == 1
        assert "0108650.40" in frames[0]
    
    def test_file_reader_close(self) -> None:
        """Test file reader close functionality."""
        reader = FileReader("test.wits")
        mock_file = Mock()
        reader._file = mock_file
        
        reader.close()
        
        mock_file.close.assert_called_once()
        assert reader._file is None


class TestSerialReader:
    """Test the SerialReader implementation."""
    
    @patch('serial.Serial')
    def test_serial_reader_initialization(self, mock_serial_class) -> None:
        """Test serial reader initializes with correct parameters."""
        mock_serial = Mock()
        mock_serial_class.return_value = mock_serial
        
        reader = SerialReader("/dev/ttyUSB0", 19200)
        
        mock_serial_class.assert_called_once_with("/dev/ttyUSB0", baudrate=19200, timeout=1)
        assert reader.serial == mock_serial
    
    @patch('serial.Serial')
    def test_serial_reader_receives_frames(self, mock_serial_class) -> None:
        """Test serial reader processes WITS frames correctly."""
        mock_serial = Mock()
        mock_serial_class.return_value = mock_serial
        
        # Mock serial data that forms complete WITS frames
        test_data = [
            b"&&0101WELL001\n0108650.40\n!!",
            b"&&0101WELL001\n0108651.50\n!!",
            # Keep reading indefinitely in real usage
        ]
        
        def mock_read(size) -> bytes:
            if test_data:
                return test_data.pop(0)
            return b""  # No more data
        
        mock_serial.read.side_effect = mock_read
        
        reader = SerialReader("/dev/ttyUSB0")
        
        # Get first two frames from stream
        stream_gen: Generator[str, None, None] = reader.stream()
        frames: list[str] = [next(stream_gen), next(stream_gen)]
        
        assert len(frames) == 2
        assert "&&0101WELL001" in frames[0]
        assert "0108650.40" in frames[0]
    
    @patch('serial.Serial')
    def test_serial_reader_close(self, mock_serial_class) -> None:
        """Test serial reader close functionality."""
        mock_serial = Mock()
        mock_serial_class.return_value = mock_serial
        
        reader = SerialReader("/dev/ttyUSB0")
        reader.close()
        
        mock_serial.close.assert_called_once()


if __name__ == "__main__":
    pytest.main([__file__]) 