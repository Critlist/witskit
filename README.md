# 🛠️ WitsKit

**WitsKit** is a Python toolkit for decoding and working with WITS (Wellsite Information Transfer Standard) data.

**Please note that I almost kind of know what i'm doing so If I did something incorrectly or badly please feel free to submit a PR. I'm very much still learning and I know this isn't the nicest codebase, but I'm working on it!
---


## 🚩 What It Does

- Parses raw WITS frames into structured, validated Python objects
- Ships with 724 symbols across 20+ record types—auto-parsed from the spec
- Includes CLI tools for symbol search, frame decoding, and validation
- Built to be extended: transports (serial, TCP) and outputs (SQLite, JSON) are plug-and-play

## 💡 Why Use It?

- 🧠 You get the *full* WITS symbol database, not someone's half-finished Excel copy
- 🔍 CLI lets you find, filter, and explore symbols without opening the spec (again)
- 📏 Works in both metric and FPS—because a boat sank and now we have 2 standards
- 🧱 Modular and testable, built with real-world telemetry in mind
- 🔒 Type-checked with `pydantic`, so your data actually means what you think it does

-Please note that I almost kind of know what i'm doing so If I did something incorrectly or badly please feel free to submit a PR.
-I'm very much still learning and I know this isnt the nicest codebase.

## 🧑‍💻 Getting Started

### Installation

**For Development:**

```bash
git clone https://github.com/yourusername/witskit
cd witskit
pip install -e .
```

**For Production (when published):**

```bash
pip install witskit
```

**With uv (recommended):**

```bash
git clone https://github.com/yourusername/witskit
cd witskit
uv pip install -e .
```

### Quick Start - Decode a WITS Frame

```python
from witskit import decode_frame

frame = """&&
01083650.40
01133.5
01142850.7
!!"""

result = decode_frame(frame)
for dp in result.data_points:
    print(f"{dp.symbol_name}: {dp.parsed_value} {dp.unit}")
```

Output:
```
DBTM: 3650.4 M
ROPA: 3.5 M/HR
HKLA: 2850.7 KDN
```

## 🕹️ CLI Commands

After installation, the `witskit` command is available globally:

**Try the demo:**

```bash
witskit demo
```

**Explore symbol database:**

```bash
witskit symbols --list-records
witskit symbols --search "depth"
witskit symbols --record 8 --search "resistivity"
```

**Decode WITS from a file:**

```bash
witskit decode sample.wits
witskit decode sample.wits --fps
witskit decode sample.wits --output results.json
```

**Decode WITS directly:**

```bash
witskit decode "&&\n01083650.40\n!!" --format table
```

**Validate WITS data:**

```bash
witskit validate "&&\n01083650.40\n!!"
```

**Convert units:**

```bash
witskit convert 3650.4 M F  # Convert 3650.4 meters to feet
witskit convert 1000 PSI KPA  # Convert 1000 PSI to kilopascals
```

### WITS File Format

Example WITS file format (sample.wits):
```
&&
01083650.40
01133.5
01142850.7
!!
&&
01083651.20
01133.7
01142855.3
!!
```

Each frame must include:

- Start line (`&&`)
- One or more data lines (4-digit symbol code + value)
- End line (`!!`)

Multiple frames can be included in a single file.

## 🧱 Project Layout

```
witskit/
├── witskit/             # Main package
│   ├── models/          # Symbol metadata, Pydantic schemas
│   ├── decoder/         # WITS frame parsing
│   ├── transport/       # Serial, TCP, file readers
│   └── cli.py          # Command-line interface
├── tests/              # Unit tests
├── pyproject.toml      # Package configuration
└── README.md           # This file
```

## 📊 Supported Record Types

| Record | Category | Description | Symbols |
|--------|----------|-------------|---------|
| 1 | Drilling | Time-Based | 40 |
| 2 | Drilling | Depth-Based | 26 |
| 8 | MWD/LWD | Formation Evaluation | 46 |
| 15 | Evaluation | Cuttings/Lithology | 54 |
| 19 | Configuration | Equipment setup | 89 |
| ... | ... | 20+ types total | 724 |

Records 5, 22–25 are defined but not implemented. You're not missing much.

## 🧪 Testing

```bash
# Run the full test suite
pytest tests/ -v

# Run specific test categories
pytest tests/test_decoder.py -v
pytest tests/test_symbols.py -v
```

## 📈 Roadmap

- ✅ Symbol parser & decoder engine
- ✅ Transport support (serial, TCP, file)
- 🚧 Output formats (SQLite, JSON, maybe Parquet if you're fancy)
- 🔜 Real-time decoding pipeline with WebSocket/MQTT
- 🔜 Web UI for monitoring decoded streams

## 🤝 Contributing

This project uses:

- Python 3.11+
- pydantic for type validation
- typer for CLI
- rich for terminal formatting
- pytest for testing

PRs welcome. Bonus points if you've ever debugged WITS over a flaky serial cable.

## 📚 References

- [WITS Specification](https://witsml.org)
- [SPE Petrowiki](https://petrowiki.spe.org)
- [SLB Oilfield Glossary](https://glossary.oilfield.slb.com)

## 📄 License

MIT. Do what you want with it—just don't sell it back to Halliburton.

---

Made by someone who got tired of writing one-off decode tools. If you work with WITS data, WitsKit's here to make your life less painful.