"""
WITS unit conversion utilities for drilling industry units.

This module provides conversion functions between metric and FPS units
specifically for drilling industry measurements like rate of penetration,
pressure, flow rates, and other drilling parameters.
"""

from typing import Dict, Optional, Union
from enum import Enum
from .symbols import WITSUnits


class ConversionError(Exception):
    """Raised when unit conversion fails or is not supported."""
    pass


class UnitConverter:
    """
    Handles conversion between metric and FPS units for drilling industry measurements.
    
    Supports all unit types used in WITS specification including:
    - Drilling rates (M/HR ↔ F/HR)
    - Pressures (KPA ↔ PSI)
    - Flow rates (LPM ↔ GPM, M3/M ↔ BPM)
    - Densities (KGM3 ↔ PPG)
    - Temperatures (DEGC ↔ DEGF)
    - Weights/Forces (KDN ↔ KLB)
    - Torques (KNM ↔ KFLB)
    - Volumes (M3 ↔ BBL)
    - And more...
    """
    
    # Conversion factors: metric_unit -> fps_unit multiplier
    CONVERSION_FACTORS: Dict[tuple[WITSUnits, WITSUnits], float] = {
        # Rate conversions (drilling speeds)
        (WITSUnits.MHR, WITSUnits.FHR): 3.28084,  # meters/hour to feet/hour
        
        # Pressure conversions
        (WITSUnits.KPA, WITSUnits.PSI): 0.145038,  # kilopascals to PSI
        (WITSUnits.BAR, WITSUnits.PSI): 14.5038,   # bar to PSI
        
        # Flow rate conversions
        (WITSUnits.LPM, WITSUnits.GPM): 0.264172,   # liters/min to gallons/min
        (WITSUnits.M3PM, WITSUnits.BPM): 6.28981,   # cubic meters/min to barrels/min
        
        # Length conversions
        (WITSUnits.METERS, WITSUnits.FEET): 3.28084,  # meters to feet
        (WITSUnits.MILLIMETERS, WITSUnits.INCHES): 0.0393701,  # mm to inches
        
        # Density conversions
        (WITSUnits.KGM3, WITSUnits.PPG): 0.00834541,  # kg/m³ to pounds/gallon
        
        # Temperature conversions (special case - not linear)
        # Handled separately in convert_temperature()
        
        # Weight/Force conversions
        (WITSUnits.KDN, WITSUnits.KLB): 0.224809,   # kilodecanewtons to kilopounds
        
        # Mass per length conversions
        (WITSUnits.KGM, WITSUnits.LBF): 0.671969,   # kg/meter to pounds/foot
        
        # Torque conversions
        (WITSUnits.KNM, WITSUnits.KFLB): 0.737562,  # kilonewton-meters to kilo foot-pounds
        
        # Volume conversions
        (WITSUnits.M3, WITSUnits.BBL): 6.28981,     # cubic meters to barrels
        
        # Speed conversions (for surface equipment)
        (WITSUnits.MS, WITSUnits.FPM): 196.85,      # meters/second to feet/minute
        (WITSUnits.KPH, WITSUnits.MPH): 0.621371,   # km/hour to miles/hour
        
        # Angular conversions
        (WITSUnits.DGHM, WITSUnits.DGHF): 0.328084,  # degrees/100m to degrees/100ft
        
        # Electrical conversions
        (WITSUnits.OHMM, WITSUnits.OHMM): 1.0,      # ohm-meters (same in both systems)
        (WITSUnits.MMHO, WITSUnits.MMHO): 1.0,      # millimhos (same in both systems)
    }
    
    @classmethod
    def convert_value(cls, value: float, from_unit: WITSUnits, to_unit: WITSUnits) -> float:
        """
        Convert a value from one unit to another.
        
        Args:
            value: The numeric value to convert
            from_unit: Source unit
            to_unit: Target unit
            
        Returns:
            Converted value
            
        Raises:
            ConversionError: If conversion is not supported or units are incompatible
        """
        if from_unit == to_unit:
            return value
            
        # Handle temperature conversions specially
        if from_unit == WITSUnits.DEGC and to_unit == WITSUnits.DEGF:
            return cls.celsius_to_fahrenheit(value)
        elif from_unit == WITSUnits.DEGF and to_unit == WITSUnits.DEGC:
            return cls.fahrenheit_to_celsius(value)
            
        # Handle direct conversions
        conversion_key: tuple[Literal[WITSUnits.METERS, WITSUnits.FEET, WITSUnits.MILLIMETERS, WITSUnits.INCHES, WITSUnits.KPA, WITSUnits.PSI, WITSUnits.BAR, WITSUnits.LPM, WITSUnits.GPM, WITSUnits.M3PM, WITSUnits.BPM, WITSUnits.KGM3, WITSUnits.PPG, WITSUnits.MHR, WITSUnits.FHR, WITSUnits.MS, WITSUnits.FPM, WITSUnits.KDN, WITSUnits.KLB, WITSUnits.KGM, WITSUnits.LBF, WITSUnits.KNM, WITSUnits.KFLB, WITSUnits.M3, WITSUnits.BBL, WITSUnits.DEG, WITSUnits.DGHM, WITSUnits.DGHF, WITSUnits.SEC, WITSUnits.MIN, WITSUnits.HR, WITSUnits.KPH, WITSUnits.MPH, WITSUnits.OHMM, WITSUnits.MMHO, WITSUnits.RPM, WITSUnits.SPM, WITSUnits.PERCENT, WITSUnits.API, WITSUnits.UNITLESS, WITSUnits.DEGC, WITSUnits.DEGF], WITSUnits] = (from_unit, to_unit)
        if conversion_key in cls.CONVERSION_FACTORS:
            return value * cls.CONVERSION_FACTORS[conversion_key]
            
        # Handle reverse conversions
        reverse_key: tuple[WITSUnits, Literal[WITSUnits.METERS, WITSUnits.FEET, WITSUnits.MILLIMETERS, WITSUnits.INCHES, WITSUnits.KPA, WITSUnits.PSI, WITSUnits.BAR, WITSUnits.LPM, WITSUnits.GPM, WITSUnits.M3PM, WITSUnits.BPM, WITSUnits.KGM3, WITSUnits.PPG, WITSUnits.MHR, WITSUnits.FHR, WITSUnits.MS, WITSUnits.FPM, WITSUnits.KDN, WITSUnits.KLB, WITSUnits.KGM, WITSUnits.LBF, WITSUnits.KNM, WITSUnits.KFLB, WITSUnits.M3, WITSUnits.BBL, WITSUnits.DEG, WITSUnits.DGHM, WITSUnits.DGHF, WITSUnits.SEC, WITSUnits.MIN, WITSUnits.HR, WITSUnits.KPH, WITSUnits.MPH, WITSUnits.OHMM, WITSUnits.MMHO, WITSUnits.RPM, WITSUnits.SPM, WITSUnits.PERCENT, WITSUnits.API, WITSUnits.UNITLESS, WITSUnits.DEGC, WITSUnits.DEGF]] = (to_unit, from_unit)
        if reverse_key in cls.CONVERSION_FACTORS:
            return value / cls.CONVERSION_FACTORS[reverse_key]
            
        # Handle unitless conversions
        if from_unit == WITSUnits.UNITLESS or to_unit == WITSUnits.UNITLESS:
            return value
            
        # Handle same units (RPM, SPM, etc.)
        if from_unit.value == to_unit.value:
            return value
            
        raise ConversionError(f"Conversion from {from_unit.value} to {to_unit.value} is not supported")
    
    @staticmethod
    def celsius_to_fahrenheit(celsius: float) -> float:
        """Convert Celsius to Fahrenheit."""
        return (celsius * 9/5) + 32
    
    @staticmethod
    def fahrenheit_to_celsius(fahrenheit: float) -> float:
        """Convert Fahrenheit to Celsius."""
        return (fahrenheit - 32) * 5/9
    
    @classmethod
    def get_conversion_factor(cls, from_unit: WITSUnits, to_unit: WITSUnits) -> Optional[float]:
        """
        Get the conversion factor between two units.
        
        Args:
            from_unit: Source unit
            to_unit: Target unit
            
        Returns:
            Conversion factor or None if not available
        """
        if from_unit == to_unit:
            return 1.0
            
        conversion_key: tuple[WITSUnits, WITSUnits] = (from_unit, to_unit)
        if conversion_key in cls.CONVERSION_FACTORS:
            return cls.CONVERSION_FACTORS[conversion_key]
            
        reverse_key: tuple[WITSUnits, WITSUnits] = (to_unit, from_unit)
        if reverse_key in cls.CONVERSION_FACTORS:
            return 1.0 / cls.CONVERSION_FACTORS[reverse_key]
            
        return None
    
    @classmethod
    def is_convertible(cls, from_unit: WITSUnits, to_unit: WITSUnits) -> bool:
        """
        Check if conversion between two units is supported.
        
        Args:
            from_unit: Source unit
            to_unit: Target unit
            
        Returns:
            True if conversion is supported
        """
        if from_unit == to_unit:
            return True
            
        # Check for temperature conversions
        if ((from_unit == WITSUnits.DEGC and to_unit == WITSUnits.DEGF) or
            (from_unit == WITSUnits.DEGF and to_unit == WITSUnits.DEGC)):
            return True
            
        # Check conversion factors
        return ((from_unit, to_unit) in cls.CONVERSION_FACTORS or
                (to_unit, from_unit) in cls.CONVERSION_FACTORS or
                from_unit == WITSUnits.UNITLESS or
                to_unit == WITSUnits.UNITLESS or
                from_unit.value == to_unit.value)
    
    @classmethod
    def get_unit_category(cls, unit: WITSUnits) -> str:
        """
        Get the category of a unit (pressure, flow, rate, etc.).
        
        Args:
            unit: The unit to categorize
            
        Returns:
            Unit category string
        """
        unit_categories: Dict[WITSUnits, str] = {
            # Pressure units
            WITSUnits.KPA: "pressure",
            WITSUnits.PSI: "pressure", 
            WITSUnits.BAR: "pressure",
            
            # Flow rate units
            WITSUnits.LPM: "flow_rate",
            WITSUnits.GPM: "flow_rate",
            WITSUnits.M3PM: "flow_rate",
            WITSUnits.BPM: "flow_rate",
            
            # Rate units (drilling speed)
            WITSUnits.MHR: "drilling_rate",
            WITSUnits.FHR: "drilling_rate",
            WITSUnits.MS: "speed",
            WITSUnits.FPM: "speed",
            
            # Length units
            WITSUnits.METERS: "length",
            WITSUnits.FEET: "length",
            WITSUnits.MILLIMETERS: "length",
            WITSUnits.INCHES: "length",
            
            # Density units
            WITSUnits.KGM3: "density",
            WITSUnits.PPG: "density",
            
            # Temperature units
            WITSUnits.DEGC: "temperature",
            WITSUnits.DEGF: "temperature",
            
            # Weight/Force units
            WITSUnits.KDN: "force",
            WITSUnits.KLB: "force",
            
            # Torque units
            WITSUnits.KNM: "torque",
            WITSUnits.KFLB: "torque",
            
            # Volume units
            WITSUnits.M3: "volume",
            WITSUnits.BBL: "volume",
            
            # Angular units
            WITSUnits.DEG: "angle",
            WITSUnits.DGHM: "angle_gradient",
            WITSUnits.DGHF: "angle_gradient",
            
            # Rotational units
            WITSUnits.RPM: "rotation",
            WITSUnits.SPM: "pumping",
            
            # Percentage
            WITSUnits.PERCENT: "percentage",
            
            # Time units
            WITSUnits.SEC: "time",
            WITSUnits.MIN: "time",
            WITSUnits.HR: "time",
            
            # Unitless
            WITSUnits.UNITLESS: "unitless",
        }
        
        return unit_categories.get(unit, "unknown")


