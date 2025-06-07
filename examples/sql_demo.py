#!/usr/bin/env python3
"""
Comprehensive demo of WITS SQL storage functionality.

This script demonstrates:
1. Streaming from file to SQLite database
2. Querying data with time filters
3. Exporting data to different formats
4. Working with multiple data sources

Requirements:
    pip install witskit[sql]
"""

import asyncio
import json
from datetime import datetime, timedelta
from pathlib import Path

from witskit.storage.sql_writer import SQLWriter, DatabaseConfig
from witskit.decoder.wits_decoder import decode_frame
from witskit.transport.file_reader import FileReader


async def demo_comprehensive_sql():
    """Comprehensive demo of SQL storage capabilities."""
    
    print("🗂️ WITS SQL Storage Comprehensive Demo")
    print("=" * 60)
    
    # Create database
    db_path = "comprehensive_demo.db"
    config = DatabaseConfig.sqlite(db_path, echo=False)
    sql_writer = SQLWriter(config)
    
    try:
        print("📁 Initializing SQLite database...")
        await sql_writer.initialize()
        print("✅ Database ready with schema and symbol definitions")
        
        # Simulate multiple data sources with sample data
        sources_data = [
            {
                "source": "tcp://drilling-rig-1:12345",
                "frames": [
                    "&&\n01083650.40\n01133.5\n01142850.7\n012112750\n!!",
                    "&&\n01083651.20\n01134.2\n01142855.1\n012112800\n!!",
                    "&&\n01083652.80\n01135.8\n01142860.3\n012112850\n!!",
                ]
            },
            {
                "source": "tcp://drilling-rig-2:12346", 
                "frames": [
                    "&&\n01083645.20\n01132.8\n01142840.5\n012112700\n!!",
                    "&&\n01083646.10\n01133.1\n01142845.2\n012112720\n!!",
                ]
            },
            {
                "source": "serial:///dev/ttyUSB0",
                "frames": [
                    "&&\n01083660.00\n01136.2\n01142870.8\n012112900\n!!",
                ]
            }
        ]
        
        print(f"\n📊 Storing data from {len(sources_data)} different sources...")
        
        all_frames = []
        for source_info in sources_data:
            source = source_info["source"]
            print(f"  Processing {len(source_info['frames'])} frames from {source}")
            
            for i, frame_data in enumerate(source_info["frames"]):
                # Add slight time offset to simulate real streaming
                frame = decode_frame(
                    frame_data,
                    source=source,
                    use_metric_units=False
                )
                # Adjust timestamp to simulate time progression
                frame.frame.timestamp = datetime.now() + timedelta(seconds=i)
                all_frames.append(frame)
        
        # Store all frames in batches
        batch_size = 3
        for i in range(0, len(all_frames), batch_size):
            batch = all_frames[i:i + batch_size]
            await sql_writer.store_frames(batch)
            print(f"  💾 Stored batch {i//batch_size + 1}: {len(batch)} frames")
        
        print(f"✅ Stored {len(all_frames)} total frames")
        
        # Query and analyze the data
        print("\n🔍 Data Analysis:")
        
        # 1. Get overview
        symbols = await sql_writer.get_available_symbols()
        print(f"  📈 Available symbols: {', '.join(symbols)}")
        
        min_time, max_time = await sql_writer.get_time_range()
        if min_time and max_time:
            duration = max_time - min_time
            print(f"  ⏰ Time range: {duration.total_seconds():.1f} seconds")
        
        # 2. Source-specific analysis
        print("\n📡 Data by Source:")
        for source_info in sources_data:
            source = source_info["source"]
            source_symbols = await sql_writer.get_available_symbols(source)
            print(f"  {source}: {len(source_symbols)} symbols")
        
        # 3. Query specific drilling parameters
        print("\n📊 Depth Analysis (Symbol 0108):")
        depth_data = []
        async for dp in sql_writer.query_data_points(
            symbol_codes=["0108"],
            limit=20
        ):
            depth_data.append(dp)
        
        if depth_data:
            depths = [dp.parsed_value for dp in depth_data if dp.parsed_value is not None]
            min_depth = min(depths)
            max_depth = max(depths)
            print(f"  📏 Depth range: {min_depth} - {max_depth} feet")
            print(f"  📊 Data points: {len(depth_data)}")
        
        # 4. Time-based query (last 30 seconds)
        print("\n⏰ Recent Data (last 30 seconds):")
        recent_time = datetime.now() - timedelta(seconds=30)
        recent_data = []
        async for dp in sql_writer.query_data_points(
            symbol_codes=["0108", "0113", "0114"],
            start_time=recent_time,
            limit=50
        ):
            recent_data.append(dp)
        
        print(f"  📈 Found {len(recent_data)} recent measurements")
        
        # 5. Export sample data
        print("\n💾 Exporting sample data...")
        
        # Export depth data to JSON format
        export_data = []
        async for dp in sql_writer.query_data_points(
            symbol_codes=["0108"],
            limit=10
        ):
            export_data.append({
                "timestamp": dp.timestamp.isoformat(),
                "depth": dp.parsed_value,
                "unit": dp.unit,
                "source": dp.source
            })
        
        if export_data:
            with open("depth_export.json", "w") as f:
                json.dump(export_data, f, indent=2)
            print(f"  📄 Exported {len(export_data)} depth measurements to depth_export.json")
        
        # 6. Frame-based queries (complete drilling records)
        print("\n📦 Complete Frame Analysis:")
        frame_count = 0
        async for frame in sql_writer.query_frames(limit=3):
            frame_count += 1
            print(f"  Frame {frame_count}: {len(frame.data_points)} parameters from {frame.source}")
            
            # Show key drilling parameters
            depth = frame.get_value("0108")
            ropa = frame.get_value("0113") 
            hookload = frame.get_value("0114")
            
            if depth:
                print(f"    Depth: {depth.parsed_value} {depth.unit}")
            if ropa:
                print(f"    ROP: {ropa.parsed_value} {ropa.unit}")
            if hookload:
                print(f"    Hook Load: {hookload.parsed_value} {hookload.unit}")
        
    finally:
        await sql_writer.close()
        print(f"\n🗂️ Database saved as: {db_path}")
    
    print("\n" + "=" * 60)
    print("✅ Comprehensive demo complete!")
    print("\nYou can now explore the data using:")
    print(f"  witskit sql-query sqlite:///{db_path} --list-symbols")
    print(f"  witskit sql-query sqlite:///{db_path} --symbols '0108,0113' --limit 20")
    print(f"  witskit sql-query sqlite:///{db_path} --symbols '0108' --format csv --output depths.csv")


