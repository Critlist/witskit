#!/usr/bin/env python3
"""
Example usage of witskit transport and decoder.

This demonstrates how to stream WITS data from TCP, decode it, and display results.
"""

import sys
from pathlib import Path
from typing import Optional

# Add the current directory to Python path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from witskit.transport.tcp_reader import TCPReader
from witskit.transport.file_reader import FileReader
from witskit.decoder.wits_decoder import decode_frame


def tcp_example() -> None:
    """Example using TCP reader."""
    print("🌐 TCP Reader Example")
    print("====================")

    reader: TCPReader = TCPReader("127.0.0.1", 12345)

    try:
        frame_count: int = 0
        for frame in reader.stream():
            if frame_count >= 5:  # Limit for demo
                break

            print(f"\n📦 Frame {frame_count + 1}:")
            print(f"Raw data: {frame[:50]}...")

            try:
                result = decode_frame(frame)
                print(f"✅ Decoded {len(result.data_points)} data points:")
                for dp in result.data_points[:3]:  # Show first 3
                    print(
                        f"  {dp.symbol_code}: {dp.parsed_value} {dp.unit} ({dp.symbol_name})"
                    )
                if len(result.data_points) > 3:
                    print(f"  ... and {len(result.data_points) - 3} more")
            except Exception as e:
                print(f"❌ Decode error: {e}")

            frame_count += 1

    except ConnectionRefusedError:
        print(
            "❌ Connection refused - make sure WITS server is running on 127.0.0.1:12345"
        )
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        reader.close()
        print("🔌 Connection closed")


def file_example() -> None:
    """Example using file reader."""
    print("\n📁 File Reader Example")
    print("=======================")

    # Check if sample file exists
    sample_files: list[str] = [
        "sample.wits",
        "sample_comprehensive.wits",
        "sample_comprehensive_v2.wits",
    ]
    sample_file: Optional[str] = None

    for file in sample_files:
        if Path(file).exists():
            sample_file = file
            break

    if not sample_file:
        print("❌ No sample .wits files found")
        return

    print(f"📖 Reading from {sample_file}")
    reader: FileReader = FileReader(sample_file)

    try:
        frame_count: int = 0
        for frame in reader.stream():
            if frame_count >= 3:  # Limit for demo
                break

            print(f"\n📦 Frame {frame_count + 1}:")
            print(f"Raw data: {frame[:50]}...")

            try:
                result = decode_frame(frame)
                print(f"✅ Decoded {len(result.data_points)} data points:")
                for dp in result.data_points[:3]:  # Show first 3
                    print(
                        f"  {dp.symbol_code}: {dp.parsed_value} {dp.unit} ({dp.symbol_name})"
                    )
                if len(result.data_points) > 3:
                    print(f"  ... and {len(result.data_points) - 3} more")
            except Exception as e:
                print(f"❌ Decode error: {e}")

            frame_count += 1

    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        reader.close()
        print("📁 File reader closed")


if __name__ == "__main__":
    print("🛠️ WitsKit Transport Examples")
    print("=============================")

    # File example (always works if sample files exist)
    file_example()

    # TCP example (requires server)
    print("\n" + "=" * 50)
    tcp_example()

    print("\n🎯 Try the CLI:")
    print("• python cli.py stream file://sample.wits")
    print("• python cli.py stream tcp://127.0.0.1:12345")
    print("• python cli.py stream serial:///dev/ttyUSB0")
