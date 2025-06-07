"""Pason-compliant TCP transport reader for WITS data with handshaking support."""

import socket
import threading
import time
from typing import Generator, Optional, Callable
from .base import BaseTransport


class PasonTCPReader(BaseTransport):
    """
    TCP reader that implements Pason EDR handshaking requirements.
    
    This reader automatically sends handshake packets every 30 seconds to maintain
    WITS communication with Pason EDR systems, as required by Pason standards.
    
    Key Pason Requirements Implemented:
    - Sends handshake packet every 30 seconds to prevent timeout
    - Uses recommended TVD WITS packet format: &&\r\n0111-9999\r\n!!\r\n
    - Supports full duplex communication
    - Handles 1984PASON/EDR headers
    """

    # Recommended handshake packet as per Pason standards (Figure 11)
    HANDSHAKE_PACKET = b"&&\r\n0111-9999\r\n!!\r\n"
    HANDSHAKE_INTERVAL = 30  # seconds
    
    def __init__(self, host: str, port: int, 
                 send_handshake: bool = True,
                 handshake_interval: int = 30,
                 custom_handshake: Optional[bytes] = None,
                 on_error: Optional[Callable[[Exception], None]] = None) -> None:
        """Initialize the Pason TCP reader.
        
        Args:
            host: The EDR host to connect to
            port: The EDR port to connect to
            send_handshake: Whether to send automatic handshake packets (default: True)
            handshake_interval: Interval between handshakes in seconds (default: 30)
            custom_handshake: Custom handshake packet (default: uses Pason recommended)
            on_error: Optional error callback function
        """
        self.host: str = host
        self.port: int = port
        self.send_handshake: bool = send_handshake
        self.handshake_interval: int = handshake_interval
        self.handshake_packet: bytes = custom_handshake or self.HANDSHAKE_PACKET
        self.on_error: Optional[Callable[[Exception], None]] = on_error
        
        self.socket: Optional[socket.socket] = None
        self._handshake_thread: Optional[threading.Thread] = None
        self._stop_handshake: threading.Event = threading.Event()
        self._connection_active: threading.Event = threading.Event()
        
    def _handshake_worker(self) -> None:
        """Background worker that sends handshake packets every 30 seconds."""
        while not self._stop_handshake.wait(self.handshake_interval):
            if not self._connection_active.is_set():
                continue
                
            try:
                if self.socket:
                    self.socket.send(self.handshake_packet)
                    # Optional: Log handshake activity
                    # print(f"DEBUG: Sent handshake at {time.strftime('%H:%M:%S')}")
            except Exception as e:
                if self.on_error:
                    self.on_error(e)
                # Continue trying - connection might recover
                
    def stream(self) -> Generator[str, None, None]:
        """Stream WITS frames from Pason EDR with automatic handshaking."""
        try:
            # Establish connection
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
            
            # Send initial handshake to establish communication
            if self.send_handshake:
                self.socket.send(self.handshake_packet)
            
            buffer: str = ""
            while True:
                try:
                    chunk: str = self.socket.recv(1024).decode("utf-8", errors="ignore")
                    if not chunk:  # Connection closed
                        break

                    buffer += chunk
                    
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
                        
                except ConnectionResetError:
                    break
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
        lines = frame.strip().split('\n')
        processed_lines = []
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            # Check for 1984PASON/EDR header and handle appropriately
            if line.startswith('1984') and 'PASON' in line:
                # This is the Pason EDR header - keep for now but mark it
                # In a production system, you might want to filter this based on configuration
                processed_lines.append(line)
            else:
                processed_lines.append(line)
        
        if processed_lines:
            return '\n'.join(processed_lines)
        return None
    
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
        """Close the connection and stop handshaking."""
        self._cleanup()
        
    def __enter__(self):
        """Context manager entry."""
        return self
        
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close() 