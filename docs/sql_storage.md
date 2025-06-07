# SQL Storage for WITS Data

The WitsKit SQL storage module provides a robust, timeseries-optimized database backend for storing and querying WITS drilling data. It supports SQLite, PostgreSQL, and MySQL databases with full async operation support.

## Features

- **Timeseries Optimized**: Database schema designed for efficient time-based queries
- **Multiple Databases**: Support for SQLite, PostgreSQL, and MySQL
- **Async Operations**: Non-blocking database operations for high-performance streaming
- **Batch Processing**: Efficient bulk insertions for streaming data
- **Symbol Normalization**: Automatic storage of WITS symbol definitions
- **Rich Querying**: Time-based filtering, symbol filtering, and statistical queries
- **CLI Integration**: Direct integration with witskit CLI commands

## Installation

Install with SQL dependencies:

```bash
# SQLite support (included by default)
pip install witskit[sql]

# PostgreSQL support
pip install witskit[postgres]

# MySQL support  
pip install witskit[mysql]

# All database support
pip install witskit[sql,postgres,mysql]
```

## Quick Start

### 1. Stream and Store Data

Stream WITS data directly to a SQLite database:

```bash
# Stream from TCP source to SQLite
witskit stream tcp://192.168.1.100:12345 --sql-db sqlite:///drilling_data.db

# Stream from serial port to PostgreSQL
witskit stream serial:///dev/ttyUSB0 --sql-db postgresql://user:pass@localhost/wits_db

# Batch processing for better performance
witskit stream tcp://localhost:12345 --sql-db sqlite:///data.db --sql-batch-size 50
```

### 2. Query Stored Data

Query the stored data with powerful filtering:

```bash
# List available symbols
witskit sql-query sqlite:///drilling_data.db --list-symbols

# Query specific drilling parameters
witskit sql-query sqlite:///drilling_data.db --symbols "0108,0113" --limit 100

# Time-based queries
witskit sql-query sqlite:///drilling_data.db \
    --symbols "0108" \
    --start "2024-01-01T10:00:00" \
    --end "2024-01-01T12:00:00"

# Export to CSV
witskit sql-query sqlite:///drilling_data.db \
    --symbols "0108,0113" \
    --format csv \
    --output drilling_data.csv
```

## Database Schema

The SQL storage uses a normalized, timeseries-optimized schema:

### Tables

**wits_symbols** - Symbol definitions (metadata)

- `symbol_code` (Primary Key): 4-digit WITS symbol code
- `name`: Human-readable symbol name
- `description`: Detailed description
- `data_type`: Data type (A/F/S/L)
- `fps_unit`, `metric_unit`: Unit information
- `record_type`: WITS record type

**wits_frames** - Frame metadata

- `id` (Primary Key): Auto-increment frame ID
- `timestamp`: Frame timestamp
- `source`: Data source identifier
- `raw_data`: Original raw WITS frame
- `created_at`: Database insertion time

**wits_data_points** - Individual measurements (main timeseries table)

- `id` (Primary Key): Auto-increment ID
- `frame_id`: Reference to wits_frames
- `symbol_code`: Reference to wits_symbols
- `timestamp`: Measurement timestamp
- `source`: Data source identifier
- `raw_value`: Original string value
- `numeric_value`: Parsed numeric value (if applicable)
- `string_value`: Parsed string value (if applicable)
- `unit`: Measurement unit

**wits_sources** - Source tracking and statistics

- `source` (Primary Key): Source identifier
- `first_seen`, `last_seen`: Activity timestamps
- `total_frames`, `total_data_points`: Statistics
- `is_active`: Active status flag

### Indexes

The schema includes optimized indexes for timeseries queries:

- Primary timeseries: `(symbol_code, timestamp)`
- Source-specific: `(symbol_code, source, timestamp)`
- Time range: `(timestamp, symbol_code)`
- Latest values: `(symbol_code, source, timestamp DESC)`

## Programming API

### Basic Usage

```python
import asyncio
from witskit.storage.sql_writer import SQLWriter, DatabaseConfig

async def store_data():
    # Create database configuration
    config = DatabaseConfig.sqlite("drilling_data.db")
    
    # Initialize writer
    sql_writer = SQLWriter(config)
    await sql_writer.initialize()
    
    try:
        # Store decoded WITS frames
        await sql_writer.store_frames(decoded_frames)
        
        # Query data points
        async for data_point in sql_writer.query_data_points(
            symbol_codes=["0108", "0113"],
            start_time=start_time,
            end_time=end_time,
            limit=1000
        ):
            print(f"{data_point.timestamp}: {data_point.parsed_value}")
    
    finally:
        await sql_writer.close()

# Run async function
asyncio.run(store_data())
```

### Database Configurations

**SQLite**

```python
config = DatabaseConfig.sqlite("path/to/database.db", echo=False)
```

**PostgreSQL**

```python
config = DatabaseConfig.postgresql(
    host="localhost",
    port=5432,
    username="postgres",
    password="password",
    database="wits_data"
)
```

**MySQL**
```python
config = DatabaseConfig.mysql(
    host="localhost",
    port=3306,
    username="root",
    password="password",
    database="wits_data"
)
```

### Advanced Querying

**Time-based filtering**

```python
from datetime import datetime, timedelta

# Query last hour of data
start_time = datetime.now() - timedelta(hours=1)
async for dp in sql_writer.query_data_points(
    symbol_codes=["0108"],
    start_time=start_time,
    limit=1000
):
    print(f"Depth: {dp.parsed_value} {dp.unit}")
```

