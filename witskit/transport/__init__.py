"""
Transport layer for WITS data sources.

This module provides various transport implementations for reading WITS data
from different sources like TCP, serial ports, and files, including Pason-compliant
readers with automatic handshaking support.
"""

from .base import BaseTransport
from .tcp_reader import TCPReader
from .requesting_tcp_reader import RequestingTCPReader
from .serial_reader import SerialReader
from .file_reader import FileReader
from .pason_tcp_reader import PasonTCPReader
from .pason_serial_reader import PasonSerialReader

__all__: list[str] = [
    "BaseTransport",
    "TCPReader",
    "RequestingTCPReader",
    "SerialReader",
    "FileReader",
    "PasonTCPReader",
    "PasonSerialReader",
]
