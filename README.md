# 🛠️ WitsKit

**WitsKit** is a Python toolkit for decoding and working with WITS (Wellsite Information Transfer Standard) data. If you've ever been stuck cleaning up toolface logs at 3AM in a rattling trailer, this one's for you.

---

## 🚩 What It Does

- Parses raw WITS frames into structured, validated Python objects
- Ships with 724 symbols across 20+ record types—auto-parsed from the spec
- Includes CLI tools for symbol search, frame decoding, and validation
- Built to be extended: transports (serial, TCP) and outputs (SQLite, JSON) are plug-and-play

## 💡 Why Use It?

- 🧠 You get the *full* WITS symbol database, not someone's half-finished Excel copy
- 🔍 CLI lets you find, filter, and explore symbols without opening the spec (again)
- 📏 Works in both metric and FPS—because we don't all live in the same unit system
- 🧱 Modular and testable, built with real-world telemetry in mind
- 🔒 Type-checked with `pydantic`, so your data actually means what you think it does

## 🧑‍💻 Getting Started

```bash
git clone https://github.com/yourusername/witskit
cd witskit
pip install -e .
```

### Decode a WITS Frame
```python
from witskit import decode_frame

frame = """&&
01083650.40
01133.5
01142850.7
!!"""

result = decode_frame(frame)
for dp in result.data_points:
    print(f"{dp.symbol_name}: {dp.raw_value} {dp.unit}")
```

Output:
```
DBTM: 3650.4 M
ROPA: 3.5 M/HR
HKLA: 2850.7 KDN
```

## 🕹️ CLI Commands

Explore symbol database:
```bash
python cli.py symbols --list-records
python cli.py symbols --search "depth"
python cli.py symbols --record 8 --search "resistivity"
```

Decode WITS from a file:
```bash
python cli.py decode sample.wits
python cli.py decode sample.wits --fps
python cli.py decode sample.wits --output results.json
```

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
- One or more data lines
- End line (`!!`)

Multiple frames can be included in a single file.

Validate or debug:
```bash
python cli.py validate "&&\n01083650.40\n!!"
```

## 🧱 Project Layout

```
witskit/
├── models/           # Symbol metadata, Pydantic schemas
├── decoder/          # WITS frame parsing
├── transport/        # Serial, TCP, etc. (coming soon)
├── output/          # Export formats (coming soon)
├── cli.py           # Command-line interface
└── tests/           # Unit tests
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
```

## 📈 Roadmap

- ✅ Symbol parser & decoder engine
- 🚧 Transport support (serial, TCP, file)
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