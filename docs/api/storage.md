# Storage API Reference

## Overview

The storage module provides interfaces and implementations for storing WITS data in various backends.

## SQL Writer

::: witskit.storage.sql_writer.SQLWriter
    options:
      show_root_heading: true
      show_source: true
      heading_level: 3

::: witskit.storage.sql_writer.DatabaseConfig
    options:
      show_root_heading: true
      show_source: true
      heading_level: 3

## Base Storage Interface

::: witskit.storage.base.StorageBackend
    options:
      show_root_heading: true
      show_source: true
      heading_level: 3

## Database Schema

::: witskit.storage.schema
    options:
      show_root_heading: true
      show_source: true
      heading_level: 3

## Usage Examples

### Basic SQL Storage

```python
import asyncio
from witskit.storage.sql_writer import SQLWriter, DatabaseConfig
from witskit.decoder import decode_frame

async def example():
    # Configure database
    config = DatabaseConfig.sqlite("example.db")
    writer = SQLWriter(config)
    
    # Initialize
    await writer.initialize()
    
    # Store data
    frame = decode_frame("&&\n01083650.40\n!!")
    await writer.store_frame(frame)
    
    # Query data
    async for dp in writer.query_data_points(
        symbol_codes=["0108"],
        limit=10
    ):
        print(f"{dp.symbol_name}: {dp.parsed_value}")
    
    await writer.close()

asyncio.run(example())
```

### Batch Processing

```python
async def batch_example():
    config = DatabaseConfig.sqlite("batch.db")
    writer = SQLWriter(config)
    await writer.initialize()
    
    # Store multiple frames at once
    frames = [
        decode_frame("&&\n01083650.40\n!!"),
        decode_frame("&&\n01083651.20\n!!")
    ]
    
    await writer.store_frames(frames)
    await writer.close()

asyncio.run(batch_example())
```

### Time-based Queries

```python
from datetime import datetime, timedelta

async def time_query_example():
    config = DatabaseConfig.sqlite("time_data.db")
    writer = SQLWriter(config)
    await writer.initialize()
    
    # Query last hour of data
    end_time = datetime.now()
    start_time = end_time - timedelta(hours=1)
    
    async for dp in writer.query_data_points(
        symbol_codes=["0108", "0113"],
        start_time=start_time,
        end_time=end_time
    ):
        print(f"{dp.timestamp}: {dp.symbol_name} = {dp.parsed_value}")
    
    await writer.close()

asyncio.run(time_query_example())
```

### Database Configuration Examples

```python
# SQLite (file-based)
sqlite_config = DatabaseConfig.sqlite("data.db")

# PostgreSQL
postgres_config = DatabaseConfig(
    database_type="postgresql",
    database_url="postgresql+asyncpg://user:pass@localhost/wits",
    echo_sql=False
)

# MySQL
mysql_config = DatabaseConfig(
    database_type="mysql",
    database_url="mysql+aiomysql://user:pass@localhost/wits",
    echo_sql=False
)
``` 