async def demo_file_integration():
    """Demo integration with existing file transport."""
    
    print("\n📁 File Integration Demo")
    print("=" * 40)
    
    # Check for sample files
    sample_files = [
        "examples/sample.wits",
        "examples/sample_comprehensive.wits"
    ]
    
    available_files = [f for f in sample_files if Path(f).exists()]
    
    if not available_files:
        print("⚠️ No sample files found, skipping file integration demo")
        return
    
    db_path = "file_integration_demo.db"
    config = DatabaseConfig.sqlite(db_path, echo=False)
    sql_writer = SQLWriter(config)
    
    try:
        await sql_writer.initialize()
        print("📁 Processing sample files...")
        
        for file_path in available_files:
            print(f"  📄 Processing {file_path}...")
            
            file_reader = FileReader(file_path)
            frames_processed = 0
            batch = []
            
            for frame_data in file_reader.stream():
                try:
                    frame = decode_frame(
                        frame_data,
                        source=f"file://{file_path}",
                        use_metric_units=False
                    )
                    batch.append(frame)
                    frames_processed += 1
                    
                    # Process in batches
                    if len(batch) >= 5:
                        await sql_writer.store_frames(batch)
                        batch.clear()
                        
                except Exception as e:
                    print(f"    ⚠️ Error processing frame: {e}")
            
            # Store remaining batch
            if batch:
                await sql_writer.store_frames(batch)
            
            file_reader.close()
            print(f"    ✅ Processed {frames_processed} frames")
        
        # Query the combined data
        symbols = await sql_writer.get_available_symbols()
        print(f"\n📊 Combined dataset: {len(symbols)} unique symbols")
        
        # Show data by source
        for file_path in available_files:
            source = f"file://{file_path}"
            source_symbols = await sql_writer.get_available_symbols(source)
            print(f"  {Path(file_path).name}: {len(source_symbols)} symbols")
    
    finally:
        await sql_writer.close()
        print(f"📁 File integration database: {db_path}")


if __name__ == "__main__":
    # Run the demos
    asyncio.run(demo_comprehensive_sql())
    asyncio.run(demo_file_integration()) 