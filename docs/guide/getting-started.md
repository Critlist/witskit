# Getting Started with WitsKit

## Installation

### Basic Installation

```bash
pip install witskit
```

### With SQL Storage Support

For time-series analysis and database storage:

```bash
pip install witskit[sql]  # Includes PostgreSQL and MySQL drivers
```

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
from witskit.models.unit_converter import UnitConverter, WITSUnits

meters = 3650.4
feet = UnitConverter.convert_value(meters, WITSUnits.METERS, WITSUnits.FEET)
print(f"{meters}m = {feet}ft")
```

## SQL Storage and Analysis

Store WITS data in SQL databases for time-series analysis:

### Basic SQL Storage

```python
from witskit.storage.sql_writer import SQLWriter, DatabaseConfig
from witskit.decoder import decode_frame
import asyncio

async def store_data():
    # Configure SQLite database
    config = DatabaseConfig.sqlite("drilling_data.db")
    writer = SQLWriter(config)
    
    # Initialize database
    await writer.initialize()
    
    # Store a frame
    frame_data = """&&
    01083650.40
    01133.5
    !!"""
    
    result = decode_frame(frame_data)
    await writer.store_frame(result)
    
    await writer.close()

# Run the example
asyncio.run(store_data())
```

### Streaming with SQL Storage

Use the CLI for streaming data:

```bash
# Stream from TCP and store in SQLite
witskit stream tcp://192.168.1.100:12345 --sql-db sqlite:///drilling_data.db

# Stream from file with batch processing
witskit stream file://sample.wits --sql-db sqlite:///data.db --sql-batch-size 100
```

### Querying Historical Data

```bash
# List available symbols in database
witskit sql-query sqlite:///drilling_data.db --list-symbols

# Query specific drilling parameters
witskit sql-query sqlite:///drilling_data.db --symbols "0108,0113" --limit 100

# Time-based analysis
witskit sql-query sqlite:///drilling_data.db \
    --start "2024-01-01T10:00:00" \
    --end "2024-01-01T12:00:00" \
    --symbols "0108" \
    --format csv \
    --output depth_analysis.csv
```

## Next Steps

- [SQL Storage Guide](../sql_storage.md) - Complete SQL storage documentation
- [API Reference](../api/) - Detailed API documentation
- [Examples](../../examples/) - Example scripts and use cases
