"""
WitsKit - Complete WITS SDK

The most comprehensive Python SDK for processing WITS (Wellsite Information Transfer Standard)
data in the oil & gas drilling industry.

This package provides:
- 724 symbols across 20+ record types from the official WITS specification
- Type-safe Pydantic models with comprehensive validation
- Fast parsing with optimized regex patterns
- Flexible units supporting both FPS (default) and metric systems
- Rich CLI with interactive exploration tools
"""

__version__ = "0.1.0"
__author__ = "WitsKit Team"
__license__ = "MIT"

# Public API exports
from .decoder.wits_decoder import (
    WITSDecoder,
    decode_frame,
    validate_wits_frame,
    decode_file,
    split_multiple_frames,
)
from .models.symbols import (
    WITSSymbol,
    WITS_SYMBOLS,
    WITSUnits,
    get_symbol_by_code,
    search_symbols,
    get_record_types,
    get_symbols_by_record_type,
    get_record_description,
)
from .models.wits_frame import WITSFrame, DecodedData, DecodedFrame
from .models.unit_converter import UnitConverter, ConversionError
from . import transport

__all__: list[str] = [
    # Core decoder functionality
    "WITSDecoder",
    "decode_frame",
    "validate_wits_frame",
    "decode_file",
    "split_multiple_frames",
    # Symbol management
    "WITSSymbol",
    "WITS_SYMBOLS",
    "WITSUnits",
    "get_symbol_by_code",
    "search_symbols",
    "get_record_types",
    "get_symbols_by_record_type",
    "get_record_description",
    # Data models
    "WITSFrame",
    "DecodedData",
    "DecodedFrame",
    # Unit conversion
    "UnitConverter",
    "ConversionError",
    # Transport layer (available as witskit.transport.*)
    "transport",
    # Package metadata
    "__version__",
    "__author__",
    "__license__",
]
