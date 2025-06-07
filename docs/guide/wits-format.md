# WITS Format Guide

## Overview

WITS (Wellsite Information Transfer Standard) is a protocol for transmitting drilling data in real-time. This guide explains the format and how WitsKit handles it.

## Frame Structure

A WITS frame consists of:

1. **Start delimiter**: `&&`
2. **Data lines**: Symbol code (4 digits) + value
3. **End delimiter**: `!!`

### Basic Example

```
&&
01083650.40
011323.38
!!
```

This frame contains:
- **0108**: Depth Below Tool (3650.40 meters)
- **0113**: Rate of Penetration Average (23.38 m/hr)

### Multi-line Data

```
&&
01083650.40
011323.38
011412.5
012112.5
!!
```

Additional parameters:
- **0114**: Flow Rate In (12.5 L/min)
- **0121**: Weight on Bit (12.5 kN)

## Symbol Codes

WITS uses 4-digit symbol codes organized by record types:

### Record Type 1: Time-Based Drilling Data

| Code | Symbol | Description | Metric Unit | FPS Unit |
|------|--------|-------------|-------------|----------|
| 0108 | DBTM | Depth Below Tool | M | F |
| 0113 | ROPA | Rate of Penetration Average | MHR | FHR |
| 0114 | FLIN | Flow Rate In | LPM | GPM |
| 0121 | WOB | Weight on Bit | KDN | KLB |

### Record Type 2: Depth-Based Data

| Code | Symbol | Description | Metric Unit | FPS Unit |
|------|--------|-------------|-------------|----------|
| 0208 | DMEA | Depth Measured | M | F |
| 0213 | ROPD | Rate of Penetration Instantaneous | MHR | FHR |

### Record Type 8: MWD/LWD Data

| Code | Symbol | Description | Metric Unit | FPS Unit |
|------|--------|-------------|-------------|----------|
| 0801 | GRAS | Gamma Ray Short | GAPI | GAPI |
| 0811 | RESS | Resistivity Shallow | OHMM | OHMM |
| 0812 | RESM | Resistivity Medium | OHMM | OHMM |
| 0813 | RESD | Resistivity Deep | OHMM | OHMM |

## Multiple Frames

Files can contain multiple frames:

```
&&
01083650.40
011323.38
!!
&&
01083651.20
011323.45
!!
&&
01083652.10
011323.52
!!
```

Each frame represents a time-stamped measurement set.

## Units and Conversion

### Metric vs FPS Systems

WITS supports both measurement systems:

- **Metric**: Meters, liters, kilopascals, etc.
- **FPS**: Feet, gallons, PSI, etc.

### Unit Handling in WitsKit

```python
from witskit import decode_frame

# Default FPS units
result_fps = decode_frame(frame_data, use_metric_units=False)

# Metric units
result_metric = decode_frame(frame_data, use_metric_units=True)

# Convert after decoding
result = decode_frame(frame_data, use_metric_units=False)
# Convert specific values as needed
```

### Common Unit Conversions

| Parameter | Metric | FPS | Conversion |
|-----------|--------|-----|------------|
| Depth | Meters (M) | Feet (F) | 1 m = 3.28084 ft |
| Rate | m/hr (MHR) | ft/hr (FHR) | 1 m/hr = 3.28084 ft/hr |
| Pressure | kPa (KPA) | PSI | 1 kPa = 0.145038 PSI |
| Flow Rate | L/min (LPM) | gal/min (GPM) | 1 L/min = 0.264172 gal/min |

## Data Types

WITS symbols have different data types:

### Numeric Values
- **Floating point**: `3650.40`, `23.38`
- **Integer**: `1`, `0`
- **Scientific notation**: `1.23E+03`

### Text Values
- **String data**: Formation names, equipment status
- **Enumerated values**: Predefined text options

### Boolean Values
- **Binary flags**: `0` (false) or `1` (true)
- **Status indicators**: Equipment on/off states

## Special Cases

### Missing Data

When a parameter is not available:
- Value may be omitted from frame
- Or sent as empty value
- WitsKit handles both cases gracefully

### Invalid Data

```
&&
01089999.99  # Invalid depth value
!!
```

WitsKit provides error handling and validation options.

### Precision

Values maintain original precision:
```
01083650.4     # 1 decimal place
01083650.40    # 2 decimal places
01083650.400   # 3 decimal places
```