**Source filtering**

```python
# Query data from specific source
async for dp in sql_writer.query_data_points(
    symbol_codes=["0108", "0113"],
    source="tcp://192.168.1.100:12345"
):
    print(f"{dp.symbol_name}: {dp.parsed_value}")
```

**Frame-based queries**

```python
# Query complete frames with all data points
async for frame in sql_writer.query_frames(
    start_time=start_time,
    end_time=end_time,
    limit=10
):
    print(f"Frame from {frame.source}: {len(frame.data_points)} measurements")
```

## Performance Optimization

### Batch Processing

For high-throughput streaming, use batch processing:

```python
batch = []
batch_size = 100

for frame_data in stream:
    decoded_frame = decode_frame(frame_data)
    batch.append(decoded_frame)
    
    if len(batch) >= batch_size:
        await sql_writer.store_frames(batch)
        batch.clear()

# Store remaining batch
if batch:
    await sql_writer.store_frames(batch)
```

### Index Usage

The schema is optimized for common query patterns:

- **Timeseries queries**: Use symbol_code + timestamp filters
- **Latest values**: Query with ORDER BY timestamp DESC LIMIT 1
- **Range queries**: Use timestamp-based WHERE clauses
- **Multi-source**: Include source in WHERE clause for optimal performance

### Connection Pooling

For production deployments, configure appropriate connection pools:

```python
config = DatabaseConfig.postgresql(
    host="localhost",
    database="wits_data",
    pool_size=10,          # Number of persistent connections
    max_overflow=20        # Additional connections under load
)
```

## CLI Reference

### Stream Command SQL Options

```bash
witskit stream <source> [OPTIONS]

SQL Storage Options:
  --sql-db TEXT             Database URL (sqlite:///path.db, postgresql://...)
  --sql-batch-size INTEGER  Batch size for SQL inserts (default: 100)
  --sql-echo                Echo SQL statements for debugging
```

### SQL Query Command

```bash
witskit sql-query <database> [OPTIONS]

Options:
  --symbols TEXT            Comma-separated symbol codes (e.g., "0108,0113")
  --start TEXT             Start time (ISO format: 2024-01-01T10:00:00)
  --end TEXT               End time (ISO format: 2024-01-01T12:00:00)
  --source TEXT            Filter by data source
  --limit INTEGER          Maximum records to return (default: 1000)
  --format TEXT            Output format: table, json, csv (default: table)
  --output PATH            Output file
  --list-symbols           List available symbols in database
  --time-range             Show time range of data in database
```

## Examples

### Complete Streaming Example

```bash
# Start streaming from TCP source to database
witskit stream tcp://drilling-rig:12345 \
    --sql-db sqlite:///rig_data.db \
    --sql-batch-size 50 \
    --metric

# In another terminal, query the live data
witskit sql-query sqlite:///rig_data.db \
    --symbols "0108,0113,0114" \
    --start "2024-01-01T08:00:00" \
    --format table
```

### Data Analysis Workflow

```bash
# 1. Check what data is available
witskit sql-query sqlite:///drilling_data.db --list-symbols
witskit sql-query sqlite:///drilling_data.db --time-range

# 2. Export drilling parameters for analysis
witskit sql-query sqlite:///drilling_data.db \
    --symbols "0108,0113,0114,0115" \
    --start "2024-01-01T00:00:00" \
    --end "2024-01-01T23:59:59" \
    --format csv \
    --output daily_drilling_report.csv

# 3. Query specific time periods
witskit sql-query sqlite:///drilling_data.db \
    --symbols "0108" \
    --start "2024-01-01T14:30:00" \
    --end "2024-01-01T15:30:00" \
    --format json \
    --output depth_analysis.json
```

## Best Practices

1. **Use batch processing** for high-throughput streaming (50-100 frames per batch)
2. **Include time filters** in queries to leverage indexes effectively
3. **Use appropriate connection pools** for production deployments
4. **Monitor database size** and implement retention policies for long-term operations
5. **Use specific symbol filters** rather than querying all symbols when possible
6. **Consider partitioning** large tables by time for very high-volume deployments

## Troubleshooting

### Common Issues

**Import Errors**

```bash
# Install SQL dependencies
pip install witskit[sql]

# For specific databases
pip install witskit[postgres]  # PostgreSQL
pip install witskit[mysql]     # MySQL
```

**Connection Issues**

```bash
# Test database connection
witskit sql-query <database_url> --list-symbols

# Enable SQL debugging
witskit stream <source> --sql-db <database_url> --sql-echo
```

**Performance Issues**

- Increase batch size: `--sql-batch-size 200`
- Use connection pooling for production
- Add indexes for custom query patterns
- Consider database-specific optimizations (PostgreSQL: work_mem, MySQL: innodb_buffer_pool_size)

### Monitoring

Monitor database performance:

```sql
-- SQLite: Check database size
SELECT page_count * page_size AS size_bytes FROM pragma_page_count(), pragma_page_size();

-- PostgreSQL: Check table sizes
SELECT schemaname, tablename, pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) AS size
FROM pg_tables WHERE schemaname = 'public';

-- MySQL: Check table sizes  
SELECT table_name, ROUND(((data_length + index_length) / 1024 / 1024), 2) AS 'Size (MB)'
FROM information_schema.TABLES WHERE table_schema = 'wits_data';
``` 