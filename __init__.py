"""
WitsKit - Complete WITS SDK

The most comprehensive Python SDK for processing WITS (Wellsite Information Transfer Standard) 
data in the oil & gas drilling industry.

This package provides:
- 742+ symbols across 20+ record types from the official WITS specification
- Type-safe Pydantic models with comprehensive validation
- Fast parsing with optimized regex patterns
- Flexible units supporting both metric and FPS systems
- Rich CLI with interactive exploration tools
"""

__version__ = "0.1.0"
__author__ = "WitsKit Team"
__license__ = "MIT"

# Public API exports
from .decoder.wits_decoder import WITSDecoder, decode_frame, validate_wits_frame
from .models.symbols import WITSSymbol, WITS_SYMBOLS, get_symbol_by_code, search_symbols
from .models.wits_frame import WITSFrame, DecodedData, DecodedFrame

__all__: list[str] = [
    # Core decoder functionality
    "WITSDecoder",
    "decode_frame", 
    "validate_wits_frame",
    
    # Symbol management
    "WITSSymbol",
    "WITS_SYMBOLS",
    "get_symbol_by_code",
    "search_symbols",
    
    # Data models
    "WITSFrame",
    "DecodedData", 
    "DecodedFrame",
    
    # Package metadata
    "__version__",
    "__author__",
    "__license__",
]
