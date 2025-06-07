#!/usr/bin/env python3
"""
Test script for WITS streaming functionality.

This script connects to a WITS simulator running on localhost:8686
and tests the streaming, decoding, and display of WITS data.
"""

import sys
import time
import signal
from pathlib import Path
from typing import Optional, Dict, Any
from datetime import datetime
try:
    from tqdm import tqdm
    HAS_TQDM = True
except ImportError:
    HAS_TQDM = False

# Add the current directory to Python path for imports
sys.path.insert(0, str(Path(__file__).parent))

from witskit.transport.tcp_reader import TCPReader
from witskit.decoder.wits_decoder import decode_frame
import socket


class RequestingTCPReader(TCPReader):
    """TCPReader that sends an initial request to trigger data streaming."""
    
    def stream(self):
        """Stream WITS frames from TCP connection with initial request."""
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.host, self.port))
        
        # Send initial request to trigger streaming
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


class WitsStreamTester:
    """Test class for WITS streaming functionality."""
    
    def __init__(self, host: str = "localhost", port: int = 8686):
        """Initialize the WITS stream tester.
        
        Args:
            host: The host to connect to (default: localhost)
            port: The port to connect to (default: 8686)
        """
        self.host = host
        self.port = port
        self.reader: Optional[TCPReader] = None
        self.running = True
        self.stats = {
            "frames_received": 0,
            "frames_decoded": 0,
            "decode_errors": 0,
            "connection_errors": 0,
            "start_time": None,
            "last_frame_time": None
        }
        
        # Set up signal handler for graceful shutdown
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)
    
    def _signal_handler(self, signum, frame):
        """Handle shutdown signals gracefully."""
        print(f"\n🛑 Received shutdown signal ({signum})")
        self.running = False
    
    def test_connection(self) -> bool:
        """Test if we can connect to the WITS server.
        
        Returns:
            True if connection is successful, False otherwise
        """
        print(f"🔍 Testing connection to {self.host}:{self.port}...")
        
        try:
            self.reader = RequestingTCPReader(self.host, self.port)
            # Try to get the generator (this will attempt connection and send request)
            print("📤 Sending initial request to simulator...")
            stream_gen = self.reader.stream()
            
            # Try to get one frame with timeout
            print("⏳ Waiting for first frame...")
            start_time = time.time()
            timeout = 10  # 10 second timeout
            
            import signal
            
            def timeout_handler(signum, frame):
                raise TimeoutError("Connection test timeout")
            
            # Set up timeout for Windows/Unix compatibility
            try:
                # This works on Unix systems
                signal.signal(signal.SIGALRM, timeout_handler)
                signal.alarm(timeout)
            except AttributeError:
                # Windows doesn't have SIGALRM, we'll use a different approach
                pass
            
            frame_received = False
            for frame in stream_gen:
                if time.time() - start_time > timeout:
                    print("❌ Connection test timeout - no frame received within 10 seconds")
                    break
                    
                print("✅ Connection successful! Received first frame.")
                print(f"📦 First frame preview: {frame[:100]}...")
                frame_received = True
                break
            
            try:
                signal.alarm(0)  # Cancel alarm
            except AttributeError:
                pass
                
            if frame_received:
                return True
            else:
                print("❌ No frames received within timeout period")
                return False
            
        except ConnectionRefusedError:
            print(f"❌ Connection refused to {self.host}:{self.port}")
            print("   Make sure your WITS simulator is running and listening on this port")
            return False
        except TimeoutError:
            print("❌ Connection test timeout")
            return False
        except Exception as e:
            print(f"❌ Connection error: {e}")
            return False
        finally:
            try:
                signal.alarm(0)  # Cancel any pending alarm
            except AttributeError:
                pass
            if self.reader:
                self.reader.close()
    
    def stream_and_decode(self, max_frames: Optional[int] = None, duration: Optional[int] = None) -> None:
        """Stream WITS data and decode frames.
        
        Args:
            max_frames: Maximum number of frames to process (None for unlimited)
            duration: Maximum duration in seconds (None for unlimited)
        """
        print(f"🌊 Starting WITS stream from {self.host}:{self.port}")
        if max_frames:
            print(f"📊 Will process maximum {max_frames} frames")
        if duration:
            print(f"⏱️  Will run for maximum {duration} seconds")
        
        print("   Press Ctrl+C to stop streaming\n")
        
        self.reader = RequestingTCPReader(self.host, self.port)
        self.stats["start_time"] = datetime.now()
        
        # Initialize progress bar if available
        pbar = None
        if HAS_TQDM and max_frames:
            pbar = tqdm(total=max_frames, desc="Processing frames", unit="frame", 
                       bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}, {rate_fmt}]")
        elif HAS_TQDM and duration:
            pbar = tqdm(total=duration, desc="Streaming time", unit="sec",
                       bar_format="{l_bar}{bar}| {elapsed}s/{total}s [{rate_fmt}]")
        
        last_stats_time = time.time()
        
        try:
            stream_gen = self.reader.stream()
            
            for frame in stream_gen:
                if not self.running:
                    break
                
                current_time = time.time()
                elapsed_seconds = (datetime.now() - self.stats["start_time"]).total_seconds()
                
                # Check duration limit
                if duration and elapsed_seconds >= duration:
                    if pbar:
                        pbar.update(duration - pbar.n)
                        pbar.close()
                    print(f"⏱️  Duration limit ({duration}s) reached")
                    break
                
                # Check frame limit
                if max_frames and self.stats["frames_received"] >= max_frames:
                    if pbar:
                        pbar.close()
                    print(f"📊 Frame limit ({max_frames}) reached")
                    break
                
                self.stats["frames_received"] += 1
                self.stats["last_frame_time"] = datetime.now()
                
                # Update progress bar
                if pbar:
                    if max_frames:
                        pbar.update(1)
                        pbar.set_postfix({
                            'decoded': self.stats["frames_decoded"],
                            'errors': self.stats["decode_errors"],
                            'rate': f"{self.stats['frames_received']/elapsed_seconds:.1f}/s" if elapsed_seconds > 0 else "0.0/s"
                        })
                    elif duration:
                        pbar.n = min(elapsed_seconds, duration)
                        pbar.set_postfix({
                            'frames': self.stats["frames_received"],
                            'decoded': self.stats["frames_decoded"],
                            'rate': f"{self.stats['frames_received']/elapsed_seconds:.1f}/s" if elapsed_seconds > 0 else "0.0/s"
                        })
                        pbar.refresh()
                
                # Only show detailed output every few frames when using progress bar, or always when not using it
                show_detail = not HAS_TQDM or self.stats["frames_received"] <= 3 or self.stats["frames_received"] % 5 == 0
                
                if show_detail:
                    print(f"\n📦 Frame #{self.stats['frames_received']} ({datetime.now().strftime('%H:%M:%S')})")
                    print(f"   Raw data: {frame[:80]}...")
                
                # Try to decode the frame
                try:
                    result = decode_frame(frame)
                    self.stats["frames_decoded"] += 1
                    
                    if show_detail:
                        print(f"✅ Decoded {len(result.data_points)} data points:")
                        
                        # Display first few data points
                        for i, dp in enumerate(result.data_points[:3]):
                            print(f"   • {dp.symbol_code}: {dp.parsed_value} {dp.unit} ({dp.symbol_name})")
                        
                        if len(result.data_points) > 3:
                            print(f"   ... and {len(result.data_points) - 3} more data points")
                        
                        # Show any errors/warnings from decoding
                        if hasattr(result, 'errors') and result.errors:
                            print(f"⚠️  Decode warnings: {len(result.errors)} issues")
                    
                except Exception as e:
                    self.stats["decode_errors"] += 1
                    if show_detail:
                        print(f"❌ Decode error: {e}")
                
                # Show running statistics every 20 frames (less frequent when using progress bar)
                if current_time - last_stats_time > 5.0:  # Every 5 seconds
                    if not HAS_TQDM:
                        self._show_stats()
                        # Show simple progress for non-tqdm users
                        if max_frames:
                            progress_pct = (self.stats["frames_received"] / max_frames) * 100
                            print(f"Progress: {progress_pct:.1f}% ({self.stats['frames_received']}/{max_frames})")
                        elif duration:
                            progress_pct = (elapsed_seconds / duration) * 100
                            print(f"Progress: {progress_pct:.1f}% ({elapsed_seconds:.1f}s/{duration}s)")
                    last_stats_time = current_time
                
        except ConnectionRefusedError:
            print(f"❌ Connection refused to {self.host}:{self.port}")
            self.stats["connection_errors"] += 1
        except Exception as e:
            print(f"❌ Streaming error: {e}")
            self.stats["connection_errors"] += 1
        finally:
            if pbar:
                pbar.close()
            if self.reader:
                self.reader.close()
            print("\n🔌 Connection closed")
    
    def _show_stats(self) -> None:
        """Display current streaming statistics."""
        runtime = (datetime.now() - self.stats["start_time"]).total_seconds()
        frames_per_sec = self.stats["frames_received"] / runtime if runtime > 0 else 0
        decode_rate = (self.stats["frames_decoded"] / self.stats["frames_received"] * 100) if self.stats["frames_received"] > 0 else 0
        
        print(f"\n📈 Statistics:")
        print(f"   • Runtime: {runtime:.1f}s")
        print(f"   • Frames received: {self.stats['frames_received']}")
        print(f"   • Frames decoded: {self.stats['frames_decoded']}")
        print(f"   • Decode errors: {self.stats['decode_errors']}")
        print(f"   • Frames/sec: {frames_per_sec:.2f}")
        print(f"   • Decode rate: {decode_rate:.1f}%")
    
    def show_final_stats(self) -> None:
        """Display final statistics."""
        if not self.stats["start_time"]:
            print("📊 No streaming session recorded")
            return
        
        runtime = (datetime.now() - self.stats["start_time"]).total_seconds()
        frames_per_sec = self.stats["frames_received"] / runtime if runtime > 0 else 0
        decode_rate = (self.stats["frames_decoded"] / self.stats["frames_received"] * 100) if self.stats["frames_received"] > 0 else 0
        
        print(f"\n📊 Final Statistics:")
        print(f"{'='*50}")
        print(f"Runtime: {runtime:.1f} seconds")
        print(f"Frames received: {self.stats['frames_received']}")
        print(f"Frames decoded successfully: {self.stats['frames_decoded']}")
        print(f"Decode errors: {self.stats['decode_errors']}")
        print(f"Connection errors: {self.stats['connection_errors']}")
        print(f"Average frames/sec: {frames_per_sec:.2f}")
        print(f"Decode success rate: {decode_rate:.1f}%")
        
        if self.stats["last_frame_time"]:
            print(f"Last frame received: {self.stats['last_frame_time'].strftime('%H:%M:%S')}")


