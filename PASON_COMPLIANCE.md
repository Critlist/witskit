# WitsKit Pason Standards Compliance

This document outlines how WitsKit has been enhanced to meet Pason EDR standards and industry best practices for WITS communication.

## Overview

Based on the Pason standards document, we've implemented key requirements to ensure reliable WITS communication with Pason EDR systems and other industry equipment.

## Key Features Implemented

### 1. Automatic Handshaking (Default Behavior)

**Industry Requirement**: Systems must send at least one WITS packet every 30 seconds to prevent timeout.

**WitsKit Solution**: 
- All transport readers now include automatic handshaking by default
- Uses industry-standard 30-second intervals
- Custom `1984WITSKIT` header identifies our SDK
- Follows WITS Level 0 packet format

```python
# Handshaking is enabled by default
reader = TCPReader("localhost", 8686)

# Disable if not needed
reader = TCPReader("localhost", 8686, send_handshake=False)
```

### 2. Custom SDK Identification

**Our Innovation**: `1984WITSKIT` header
- Identifies WitsKit SDK in WITS streams
- Prevents conflicts with Pason's `1984PASON/EDR` header
- Helps with debugging and system identification

**Packet Format**:
```
&&\r\n
1984WITSKIT\r\n
0111-9999\r\n
!!\r\n
```

### 3. Pason EDR Compliance

**Specific Pason Features**:
- Dedicated `PasonTCPReader` and `PasonSerialReader` classes
- Uses Pason-recommended handshake packet: `&&\r\n0111-9999\r\n!!\r\n`
- Handles `1984PASON/EDR` headers properly
- Supports both half-duplex and full-duplex communication

```python
from witskit import PasonTCPReader

# Pason-compliant reader
reader = PasonTCPReader("edr_host", 8686)
```

### 4. Full Duplex Communication Support

**Implementation**:
- All readers support bidirectional communication
- Separate handshake threads don't interfere with data reception
- Automatic filtering of own handshake packets from data stream

### 5. WITS Level 0 Compliance

**Standards Met**:
- Proper `&&` start and `!!` end markers
- 4-digit symbol codes (using 0111 for TVD)
- Correct carriage return and line feed sequences
- Compatible with existing WITS infrastructure

## Transport Classes

### Base Transport Enhancement

All transport classes now inherit handshaking capabilities:

```python
class BaseTransport(ABC):
    DEFAULT_HANDSHAKE_PACKET = b"&&\r\n1984WITSKIT\r\n0111-9999\r\n!!\r\n"
    DEFAULT_HANDSHAKE_INTERVAL = 30  # seconds
```

### Enhanced Standard Readers

#### TCPReader
- Now includes automatic handshaking
- Filters own handshake packets
- Error handling with optional callbacks

#### SerialReader  
- Serial port handshaking support
- Configurable baud rates and port settings
- Non-blocking operation with proper timeouts

#### RequestingTCPReader
- Uses handshake packet as default request
- Backward compatible with existing code

### Pason-Specific Readers

#### PasonTCPReader
- Implements exact Pason recommendations
- Handles EDR-specific headers
- Configurable for different Pason modes

#### PasonSerialReader
- Serial communication with Pason EDR
- Supports toolpush and network panel connections
- Proper handling of half-duplex constraints

## Configuration Options

### Handshaking Control

```python
# Enable/disable handshaking
reader = TCPReader(host, port, send_handshake=True)

# Custom interval (default: 30 seconds)
reader = TCPReader(host, port, handshake_interval=15)

# Custom handshake packet
custom_packet = b"&&\r\n1984MYCOMPANY\r\n0111-8888\r\n!!\r\n"
reader = TCPReader(host, port, custom_handshake=custom_packet)

# Error handling callback
def handle_error(error):
    print(f"Connection error: {error}")

reader = TCPReader(host, port, on_error=handle_error)
```

## Benefits

1. **Automatic Connection Maintenance**: No more manual timeout handling
2. **Industry Compliance**: Meets Pason and general WITS standards  
3. **SDK Identification**: Clear identification in WITS streams
4. **Backward Compatibility**: Can be disabled for legacy systems
5. **Error Resilience**: Continues operation despite temporary connection issues
6. **Resource Management**: Proper cleanup of threads and connections

## Migration Guide

### Existing Code
No changes required! Handshaking is enabled by default but won't break existing functionality.

### New Pason Projects
```python
from witskit import PasonTCPReader

# Replace regular TCPReader with Pason-compliant version
reader = PasonTCPReader("edr_host", 8686)
for frame in reader.stream():
    # Process WITS data
    pass
```

### Disable Handshaking
```python
# If you need to disable handshaking for any reason
reader = TCPReader("localhost", 8686, send_handshake=False)
```

## Testing

Run the handshaking test to validate functionality:

```bash
python test_handshaking.py
```

This test validates:
- Packet format compliance
- Configuration options
- Pason-specific features
- Error handling

## References

- Pason EDR Documentation (DOCU225, Revision 40)
- WITS Level 0 Specification
- Industry best practices for drilling data communication

## Support

The handshaking implementation is designed to be:
- **Reliable**: Tested against industry standards
- **Configurable**: Adaptable to different systems
- **Maintainable**: Clean, well-documented code
- **Future-proof**: Extensible for additional protocols 