#!/usr/bin/env python3
"""
Example script demonstrating SQL storage of WITS data.

This script shows how to:
1. Set up a SQLite database for WITS data storage
2. Stream and store WITS data from multiple sources
3. Query stored data with time-based filters
4. Export data to different formats

Requirements:
    pip install witskit[sql]
"""

import asyncio
from datetime import datetime, timedelta
from pathlib import Path

from witskit.storage.sql_writer import SQLWriter, DatabaseConfig
from witskit.decoder.wits_decoder import decode_frame
from witskit.transport.file_reader import FileReader


async def demo_sql_storage():
    """Demonstrate SQL storage functionality."""
    
    print("🛠️ WITS SQL Storage Demo")
    print("=" * 50)
    
    # 1. Create database configuration (SQLite for simplicity)
    db_path = "demo_drilling_data.db"
    config = DatabaseConfig.sqlite(db_path, echo=True)
    
    print(f"📁 Creating SQLite database: {db_path}")
    
    # 2. Initialize SQL writer
    sql_writer = SQLWriter(config)
    await sql_writer.initialize()
    print("✅ Database initialized with tables and symbol definitions")
    
    try:
        # 3. Load and store sample WITS data
        sample_frames = [
            """&&
01083650.40
011323.38
011412.5
012112.5
!!""",
            """&&
01083651.20
011324.15
011413.2
012113.1
!!""",
            """&&
01083652.80
011325.92
011414.8
012114.7
!!"""
        ]
        
        print("\n📊 Processing sample WITS frames...")
        
        # Decode and store frames
        decoded_frames = []
        for i, frame_data in enumerate(sample_frames):
            frame = decode_frame(
                frame_data, 
                source=f"demo_source_{i%2}",  # Simulate multiple sources
                use_metric_units=True
            )
            decoded_frames.append(frame)
            print(f"  Decoded frame {i+1}: {len(frame.data_points)} data points")
        
        # Store all frames in batch
        await sql_writer.store_frames(decoded_frames)
        print(f"✅ Stored {len(decoded_frames)} frames to database")
        
        # 4. Query stored data
        print("\n🔍 Querying stored data...")
        
        # Get available symbols
        symbols = await sql_writer.get_available_symbols()
        print(f"Available symbols: {', '.join(symbols)}")
        
        # Get time range
        min_time, max_time = await sql_writer.get_time_range()
        print(f"Data time range: {min_time} to {max_time}")
        
        # Query specific symbols
        print("\n📈 Querying depth and temperature data...")
        depth_data = []
        async for data_point in sql_writer.query_data_points(
            symbol_codes=["0108"],  # Depth symbol
            limit=10
        ):
            depth_data.append(data_point)
        
        print(f"Found {len(depth_data)} depth measurements:")
        for dp in depth_data:
            print(f"  {dp.timestamp.strftime('%H:%M:%S')}: {dp.parsed_value} {dp.unit}")
        
        # 5. Advanced queries with time filtering
        print("\n⏰ Time-based filtering demo...")
        
        # Get data from the last minute
        one_minute_ago = datetime.now() - timedelta(minutes=1)
        recent_data = []
        async for data_point in sql_writer.query_data_points(
            symbol_codes=["0108", "0113"],
            start_time=one_minute_ago,
            limit=20
        ):
            recent_data.append(data_point)
        
        print(f"Data points from last minute: {len(recent_data)}")
        
        # 6. Query frames (grouped data)
        print("\n📦 Querying complete frames...")
        frame_count = 0
        async for frame in sql_writer.query_frames(limit=2):
            frame_count += 1
            print(f"Frame {frame_count}: {len(frame.data_points)} data points from {frame.source}")
            for dp in frame.data_points:
                print(f"  {dp.symbol_code}: {dp.parsed_value} {dp.unit}")
        
    finally:
        # Clean up
        await sql_writer.close()
        print("\n🧹 Database connection closed")
    
    print(f"\n✅ Demo complete! Database saved as: {db_path}")
    print("You can now query this database using:")
    print(f"  witskit sql-query sqlite:///{db_path} --list-symbols")
    print(f"  witskit sql-query sqlite:///{db_path} --symbols 0108,0113 --limit 10")


async def demo_file_streaming():
    """Demonstrate streaming from WITS file and storing to SQL."""
    
    print("\n" + "=" * 50)
    print("📁 File Streaming to SQL Demo")
    print("=" * 50)
    
    # Check if sample file exists
    sample_file = Path("sample.wits")
    if not sample_file.exists():
        print(f"❌ Sample file {sample_file} not found")
        return
    
    # Create database
    db_path = "file_streaming_demo.db"
    config = DatabaseConfig.sqlite(db_path)
    sql_writer = SQLWriter(config)
    await sql_writer.initialize()
    
    try:
        print(f"📖 Reading WITS data from {sample_file}")
        
        # Stream from file
        file_reader = FileReader(str(sample_file))
        frames_processed = 0
        batch = []
        
        for frame_data in file_reader.stream():
            try:
                decoded_frame = decode_frame(
                    frame_data,
                    source=f"file://{sample_file}",
                    use_metric_units=True
                )
                batch.append(decoded_frame)
                frames_processed += 1
                
                # Process in batches of 10
                if len(batch) >= 10:
                    await sql_writer.store_frames(batch)
                    print(f"  Stored batch of {len(batch)} frames")
                    batch.clear()
                    
            except Exception as e:
                print(f"  ⚠️ Error processing frame {frames_processed + 1}: {e}")
        
        # Store remaining batch
        if batch:
            await sql_writer.store_frames(batch)
            print(f"  Stored final batch of {len(batch)} frames")
        
        file_reader.close()
        
        print(f"✅ Processed {frames_processed} frames from file")
        
        # Query the results
        symbols = await sql_writer.get_available_symbols()
        print(f"Available symbols: {', '.join(symbols)}")
        
    finally:
        await sql_writer.close()
        print(f"Database saved as: {db_path}")


if __name__ == "__main__":
    # Run the demos
    asyncio.run(demo_sql_storage())
    asyncio.run(demo_file_streaming()) 