## Frame Validation

### Valid Frame Requirements

1. Must start with `&&`
2. Must end with `!!`
3. Symbol codes must be 4 digits
4. Values must be valid for symbol type

### Common Issues

#### Missing Delimiters
```
# Invalid - missing start delimiter
01083650.40
!!

# Invalid - missing end delimiter
&&
01083650.40
```

#### Invalid Symbol Codes
```
&&
10803650.40  # Invalid - 5 digits
abc3650.40   # Invalid - non-numeric
!!
```

#### Malformed Values
```
&&
0108abc      # Invalid - non-numeric value for numeric symbol
!!
```

## Real-World Examples

### Basic Drilling Frame
```
&&
01083650.40    # Depth: 3650.40 m
011323.38      # ROP: 23.38 m/hr
011412.5       # Flow In: 12.5 L/min
012112.5       # Weight on Bit: 12.5 kN
014175.0       # Standpipe Pressure: 75.0 bar
!!
```

### MWD Logging Frame
```
&&
02083652.10    # Measured Depth: 3652.10 m
080145.6       # Gamma Ray: 45.6 GAPI
081125.8       # Resistivity Shallow: 25.8 ohm·m
081212.4       # Resistivity Medium: 12.4 ohm·m
081385.2       # Resistivity Deep: 85.2 ohm·m
!!
```

### Mixed Data Frame
```
&&
01083650.40    # Drilling depth
011323.38      # ROP
080145.6       # Gamma ray
240128.5       # Surface temperature
241235.8       # Downhole temperature
!!
```

## Working with WitsKit

### Decoding Frames

```python
from witskit import decode_frame

frame = """&&
01083650.40
011323.38
!!"""

result = decode_frame(frame)
for dp in result.data_points:
    print(f"{dp.symbol_name}: {dp.parsed_value} {dp.unit}")
```

### Handling Multiple Frames

```python
from witskit.decoder import decode_file

# File with multiple frames
with open("drilling_data.wits", "r") as f:
    content = f.read()

results = decode_file(content)
for frame_result in results:
    print(f"Frame timestamp: {frame_result.timestamp}")
    for dp in frame_result.data_points:
        print(f"  {dp.symbol_name}: {dp.parsed_value}")
```

### Symbol Lookup

```python
from witskit.models.symbols import WITS_SYMBOLS

# Get symbol information
symbol = WITS_SYMBOLS.get("0108")
if symbol:
    print(f"Name: {symbol.name}")
    print(f"Description: {symbol.description}")
    print(f"Metric unit: {symbol.metric_units}")
    print(f"FPS unit: {symbol.fps_units}")
```

## Best Practices

### Frame Construction
1. Always include start/end delimiters
2. Use consistent decimal precision
3. Include timestamp information when possible
4. Group related parameters in frames

### Data Validation
1. Validate symbol codes against WITS specification
2. Check value ranges for reasonableness
3. Handle missing data gracefully
4. Implement error logging

### Performance
1. Process frames in batches for high-volume data
2. Use appropriate data storage for historical analysis
3. Consider compression for long-term storage
4. Implement buffering for real-time streams

### Error Handling
1. Validate frame format before processing
2. Handle partial frames gracefully
3. Log parsing errors with context
4. Provide fallback values for critical parameters

## Advanced Topics

### Custom Symbol Definitions

While WitsKit includes the full WITS specification, you can work with custom symbols:

```python
from witskit.models.symbols import WITSSymbol, WITSDataType, WITSUnits

# Define custom symbol
custom_symbol = WITSSymbol(
    record_type=99,
    name="CUSTOM",
    description="Custom parameter",
    data_type=WITSDataType.FLOAT,
    metric_units=WITSUnits.METERS,
    fps_units=WITSUnits.FEET
)
```

### Real-time Processing

For real-time drilling operations:

```python
from witskit.transport import TCPReader

reader = TCPReader("192.168.1.100", 12345)
for frame in reader.stream():
    result = decode_frame(frame)
    # Process real-time data
    for dp in result.data_points:
        if dp.symbol_code == "0108":  # Depth
            print(f"Current depth: {dp.parsed_value} {dp.unit}")
```

This guide provides a comprehensive understanding of the WITS format and how to work with it using WitsKit. For more advanced usage, see the [API documentation](../api/) and [examples](../../examples/). 