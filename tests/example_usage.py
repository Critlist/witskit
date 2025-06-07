#!/usr/bin/env python3
"""
Example usage of witskit transport and decoder.

This demonstrates how to stream WITS data from TCP, decode it, and display results.
"""

import sys
from pathlib import Path

# Add the current directory to Python path for imports
sys.path.insert(0, str(Path(__file__).parent))

from transport.tcp_reader import TCPReader
from transport.file_reader import FileReader
from decoder.wits_decoder import decode_frame


def tcp_example():
    """Example using TCP reader."""
    print("🌐 TCP Reader Example")
    print("====================")

    reader = TCPReader("127.0.0.1", 12345)

    try:
        frame_count = 0
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


def file_example():
    """Example using file reader."""
    print("\n📁 File Reader Example")
    print("=======================")

    # Check if sample file exists
    sample_files = [
        "sample.wits",
        "sample_comprehensive.wits",
        "sample_comprehensive_v2.wits",
    ]
    sample_file = None

    for file in sample_files:
        if Path(file).exists():
            sample_file = file
            break

    if not sample_file:
        print("❌ No sample .wits files found")
        return

    print(f"📖 Reading from {sample_file}")
    reader = FileReader(sample_file)

    try:
        frame_count = 0
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
