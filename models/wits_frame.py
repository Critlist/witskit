"""
WITS frame and decoded data models.

This module defines the data structures for representing WITS frames
and decoded drilling data with full type safety and validation.
"""

from datetime import datetime
from typing import Any, Dict, List, Optional, Union
from pydantic import BaseModel, Field, field_validator

from .symbols import WITSSymbol


class WITSFrame(BaseModel):
    """
    Represents a raw WITS data frame.
    
    WITS Level 0 format uses ASCII with && start and !! end markers.
    Each data line contains a 4-digit symbol code followed by a value.
    """
    
    raw_data: str = Field(..., description="Raw WITS frame data")
    timestamp: datetime = Field(default_factory=datetime.now, description="Frame reception timestamp")
    source: Optional[str] = Field(None, description="Data source identifier")
    
    @field_validator('raw_data')
    @classmethod
    def validate_wits_format(cls, v):
        """Validate basic WITS frame format."""
        if not v.strip():
            raise ValueError("WITS frame cannot be empty")
            
        lines = v.strip().split('\n')
        if len(lines) < 3:  # Minimum: start, data, end
            raise ValueError("WITS frame must have at least start, data, and end lines")
            
        if not lines[0].strip().startswith('&&'):
            raise ValueError("WITS frame must start with &&")
            
        if not lines[-1].strip().startswith('!!'):
            raise ValueError("WITS frame must end with !!")
            
        return v
    
    @property
    def data_lines(self) -> List[str]:
        """Extract data lines (excluding start && and end !! markers)."""
        lines: List[str] = self.raw_data.strip().split('\n')
        return [line.strip() for line in lines[1:-1] if line.strip()]
    
    def parse_data_line(self, line: str) -> tuple[str, str]:
        """
        Parse a WITS data line into symbol code and value.
        
        Args:
            line: Data line in format "01083650.40"
            
        Returns:
            Tuple of (symbol_code, value_string)
            
        Raises:
            ValueError: If line format is invalid
        """
        if len(line) < 4:
            raise ValueError(f"Invalid WITS data line: {line}")
            
        symbol_code = line[:4]
        value_str = line[4:]
        
        if not symbol_code.isdigit():
            raise ValueError(f"Invalid symbol code in line: {line}")
            
        return symbol_code, value_str


class DecodedData(BaseModel):
    """
    Represents a decoded WITS data point with symbol metadata.
    """
    
    symbol: WITSSymbol = Field(..., description="WITS symbol definition")
    raw_value: str = Field(..., description="Raw value string from WITS frame")
    parsed_value: Union[str, int, float, None] = Field(None, description="Parsed and typed value")
    unit: str = Field(..., description="Unit of measurement (metric or FPS)")
    timestamp: datetime = Field(..., description="Data timestamp")
    source: Optional[str] = Field(None, description="Data source identifier")
    
    class Config:
        # Allow WITSSymbol model to be used as a field type
        arbitrary_types_allowed = True
    
    def __init__(self, **data):
        """Initialize and parse the value according to symbol data type."""
        super().__init__(**data)
        # Parse the value after initialization when all fields are available
        if self.raw_value and self.raw_value.strip():
            try:
                if self.symbol.data_type.value == 'A':  # ASCII
                    self.parsed_value = self.raw_value
                elif self.symbol.data_type.value == 'F':  # Float
                    self.parsed_value = float(self.raw_value)
                elif self.symbol.data_type.value in ['S', 'L']:  # Integer types
                    self.parsed_value = int(float(self.raw_value))  # Handle decimal integers
                else:
                    self.parsed_value = self.raw_value
            except (ValueError, TypeError):
                # If parsing fails, keep as string
                self.parsed_value = self.raw_value
        else:
            self.parsed_value = None
    
    @property
    def symbol_name(self) -> str:
        """Get the symbol's short name."""
        return self.symbol.name
    
    @property
    def symbol_description(self) -> str:
        """Get the symbol's description."""
        return self.symbol.description
    
    @property
    def symbol_code(self) -> str:
        """Get the symbol's code."""
        return self.symbol.code


class DecodedFrame(BaseModel):
    """
    Represents a fully decoded WITS frame with all data points.
    """
    
    frame: WITSFrame = Field(..., description="Original WITS frame")
    data_points: List[DecodedData] = Field(default_factory=list, description="Decoded data points")
    errors: List[str] = Field(default_factory=list, description="Parsing errors")
    
    class Config:
        arbitrary_types_allowed = True
    
    @property
    def timestamp(self) -> datetime:
        """Get the frame timestamp."""
        return self.frame.timestamp
    
    @property
    def source(self) -> Optional[str]:
        """Get the frame source."""
        return self.frame.source
    
    def get_value(self, symbol_code: str) -> Optional[DecodedData]:
        """Get a decoded data point by symbol code."""
        for data_point in self.data_points:
            if data_point.symbol_code == symbol_code:
                return data_point
        return None
    
    def get_values_by_name(self, symbol_name: str) -> List[DecodedData]:
        """Get all decoded data points matching a symbol name."""
        return [
            data_point for data_point in self.data_points
            if data_point.symbol_name == symbol_name
        ]
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert decoded frame to dictionary format."""
        return {
            'timestamp': self.timestamp.isoformat(),
            'source': self.source,
            'data': {
                dp.symbol_code: {
                    'name': dp.symbol_name,
                    'description': dp.symbol_description,
                    'value': dp.parsed_value,
                    'raw_value': dp.raw_value,
                    'unit': dp.unit
                }
                for dp in self.data_points
            },
            'errors': self.errors
        } 