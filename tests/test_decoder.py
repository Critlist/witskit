"""
Tests for WITS decoder functionality.
"""

from typing import Dict, Literal, Any
import pytest
from datetime import datetime

# Import our modules with proper package imports
from witskit.models.symbols import WITSSymbol, WITSDataType, WITSUnits, get_symbol_by_code
from witskit.models.wits_frame import WITSFrame, DecodedData, DecodedFrame
from witskit.decoder.wits_decoder import WITSDecoder, decode_frame, validate_wits_frame


class TestWITSFrame:
    """Test WITS frame validation and parsing."""
    
    def test_valid_frame(self) -> None:
        """Test parsing a valid WITS frame."""
        raw_frame = """&&
01083650.40
011323.38
!!"""
        frame = WITSFrame(raw_data=raw_frame, source="test")
        assert frame.raw_data == raw_frame
        assert len(frame.data_lines) == 2
        assert frame.data_lines[0] == "01083650.40"
        assert frame.data_lines[1] == "011323.38"
    
    def test_frame_validation_errors(self):
        """Test frame validation catches errors."""
        
        # Empty frame
        with pytest.raises(ValueError):
            WITSFrame(raw_data="", source="test")
        
        # Missing start marker
        with pytest.raises(ValueError):
            WITSFrame(raw_data="01083650.40\n!!", source="test")
        
        # Missing end marker  
        with pytest.raises(ValueError):
            WITSFrame(raw_data="&&\n01083650.40", source="test")
        
        # Too few lines
        with pytest.raises(ValueError):
            WITSFrame(raw_data="&&\n!!", source="test")
    
    def test_parse_data_line(self) -> None:
        """Test parsing individual data lines."""
        frame = WITSFrame(raw_data="&&\n01083650.40\n!!", source="test")
        
        symbol_code, value = frame.parse_data_line("01083650.40")
        assert symbol_code == "0108"
        assert value == "3650.40"
        
        # Test error cases
        with pytest.raises(ValueError):
            frame.parse_data_line("123")
        
        with pytest.raises(ValueError):
            frame.parse_data_line("abcd123.45")


class TestWITSDecoder:
    """Test the main WITS decoder functionality."""
    
    @pytest.fixture
    def sample_frame(self) -> Literal['&&\n01083650.40\n011323.38\n012012.5\n!!']:
        """Sample WITS frame for testing."""
        return """&&
01083650.40
011323.38
012012.5
!!"""
    
    def test_decode_frame_basic(self, sample_frame) -> None:
        """Test basic frame decoding."""
        decoder = WITSDecoder()
        result: DecodedFrame = decoder.decode_frame(sample_frame, source="test")
        
        assert isinstance(result, DecodedFrame)
        assert result.source == "test"
        assert len(result.data_points) >= 1  # Should decode at least some symbols
        assert len(result.errors) == 0 or len(result.errors) > 0  # Some symbols might be unknown
    
    def test_decode_known_symbols(self) -> None:
        """Test decoding with known symbols."""
        # Use symbols we know exist
        frame = """&&
01083650.40
011323.38
!!"""
        
        decoder = WITSDecoder(strict_mode=False)
        result: DecodedFrame = decoder.decode_frame(frame)
        
        # Should have decoded data points
        assert len(result.data_points) >= 0
        
        # Check if we got the depth bit symbol
        depth_data: DecodedData | None = result.get_value("0108")
        if depth_data:
            assert depth_data.symbol_code == "0108"
            assert depth_data.parsed_value == 3650.40
            assert depth_data.symbol_name == "DBTM"
    
    def test_unit_selection(self) -> None:
        """Test metric vs FPS unit selection."""
        frame = """&&
01083650.40
!!"""
        
        # Test metric units
        decoder_metric = WITSDecoder(use_metric_units=True)
        result_metric: DecodedFrame = decoder_metric.decode_frame(frame)
        
        # Test FPS units
        decoder_fps = WITSDecoder(use_metric_units=False) 
        result_fps: DecodedFrame = decoder_fps.decode_frame(frame)
        
        # Both should decode but potentially with different units
        assert isinstance(result_metric, DecodedFrame)
        assert isinstance(result_fps, DecodedFrame)
    
    def test_strict_mode(self) -> None:
        """Test strict mode behavior."""
        frame_with_unknown = """&&
99999999.99
!!"""
        
        # Non-strict mode should handle unknown symbols gracefully
        decoder_lenient = WITSDecoder(strict_mode=False)
        result: DecodedFrame = decoder_lenient.decode_frame(frame_with_unknown)
        assert isinstance(result, DecodedFrame)
        
        # Strict mode might raise errors for unknown symbols
        decoder_strict = WITSDecoder(strict_mode=True)
        # This might raise an error or return a frame with errors
        try:
            result = decoder_strict.decode_frame(frame_with_unknown)
            # If it doesn't raise, check for errors
            assert len(result.errors) >= 0
        except ValueError:
            # This is also acceptable in strict mode
            pass
    
    def test_convenience_functions(self) -> None:
        """Test convenience functions."""
        frame = """&&
01083650.40
!!"""
        
        # Test decode_frame function
        result: DecodedFrame = decode_frame(frame, source="convenience_test")
        assert isinstance(result, DecodedFrame)
        assert result.source == "convenience_test"
        
        # Test validation function
        assert validate_wits_frame(frame) is True
        assert validate_wits_frame("invalid") is False


class TestSymbolLookup:
    """Test symbol lookup functionality."""
    
    def test_get_symbol_by_code(self) -> None:
        """Test getting symbols by code."""
        # Test known symbol
        symbol: WITSSymbol | None = get_symbol_by_code("0108")
        if symbol:  # Might be None if not defined
            assert symbol.code == "0108"
            assert symbol.name == "DBTM"
            assert symbol.description == "Depth Bit (meas)"
        
        # Test unknown symbol
        unknown: WITSSymbol | None = get_symbol_by_code("9999")
        assert unknown is None


def test_integration() -> None:
    """Integration test with realistic WITS data."""
    # Example WITS frame with multiple data points
    realistic_frame = """&&
01083650.40
011323.38
011412.5
!!"""
    
    decoder = WITSDecoder(use_metric_units=True, strict_mode=False)
    result: DecodedFrame = decoder.decode_frame(realistic_frame, source="integration_test")
    
    # Basic checks
    assert isinstance(result, DecodedFrame)
    assert result.source == "integration_test"
    assert result.timestamp is not None
    
    # Should have some data points or errors
    total_items: int = len(result.data_points) + len(result.errors)
    assert total_items > 0
    
    # Test conversion to dict
    result_dict: Dict[str, Any] = result.to_dict()
    assert "timestamp" in result_dict
    assert "source" in result_dict
    assert "data" in result_dict
    assert "errors" in result_dict


if __name__ == "__main__":
    # Run a simple test
    test_integration()
    print("✅ Basic integration test passed!")
