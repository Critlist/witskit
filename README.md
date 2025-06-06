# 🛠️ WitsKit - Complete WITS SDK

**The most comprehensive Python SDK for processing WITS (Wellsite Information Transfer Standard) data in the oil & gas drilling industry.**

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://python.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![WITS Standard](https://img.shields.io/badge/WITS-Level%200--4-green.svg)](https://witsml.org)

## ✨ Features

### 🔥 **Industry-Complete Symbol Database**

- **724 symbols** across **20 record types** from the official WITS specification
- Full coverage of drilling, MWD/LWD, formation evaluation, and completion operations
- Automatically parsed from the official WITS HTML specification

### 📊 **Comprehensive Record Type Support**

- **Drilling Operations**: Time-based, depth-based, and connection data
- **MWD/LWD**: Formation evaluation, mechanical data, and resistivity logs  
- **Gas Monitoring**: Chromatography and hydrocarbon detection
- **Formation Evaluation**: Pressure analysis, cuttings, and lithology
- **Operations**: Cementing, DST, mud reports, and bit reports
- **Configuration**: Drill string, rig setup, and equipment specs

### ⚡ **Modern Python Architecture**

- **Type-safe** with Pydantic models and comprehensive validation
- **Fast parsing** with optimized regex patterns
- **Flexible units** supporting both metric and FPS systems
- **Rich logging** with structured error handling

### 🎯 **Developer-Friendly CLI**

- **Interactive exploration** of 724 symbols with advanced search
- **Multi-format output** (table, JSON, raw) for integration
- **Real-time validation** and debugging tools
- **Beautiful terminal UI** with Rich formatting

### 🔌 **Extensible Design**

- **Transport layer ready** for serial, TCP, and file inputs
- **Output adapters** for SQLite, JSON, and custom formats
- **Plugin architecture** for custom symbol definitions
- **Multi-frame processing** with batch operations

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/witskit
cd witskit

# Install dependencies
pip install -r requirements.txt

# Or install in development mode
pip install -e .
```

### Decode Your First WITS Frame

```python
from witskit import decode_frame

# Sample WITS frame with drilling data
frame = """&&
01083650.40
01133.5
01142850.7
!!"""

result = decode_frame(frame)
print(f"Decoded {len(result.data_points)} parameters:")
for dp in result.data_points:
    print(f"{dp.symbol_name}: {dp.parsed_value} {dp.unit}")
```

Output:
```
Decoded 3 parameters:
DBTM: 3650.4 M
ROPA: 3.5 M/HR  
HKLA: 2850.7 KDN
```

**Note**: Output depends on which symbols are currently defined in the symbol database.

## 🎮 Interactive CLI

### Explore the Complete WITS Specification

```bash
# List all 20+ record types
python cli.py symbols --list-records

# Search across 724 symbols
python cli.py symbols --search "depth"

# Focus on specific operations
python cli.py symbols --record 8 --search "resistivity"
```

### Process Real WITS Data

```bash
# Decode from file
python cli.py decode sample.wits

# Use FPS units instead of metric
python cli.py decode sample.wits --fps

# Export to JSON
python cli.py decode sample.wits --output results.json
```

### Validate and Debug

```bash
# Validate frame format
python cli.py validate "&&\n01083650.40\n!!"

# Run interactive demo
python cli.py demo
```

## 📈 Comprehensive Examples

### Multi-Record Type Processing

```python
from witskit import WITSDecoder

# Process comprehensive drilling data
decoder = WITSDecoder(use_metric_units=True)

# Decode drilling operations (Record 1)
drilling_frame = """&&
01083650.40
01133.5
01142850.7
012112750
!!"""

# Decode MWD formation evaluation (Record 8)  
mwd_frame = """&&
08154.2
081615.8
08239.7
08241.3
!!"""

# Process both frames
for frame in [drilling_frame, mwd_frame]:
    result = decoder.decode_frame(frame)
    print(f"Record type data: {len(result.data_points)} parameters")
```

### Advanced Symbol Exploration

```python
from witskit.models.symbols import (
    get_record_types, 
    search_symbols,
    get_symbols_by_record_type
)

# Find all depth-related symbols
depth_symbols = search_symbols("depth")
print(f"Found {len(depth_symbols)} depth-related symbols")

# Get all MWD symbols
mwd_symbols = get_symbols_by_record_type(8)
print(f"MWD record has {len(mwd_symbols)} symbols")

# List all available record types
record_types = get_record_types()
print(f"Supporting {len(record_types)} record types")
```

### Batch Processing

```python
import glob
from witskit import WITSDecoder

