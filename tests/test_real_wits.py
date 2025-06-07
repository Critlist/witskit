#!/usr/bin/env python3
"""
Test script to analyze real WITS communication data captured from:
- Polaris logging software (inbound)
- Erdos Miller Eclipse software (outbound)
"""

from witskit.decoder.wits_decoder import decode_file, split_multiple_frames
import json
from datetime import datetime

def analyze_wits_file(filename, source_name):
    """Analyze a WITS communication file and return statistics."""
    print(f"\n=== Analyzing {filename} ({source_name}) ===")
    
    try:
        with open(filename, 'r') as f:
            raw_data = f.read()
        
        print(f"File size: {len(raw_data)} characters")
        
        # Split into individual frames
        frames = split_multiple_frames(raw_data)
        print(f"Found {len(frames)} WITS frames")
        
        if not frames:
            print("No valid frames found!")
            return
        
        # Decode all frames
        decoded_frames = decode_file(raw_data, source=source_name)
        print(f"Successfully decoded {len(decoded_frames)} frames")
        
        # Analyze frame contents
        total_data_points = 0
        total_errors = 0
        symbol_counts = {}
        
        for frame in decoded_frames:
            total_data_points += len(frame.data_points)
            total_errors += len(frame.errors)
            
            # Count symbol usage
            for dp in frame.data_points:
                symbol_code = dp.symbol.code
                symbol_counts[symbol_code] = symbol_counts.get(symbol_code, 0) + 1
        
        print(f"Total data points: {total_data_points}")
        print(f"Total errors: {total_errors}")
        
        # Show most common symbols
        if symbol_counts:
            print("\nMost common WITS symbols:")
            sorted_symbols = sorted(symbol_counts.items(), key=lambda x: x[1], reverse=True)
            for symbol_code, count in sorted_symbols[:10]:
                print(f"  {symbol_code}: {count} occurrences")
        
        # Show sample frame
        if decoded_frames and decoded_frames[0].data_points:
            print(f"\nSample decoded data from first frame:")
            for dp in decoded_frames[0].data_points[:5]:
                print(f"  - {dp.symbol.name} ({dp.symbol.code}): {dp.parsed_value} {dp.unit}")
        
        # Show errors if any
        if total_errors > 0:
            print(f"\nSample errors:")
            error_count = 0
            for frame in decoded_frames:
                for error in frame.errors:
                    print(f"  - {error}")
                    error_count += 1
                    if error_count >= 3:
                        break
                if error_count >= 3:
                    break
        
        return {
            'filename': filename,
            'source': source_name,
            'frame_count': len(frames),
            'decoded_count': len(decoded_frames),
            'data_points': total_data_points,
            'errors': total_errors,
            'symbols': symbol_counts
        }
        
    except Exception as e:
        print(f"Error analyzing {filename}: {str(e)}")
        return None

def main():
    """Main analysis function."""
    print("WITS Communication Analysis")
    print("===========================")
    
    results = []
    
    # Analyze Polaris inbound data
    polaris_result = analyze_wits_file('inboundPolarisWITS.txt', 'Polaris_Inbound')
    if polaris_result:
        results.append(polaris_result)
    
    # Analyze Erdos Miller outbound data
    em_result = analyze_wits_file('outboundEMwits.txt', 'ErdosMiller_Eclipse_Outbound')
    if em_result:
        results.append(em_result)
    
    # Summary comparison
    if len(results) >= 2:
        print(f"\n=== Summary Comparison ===")
        for result in results:
            print(f"{result['source']}:")
            print(f"  Frames: {result['frame_count']}")
            print(f"  Data points: {result['data_points']}")
            print(f"  Unique symbols: {len(result['symbols'])}")
            print(f"  Errors: {result['errors']}")
    
    # Save detailed results
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = f"real_wits_analysis_{timestamp}.json"
    
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2, default=str)
    
    print(f"\nDetailed analysis saved to: {output_file}")

if __name__ == "__main__":
    main() 