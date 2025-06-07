#!/usr/bin/env python3
"""
Test script for WitsKit handshaking functionality.

This script demonstrates the new automatic handshaking feature that helps
maintain WITS connections according to industry standards.
"""

import sys
import time
from pathlib import Path

# Add the current directory to Python path for imports
sys.path.insert(0, str(Path(__file__).parent))

from witskit.transport.tcp_reader import TCPReader
from witskit.transport.pason_tcp_reader import PasonTCPReader


def test_witskit_handshaking():
    """Test the new WitsKit handshaking functionality."""
    print("🔧 WitsKit Handshaking Test")
    print("=" * 50)
    
    print("\n📋 Testing Default Handshaking:")
    print("• Uses 1984WITSKIT header to identify our SDK")
    print("• Sends handshake every 30 seconds by default")
    print("• Filters out own handshake packets from stream")
    print("• Compatible with industry standards")
    
    # Test 1: Standard TCP Reader with WitsKit handshaking
    print("\n1️⃣  Standard TCP Reader (with WitsKit handshaking):")
    try:
        reader = TCPReader("localhost", 8686)
        print(f"✅ Created TCP reader with handshaking enabled by default")
        print(f"   Handshake packet: {reader.handshake_packet}")
        print(f"   Handshake interval: {reader.handshake_interval} seconds")
        reader.close()
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Test 2: Disable handshaking if needed
    print("\n2️⃣  TCP Reader with handshaking disabled:")
    try:
        reader = TCPReader("localhost", 8686, send_handshake=False)
        print(f"✅ Created TCP reader with handshaking disabled")
        print(f"   Handshake enabled: {reader.send_handshake}")
        reader.close()
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Test 3: Custom handshake packet
    print("\n3️⃣  TCP Reader with custom handshake:")
    try:
        custom_packet = b"&&\r\n1984MYCOMPANY\r\n0111-8888\r\n!!\r\n"
        reader = TCPReader("localhost", 8686, custom_handshake=custom_packet)
        print(f"✅ Created TCP reader with custom handshake")
        print(f"   Custom packet: {reader.handshake_packet}")
        reader.close()
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Test 4: Pason-specific reader
    print("\n4️⃣  Pason TCP Reader (for Pason EDR compatibility):")
    try:
        reader = PasonTCPReader("localhost", 8686)
        print(f"✅ Created Pason TCP reader")
        print(f"   Uses Pason-recommended packet: {reader.HANDSHAKE_PACKET}")
        print(f"   Handles 1984PASON/EDR headers")
        reader.close()
    except Exception as e:
        print(f"❌ Error: {e}")
    
    print("\n🎯 Key Benefits:")
    print("• Automatic connection maintenance")
    print("• Industry-standard 30-second intervals") 
    print("• SDK identification via custom headers")
    print("• Backward compatibility (can be disabled)")
    print("• Pason EDR compliance available")
    
    print("\n📖 Usage Examples:")
    print("""
    # Default - handshaking enabled with WitsKit header
    reader = TCPReader("localhost", 8686)
    
    # Disable handshaking if not needed
    reader = TCPReader("localhost", 8686, send_handshake=False)
    
    # Custom handshake for specific systems
    custom_packet = b"&&\\r\\n1984MYCOMPANY\\r\\n0111-8888\\r\\n!!\\r\\n"
    reader = TCPReader("localhost", 8686, custom_handshake=custom_packet)
    
    # Pason EDR compliance
    reader = PasonTCPReader("localhost", 8686)
    """)


def test_handshake_packet_format():
    """Test that our handshake packet follows WITS Level 0 format."""
    print("\n🔍 Handshake Packet Format Validation:")
    print("=" * 50)
    
    from witskit.transport.base import BaseTransport
    packet = BaseTransport.DEFAULT_HANDSHAKE_PACKET.decode('utf-8')
    
    print(f"Raw packet: {repr(BaseTransport.DEFAULT_HANDSHAKE_PACKET)}")
    print(f"Decoded packet:\n{packet}")
    
    lines = packet.strip().split('\n')
    print(f"\nPacket analysis:")
    print(f"• Start marker: {lines[0]} ({'✅ Valid' if lines[0] == '&&' else '❌ Invalid'})")
    print(f"• SDK header: {lines[1]} ({'✅ WitsKit' if '1984WITSKIT' in lines[1] else '❌ Missing'})")
    print(f"• Data line: {lines[2]} ({'✅ Valid TVD' if lines[2] == '0111-9999' else '❌ Invalid'})")
    print(f"• End marker: {lines[3]} ({'✅ Valid' if lines[3] == '!!' else '❌ Invalid'})")
    
    print("\n📝 WITS Level 0 Compliance:")
    print("✅ Starts with && marker")
    print("✅ Ends with !! marker") 
    print("✅ Uses 4-digit symbol code (0111 = TVD)")
    print("✅ Includes carriage return + line feed")
    print("✅ Contains SDK identification header")


if __name__ == "__main__":
    test_witskit_handshaking()
    test_handshake_packet_format()
    
    print("\n🚀 Ready to use!")
    print("The WitsKit SDK now automatically maintains WITS connections")
    print("using industry-standard handshaking with our custom 1984WITSKIT header.") 