def main():
    """Main function to run the WITS streaming test."""
    print("🛠️  WITS Streaming Test Tool")
    print("="*50)
    
    if HAS_TQDM:
        print("📊 Progress bars enabled (tqdm available)")
    else:
        print("📊 Basic progress display (install tqdm for progress bars: pip install tqdm)")
    
    # Create tester instance
    tester = WitsStreamTester("localhost", 8686)
    
    # Test connection first
    if not tester.test_connection():
        print("\n❌ Connection test failed!")
        print("Please check that your WITS simulator is:")
        print("• Running and accessible")
        print("• Listening on localhost:8686")
        print("• Sending WITS formatted data")
        sys.exit(1)
    
    print("\n" + "="*50)
    
    # Ask user for streaming parameters
    try:
        print("🔧 Streaming Options:")
        print("1. Stream 20 frames (quick test)")
        print("2. Stream for 30 seconds") 
        print("3. Stream for 60 seconds")
        print("4. Stream unlimited (Ctrl+C to stop)")
        
        choice = input("\nEnter your choice (1-4): ").strip()
        
        if choice == "1":
            tester.stream_and_decode(max_frames=20)
        elif choice == "2":
            tester.stream_and_decode(duration=30)
        elif choice == "3":
            tester.stream_and_decode(duration=60)
        elif choice == "4":
            tester.stream_and_decode()
        else:
            print("Invalid choice, defaulting to 20 frames")
            tester.stream_and_decode(max_frames=20)
            
    except KeyboardInterrupt:
        print("\n🛑 Interrupted by user")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
    finally:
        tester.show_final_stats()


if __name__ == "__main__":
    main() 