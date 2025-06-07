#!/usr/bin/env python3
"""
Quick streaming test with progress bar.
"""

import sys
import time
from pathlib import Path
from datetime import datetime
try:
    from tqdm import tqdm
    HAS_TQDM = True
except ImportError:
    HAS_TQDM = False

# Add the current directory to Python path for imports
sys.path.insert(0, str(Path(__file__).parent))

from witskit.decoder.wits_decoder import decode_frame
import socket

class RequestingTCPReader:
    """TCPReader that sends an initial request to trigger data streaming."""
    
    def __init__(self, host: str, port: int) -> None:
        self.host = host
        self.port = port
        self.socket = None
    
    def stream(self):
        """Stream WITS frames from TCP connection with initial request."""
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.host, self.port))
        
        # Send initial request to trigger streaming
        print("📤 Sending request to simulator...")
        self.socket.send(b"&&\r\n")
        
        buffer = ""
        while True:
            try:
                chunk = self.socket.recv(1024).decode("utf-8", errors="ignore")
                if not chunk:  # Connection closed
                    break

                buffer += chunk
                while "&&" in buffer and "!!" in buffer:
                    start = buffer.index("&&")
                    end = buffer.index("!!") + 2
                    yield buffer[start:end]
                    buffer = buffer[end:]
            except ConnectionResetError:
                break
            except Exception as e:
                print(f"TCP connection error: {e}")
                break
    
    def close(self):
        if self.socket:
            self.socket.close()
            self.socket = None

def main():
    print("🚀 Quick WITS Streaming Test")
    print("="*40)
    
    reader = RequestingTCPReader("localhost", 8686)
    
    try:
        print("🌊 Starting stream...")
        frames_processed = 0
        start_time = datetime.now()
        
        # Use progress bar if available
        if HAS_TQDM:
            pbar = tqdm(total=20, desc="Processing frames", unit="frame")
        
        for frame in reader.stream():
            frames_processed += 1
            
            if HAS_TQDM:
                pbar.update(1)
                pbar.set_postfix({'frame': frames_processed})
            
            print(f"\n📦 Frame {frames_processed}:")
            print(f"   Raw: {frame[:60]}...")
            
            # Try to decode
            try:
                result = decode_frame(frame)
                print(f"✅ Decoded {len(result.data_points)} data points")
                
                # Show first few
                for dp in result.data_points[:3]:
                    print(f"   • {dp.symbol_code}: {dp.parsed_value} {dp.unit}")
                    
            except Exception as e:
                print(f"❌ Decode error: {e}")
            
            if frames_processed >= 20:
                break
        
        if HAS_TQDM:
            pbar.close()
        
        runtime = (datetime.now() - start_time).total_seconds()
        print(f"\n🎉 Processed {frames_processed} frames in {runtime:.1f}s")
        print(f"Rate: {frames_processed/runtime:.1f} frames/sec")
        
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        reader.close()

if __name__ == "__main__":
    main() 