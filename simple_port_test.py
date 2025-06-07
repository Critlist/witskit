#!/usr/bin/env python3
"""
Simple port connectivity test for WITS simulator.
"""

import socket
import time
import sys

def test_port_connectivity(host="localhost", port=8686, timeout=5):
    """Test basic TCP connectivity to a host and port."""
    print(f"🔍 Testing basic TCP connectivity to {host}:{port}...")
    
    try:
        # Create a socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        
        # Try to connect
        result = sock.connect_ex((host, port))
        sock.close()
        
        if result == 0:
            print(f"✅ Port {port} is open and accepting connections")
            return True
        else:
            print(f"❌ Port {port} is not accessible (error code: {result})")
            return False
            
    except socket.gaierror as e:
        print(f"❌ Hostname resolution failed: {e}")
        return False
    except Exception as e:
        print(f"❌ Connection test failed: {e}")
        return False

def test_data_reception(host="localhost", port=8686, timeout=10):
    """Test if we can receive data from the port."""
    print(f"📡 Testing data reception from {host}:{port}...")
    
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        
        print(f"🔌 Connecting to {host}:{port}...")
        sock.connect((host, port))
        print("✅ Connected! Waiting for data...")
        
        # Try to receive some data
        start_time = time.time()
        data_received = False
        
        while time.time() - start_time < timeout:
            try:
                sock.settimeout(1)  # Short timeout for each recv
                data = sock.recv(1024)
                if data:
                    print(f"✅ Received data: {data[:100]}...")
                    data_received = True
                    break
                else:
                    print("⚠️  Connection closed by remote host")
                    break
            except socket.timeout:
                print(".", end="", flush=True)
                continue
                
        sock.close()
        
        if data_received:
            print("\n✅ Data reception test successful!")
            return True
        else:
            print(f"\n❌ No data received within {timeout} seconds")
            return False
            
    except ConnectionRefusedError:
        print(f"❌ Connection refused to {host}:{port}")
        return False
    except socket.timeout:
        print(f"❌ Connection timeout after {timeout} seconds")
        return False
    except Exception as e:
        print(f"❌ Data reception test failed: {e}")
        return False

def main():
    """Run connectivity tests."""
    print("🛠️  Simple WITS Port Connectivity Test")
    print("="*50)
    
    host = "localhost"
    port = 8686
    
    # Test 1: Basic port connectivity
    print("\n1️⃣  Basic Port Test:")
    port_open = test_port_connectivity(host, port)
    
    if not port_open:
        print("\n❌ Basic connectivity failed!")
        print("Please check:")
        print("• Is your WITS simulator running?")
        print("• Is it listening on localhost:8686?")
        print("• Are there any firewall issues?")
        sys.exit(1)
    
    # Test 2: Data reception
    print("\n2️⃣  Data Reception Test:")
    data_ok = test_data_reception(host, port)
    
    if not data_ok:
        print("\n❌ Data reception failed!")
        print("The port is open but no data is being sent.")
        print("Please check:")
        print("• Is your WITS simulator actually sending data?")
        print("• Is it sending WITS formatted data?")
        sys.exit(1)
    
    print("\n🎉 All tests passed!")
    print("Your WITS simulator appears to be working correctly.")
    print("You can now run the full streaming test.")

if __name__ == "__main__":
    main() 