decoder = WITSDecoder()

# Process all WITS files in directory
for file_path in glob.glob("data/*.wits"):
    with open(file_path) as f:
        content = f.read()
    
    # Split multiple frames
    frames = content.split('&&')[1:]  # Skip empty first element
    frames = ['&&' + frame for frame in frames]
    
    results = decoder.decode_multiple_frames(frames, source=file_path)
    print(f"{file_path}: {len(results)} frames processed")
```

## 🔬 Technical Specifications

### Supported WITS Record Types

| Record | Category | Description | Symbols |
|--------|----------|-------------|---------|
| 1 | Drilling | General Time-Based | 40 |
| 2 | Drilling | Depth-Based | 26 |  
| 3 | Drilling | Connections | 21 |
| 4 | Drilling | Hydraulics | 34 |
| 6 | Tripping | Connections | 29 |
| 7 | Surveying | Directional | 21 |
| 8 | MWD/LWD | Formation Evaluation | 46 |
| 9 | MWD/LWD | Mechanical | 20 |
| 10 | Evaluation | Pressure Analysis | 24 |
| 11 | Operations | Mud Tank Volumes | 30 |
| 12 | Evaluation | Chromatography (Cycle) | 23 |
| 13 | Evaluation | Chromatography (Depth) | 43 |
| 14 | Evaluation | Lagged Mud Properties | 24 |
| 15 | Evaluation | Cuttings/Lithology | 54 |
| 16 | Evaluation | Hydrocarbon Shows | 41 |
| 17 | Operations | Cementing | 33 |
| 18 | Operations | Drill Stem Testing | 26 |
| 19 | Configuration | Configuration | 89 |
| 20 | Configuration | Mud Report | 60 |
| 21 | Configuration | Bit Report | 40 |

*Note: Record types 5, 22-25 are defined in the WITS specification but not yet implemented in this version.*

### Data Types & Units

- **ASCII (A)**: Text strings and identifiers
- **Float (F)**: Decimal measurements with full precision  
- **Integer (S)**: Short integers (2 bytes)
- **Long (L)**: Long integers (4 bytes)

**Units**: Comprehensive support for both metric (M, KPA, KGM3, DEGC) and FPS (F, PSI, PPG, DEGF) unit systems.

## 🏗️ Architecture

```
witskit/
├── models/           # Data models and validation
│   ├── symbols.py    # 724 WITS symbols (auto-generated)
│   └── wits_frame.py # Frame structure and validation
├── decoder/          # Core decoding engine  
│   └── wits_decoder.py
├── transport/        # Input sources (under development)
├── output/           # Export formats (under development)
├── cli.py           # Command-line interface
└── tests/           # Comprehensive test suite
```

## 🧪 Testing

Run the comprehensive test suite:

```bash
# Run all tests
python -m pytest tests/ -v

# Test specific functionality
python -m pytest tests/test_decoder.py -v

# Test with the demo
python cli.py demo
```

## 🤝 Contributing

We welcome contributions! This project uses:

- **Modern Python** (3.11+) with type hints
- **Pydantic** for data validation  
- **Rich** for beautiful terminal output
- **Typer** for CLI framework
- **pytest** for testing

### Adding New Features

1. **Symbol definitions**: Auto-generated from WITS specification
2. **Transport layers**: Add new input sources (serial, TCP, etc.)  
3. **Output formats**: Add new export options
4. **Custom validations**: Extend the validation framework

## 📚 Resources

- [WITS Specification](https://witsml.org) - Official WITS standards
- [Oil & Gas Drilling Primer](https://petrowiki.spe.org) - Industry background
- [MWD/LWD Technology](https://glossary.oilfield.slb.com) - Logging technology

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details.

## 🎯 Roadmap

- **Phase 2**: Transport layer (serial, TCP, file readers) - *In Progress*
- **Phase 3**: Output adapters (SQLite, JSON, custom) - *In Progress*
- **Phase 4**: Real-time streaming and WebSocket support
- **Phase 5**: WITS Level 1-4 support (binary formats)

## ⚠️ Current Status

This is an active development project. Core features are functional but some advanced features are still under development:

- ✅ **Complete symbol database** (724 symbols)
- ✅ **Core decoder** with type validation
- ✅ **Interactive CLI** with search and exploration
- ✅ **Comprehensive testing framework**
- 🚧 **Transport layer** (basic structure in place)
- 🚧 **Output adapters** (basic structure in place)
- 🚧 **Real-time streaming** (planned)

---

**Built with ❤️ for the oil & gas drilling community**

*Transform your WITS data processing with the most complete Python SDK available.*