"""
WITS data models and symbols for drilling data validation and processing.
"""

from .symbols import (
    WITSSymbol,
    WITS_SYMBOLS,
    WITSUnits,
    get_symbol_by_code,
    search_symbols,
    get_record_types,
    get_symbols_by_record_type,
    get_record_description,
)
from .wits_frame import WITSFrame, DecodedData, DecodedFrame
from .unit_converter import UnitConverter, ConversionError
from typing import List

# __all__: list[str] = [
__all__: List[str] = [
    # Symbols and related functions
    "WITSSymbol",
    "WITS_SYMBOLS",
    "WITSUnits",
    "get_symbol_by_code",
    "search_symbols",
    "get_record_types",
    "get_symbols_by_record_type",
    "get_record_description",
    # WITS frame and decoded data
    "WITSFrame",
    "DecodedData",
    "DecodedFrame",
    # Unit conversion
    "UnitConverter",
    "ConversionError",
]
