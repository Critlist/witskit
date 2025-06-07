# CLI Usage Guide

WitsKit provides a comprehensive command-line interface for decoding, analyzing, and storing WITS data.

## Installation

```bash
# Basic installation
pip install witskit

# With SQL storage support
pip install witskit[sql]
```

## Quick Start

```bash
# Try the demo
witskit demo

# Get help
witskit --help
```

## Core Commands

### 1. Decode Command

Decode WITS frames from strings or files:

```bash
# Decode a WITS frame directly
witskit decode "&&\n01083650.40\n011323.38\n!!"

# Decode from file
witskit decode sample.wits

# Output formats
witskit decode sample.wits --format json
witskit decode sample.wits --format table
witskit decode sample.wits --format raw

# Save results
witskit decode sample.wits --output results.json

# Use metric units (default is FPS)
witskit decode sample.wits --metric

# Convert all values after decoding
witskit decode sample.wits --fps --convert-to-metric
witskit decode sample.wits --metric --convert-to-fps

# Strict mode (fail on unknown symbols)
witskit decode sample.wits --strict
```

### 2. Symbols Command

Explore the WITS symbol database:

```bash
# List all record types
witskit symbols --list-records

# Search symbols by name or description
witskit symbols --search "depth"
witskit symbols --search "pressure"

# Filter by record type
witskit symbols --record 1  # Drilling record type 1
witskit symbols --record 8  # MWD/LWD record type 8

# Combined search and filter
witskit symbols --record 8 --search "resistivity"
```

### 3. Convert Command

Convert between drilling industry units:

```bash
# Basic conversions
witskit convert 30 MHR FHR        # Drilling rate
witskit convert 2500 PSI KPA      # Pressure
witskit convert 800 GPM LPM       # Flow rate
witskit convert 150 DEGF DEGC     # Temperature

# High precision
witskit convert 2500 PSI KPA --precision 5

# Show conversion formula
witskit convert 30 MHR FHR --formula

# List all available units
witskit convert 0 _ _ --list-units
```

### 4. Validate Command

Validate WITS frame format:

```bash
# Validate a frame
witskit validate "&&\n01083650.40\n!!"

# Validate from file
witskit validate sample.wits
```

## Streaming and Storage

### 5. Stream Command

Stream WITS data from various sources with optional SQL storage:

#### Basic Streaming

```bash
# Stream from TCP server
witskit stream tcp://192.168.1.100:12345

# Stream from serial port
witskit stream serial:///dev/ttyUSB0 --baudrate 19200

# Stream from file (for testing)
witskit stream file://sample.wits

# Limit number of frames
witskit stream tcp://localhost:12345 --max-frames 10

# Different output formats
witskit stream tcp://localhost:12345 --format json
witskit stream tcp://localhost:12345 --format raw
```

#### SQL Storage

Store streaming data in databases:

```bash
# SQLite database
witskit stream tcp://192.168.1.100:12345 --sql-db sqlite:///drilling_data.db

# PostgreSQL database
witskit stream tcp://192.168.1.100:12345 --sql-db postgresql://user:pass@localhost/wits

# MySQL database
witskit stream tcp://192.168.1.100:12345 --sql-db mysql://user:pass@localhost/wits

# Batch processing for performance
witskit stream tcp://192.168.1.100:12345 \
    --sql-db sqlite:///data.db \
    --sql-batch-size 50

# Debug SQL statements
witskit stream tcp://192.168.1.100:12345 \
    --sql-db sqlite:///data.db \
    --sql-echo
```

### 6. SQL Query Command

Query stored WITS data from SQL databases:

#### Database Exploration

```bash
# List available symbols in database
witskit sql-query sqlite:///drilling_data.db --list-symbols

# Show time range of data
witskit sql-query sqlite:///drilling_data.db --time-range
```

#### Data Queries

```bash
# Query specific symbols
witskit sql-query sqlite:///drilling_data.db --symbols "0108,0113" --limit 100

# Time-based filtering
witskit sql-query sqlite:///drilling_data.db \
    --symbols "0108,0113" \
    --start "2024-01-01T10:00:00" \
    --end "2024-01-01T12:00:00"

# Filter by data source
witskit sql-query sqlite:///drilling_data.db \
    --symbols "0108" \
    --source "tcp://192.168.1.100:12345"
```

#### Export Options

```bash
# Table format (default)
witskit sql-query sqlite:///drilling_data.db --symbols "0108" --format table

# JSON export
witskit sql-query sqlite:///drilling_data.db --symbols "0108" --format json

# CSV export
witskit sql-query sqlite:///drilling_data.db \
    --symbols "0108" \
    --format csv \
    --output depth_data.csv

# JSON export to file
witskit sql-query sqlite:///drilling_data.db \
    --symbols "0108,0113" \
    --format json \
    --output drilling_analysis.json
```

## Common Use Cases

### Development and Testing

```bash
# Quick demo
witskit demo

# Validate your WITS files
witskit validate *.wits

# Explore symbols before coding
witskit symbols --search "depth"
witskit symbols --record 1
```

### Data Analysis

```bash
# Decode and analyze files
witskit decode historical_data.wits --format json --output analysis.json

# Convert units for standardization
witskit decode data.wits --fps --convert-to-metric

# Stream file data to database for analysis
witskit stream file://historical_data.wits --sql-db sqlite:///analysis.db
```

### Production Monitoring

```bash
# Real-time streaming to database
witskit stream tcp://rig-server:12345 \
    --sql-db postgresql://user:pass@analytics-server/drilling \
    --sql-batch-size 100

# Monitor serial data
witskit stream serial:///dev/ttyUSB0 \
    --baudrate 19200 \
    --sql-db sqlite:///live_data.db
```

### Historical Analysis

```bash
# Query drilling depth progression
witskit sql-query sqlite:///drilling_data.db \
    --symbols "0108" \
    --start "2024-01-01" \
    --format csv \
    --output depth_progression.csv

# Analyze drilling rates
witskit sql-query sqlite:///drilling_data.db \
    --symbols "0113" \
    --time-range
```

## Global Options

All commands support these global options:

```bash
# Show version
witskit --version

# Get help for any command
witskit decode --help
witskit stream --help
witskit sql-query --help
```

## Environment Variables

Set these environment variables for convenience:

```bash
# Default SQL database
export WITSKIT_DEFAULT_DB="sqlite:///drilling_data.db"

# Default serial port
export WITSKIT_SERIAL_PORT="/dev/ttyUSB0"

# Default TCP server
export WITSKIT_TCP_HOST="192.168.1.100:12345"
```

## Error Handling

WitsKit provides helpful error messages:

```bash
# Invalid WITS frame
witskit decode "invalid frame"
# ❌ Error: Invalid WITS frame format

# Unknown symbol in strict mode
witskit decode sample.wits --strict
# ❌ Error: Unknown symbol code: 9999

# Database connection issues
witskit stream tcp://localhost:12345 --sql-db postgresql://invalid
# ❌ Error: Failed to connect to database: connection refused
```

## Tips and Best Practices

1. **Start with the demo**: `witskit demo` to understand the basics
2. **Explore symbols first**: Use `witskit symbols` to understand your data
3. **Validate before processing**: Use `witskit validate` on your WITS files
4. **Use SQL storage for analysis**: Store data in databases for complex queries
5. **Batch processing**: Use `--sql-batch-size` for high-volume streaming
6. **Monitor with time ranges**: Use `--start` and `--end` for focused analysis 