# Getting Started with WitsKit

## Basic Usage

WitsKit makes it easy to work with WITS data. Here's a quick example:

```python
from witskit import decode_frame

# Parse a WITS frame
frame = """&&
01083650.40
01133.5
01142850.7
!!"""

result = decode_frame(frame)
for dp in result.data_points:
    print(f"{dp.symbol_name}: {dp.parsed_value} {dp.unit}")
```

## Working with Files

```python
from witskit.transport import FileReader

# Read from a WITS file
reader = FileReader("path/to/your/data.wits")
for frame in reader.read_frames():
    for dp in frame.data_points:
        print(f"{dp.symbol_name}: {dp.parsed_value} {dp.unit}")
```

## Real-time Data

```python
from witskit.transport import SerialReader

# Read from a serial port
reader = SerialReader(port="COM1", baudrate=9600)
for frame in reader.read_frames():
    # Process real-time WITS data
    pass
```

## Unit Conversion

WitsKit handles both metric and FPS (Foot-Pound-Second) units:

```python
from witskit.models import convert_units

meters = 3650.4
feet = convert_units(meters, from_unit="M", to_unit="F")
print(f"{meters}m = {feet}ft")
```