# Convenience functions
def convert_drilling_rate(value: float, from_metric: bool = True) -> float:
    """
    Convert drilling rate between metric (M/HR) and FPS (F/HR).
    
    Args:
        value: Rate value to convert
        from_metric: If True, convert from M/HR to F/HR, otherwise F/HR to M/HR
        
    Returns:
        Converted rate value
    """
    if from_metric:
        return UnitConverter.convert_value(value, WITSUnits.MHR, WITSUnits.FHR)
    else:
        return UnitConverter.convert_value(value, WITSUnits.FHR, WITSUnits.MHR)


def convert_pressure(value: float, from_metric: bool = True) -> float:
    """
    Convert pressure between metric (KPA) and FPS (PSI).
    
    Args:
        value: Pressure value to convert
        from_metric: If True, convert from KPA to PSI, otherwise PSI to KPA
        
    Returns:
        Converted pressure value
    """
    if from_metric:
        return UnitConverter.convert_value(value, WITSUnits.KPA, WITSUnits.PSI)
    else:
        return UnitConverter.convert_value(value, WITSUnits.PSI, WITSUnits.KPA)


def convert_flow_rate(value: float, from_metric: bool = True) -> float:
    """
    Convert flow rate between metric (LPM) and FPS (GPM).
    
    Args:
        value: Flow rate value to convert  
        from_metric: If True, convert from LPM to GPM, otherwise GPM to LPM
        
    Returns:
        Converted flow rate value
    """
    if from_metric:
        return UnitConverter.convert_value(value, WITSUnits.LPM, WITSUnits.GPM)
    else:
        return UnitConverter.convert_value(value, WITSUnits.GPM, WITSUnits.LPM)


def convert_mud_density(value: float, from_metric: bool = True) -> float:
    """
    Convert mud density between metric (KGM3) and FPS (PPG).
    
    Args:
        value: Density value to convert
        from_metric: If True, convert from KGM3 to PPG, otherwise PPG to KGM3
        
    Returns:
        Converted density value
    """
    if from_metric:
        return UnitConverter.convert_value(value, WITSUnits.KGM3, WITSUnits.PPG)
    else:
        return UnitConverter.convert_value(value, WITSUnits.PPG, WITSUnits.KGM3)


def convert_temperature(value: float, from_celsius: bool = True) -> float:
    """
    Convert temperature between Celsius and Fahrenheit.
    
    Args:
        value: Temperature value to convert
        from_celsius: If True, convert from Celsius to Fahrenheit, otherwise reverse
        
    Returns:
        Converted temperature value
    """
    if from_celsius:
        return UnitConverter.celsius_to_fahrenheit(value)
    else:
        return UnitConverter.fahrenheit_to_celsius(value) 