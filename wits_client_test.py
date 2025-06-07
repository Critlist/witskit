#!/usr/bin/env python3
"""
WITS client test - tries to request data from WITS simulator.
Some simulators wait for a request before sending data.
"""

import socket
import time
import threading

def send_wits_request(host="localhost", port=8686):
    """Send a WITS data request to the simulator."""
    print(f"📤 Sending WITS request to {host}:{port}...")
    
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(10)
        
        sock.connect((host, port))
        print("✅ Connected! Sending request...")
        
        # Try different WITS request formats
        requests = [
            b"&&\r\n",  # Simple start request
            b"&&\n",     # Unix style
            b"REQUEST\r\n",  # Generic request
            b"START\r\n",    # Start command
            b"\r\n",         # Empty line
        ]
        
        for i, req in enumerate(requests):
            print(f"📤 Sending request #{i+1}: {req}")
            sock.send(req)
            time.sleep(1)
        
        # Keep connection open and listen for response
        print("👂 Listening for response...")
        sock.settimeout(5)
        
        for _ in range(10):  # Try for 10 seconds
            try:
                data = sock.recv(1024)
                if data:
                    print(f"✅ Received response: {data[:100]}...")
                    return True
            except socket.timeout:
                print(".", end="", flush=True)
                time.sleep(1)
                continue
        
        sock.close()
        print("\n❌ No response received")
        return False
        
    except Exception as e:
        print(f"❌ Request failed: {e}")
        return False

def listen_continuously(host="localhost", port=8686, duration=30):
    """Listen continuously for any data from the simulator."""
    print(f"👂 Listening continuously to {host}:{port} for {duration} seconds...")
    
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((host, port))
        print("✅ Connected! Listening...")
        
        sock.settimeout(1)  # Short timeout for each recv
        start_time = time.time()
        data_count = 0
        
        while time.time() - start_time < duration:
            try:
                data = sock.recv(1024)
                if data:
                    data_count += 1
                    print(f"\n📦 Data #{data_count}: {data[:100]}...")
                else:
                    print("⚠️  Connection closed by remote host")
                    break
            except socket.timeout:
                print(".", end="", flush=True)
                continue
        
        sock.close()
        
        if data_count > 0:
            print(f"\n✅ Received {data_count} data packets!")
            return True
        else:
            print(f"\n❌ No data received in {duration} seconds")
            return False
            
    except Exception as e:
        print(f"❌ Listening failed: {e}")
        return False

def main():
    """Run WITS client tests."""
    print("🛠️  WITS Client Test Tool")
    print("="*50)
    
    host = "localhost"
    port = 8686
    
    print("This tool tries different approaches to get data from your WITS simulator.\n")
    
    # Test 1: Send requests and listen for response
    print("1️⃣  Request/Response Test:")
    if send_wits_request(host, port):
        print("✅ Simulator responds to requests!")
        return
    
    # Test 2: Just listen continuously
    print("\n2️⃣  Continuous Listening Test:")
    if listen_continuously(host, port, 15):
        print("✅ Simulator sends data continuously!")
        return
    
    print("\n❌ No data received from simulator.")
    print("\nTroubleshooting suggestions:")
    print("• Check if your WITS simulator has a 'Start' or 'Stream' button")
    print("• Look for simulator settings about data transmission mode")
    print("• Check if it needs to be in 'Server' mode vs 'Client' mode")
    print("• Verify it's configured to send WITS data (not just listen)")
    print("• Check the simulator's log/console for any error messages")

if __name__ == "__main__":
    main() 