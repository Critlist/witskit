"""
WITS symbol definitions and data types.

This file contains the complete WITS specification with all symbols
from all 25 record types, automatically generated from WITSRecords.htm.

Based on the WITS (Wellsite Information Transfer Standard) specification.
"""

from enum import Enum
from typing import Dict, Optional, Union, List
from pydantic import BaseModel


class WITSDataType(str, Enum):
    """WITS data types as defined in the specification."""
    ASCII = "A"      # ASCII string
    FLOAT = "F"      # Floating point
    INTEGER = "S"    # Short integer (2 bytes)
    LONG = "L"       # Long integer (4 bytes)


class WITSUnits(str, Enum):
    """All units used in WITS data across all record types."""
    # Length units
    METERS = "M"
    FEET = "F"
    MILLIMETERS = "MM"  # Millimeters
    INCHES = "IN"       # Inches
    
    # Pressure units
    KPA = "KPA"      # Kilopascals
    PSI = "PSI"      # Pounds per square inch
    BAR = "BAR"      # Bar
    
    # Flow rate units
    LPM = "L/M"      # Liters per minute
    GPM = "GPM"      # Gallons per minute
    M3PM = "M3/M"    # Cubic meters per minute
    BPM = "BPM"      # Barrels per minute
    
    # Density units
    KGM3 = "KGM3"    # Kg per cubic meter
    PPG = "PPG"      # Pounds per gallon
    
    # Temperature units
    DEGC = "DEGC"    # Degrees Celsius
    DEGF = "DEGF"    # Degrees Fahrenheit
    
    # Rate units
    MHR = "M/HR"     # Meters per hour
    FHR = "F/HR"     # Feet per hour
    MS = "M/S"       # Meters per second
    FPM = "FPM"      # Feet per minute
    
    # Weight/Force units
    KDN = "KDN"      # Kilodecanewtons
    KLB = "KLB"      # Kilopounds
    
    # Mass per length units
    KGM = "KG/M"     # Kilograms per meter
    LBF = "LB/F"     # Pounds per foot
    
    # Torque units
    KNM = "KNM"      # Kilonewton-meters
    KFLB = "KFLB"    # Kilo foot-pounds
    
    # Volume units
    M3 = "M3"        # Cubic meters
    BBL = "BBL"      # Barrels
    
    # Angular units
    DEG = "DEG"      # Degrees
    DGHM = "DGHM"    # Degrees per hundred meters
    DGHF = "DGHF"    # Degrees per hundred feet
    
    # Time units
    SEC = "SEC"      # Seconds
    MIN = "MIN"      # Minutes
    HR = "HR"        # Hours
    
    # Speed units
    KPH = "KPH"      # Kilometers per hour
    MPH = "MPH"      # Miles per hour
    
    # Electrical units
    OHMM = "OHMM"    # Ohm-meters
    MMHO = "MMHO"    # Millimhos
    
    # Other units
    RPM = "RPM"      # Revolutions per minute
    SPM = "SPM"      # Strokes per minute
    PERCENT = "%"    # Percentage
    API = "API"      # API units (gamma ray)
    
    # Unitless
    UNITLESS = "----"


class WITSSymbol(BaseModel):
    """
    Represents a WITS symbol definition.
    
    Each symbol corresponds to a specific drilling parameter with
    metadata about its data type, units, and description.
    """
    
    code: str
    name: str
    description: str
    data_type: WITSDataType
    length: int
    metric_units: WITSUnits
    fps_units: WITSUnits
    record_type: int
    item_number: int
    
    class Config:
        frozen = True  # Make immutable


# Record type descriptions
RECORD_DESCRIPTIONS: Dict[int, str] = {
    1: "General Time-Based",
    2: "Drilling - Depth Based",
    3: "Drilling - Connections",
    4: "Hydraulics",
    6: "Trip - Connections",
    7: "Survey/Directional",
    8: "MWD Formation Evaluation",
    9: "MWD Mechanical",
    10: "Pressure Evaluation",
    11: "Mud Tank Volumes",
    12: "Chromatograph Cycle-Based",
    13: "Chromatograph Depth-Based",
    14: "Lagged Mud Properties",
    15: "Cuttings / Lithology",
    16: "Hydrocarbon Show",
    17: "Cementing",
    18: "Drill Stem Testing",
    19: "Configuration",
    20: "Mud Report",
    21: "Bit Report",
}

# WITS Record 1 symbols - General Time-Based
WITS_RECORD_1_SYMBOLS: Dict[str, WITSSymbol] = {
    "0101": WITSSymbol(
        code="0101",
        name="WID",
        description="Well Identifier",
        data_type=WITSDataType.ASCII,
        length=16,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=1,
        item_number=1
    ),
    "0102": WITSSymbol(
        code="0102",
        name="SKNO",
        description="Sidetrack/Hole Sect No.",
        data_type=WITSDataType.INTEGER,
        length=2,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=1,
        item_number=2
    ),
    "0103": WITSSymbol(
        code="0103",
        name="RID",
        description="Record Identifier",
        data_type=WITSDataType.INTEGER,
        length=2,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=1,
        item_number=3
    ),
    "0104": WITSSymbol(
        code="0104",
        name="SQID",
        description="Sequence Identifier",
        data_type=WITSDataType.LONG,
        length=4,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=1,
        item_number=4
    ),
    "0105": WITSSymbol(
        code="0105",
        name="DATE",
        description="Date",
        data_type=WITSDataType.LONG,
        length=4,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=1,
        item_number=5
    ),
    "0106": WITSSymbol(
        code="0106",
        name="TIME",
        description="Time",
        data_type=WITSDataType.LONG,
        length=4,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=1,
        item_number=6
    ),
    "0107": WITSSymbol(
        code="0107",
        name="ACTC",
        description="Activity Code",
        data_type=WITSDataType.INTEGER,
        length=2,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=1,
        item_number=7
    ),
    "0108": WITSSymbol(
        code="0108",
        name="DBTM",
        description="Depth Bit (meas)",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.METERS,
        fps_units=WITSUnits.FEET,
        record_type=1,
        item_number=8
    ),
    "0109": WITSSymbol(
        code="0109",
        name="DBTV",
        description="Depth Bit (vert)",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.METERS,
        fps_units=WITSUnits.FEET,
        record_type=1,
        item_number=9
    ),
    "0110": WITSSymbol(
        code="0110",
        name="DMEA",
        description="Depth Hole (meas)",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.METERS,
        fps_units=WITSUnits.FEET,
        record_type=1,
        item_number=10
    ),
    "0111": WITSSymbol(
        code="0111",
        name="DVER",
        description="Depth Hole (vert)",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.METERS,
        fps_units=WITSUnits.FEET,
        record_type=1,
        item_number=11
    ),
    "0112": WITSSymbol(
        code="0112",
        name="BPOS",
        description="Block Position",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.METERS,
        fps_units=WITSUnits.FEET,
        record_type=1,
        item_number=12
    ),
    "0113": WITSSymbol(
        code="0113",
        name="ROPA",
        description="Rate of Penetration (avg)",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.MHR,
        fps_units=WITSUnits.FHR,
        record_type=1,
        item_number=13
    ),
    "0114": WITSSymbol(
        code="0114",
        name="HKLA",
        description="Hookload (avg)",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.KDN,
        fps_units=WITSUnits.KLB,
        record_type=1,
        item_number=14
    ),
    "0115": WITSSymbol(
        code="0115",
        name="HKLX",
        description="Hookload (max)",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.KDN,
        fps_units=WITSUnits.KLB,
        record_type=1,
        item_number=15
    ),
    "0116": WITSSymbol(
        code="0116",
        name="WOBA",
        description="Weight-on-Bit (surf,avg)",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.KDN,
        fps_units=WITSUnits.KLB,
        record_type=1,
        item_number=16
    ),
    "0117": WITSSymbol(
        code="0117",
        name="WOBX",
        description="Weight-on-Bit (surf,max)",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.KDN,
        fps_units=WITSUnits.KLB,
        record_type=1,
        item_number=17
    ),
    "0118": WITSSymbol(
        code="0118",
        name="TQA",
        description="Rotary Torque (surf,avg)",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.KNM,
        fps_units=WITSUnits.KFLB,
        record_type=1,
        item_number=18
    ),
    "0119": WITSSymbol(
        code="0119",
        name="TQX",
        description="Rotary Torque (surf,max)",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.KNM,
        fps_units=WITSUnits.KFLB,
        record_type=1,
        item_number=19
    ),
    "0120": WITSSymbol(
        code="0120",
        name="RPMA",
        description="Rotary Speed (surf,avg)",
        data_type=WITSDataType.INTEGER,
        length=2,
        metric_units=WITSUnits.RPM,
        fps_units=WITSUnits.RPM,
        record_type=1,
        item_number=20
    ),
    "0121": WITSSymbol(
        code="0121",
        name="SPPA",
        description="Standpipe Pressure (avg)",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.KPA,
        fps_units=WITSUnits.PSI,
        record_type=1,
        item_number=21
    ),
    "0122": WITSSymbol(
        code="0122",
        name="CHKP",
        description="Casing (Choke) Pressure",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.KPA,
        fps_units=WITSUnits.PSI,
        record_type=1,
        item_number=22
    ),
    "0123": WITSSymbol(
        code="0123",
        name="SPM1",
        description="Pump Stroke Rate #1",
        data_type=WITSDataType.INTEGER,
        length=2,
        metric_units=WITSUnits.SPM,
        fps_units=WITSUnits.SPM,
        record_type=1,
        item_number=23
    ),
    "0124": WITSSymbol(
        code="0124",
        name="SPM2",
        description="Pump Stroke Rate #2",
        data_type=WITSDataType.INTEGER,
        length=2,
        metric_units=WITSUnits.SPM,
        fps_units=WITSUnits.SPM,
        record_type=1,
        item_number=24
    ),
    "0125": WITSSymbol(
        code="0125",
        name="SPM3",
        description="Pump Stroke Rate #3",
        data_type=WITSDataType.INTEGER,
        length=2,
        metric_units=WITSUnits.SPM,
        fps_units=WITSUnits.SPM,
        record_type=1,
        item_number=25
    ),
    "0126": WITSSymbol(
        code="0126",
        name="TVA",
        description="Tank Volume (active)",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.M3,
        fps_units=WITSUnits.BBL,
        record_type=1,
        item_number=26
    ),
    "0127": WITSSymbol(
        code="0127",
        name="TVCA",
        description="Tank Volume Change (act)",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.M3,
        fps_units=WITSUnits.BBL,
        record_type=1,
        item_number=27
    ),
    "0128": WITSSymbol(
        code="0128",
        name="MFOP",
        description="Mud Flow Out %",
        data_type=WITSDataType.INTEGER,
        length=2,
        metric_units=WITSUnits.PERCENT,
        fps_units=WITSUnits.PERCENT,
        record_type=1,
        item_number=28
    ),
    "0129": WITSSymbol(
        code="0129",
        name="MFOA",
        description="Mud Flow Out (avg)",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.LPM,
        fps_units=WITSUnits.GPM,
        record_type=1,
        item_number=29
    ),
    "0130": WITSSymbol(
        code="0130",
        name="MFIA",
        description="Mud Flow In (avg)",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.LPM,
        fps_units=WITSUnits.GPM,
        record_type=1,
        item_number=30
    ),
    "0131": WITSSymbol(
        code="0131",
        name="MDOA",
        description="Mud Density Out (avg)",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.KGM3,
        fps_units=WITSUnits.PPG,
        record_type=1,
        item_number=31
    ),
    "0132": WITSSymbol(
        code="0132",
        name="MDIA",
        description="Mud Density In (avg)",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.KGM3,
        fps_units=WITSUnits.PPG,
        record_type=1,
        item_number=32
    ),
    "0133": WITSSymbol(
        code="0133",
        name="MTOA",
        description="Mud Temperature Out (avg)",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.DEGC,
        fps_units=WITSUnits.DEGF,
        record_type=1,
        item_number=33
    ),
    "0134": WITSSymbol(
        code="0134",
        name="MTIA",
        description="Mud Temperature In (avg)",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.DEGC,
        fps_units=WITSUnits.DEGF,
        record_type=1,
        item_number=34
    ),
    "0135": WITSSymbol(
        code="0135",
        name="MCOA",
        description="Mud Conductivity Out (avg)",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.MMHO,
        fps_units=WITSUnits.MMHO,
        record_type=1,
        item_number=35
    ),
    "0136": WITSSymbol(
        code="0136",
        name="MCIA",
        description="Mud Conductivity In (avg)",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.MMHO,
        fps_units=WITSUnits.MMHO,
        record_type=1,
        item_number=36
    ),
    "0137": WITSSymbol(
        code="0137",
        name="STKC",
        description="Pump Stroke Count (cum)",
        data_type=WITSDataType.LONG,
        length=4,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=1,
        item_number=37
    ),
    "0138": WITSSymbol(
        code="0138",
        name="LSTK",
        description="Lag Strokes",
        data_type=WITSDataType.INTEGER,
        length=2,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=1,
        item_number=38
    ),
    "0139": WITSSymbol(
        code="0139",
        name="DRTM",
        description="Depth Returns (meas)",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.METERS,
        fps_units=WITSUnits.FEET,
        record_type=1,
        item_number=39
    ),
    "0140": WITSSymbol(
        code="0140",
        name="GASA",
        description="Gas (avg)",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.PERCENT,
        fps_units=WITSUnits.PERCENT,
        record_type=1,
        item_number=40
    ),
}

# WITS Record 2 symbols - Drilling - Depth Based
WITS_RECORD_2_SYMBOLS = {
    "0201": WITSSymbol(
        code="0201",
        name="WID",
        description="Well Identifier",
        data_type=WITSDataType.ASCII,
        length=16,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=2,
        item_number=1
    ),
    "0202": WITSSymbol(
        code="0202",
        name="SKNO",
        description="Sidetrack/Hole Sect No.",
        data_type=WITSDataType.INTEGER,
        length=2,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=2,
        item_number=2
    ),
    "0203": WITSSymbol(
        code="0203",
        name="RID",
        description="Record Identifier",
        data_type=WITSDataType.INTEGER,
        length=2,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=2,
        item_number=3
    ),
    "0204": WITSSymbol(
        code="0204",
        name="SQID",
        description="Sequence Identifier",
        data_type=WITSDataType.LONG,
        length=4,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=2,
        item_number=4
    ),
    "0205": WITSSymbol(
        code="0205",
        name="DATE",
        description="Date",
        data_type=WITSDataType.LONG,
        length=4,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=2,
        item_number=5
    ),
    "0206": WITSSymbol(
        code="0206",
        name="TIME",
        description="Time",
        data_type=WITSDataType.LONG,
        length=4,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=2,
        item_number=6
    ),
    "0207": WITSSymbol(
        code="0207",
        name="ACTC",
        description="Activity Code",
        data_type=WITSDataType.INTEGER,
        length=2,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=2,
        item_number=7
    ),
    "0208": WITSSymbol(
        code="0208",
        name="DMEA",
        description="Depth Hole (meas)",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.METERS,
        fps_units=WITSUnits.FEET,
        record_type=2,
        item_number=8
    ),
    "0209": WITSSymbol(
        code="0209",
        name="DVER",
        description="Depth Hole (vert)",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.METERS,
        fps_units=WITSUnits.FEET,
        record_type=2,
        item_number=9
    ),
    "0210": WITSSymbol(
        code="0210",
        name="ROPA",
        description="Rate of Penetration (avg)",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.MHR,
        fps_units=WITSUnits.FHR,
        record_type=2,
        item_number=10
    ),
    "0211": WITSSymbol(
        code="0211",
        name="WOBA",
        description="Weight-on-Bit (surf,avg)",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.KDN,
        fps_units=WITSUnits.KLB,
        record_type=2,
        item_number=11
    ),
    "0212": WITSSymbol(
        code="0212",
        name="HKLA",
        description="Hookload (avg)",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.KDN,
        fps_units=WITSUnits.KLB,
        record_type=2,
        item_number=12
    ),
    "0213": WITSSymbol(
        code="0213",
        name="SPPA",
        description="Standpipe Pressure (avg)",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.KPA,
        fps_units=WITSUnits.PSI,
        record_type=2,
        item_number=13
    ),
    "0214": WITSSymbol(
        code="0214",
        name="TQA",
        description="Rotary Torque (surf,avg)",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.KNM,
        fps_units=WITSUnits.KFLB,
        record_type=2,
        item_number=14
    ),
    "0215": WITSSymbol(
        code="0215",
        name="RPMA",
        description="Rotary Speed (surf,avg)",
        data_type=WITSDataType.INTEGER,
        length=2,
        metric_units=WITSUnits.RPM,
        fps_units=WITSUnits.RPM,
        record_type=2,
        item_number=15
    ),
    "0216": WITSSymbol(
        code="0216",
        name="BRVC",
        description="Bit Revolutions (cum)",
        data_type=WITSDataType.LONG,
        length=4,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=2,
        item_number=16
    ),
    "0217": WITSSymbol(
        code="0217",
        name="MDIA",
        description="Mud Density In (avg)",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.KGM3,
        fps_units=WITSUnits.PPG,
        record_type=2,
        item_number=17
    ),
    "0218": WITSSymbol(
        code="0218",
        name="ECDT",
        description="ECD at Total Depth",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.KGM3,
        fps_units=WITSUnits.PPG,
        record_type=2,
        item_number=18
    ),
    "0219": WITSSymbol(
        code="0219",
        name="MFIA",
        description="Mud Flow In (avg)",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.LPM,
        fps_units=WITSUnits.GPM,
        record_type=2,
        item_number=19
    ),
    "0220": WITSSymbol(
        code="0220",
        name="MFOA",
        description="Mud Flow Out (avg)",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.LPM,
        fps_units=WITSUnits.GPM,
        record_type=2,
        item_number=20
    ),
    "0221": WITSSymbol(
        code="0221",
        name="MFOP",
        description="Mud Flow Out %",
        data_type=WITSDataType.INTEGER,
        length=2,
        metric_units=WITSUnits.PERCENT,
        fps_units=WITSUnits.PERCENT,
        record_type=2,
        item_number=21
    ),
    "0222": WITSSymbol(
        code="0222",
        name="TVA",
        description="Tank Volume (active)",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.M3,
        fps_units=WITSUnits.BBL,
        record_type=2,
        item_number=22
    ),
    "0223": WITSSymbol(
        code="0223",
        name="CPDC",
        description="Cost/Distance (inst) CPDI CPDI F &nbsp; $/M $/F 24 Cost/Distance (cum)",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=2,
        item_number=23
    ),
    "0225": WITSSymbol(
        code="0225",
        name="BDTI",
        description="Bit Drilled Time",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=2,
        item_number=25
    ),
    "0226": WITSSymbol(
        code="0226",
        name="BDDI",
        description="Bit Drilled Distance",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.METERS,
        fps_units=WITSUnits.FEET,
        record_type=2,
        item_number=26
    ),
    "0227": WITSSymbol(
        code="0227",
        name="DXC",
        description="Corr. Drilling Exponent",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=2,
        item_number=27
    ),
}

# WITS Record 3 symbols - Drilling - Connections
WITS_RECORD_3_SYMBOLS = {
    "0301": WITSSymbol(
        code="0301",
        name="WID",
        description="Well Identifier",
        data_type=WITSDataType.ASCII,
        length=16,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=3,
        item_number=1
    ),
    "0302": WITSSymbol(
        code="0302",
        name="SKNO",
        description="Sidetrack/Hole Sect No.",
        data_type=WITSDataType.INTEGER,
        length=2,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=3,
        item_number=2
    ),
    "0303": WITSSymbol(
        code="0303",
        name="RID",
        description="Record Identifier",
        data_type=WITSDataType.INTEGER,
        length=2,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=3,
        item_number=3
    ),
    "0304": WITSSymbol(
        code="0304",
        name="SQID",
        description="Sequence Identifier",
        data_type=WITSDataType.LONG,
        length=4,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=3,
        item_number=4
    ),
    "0305": WITSSymbol(
        code="0305",
        name="DATE",
        description="Date",
        data_type=WITSDataType.LONG,
        length=4,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=3,
        item_number=5
    ),
    "0306": WITSSymbol(
        code="0306",
        name="TIME",
        description="Time",
        data_type=WITSDataType.LONG,
        length=4,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=3,
        item_number=6
    ),
    "0307": WITSSymbol(
        code="0307",
        name="ACTC",
        description="Activity Code",
        data_type=WITSDataType.INTEGER,
        length=2,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=3,
        item_number=7
    ),
    "0308": WITSSymbol(
        code="0308",
        name="DCNM",
        description="Depth Connection (meas)",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.METERS,
        fps_units=WITSUnits.FEET,
        record_type=3,
        item_number=8
    ),
    "0309": WITSSymbol(
        code="0309",
        name="DCNV",
        description="Depth Connection (vert)",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.METERS,
        fps_units=WITSUnits.FEET,
        record_type=3,
        item_number=9
    ),
    "0310": WITSSymbol(
        code="0310",
        name="DMEA",
        description="Depth Hole (meas)",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.METERS,
        fps_units=WITSUnits.FEET,
        record_type=3,
        item_number=10
    ),
    "0311": WITSSymbol(
        code="0311",
        name="DVER",
        description="Depth Hole (vert)",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.METERS,
        fps_units=WITSUnits.FEET,
        record_type=3,
        item_number=11
    ),
    "0312": WITSSymbol(
        code="0312",
        name="ETBS",
        description="Elapsed Time Bottom-Slips",
        data_type=WITSDataType.INTEGER,
        length=2,
        metric_units=WITSUnits.SEC,
        fps_units=WITSUnits.SEC,
        record_type=3,
        item_number=12
    ),
    "0313": WITSSymbol(
        code="0313",
        name="ETSL",
        description="Elapsed Time In-Slips",
        data_type=WITSDataType.INTEGER,
        length=2,
        metric_units=WITSUnits.SEC,
        fps_units=WITSUnits.SEC,
        record_type=3,
        item_number=13
    ),
    "0314": WITSSymbol(
        code="0314",
        name="ETSB",
        description="Elapsed Time Slips-Bottom",
        data_type=WITSDataType.INTEGER,
        length=2,
        metric_units=WITSUnits.SEC,
        fps_units=WITSUnits.SEC,
        record_type=3,
        item_number=14
    ),
    "0315": WITSSymbol(
        code="0315",
        name="ETPO",
        description="Elapsed Time Pumps-Off",
        data_type=WITSDataType.INTEGER,
        length=2,
        metric_units=WITSUnits.SEC,
        fps_units=WITSUnits.SEC,
        record_type=3,
        item_number=15
    ),
    "0316": WITSSymbol(
        code="0316",
        name="RSUX",
        description="Running Speed - up (max)",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.MS,
        fps_units=WITSUnits.FPM,
        record_type=3,
        item_number=16
    ),
    "0317": WITSSymbol(
        code="0317",
        name="RSDX",
        description="Running Speed - down (max)",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.MS,
        fps_units=WITSUnits.FPM,
        record_type=3,
        item_number=17
    ),
    "0318": WITSSymbol(
        code="0318",
        name="HKLX",
        description="Hookload (max)",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.KDN,
        fps_units=WITSUnits.KLB,
        record_type=3,
        item_number=18
    ),
    "0319": WITSSymbol(
        code="0319",
        name="STWT",
        description="String Weight (rot,avg)",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.KDN,
        fps_units=WITSUnits.KLB,
        record_type=3,
        item_number=19
    ),
    "0320": WITSSymbol(
        code="0320",
        name="TQMX",
        description="Torque - Make Up (max)",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.KNM,
        fps_units=WITSUnits.KFLB,
        record_type=3,
        item_number=20
    ),
    "0321": WITSSymbol(
        code="0321",
        name="TQBX",
        description="Torque - Breakout (max)",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.KNM,
        fps_units=WITSUnits.KFLB,
        record_type=3,
        item_number=21
    ),
}

# WITS Record 4 symbols - Hydraulics
WITS_RECORD_4_SYMBOLS = {
    "0401": WITSSymbol(
        code="0401",
        name="WID",
        description="Well Identifier",
        data_type=WITSDataType.ASCII,
        length=16,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=4,
        item_number=1
    ),
    "0401": WITSSymbol(
        code="0401",
        name="WID",
        description="Well Identifier",
        data_type=WITSDataType.ASCII,
        length=16,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=4,
        item_number=1
    ),
    "0402": WITSSymbol(
        code="0402",
        name="SKNO",
        description="Sidetrack/Hole Sect No.",
        data_type=WITSDataType.INTEGER,
        length=2,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=4,
        item_number=2
    ),
    "0402": WITSSymbol(
        code="0402",
        name="SKNO",
        description="Sidetrack/Hole Sect No.",
        data_type=WITSDataType.INTEGER,
        length=2,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=4,
        item_number=2
    ),
    "0403": WITSSymbol(
        code="0403",
        name="RID",
        description="Record Identifier",
        data_type=WITSDataType.INTEGER,
        length=2,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=4,
        item_number=3
    ),
    "0403": WITSSymbol(
        code="0403",
        name="RID",
        description="Record Identifier",
        data_type=WITSDataType.INTEGER,
        length=2,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=4,
        item_number=3
    ),
    "0404": WITSSymbol(
        code="0404",
        name="SQID",
        description="Sequence Identifier",
        data_type=WITSDataType.LONG,
        length=4,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=4,
        item_number=4
    ),
    "0404": WITSSymbol(
        code="0404",
        name="SQID",
        description="Sequence Identifier",
        data_type=WITSDataType.LONG,
        length=4,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=4,
        item_number=4
    ),
    "0405": WITSSymbol(
        code="0405",
        name="DATE",
        description="Date",
        data_type=WITSDataType.LONG,
        length=4,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=4,
        item_number=5
    ),
    "0405": WITSSymbol(
        code="0405",
        name="DATE",
        description="Date",
        data_type=WITSDataType.LONG,
        length=4,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=4,
        item_number=5
    ),
    "0406": WITSSymbol(
        code="0406",
        name="TIME",
        description="Time",
        data_type=WITSDataType.LONG,
        length=4,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=4,
        item_number=6
    ),
    "0406": WITSSymbol(
        code="0406",
        name="TIME",
        description="Time",
        data_type=WITSDataType.LONG,
        length=4,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=4,
        item_number=6
    ),
    "0407": WITSSymbol(
        code="0407",
        name="ACTC",
        description="Activity Code",
        data_type=WITSDataType.INTEGER,
        length=2,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=4,
        item_number=7
    ),
    "0407": WITSSymbol(
        code="0407",
        name="ACTC",
        description="Activity Code",
        data_type=WITSDataType.INTEGER,
        length=2,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=4,
        item_number=7
    ),
    "0408": WITSSymbol(
        code="0408",
        name="DMEA",
        description="Depth Hole (meas)",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.METERS,
        fps_units=WITSUnits.FEET,
        record_type=4,
        item_number=8
    ),
    "0408": WITSSymbol(
        code="0408",
        name="DBTM",
        description="Depth Bit (meas)",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.METERS,
        fps_units=WITSUnits.FEET,
        record_type=4,
        item_number=8
    ),
    "0409": WITSSymbol(
        code="0409",
        name="DVER",
        description="Depth Hole (vert)",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.METERS,
        fps_units=WITSUnits.FEET,
        record_type=4,
        item_number=9
    ),
    "0409": WITSSymbol(
        code="0409",
        name="DBTV",
        description="Depth Bit (vert)",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.METERS,
        fps_units=WITSUnits.FEET,
        record_type=4,
        item_number=9
    ),
    "0410": WITSSymbol(
        code="0410",
        name="DBTM",
        description="Depth Bit (meas)",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.METERS,
        fps_units=WITSUnits.FEET,
        record_type=4,
        item_number=10
    ),
    "0410": WITSSymbol(
        code="0410",
        name="DMEA",
        description="Depth Hole (meas)",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.METERS,
        fps_units=WITSUnits.FEET,
        record_type=4,
        item_number=10
    ),
    "0411": WITSSymbol(
        code="0411",
        name="DBTV",
        description="Depth Bit (vert)",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.METERS,
        fps_units=WITSUnits.FEET,
        record_type=4,
        item_number=11
    ),
    "0411": WITSSymbol(
        code="0411",
        name="DVER",
        description="Depth Hole (vert)",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.METERS,
        fps_units=WITSUnits.FEET,
        record_type=4,
        item_number=11
    ),
    "0412": WITSSymbol(
        code="0412",
        name="MDIA",
        description="Mud Density In (avg)",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.KGM3,
        fps_units=WITSUnits.PPG,
        record_type=4,
        item_number=12
    ),
    "0412": WITSSymbol(
        code="0412",
        name="TNUM",
        description="Trip Number",
        data_type=WITSDataType.INTEGER,
        length=2,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=4,
        item_number=12
    ),
    "0413": WITSSymbol(
        code="0413",
        name="MFIA",
        description="Mud Flow In (avg)",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.LPM,
        fps_units=WITSUnits.GPM,
        record_type=4,
        item_number=13
    ),
    "0413": WITSSymbol(
        code="0413",
        name="STIS",
        description="In-Slips Status",
        data_type=WITSDataType.ASCII,
        length=2,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=4,
        item_number=13
    ),
    "0414": WITSSymbol(
        code="0414",
        name="SPPA",
        description="Standpipe Pressure (avg)",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.KPA,
        fps_units=WITSUnits.PSI,
        record_type=4,
        item_number=14
    ),
    "0414": WITSSymbol(
        code="0414",
        name="HKLA",
        description="Hookload (avg)",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.KDN,
        fps_units=WITSUnits.KLB,
        record_type=4,
        item_number=14
    ),
    "0415": WITSSymbol(
        code="0415",
        name="PV",
        description="Plastic Viscosity",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=4,
        item_number=15
    ),
    "0415": WITSSymbol(
        code="0415",
        name="BPOS",
        description="Block Position",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.METERS,
        fps_units=WITSUnits.FEET,
        record_type=4,
        item_number=15
    ),
    "0416": WITSSymbol(
        code="0416",
        name="YP",
        description="Yield Point",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=4,
        item_number=16
    ),
    "0416": WITSSymbol(
        code="0416",
        name="RSUX",
        description="Running Speed - up (max)",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=4,
        item_number=16
    ),
    "0417": WITSSymbol(
        code="0417",
        name="PLB",
        description="Pressure Loss - bit",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.KPA,
        fps_units=WITSUnits.PSI,
        record_type=4,
        item_number=17
    ),
    "0417": WITSSymbol(
        code="0417",
        name="RSDX",
        description="Running Speed - down (max)",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=4,
        item_number=17
    ),
    "0418": WITSSymbol(
        code="0418",
        name="PLDS",
        description="Pressure Loss - string",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.KPA,
        fps_units=WITSUnits.PSI,
        record_type=4,
        item_number=18
    ),
    "0418": WITSSymbol(
        code="0418",
        name="FVOC",
        description="Fill/Gain Volume Obs.(cum)",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.M3,
        fps_units=WITSUnits.BBL,
        record_type=4,
        item_number=18
    ),
    "0419": WITSSymbol(
        code="0419",
        name="PLA",
        description="Pressure Loss - annulus",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.KPA,
        fps_units=WITSUnits.PSI,
        record_type=4,
        item_number=19
    ),
    "0420": WITSSymbol(
        code="0420",
        name="PLSU",
        description="Pressure Loss - surface",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.KPA,
        fps_units=WITSUnits.PSI,
        record_type=4,
        item_number=20
    ),
    "0421": WITSSymbol(
        code="0421",
        name="PLMM",
        description="Pressure Loss - mud motor",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.KPA,
        fps_units=WITSUnits.PSI,
        record_type=4,
        item_number=21
    ),
    "0422": WITSSymbol(
        code="0422",
        name="PLMW",
        description="Pressure Loss - MWD tool",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.KPA,
        fps_units=WITSUnits.PSI,
        record_type=4,
        item_number=22
    ),
    "0423": WITSSymbol(
        code="0423",
        name="PLPB",
        description="Pressure Loss - % at bit",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.PERCENT,
        fps_units=WITSUnits.PERCENT,
        record_type=4,
        item_number=23
    ),
    "0424": WITSSymbol(
        code="0424",
        name="BHP",
        description="Bit Hydraulic Power",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=4,
        item_number=24
    ),
    "0425": WITSSymbol(
        code="0425",
        name="BHPA",
        description="Bit Hydraulic Power/Area",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=4,
        item_number=25
    ),
    "0426": WITSSymbol(
        code="0426",
        name="JIF",
        description="Jet Impact Force",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.KDN,
        fps_units=WITSUnits.UNITLESS,
        record_type=4,
        item_number=26
    ),
    "0427": WITSSymbol(
        code="0427",
        name="JV",
        description="Jet Velocity",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=4,
        item_number=27
    ),
    "0428": WITSSymbol(
        code="0428",
        name="AVN",
        description="Annular Velocity (min)",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=4,
        item_number=28
    ),
    "0429": WITSSymbol(
        code="0429",
        name="AVX",
        description="Annular Velocity (max)",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=4,
        item_number=29
    ),
    "0430": WITSSymbol(
        code="0430",
        name="ECDT",
        description="ECD at Total Depth",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.KGM3,
        fps_units=WITSUnits.PPG,
        record_type=4,
        item_number=30
    ),
    "0431": WITSSymbol(
        code="0431",
        name="ECDB",
        description="ECD at Bit",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.KGM3,
        fps_units=WITSUnits.PPG,
        record_type=4,
        item_number=31
    ),
    "0432": WITSSymbol(
        code="0432",
        name="ECDC",
        description="ECD at Casing Shoe",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.KGM3,
        fps_units=WITSUnits.PPG,
        record_type=4,
        item_number=32
    ),
    "0433": WITSSymbol(
        code="0433",
        name="PHP",
        description="Pump Hydraulic Power",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=4,
        item_number=33
    ),
    "0434": WITSSymbol(
        code="0434",
        name="PLCO",
        description="Calc/Obs Press.Loss ratio",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.PERCENT,
        fps_units=WITSUnits.PERCENT,
        record_type=4,
        item_number=34
    ),
}

# WITS Record 6 symbols - Trip - Connections
WITS_RECORD_6_SYMBOLS = {
    "0601": WITSSymbol(
        code="0601",
        name="WID",
        description="Well Identifier",
        data_type=WITSDataType.ASCII,
        length=16,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=6,
        item_number=1
    ),
    "0602": WITSSymbol(
        code="0602",
        name="SKNO",
        description="Sidetrack/Hole Sect No.",
        data_type=WITSDataType.INTEGER,
        length=2,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=6,
        item_number=2
    ),
    "0603": WITSSymbol(
        code="0603",
        name="RID",
        description="Record Identifier",
        data_type=WITSDataType.INTEGER,
        length=2,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=6,
        item_number=3
    ),
    "0604": WITSSymbol(
        code="0604",
        name="SQID",
        description="Sequence Identifier",
        data_type=WITSDataType.LONG,
        length=4,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=6,
        item_number=4
    ),
    "0605": WITSSymbol(
        code="0605",
        name="DATE",
        description="Date",
        data_type=WITSDataType.LONG,
        length=4,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=6,
        item_number=5
    ),
    "0606": WITSSymbol(
        code="0606",
        name="TIME",
        description="Time",
        data_type=WITSDataType.LONG,
        length=4,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=6,
        item_number=6
    ),
    "0607": WITSSymbol(
        code="0607",
        name="ACTC",
        description="Activity Code",
        data_type=WITSDataType.INTEGER,
        length=2,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=6,
        item_number=7
    ),
    "0608": WITSSymbol(
        code="0608",
        name="DBTM",
        description="Depth Bit (meas)",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.METERS,
        fps_units=WITSUnits.FEET,
        record_type=6,
        item_number=8
    ),
    "0609": WITSSymbol(
        code="0609",
        name="DBTV",
        description="Depth Bit (vert)",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.METERS,
        fps_units=WITSUnits.FEET,
        record_type=6,
        item_number=9
    ),
    "0610": WITSSymbol(
        code="0610",
        name="DMEA",
        description="Depth Hole (meas)",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.METERS,
        fps_units=WITSUnits.FEET,
        record_type=6,
        item_number=10
    ),
    "0611": WITSSymbol(
        code="0611",
        name="DVER",
        description="Depth Hole (vert)",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.METERS,
        fps_units=WITSUnits.FEET,
        record_type=6,
        item_number=11
    ),
    "0612": WITSSymbol(
        code="0612",
        name="TNUM",
        description="Trip Number",
        data_type=WITSDataType.INTEGER,
        length=2,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=6,
        item_number=12
    ),
    "0613": WITSSymbol(
        code="0613",
        name="CDON",
        description="Connections Done",
        data_type=WITSDataType.INTEGER,
        length=2,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=6,
        item_number=13
    ),
    "0614": WITSSymbol(
        code="0614",
        name="CREM",
        description="Connections Remaining",
        data_type=WITSDataType.INTEGER,
        length=2,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=6,
        item_number=14
    ),
    "0615": WITSSymbol(
        code="0615",
        name="ETSL",
        description="Elapsed Time In-Slips",
        data_type=WITSDataType.INTEGER,
        length=2,
        metric_units=WITSUnits.SEC,
        fps_units=WITSUnits.SEC,
        record_type=6,
        item_number=15
    ),
    "0616": WITSSymbol(
        code="0616",
        name="ETOS",
        description="Elapsed Time Out-of-Slips",
        data_type=WITSDataType.INTEGER,
        length=2,
        metric_units=WITSUnits.SEC,
        fps_units=WITSUnits.SEC,
        record_type=6,
        item_number=16
    ),
    "0617": WITSSymbol(
        code="0617",
        name="RSUX",
        description="Running Speed -up (max)",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.MS,
        fps_units=WITSUnits.FPM,
        record_type=6,
        item_number=17
    ),
    "0618": WITSSymbol(
        code="0618",
        name="RSUA",
        description="Running Speed -up (avg)",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.MS,
        fps_units=WITSUnits.FPM,
        record_type=6,
        item_number=18
    ),
    "0619": WITSSymbol(
        code="0619",
        name="RSDX",
        description="Running Speed -down (max)",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.MS,
        fps_units=WITSUnits.FPM,
        record_type=6,
        item_number=19
    ),
    "0620": WITSSymbol(
        code="0620",
        name="RSDA",
        description="Running Speed -down (avg)",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.MS,
        fps_units=WITSUnits.FPM,
        record_type=6,
        item_number=20
    ),
    "0621": WITSSymbol(
        code="0621",
        name="HKLX",
        description="Hookload (max)",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.KDN,
        fps_units=WITSUnits.KLB,
        record_type=6,
        item_number=21
    ),
    "0622": WITSSymbol(
        code="0622",
        name="HKLN",
        description="Hookload (min)",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.KDN,
        fps_units=WITSUnits.KLB,
        record_type=6,
        item_number=22
    ),
    "0623": WITSSymbol(
        code="0623",
        name="HKLA",
        description="Hookload (avg)",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.KDN,
        fps_units=WITSUnits.KLB,
        record_type=6,
        item_number=23
    ),
    "0624": WITSSymbol(
        code="0624",
        name="TQMX",
        description="Torque - Make Up (max)",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.KNM,
        fps_units=WITSUnits.KFLB,
        record_type=6,
        item_number=24
    ),
    "0625": WITSSymbol(
        code="0625",
        name="TQBX",
        description="Torque - Breakout (max)",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.KNM,
        fps_units=WITSUnits.KFLB,
        record_type=6,
        item_number=25
    ),
    "0626": WITSSymbol(
        code="0626",
        name="FVO",
        description="Fill/Gain Volume Obs.",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.M3,
        fps_units=WITSUnits.BBL,
        record_type=6,
        item_number=26
    ),
    "0627": WITSSymbol(
        code="0627",
        name="FVE",
        description="Fill/Gain Volume Exp.",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.M3,
        fps_units=WITSUnits.BBL,
        record_type=6,
        item_number=27
    ),
    "0628": WITSSymbol(
        code="0628",
        name="FVOC",
        description="Fill/Gain Volume Obs.(cum)",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.M3,
        fps_units=WITSUnits.BBL,
        record_type=6,
        item_number=28
    ),
    "0629": WITSSymbol(
        code="0629",
        name="FVEC",
        description="Fill/Gain Volume Exp (cum)",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.M3,
        fps_units=WITSUnits.BBL,
        record_type=6,
        item_number=29
    ),
}

# WITS Record 7 symbols - Survey/Directional
WITS_RECORD_7_SYMBOLS = {
    "0701": WITSSymbol(
        code="0701",
        name="WID",
        description="Well Identifier",
        data_type=WITSDataType.ASCII,
        length=16,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=7,
        item_number=1
    ),
    "0702": WITSSymbol(
        code="0702",
        name="SKNO",
        description="Sidetrack/Hole Sect No.",
        data_type=WITSDataType.INTEGER,
        length=2,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=7,
        item_number=2
    ),
    "0703": WITSSymbol(
        code="0703",
        name="RID",
        description="Record Identifier",
        data_type=WITSDataType.INTEGER,
        length=2,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=7,
        item_number=3
    ),
    "0704": WITSSymbol(
        code="0704",
        name="SQID",
        description="Sequence Identifier",
        data_type=WITSDataType.LONG,
        length=4,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=7,
        item_number=4
    ),
    "0705": WITSSymbol(
        code="0705",
        name="DATE",
        description="Date",
        data_type=WITSDataType.LONG,
        length=4,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=7,
        item_number=5
    ),
    "0706": WITSSymbol(
        code="0706",
        name="TIME",
        description="Time",
        data_type=WITSDataType.LONG,
        length=4,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=7,
        item_number=6
    ),
    "0707": WITSSymbol(
        code="0707",
        name="ACTC",
        description="Activity Code",
        data_type=WITSDataType.INTEGER,
        length=2,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=7,
        item_number=7
    ),
    "0708": WITSSymbol(
        code="0708",
        name="DSVM",
        description="Depth Svy/reading (meas)",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.METERS,
        fps_units=WITSUnits.FEET,
        record_type=7,
        item_number=8
    ),
    "0709": WITSSymbol(
        code="0709",
        name="DSVV",
        description="Depth Svy/reading (vert)",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.METERS,
        fps_units=WITSUnits.FEET,
        record_type=7,
        item_number=9
    ),
    "0710": WITSSymbol(
        code="0710",
        name="PASS",
        description="Pass Number",
        data_type=WITSDataType.INTEGER,
        length=2,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=7,
        item_number=10
    ),
    "0711": WITSSymbol(
        code="0711",
        name="DMEA",
        description="Depth Hole (meas)",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.METERS,
        fps_units=WITSUnits.FEET,
        record_type=7,
        item_number=11
    ),
    "0712": WITSSymbol(
        code="0712",
        name="STYP",
        description="Svy Type",
        data_type=WITSDataType.ASCII,
        length=8,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=7,
        item_number=12
    ),
    "0713": WITSSymbol(
        code="0713",
        name="SINC",
        description="Svy Inclination",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.DEG,
        fps_units=WITSUnits.DEG,
        record_type=7,
        item_number=13
    ),
    "0714": WITSSymbol(
        code="0714",
        name="SAZU",
        description="Svy Azimuth (uncorrected)",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.DEG,
        fps_units=WITSUnits.DEG,
        record_type=7,
        item_number=14
    ),
    "0715": WITSSymbol(
        code="0715",
        name="SAZC",
        description="Svy Azimuth (corrected)",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.DEG,
        fps_units=WITSUnits.DEG,
        record_type=7,
        item_number=15
    ),
    "0716": WITSSymbol(
        code="0716",
        name="SMTF",
        description="Svy Magnetic Toolface",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.DEG,
        fps_units=WITSUnits.DEG,
        record_type=7,
        item_number=16
    ),
    "0717": WITSSymbol(
        code="0717",
        name="SGTF",
        description="Svy Gravity Toolface",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.DEG,
        fps_units=WITSUnits.DEG,
        record_type=7,
        item_number=17
    ),
    "0718": WITSSymbol(
        code="0718",
        name="SNS",
        description="Svy North-South Position",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.METERS,
        fps_units=WITSUnits.FEET,
        record_type=7,
        item_number=18
    ),
    "0719": WITSSymbol(
        code="0719",
        name="SEW",
        description="Svy East-West Position",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.METERS,
        fps_units=WITSUnits.FEET,
        record_type=7,
        item_number=19
    ),
    "0720": WITSSymbol(
        code="0720",
        name="SDLS",
        description="Svy Dog Leg Severity",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.DGHM,
        fps_units=WITSUnits.DGHF,
        record_type=7,
        item_number=20
    ),
    "0721": WITSSymbol(
        code="0721",
        name="SWLK",
        description="Svy Rate of Walk",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.DGHM,
        fps_units=WITSUnits.DGHF,
        record_type=7,
        item_number=21
    ),
}

# WITS Record 8 symbols - MWD Formation Evaluation
WITS_RECORD_8_SYMBOLS = {
    "0801": WITSSymbol(
        code="0801",
        name="WID",
        description="Well Identifier",
        data_type=WITSDataType.ASCII,
        length=16,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=8,
        item_number=1
    ),
    "0802": WITSSymbol(
        code="0802",
        name="SKNO",
        description="Sidetrack/Hole Sect No.",
        data_type=WITSDataType.INTEGER,
        length=2,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=8,
        item_number=2
    ),
    "0803": WITSSymbol(
        code="0803",
        name="RID",
        description="Record Identifier",
        data_type=WITSDataType.INTEGER,
        length=2,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=8,
        item_number=3
    ),
    "0804": WITSSymbol(
        code="0804",
        name="SQID",
        description="Sequence Identifier",
        data_type=WITSDataType.LONG,
        length=4,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=8,
        item_number=4
    ),
    "0805": WITSSymbol(
        code="0805",
        name="DATE",
        description="Date",
        data_type=WITSDataType.LONG,
        length=4,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=8,
        item_number=5
    ),
    "0806": WITSSymbol(
        code="0806",
        name="TIME",
        description="Time",
        data_type=WITSDataType.LONG,
        length=4,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=8,
        item_number=6
    ),
    "0807": WITSSymbol(
        code="0807",
        name="ACTC",
        description="Activity Code",
        data_type=WITSDataType.INTEGER,
        length=2,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=8,
        item_number=7
    ),
    "0808": WITSSymbol(
        code="0808",
        name="DMEA",
        description="Depth Hole (meas)",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.METERS,
        fps_units=WITSUnits.FEET,
        record_type=8,
        item_number=8
    ),
    "0809": WITSSymbol(
        code="0809",
        name="DVER",
        description="Depth Hole (vert)",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.METERS,
        fps_units=WITSUnits.FEET,
        record_type=8,
        item_number=9
    ),
    "0810": WITSSymbol(
        code="0810",
        name="DBTM",
        description="Depth Bit (meas)",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.METERS,
        fps_units=WITSUnits.FEET,
        record_type=8,
        item_number=10
    ),
    "0811": WITSSymbol(
        code="0811",
        name="DBTV",
        description="Depth Bit (vert)",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.METERS,
        fps_units=WITSUnits.FEET,
        record_type=8,
        item_number=11
    ),
    "0812": WITSSymbol(
        code="0812",
        name="PASS",
        description="Pass Number",
        data_type=WITSDataType.INTEGER,
        length=2,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=8,
        item_number=12
    ),
    "0813": WITSSymbol(
        code="0813",
        name="DR1M",
        description="Depth Resis 1 sensor (meas)",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.METERS,
        fps_units=WITSUnits.FEET,
        record_type=8,
        item_number=13
    ),
    "0814": WITSSymbol(
        code="0814",
        name="DR1V",
        description="Depth Resis 1 sensor (vert)",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.METERS,
        fps_units=WITSUnits.FEET,
        record_type=8,
        item_number=14
    ),
    "0815": WITSSymbol(
        code="0815",
        name="MR1",
        description="Resis 1 reading",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=8,
        item_number=15
    ),
    "0816": WITSSymbol(
        code="0816",
        name="MR1C",
        description="Resis 1 (borehole corr)",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=8,
        item_number=16
    ),
    "0817": WITSSymbol(
        code="0817",
        name="DR2M",
        description="Depth Resis 2 sensor (meas)",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.METERS,
        fps_units=WITSUnits.FEET,
        record_type=8,
        item_number=17
    ),
    "0818": WITSSymbol(
        code="0818",
        name="DR2V",
        description="Depth Resis 2 sensor (vert)",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.METERS,
        fps_units=WITSUnits.FEET,
        record_type=8,
        item_number=18
    ),
    "0819": WITSSymbol(
        code="0819",
        name="MR2",
        description="Resis 2 reading",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=8,
        item_number=19
    ),
    "0820": WITSSymbol(
        code="0820",
        name="MR2C",
        description="Resis 2 (borehole corr)",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=8,
        item_number=20
    ),
    "0821": WITSSymbol(
        code="0821",
        name="DG1M",
        description="Depth G.Ray 1 sensor(meas)",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.METERS,
        fps_units=WITSUnits.FEET,
        record_type=8,
        item_number=21
    ),
    "0822": WITSSymbol(
        code="0822",
        name="DG1V",
        description="Depth G.Ray 1 sensor(vert)",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.METERS,
        fps_units=WITSUnits.FEET,
        record_type=8,
        item_number=22
    ),
    "0823": WITSSymbol(
        code="0823",
        name="MG1",
        description="Gamma Ray 1 reading",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=8,
        item_number=23
    ),
    "0824": WITSSymbol(
        code="0824",
        name="MG1C",
        description="Gamma Ray 1(borehole corr)",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=8,
        item_number=24
    ),
    "0825": WITSSymbol(
        code="0825",
        name="DG2M",
        description="Depth G.Ray 2 sensor(meas)",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.METERS,
        fps_units=WITSUnits.FEET,
        record_type=8,
        item_number=25
    ),
    "0826": WITSSymbol(
        code="0826",
        name="DG2V",
        description="Depth G.Ray 2 sensor(vert)",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.METERS,
        fps_units=WITSUnits.FEET,
        record_type=8,
        item_number=26
    ),
    "0827": WITSSymbol(
        code="0827",
        name="MG2",
        description="Gamma Ray 2 reading",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=8,
        item_number=27
    ),
    "0828": WITSSymbol(
        code="0828",
        name="MG2C",
        description="Gamma Ray 2(borehole corr)",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=8,
        item_number=28
    ),
    "0829": WITSSymbol(
        code="0829",
        name="DP1M",
        description="Depth Por 1 sensor (meas)",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.METERS,
        fps_units=WITSUnits.FEET,
        record_type=8,
        item_number=29
    ),
    "0830": WITSSymbol(
        code="0830",
        name="DP1V",
        description="Depth Por 1 sensor (vert)",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.METERS,
        fps_units=WITSUnits.FEET,
        record_type=8,
        item_number=30
    ),
    "0831": WITSSymbol(
        code="0831",
        name="MPO1",
        description="Porosity Tool 1 reading",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=8,
        item_number=31
    ),
    "0832": WITSSymbol(
        code="0832",
        name="DP2M",
        description="Depth Por 2 sensor (meas)",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.METERS,
        fps_units=WITSUnits.FEET,
        record_type=8,
        item_number=32
    ),
    "0833": WITSSymbol(
        code="0833",
        name="DP2V",
        description="Depth Por 2 sensor (vert)",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.METERS,
        fps_units=WITSUnits.FEET,
        record_type=8,
        item_number=33
    ),
    "0834": WITSSymbol(
        code="0834",
        name="MPO2",
        description="Porosity Tool 2 reading",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=8,
        item_number=34
    ),
    "0835": WITSSymbol(
        code="0835",
        name="MFTA",
        description="Downhole Fluid Temp (ann)",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.DEGC,
        fps_units=WITSUnits.DEGF,
        record_type=8,
        item_number=35
    ),
    "0836": WITSSymbol(
        code="0836",
        name="MFTP",
        description="Downhole Fluid Temp (pipe)",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.DEGC,
        fps_units=WITSUnits.DEGF,
        record_type=8,
        item_number=36
    ),
    "0837": WITSSymbol(
        code="0837",
        name="MFRA",
        description="Downhole Fluid Resis (ann)",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=8,
        item_number=37
    ),
    "0838": WITSSymbol(
        code="0838",
        name="MFRP",
        description="Downhole Fluid Resis (pipe)",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=8,
        item_number=38
    ),
    "0839": WITSSymbol(
        code="0839",
        name="DFDM",
        description="Depth Form Density (meas)",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.METERS,
        fps_units=WITSUnits.FEET,
        record_type=8,
        item_number=39
    ),
    "0840": WITSSymbol(
        code="0840",
        name="DFDV",
        description="Depth Form Density (vert)",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.METERS,
        fps_units=WITSUnits.FEET,
        record_type=8,
        item_number=40
    ),
    "0841": WITSSymbol(
        code="0841",
        name="MFD",
        description="Formation Density",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=8,
        item_number=41
    ),
    "0842": WITSSymbol(
        code="0842",
        name="DCLM",
        description="Depth Caliper (meas)",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.METERS,
        fps_units=WITSUnits.FEET,
        record_type=8,
        item_number=42
    ),
    "0843": WITSSymbol(
        code="0843",
        name="DCLV",
        description="Depth Caliper (vert)",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.METERS,
        fps_units=WITSUnits.FEET,
        record_type=8,
        item_number=43
    ),
    "0844": WITSSymbol(
        code="0844",
        name="MCLP",
        description="Caliper",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=8,
        item_number=44
    ),
    "0845": WITSSymbol(
        code="0845",
        name="MFPP",
        description="Pore Pressure Grad MWD",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.KGM3,
        fps_units=WITSUnits.PPG,
        record_type=8,
        item_number=45
    ),
    "0846": WITSSymbol(
        code="0846",
        name="MFFP",
        description="Frac Pressure Grad MWD",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.KGM3,
        fps_units=WITSUnits.PPG,
        record_type=8,
        item_number=46
    ),
}

# WITS Record 9 symbols - MWD Mechanical
WITS_RECORD_9_SYMBOLS = {
    "0901": WITSSymbol(
        code="0901",
        name="WID",
        description="Well Identifier",
        data_type=WITSDataType.ASCII,
        length=16,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=9,
        item_number=1
    ),
    "0902": WITSSymbol(
        code="0902",
        name="SKNO",
        description="Sidetrack/Hole Sect No.",
        data_type=WITSDataType.INTEGER,
        length=2,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=9,
        item_number=2
    ),
    "0903": WITSSymbol(
        code="0903",
        name="RID",
        description="Record Identifier",
        data_type=WITSDataType.INTEGER,
        length=2,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=9,
        item_number=3
    ),
    "0904": WITSSymbol(
        code="0904",
        name="SQID",
        description="Sequence Identifier",
        data_type=WITSDataType.LONG,
        length=4,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=9,
        item_number=4
    ),
    "0905": WITSSymbol(
        code="0905",
        name="DATE",
        description="Date",
        data_type=WITSDataType.LONG,
        length=4,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=9,
        item_number=5
    ),
    "0906": WITSSymbol(
        code="0906",
        name="TIME",
        description="Time",
        data_type=WITSDataType.LONG,
        length=4,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=9,
        item_number=6
    ),
    "0907": WITSSymbol(
        code="0907",
        name="ACTC",
        description="Activity Code",
        data_type=WITSDataType.INTEGER,
        length=2,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=9,
        item_number=7
    ),
    "0908": WITSSymbol(
        code="0908",
        name="DMEA",
        description="Depth Hole (meas)",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.METERS,
        fps_units=WITSUnits.FEET,
        record_type=9,
        item_number=8
    ),
    "0909": WITSSymbol(
        code="0909",
        name="DVER",
        description="Depth Hole (vert)",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.METERS,
        fps_units=WITSUnits.FEET,
        record_type=9,
        item_number=9
    ),
    "0910": WITSSymbol(
        code="0910",
        name="DBTM",
        description="Depth Bit (meas)",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.METERS,
        fps_units=WITSUnits.FEET,
        record_type=9,
        item_number=10
    ),
    "0911": WITSSymbol(
        code="0911",
        name="DBTV",
        description="Depth Bit (vert)",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.METERS,
        fps_units=WITSUnits.FEET,
        record_type=9,
        item_number=11
    ),
    "0912": WITSSymbol(
        code="0912",
        name="PASS",
        description="Pass Number",
        data_type=WITSDataType.INTEGER,
        length=2,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=9,
        item_number=12
    ),
    "0913": WITSSymbol(
        code="0913",
        name="MBPA",
        description="Bottom-hole annulus press",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.KPA,
        fps_units=WITSUnits.PSI,
        record_type=9,
        item_number=13
    ),
    "0914": WITSSymbol(
        code="0914",
        name="MBPI",
        description="Bottom-hole internal press",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.KPA,
        fps_units=WITSUnits.PSI,
        record_type=9,
        item_number=14
    ),
    "0915": WITSSymbol(
        code="0915",
        name="MWBA",
        description="Downhole Wt-on-Bit (avg)",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.KDN,
        fps_units=WITSUnits.KLB,
        record_type=9,
        item_number=15
    ),
    "0916": WITSSymbol(
        code="0916",
        name="MWBX",
        description="Downhole Wt-on-Bit (max)",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.KDN,
        fps_units=WITSUnits.KLB,
        record_type=9,
        item_number=16
    ),
    "0917": WITSSymbol(
        code="0917",
        name="MTQA",
        description="Downhole Torque (avg)",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.KNM,
        fps_units=WITSUnits.KFLB,
        record_type=9,
        item_number=17
    ),
    "0918": WITSSymbol(
        code="0918",
        name="MTQX",
        description="Downhole Torque (max)",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.KNM,
        fps_units=WITSUnits.KFLB,
        record_type=9,
        item_number=18
    ),
    "0919": WITSSymbol(
        code="0919",
        name="MMRP",
        description="Downhole Motor RPM",
        data_type=WITSDataType.INTEGER,
        length=2,
        metric_units=WITSUnits.RPM,
        fps_units=WITSUnits.RPM,
        record_type=9,
        item_number=19
    ),
    "0920": WITSSymbol(
        code="0920",
        name="MALT",
        description="MWD Tool Alternator Voltage",
        data_type=WITSDataType.INTEGER,
        length=2,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=9,
        item_number=20
    ),
}

# WITS Record 10 symbols - Pressure Evaluation
WITS_RECORD_10_SYMBOLS = {
    "1001": WITSSymbol(
        code="1001",
        name="WID",
        description="Well Identifier",
        data_type=WITSDataType.ASCII,
        length=16,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=10,
        item_number=1
    ),
    "1002": WITSSymbol(
        code="1002",
        name="SKNO",
        description="Sidetrack/Hole Sect No.",
        data_type=WITSDataType.INTEGER,
        length=2,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=10,
        item_number=2
    ),
    "1003": WITSSymbol(
        code="1003",
        name="RID",
        description="Record Identifier",
        data_type=WITSDataType.INTEGER,
        length=2,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=10,
        item_number=3
    ),
    "1004": WITSSymbol(
        code="1004",
        name="SQID",
        description="Sequence Identifier",
        data_type=WITSDataType.LONG,
        length=4,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=10,
        item_number=4
    ),
    "1005": WITSSymbol(
        code="1005",
        name="DATE",
        description="Date",
        data_type=WITSDataType.LONG,
        length=4,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=10,
        item_number=5
    ),
    "1006": WITSSymbol(
        code="1006",
        name="TIME",
        description="Time",
        data_type=WITSDataType.LONG,
        length=4,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=10,
        item_number=6
    ),
    "1007": WITSSymbol(
        code="1007",
        name="ACTC",
        description="Activity Code",
        data_type=WITSDataType.INTEGER,
        length=2,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=10,
        item_number=7
    ),
    "1008": WITSSymbol(
        code="1008",
        name="DMEA",
        description="Depth Hole (meas)",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.METERS,
        fps_units=WITSUnits.FEET,
        record_type=10,
        item_number=8
    ),
    "1009": WITSSymbol(
        code="1009",
        name="DVER",
        description="Depth Hole (vert)",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.METERS,
        fps_units=WITSUnits.FEET,
        record_type=10,
        item_number=9
    ),
    "1010": WITSSymbol(
        code="1010",
        name="DSAM",
        description="Depth Sample (meas)",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.METERS,
        fps_units=WITSUnits.FEET,
        record_type=10,
        item_number=10
    ),
    "1011": WITSSymbol(
        code="1011",
        name="DSAV",
        description="Depth Sample (vert)",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.METERS,
        fps_units=WITSUnits.FEET,
        record_type=10,
        item_number=11
    ),
    "1012": WITSSymbol(
        code="1012",
        name="FPPG",
        description="Est. Form. Pore Press Grad.",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.KGM3,
        fps_units=WITSUnits.PPG,
        record_type=10,
        item_number=12
    ),
    "1013": WITSSymbol(
        code="1013",
        name="FFPG",
        description="Est. Form. Frac Press Grad.",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.KGM3,
        fps_units=WITSUnits.PPG,
        record_type=10,
        item_number=13
    ),
    "1014": WITSSymbol(
        code="1014",
        name="FOPG",
        description="Est. Form. Overburden Grad.",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.KGM3,
        fps_units=WITSUnits.PPG,
        record_type=10,
        item_number=14
    ),
    "1015": WITSSymbol(
        code="1015",
        name="KTOL",
        description="Est. Kick Tolerance",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.KGM3,
        fps_units=WITSUnits.PPG,
        record_type=10,
        item_number=15
    ),
    "1016": WITSSymbol(
        code="1016",
        name="PSIP",
        description="Max. Permitted SICP (init)",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.KPA,
        fps_units=WITSUnits.PSI,
        record_type=10,
        item_number=16
    ),
    "1017": WITSSymbol(
        code="1017",
        name="CGSA",
        description="Connection Gas (avg)",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.PERCENT,
        fps_units=WITSUnits.PERCENT,
        record_type=10,
        item_number=17
    ),
    "1018": WITSSymbol(
        code="1018",
        name="CGSX",
        description="Connection Gas (max)",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.PERCENT,
        fps_units=WITSUnits.PERCENT,
        record_type=10,
        item_number=18
    ),
    "1019": WITSSymbol(
        code="1019",
        name="CGSL",
        description="Connection Gas (last)",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.PERCENT,
        fps_units=WITSUnits.PERCENT,
        record_type=10,
        item_number=19
    ),
    "1020": WITSSymbol(
        code="1020",
        name="TGAS",
        description="Last Trip Gas",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.PERCENT,
        fps_units=WITSUnits.PERCENT,
        record_type=10,
        item_number=20
    ),
    "1021": WITSSymbol(
        code="1021",
        name="SDEN",
        description="Shale Density",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=10,
        item_number=21
    ),
    "1022": WITSSymbol(
        code="1022",
        name="CEC",
        description="Cuttings CEC",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=10,
        item_number=22
    ),
    "1023": WITSSymbol(
        code="1023",
        name="CAV",
        description="Cavings %",
        data_type=WITSDataType.INTEGER,
        length=2,
        metric_units=WITSUnits.PERCENT,
        fps_units=WITSUnits.PERCENT,
        record_type=10,
        item_number=23
    ),
    "1024": WITSSymbol(
        code="1024",
        name="DXC",
        description="Corr. Drilling Exponent",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=10,
        item_number=24
    ),
}

# WITS Record 11 symbols - Mud Tank Volumes
WITS_RECORD_11_SYMBOLS = {
    "1101": WITSSymbol(
        code="1101",
        name="WID",
        description="Well Identifier",
        data_type=WITSDataType.ASCII,
        length=16,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=11,
        item_number=1
    ),
    "1102": WITSSymbol(
        code="1102",
        name="SKNO",
        description="Sidetrack/Hole Sect No.",
        data_type=WITSDataType.INTEGER,
        length=2,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=11,
        item_number=2
    ),
    "1103": WITSSymbol(
        code="1103",
        name="RID",
        description="Record Identifier",
        data_type=WITSDataType.INTEGER,
        length=2,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=11,
        item_number=3
    ),
    "1104": WITSSymbol(
        code="1104",
        name="SQID",
        description="Sequence Identifier",
        data_type=WITSDataType.LONG,
        length=4,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=11,
        item_number=4
    ),
    "1105": WITSSymbol(
        code="1105",
        name="DATE",
        description="Date",
        data_type=WITSDataType.LONG,
        length=4,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=11,
        item_number=5
    ),
    "1106": WITSSymbol(
        code="1106",
        name="TIME",
        description="Time",
        data_type=WITSDataType.LONG,
        length=4,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=11,
        item_number=6
    ),
    "1107": WITSSymbol(
        code="1107",
        name="ACTC",
        description="Activity Code",
        data_type=WITSDataType.INTEGER,
        length=2,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=11,
        item_number=7
    ),
    "1108": WITSSymbol(
        code="1108",
        name="DMEA",
        description="Depth Hole (meas)",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.METERS,
        fps_units=WITSUnits.FEET,
        record_type=11,
        item_number=8
    ),
    "1109": WITSSymbol(
        code="1109",
        name="DVER",
        description="Depth Hole (vert)",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.METERS,
        fps_units=WITSUnits.FEET,
        record_type=11,
        item_number=9
    ),
    "1110": WITSSymbol(
        code="1110",
        name="TVT",
        description="Tank Volume (total)",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.M3,
        fps_units=WITSUnits.BBL,
        record_type=11,
        item_number=10
    ),
    "1111": WITSSymbol(
        code="1111",
        name="TVA",
        description="Tank Volume (active)",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.M3,
        fps_units=WITSUnits.BBL,
        record_type=11,
        item_number=11
    ),
    "1112": WITSSymbol(
        code="1112",
        name="TVCT",
        description="Tank Volume Change (total)",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.M3,
        fps_units=WITSUnits.BBL,
        record_type=11,
        item_number=12
    ),
    "1113": WITSSymbol(
        code="1113",
        name="TVCA",
        description="Tank Volume Change (active)",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.M3,
        fps_units=WITSUnits.BBL,
        record_type=11,
        item_number=13
    ),
    "1114": WITSSymbol(
        code="1114",
        name="TVRT",
        description="Tank Volume Reset Time",
        data_type=WITSDataType.LONG,
        length=4,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=11,
        item_number=14
    ),
    "1115": WITSSymbol(
        code="1115",
        name="TV01",
        description="Tank 01 Volume",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.M3,
        fps_units=WITSUnits.BBL,
        record_type=11,
        item_number=15
    ),
    "1116": WITSSymbol(
        code="1116",
        name="TV02",
        description="Tank 02 Volume",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.M3,
        fps_units=WITSUnits.BBL,
        record_type=11,
        item_number=16
    ),
    "1117": WITSSymbol(
        code="1117",
        name="TV03",
        description="Tank 03 Volume",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.M3,
        fps_units=WITSUnits.BBL,
        record_type=11,
        item_number=17
    ),
    "1118": WITSSymbol(
        code="1118",
        name="TV04",
        description="Tank 04 Volume",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.M3,
        fps_units=WITSUnits.BBL,
        record_type=11,
        item_number=18
    ),
    "1119": WITSSymbol(
        code="1119",
        name="TV05",
        description="Tank 05 Volume",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.M3,
        fps_units=WITSUnits.BBL,
        record_type=11,
        item_number=19
    ),
    "1120": WITSSymbol(
        code="1120",
        name="TV06",
        description="Tank 06 Volume",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.M3,
        fps_units=WITSUnits.BBL,
        record_type=11,
        item_number=20
    ),
    "1121": WITSSymbol(
        code="1121",
        name="TV07",
        description="Tank 07 Volume",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.M3,
        fps_units=WITSUnits.BBL,
        record_type=11,
        item_number=21
    ),
    "1122": WITSSymbol(
        code="1122",
        name="TV08",
        description="Tank 08 Volume",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.M3,
        fps_units=WITSUnits.BBL,
        record_type=11,
        item_number=22
    ),
    "1123": WITSSymbol(
        code="1123",
        name="TV09",
        description="Tank 09 Volume",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.M3,
        fps_units=WITSUnits.BBL,
        record_type=11,
        item_number=23
    ),
    "1124": WITSSymbol(
        code="1124",
        name="TV10",
        description="Tank 10 Volume",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.M3,
        fps_units=WITSUnits.BBL,
        record_type=11,
        item_number=24
    ),
    "1125": WITSSymbol(
        code="1125",
        name="TV11",
        description="Tank 11 Volume",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.M3,
        fps_units=WITSUnits.BBL,
        record_type=11,
        item_number=25
    ),
    "1126": WITSSymbol(
        code="1126",
        name="TV12",
        description="Tank 12 Volume",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.M3,
        fps_units=WITSUnits.BBL,
        record_type=11,
        item_number=26
    ),
    "1127": WITSSymbol(
        code="1127",
        name="TV13",
        description="Tank 13 Volume",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.M3,
        fps_units=WITSUnits.BBL,
        record_type=11,
        item_number=27
    ),
    "1128": WITSSymbol(
        code="1128",
        name="TV14",
        description="Tank 14 Volume",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.M3,
        fps_units=WITSUnits.BBL,
        record_type=11,
        item_number=28
    ),
    "1129": WITSSymbol(
        code="1129",
        name="TTV1",
        description="Trip Tank 1 Volume",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.M3,
        fps_units=WITSUnits.BBL,
        record_type=11,
        item_number=29
    ),
    "1130": WITSSymbol(
        code="1130",
        name="TTV2",
        description="Trip Tank 2 Volume",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.M3,
        fps_units=WITSUnits.BBL,
        record_type=11,
        item_number=30
    ),
}

# WITS Record 12 symbols - Chromatograph Cycle-Based
WITS_RECORD_12_SYMBOLS = {
    "1201": WITSSymbol(
        code="1201",
        name="WID",
        description="Well Identifier",
        data_type=WITSDataType.ASCII,
        length=16,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=12,
        item_number=1
    ),
    "1202": WITSSymbol(
        code="1202",
        name="SKNO",
        description="Sidetrack/Hole Sect No.",
        data_type=WITSDataType.INTEGER,
        length=2,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=12,
        item_number=2
    ),
    "1203": WITSSymbol(
        code="1203",
        name="RID",
        description="Record Identifier",
        data_type=WITSDataType.INTEGER,
        length=2,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=12,
        item_number=3
    ),
    "1204": WITSSymbol(
        code="1204",
        name="SQID",
        description="Sequence Identifier",
        data_type=WITSDataType.LONG,
        length=4,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=12,
        item_number=4
    ),
    "1205": WITSSymbol(
        code="1205",
        name="DATE",
        description="Date",
        data_type=WITSDataType.LONG,
        length=4,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=12,
        item_number=5
    ),
    "1206": WITSSymbol(
        code="1206",
        name="TIME",
        description="Time",
        data_type=WITSDataType.LONG,
        length=4,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=12,
        item_number=6
    ),
    "1207": WITSSymbol(
        code="1207",
        name="ACTC",
        description="Activity Code",
        data_type=WITSDataType.INTEGER,
        length=2,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=12,
        item_number=7
    ),
    "1208": WITSSymbol(
        code="1208",
        name="DCHM",
        description="Depth Chrom Sample (meas)",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.METERS,
        fps_units=WITSUnits.FEET,
        record_type=12,
        item_number=8
    ),
    "1209": WITSSymbol(
        code="1209",
        name="DCHV",
        description="Depth Chrom Sample (vert)",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.METERS,
        fps_units=WITSUnits.FEET,
        record_type=12,
        item_number=9
    ),
    "1210": WITSSymbol(
        code="1210",
        name="DCHR",
        description="Date Chrom Sample",
        data_type=WITSDataType.LONG,
        length=4,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=12,
        item_number=10
    ),
    "1211": WITSSymbol(
        code="1211",
        name="TCHR",
        description="Time Chrom Sample",
        data_type=WITSDataType.LONG,
        length=4,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=12,
        item_number=11
    ),
    "1212": WITSSymbol(
        code="1212",
        name="METH",
        description="Methane (C1)",
        data_type=WITSDataType.LONG,
        length=4,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=12,
        item_number=12
    ),
    "1213": WITSSymbol(
        code="1213",
        name="ETH",
        description="Ethane (C2)",
        data_type=WITSDataType.LONG,
        length=4,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=12,
        item_number=13
    ),
    "1214": WITSSymbol(
        code="1214",
        name="PRP",
        description="Propane (C3)",
        data_type=WITSDataType.LONG,
        length=4,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=12,
        item_number=14
    ),
    "1215": WITSSymbol(
        code="1215",
        name="IBUT",
        description="Iso-Butane (IC4)",
        data_type=WITSDataType.LONG,
        length=4,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=12,
        item_number=15
    ),
    "1216": WITSSymbol(
        code="1216",
        name="NBUT",
        description="Nor-Butane (NC4)",
        data_type=WITSDataType.LONG,
        length=4,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=12,
        item_number=16
    ),
    "1217": WITSSymbol(
        code="1217",
        name="IPEN",
        description="Iso-Pentane (IC5)",
        data_type=WITSDataType.LONG,
        length=4,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=12,
        item_number=17
    ),
    "1218": WITSSymbol(
        code="1218",
        name="NPEN",
        description="Nor-Pentane (NC5)",
        data_type=WITSDataType.LONG,
        length=4,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=12,
        item_number=18
    ),
    "1219": WITSSymbol(
        code="1219",
        name="EPEN",
        description="Neo-Pentane (EC5)",
        data_type=WITSDataType.LONG,
        length=4,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=12,
        item_number=19
    ),
    "1220": WITSSymbol(
        code="1220",
        name="IHEX",
        description="Iso-Hexane (IC6)",
        data_type=WITSDataType.LONG,
        length=4,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=12,
        item_number=20
    ),
    "1221": WITSSymbol(
        code="1221",
        name="NHEX",
        description="Nor-Hexane (NC6)",
        data_type=WITSDataType.LONG,
        length=4,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=12,
        item_number=21
    ),
    "1222": WITSSymbol(
        code="1222",
        name="CO2",
        description="Carbon Dioxide",
        data_type=WITSDataType.LONG,
        length=4,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=12,
        item_number=22
    ),
    "1223": WITSSymbol(
        code="1223",
        name="ACET",
        description="Acetylene",
        data_type=WITSDataType.LONG,
        length=4,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=12,
        item_number=23
    ),
}

# WITS Record 13 symbols - Chromatograph Depth-Based
WITS_RECORD_13_SYMBOLS = {
    "1301": WITSSymbol(
        code="1301",
        name="WID",
        description="Well Identifier",
        data_type=WITSDataType.ASCII,
        length=16,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=13,
        item_number=1
    ),
    "1302": WITSSymbol(
        code="1302",
        name="SKNO",
        description="Sidetrack/Hole Sect No.",
        data_type=WITSDataType.INTEGER,
        length=2,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=13,
        item_number=2
    ),
    "1303": WITSSymbol(
        code="1303",
        name="RID",
        description="Record Identifier",
        data_type=WITSDataType.INTEGER,
        length=2,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=13,
        item_number=3
    ),
    "1304": WITSSymbol(
        code="1304",
        name="SQID",
        description="Sequence Identifier",
        data_type=WITSDataType.LONG,
        length=4,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=13,
        item_number=4
    ),
    "1305": WITSSymbol(
        code="1305",
        name="DATE",
        description="Date",
        data_type=WITSDataType.LONG,
        length=4,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=13,
        item_number=5
    ),
    "1306": WITSSymbol(
        code="1306",
        name="TIME",
        description="Time",
        data_type=WITSDataType.LONG,
        length=4,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=13,
        item_number=6
    ),
    "1307": WITSSymbol(
        code="1307",
        name="ACTC",
        description="Activity Code",
        data_type=WITSDataType.INTEGER,
        length=2,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=13,
        item_number=7
    ),
    "1308": WITSSymbol(
        code="1308",
        name="DRTM",
        description="Depth Returns (meas)",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.METERS,
        fps_units=WITSUnits.FEET,
        record_type=13,
        item_number=8
    ),
    "1309": WITSSymbol(
        code="1309",
        name="DRTV",
        description="Depth Returns (vert)",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.METERS,
        fps_units=WITSUnits.FEET,
        record_type=13,
        item_number=9
    ),
    "1310": WITSSymbol(
        code="1310",
        name="MTHA",
        description="Methane (C1) (avg)",
        data_type=WITSDataType.LONG,
        length=4,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=13,
        item_number=10
    ),
    "1311": WITSSymbol(
        code="1311",
        name="MTHN",
        description="Methane (C1) (min)",
        data_type=WITSDataType.LONG,
        length=4,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=13,
        item_number=11
    ),
    "1312": WITSSymbol(
        code="1312",
        name="MTHX",
        description="Methane (C1) (max)",
        data_type=WITSDataType.LONG,
        length=4,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=13,
        item_number=12
    ),
    "1313": WITSSymbol(
        code="1313",
        name="ETHA",
        description="Ethane (C2) (avg)",
        data_type=WITSDataType.LONG,
        length=4,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=13,
        item_number=13
    ),
    "1314": WITSSymbol(
        code="1314",
        name="ETHN",
        description="Ethane (C2) (min)",
        data_type=WITSDataType.LONG,
        length=4,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=13,
        item_number=14
    ),
    "1315": WITSSymbol(
        code="1315",
        name="ETHX",
        description="Ethane (C2) (max)",
        data_type=WITSDataType.LONG,
        length=4,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=13,
        item_number=15
    ),
    "1316": WITSSymbol(
        code="1316",
        name="PRPA",
        description="Propane (C3) (avg)",
        data_type=WITSDataType.LONG,
        length=4,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=13,
        item_number=16
    ),
    "1317": WITSSymbol(
        code="1317",
        name="PRPN",
        description="Propane (C3) (min)",
        data_type=WITSDataType.LONG,
        length=4,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=13,
        item_number=17
    ),
    "1318": WITSSymbol(
        code="1318",
        name="PRPX",
        description="Propane (C3) (max)",
        data_type=WITSDataType.LONG,
        length=4,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=13,
        item_number=18
    ),
    "1319": WITSSymbol(
        code="1319",
        name="IBTA",
        description="Iso-Butane (IC4) (avg)",
        data_type=WITSDataType.LONG,
        length=4,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=13,
        item_number=19
    ),
    "1320": WITSSymbol(
        code="1320",
        name="IBTN",
        description="Iso-Butane (IC4) (min)",
        data_type=WITSDataType.LONG,
        length=4,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=13,
        item_number=20
    ),
    "1321": WITSSymbol(
        code="1321",
        name="IBTX",
        description="Iso-Butane (IC4) (max)",
        data_type=WITSDataType.LONG,
        length=4,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=13,
        item_number=21
    ),
    "1322": WITSSymbol(
        code="1322",
        name="NBTA",
        description="Nor-Butane (NC4) (avg)",
        data_type=WITSDataType.LONG,
        length=4,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=13,
        item_number=22
    ),
    "1323": WITSSymbol(
        code="1323",
        name="NBTN",
        description="Nor-Butane (NC4) (min)",
        data_type=WITSDataType.LONG,
        length=4,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=13,
        item_number=23
    ),
    "1324": WITSSymbol(
        code="1324",
        name="NBTX",
        description="Nor-Butane (NC4) (max)",
        data_type=WITSDataType.LONG,
        length=4,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=13,
        item_number=24
    ),
    "1325": WITSSymbol(
        code="1325",
        name="IPNA",
        description="Iso-Pentane (IC5) (avg)",
        data_type=WITSDataType.LONG,
        length=4,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=13,
        item_number=25
    ),
    "1326": WITSSymbol(
        code="1326",
        name="IPNN",
        description="Iso-Pentane (IC5) (min)",
        data_type=WITSDataType.LONG,
        length=4,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=13,
        item_number=26
    ),
    "1327": WITSSymbol(
        code="1327",
        name="IPNX",
        description="Iso-Pentane (IC5) (max)",
        data_type=WITSDataType.LONG,
        length=4,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=13,
        item_number=27
    ),
    "1328": WITSSymbol(
        code="1328",
        name="NPNA",
        description="Nor-Pentane (NC5) (avg)",
        data_type=WITSDataType.LONG,
        length=4,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=13,
        item_number=28
    ),
    "1329": WITSSymbol(
        code="1329",
        name="NPNN",
        description="Nor-Pentane (NC5) (min)",
        data_type=WITSDataType.LONG,
        length=4,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=13,
        item_number=29
    ),
    "1330": WITSSymbol(
        code="1330",
        name="NPNX",
        description="Nor-Pentane (NC5) (max)",
        data_type=WITSDataType.LONG,
        length=4,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=13,
        item_number=30
    ),
    "1331": WITSSymbol(
        code="1331",
        name="EPNA",
        description="Neo-Pentane (EC5) (avg)",
        data_type=WITSDataType.LONG,
        length=4,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=13,
        item_number=31
    ),
    "1332": WITSSymbol(
        code="1332",
        name="EPNN",
        description="Neo-Pentane (EC5) (min)",
        data_type=WITSDataType.LONG,
        length=4,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=13,
        item_number=32
    ),
    "1333": WITSSymbol(
        code="1333",
        name="EPNX",
        description="Neo-Pentane (EC5) (max)",
        data_type=WITSDataType.LONG,
        length=4,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=13,
        item_number=33
    ),
    "1334": WITSSymbol(
        code="1334",
        name="IHXA",
        description="Iso-Hexane (IC6) (avg)",
        data_type=WITSDataType.LONG,
        length=4,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=13,
        item_number=34
    ),
    "1335": WITSSymbol(
        code="1335",
        name="IHXN",
        description="Iso-Hexane (IC6) (min)",
        data_type=WITSDataType.LONG,
        length=4,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=13,
        item_number=35
    ),
    "1336": WITSSymbol(
        code="1336",
        name="IHXX",
        description="Iso-Hexane (IC6) (max)",
        data_type=WITSDataType.LONG,
        length=4,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=13,
        item_number=36
    ),
    "1337": WITSSymbol(
        code="1337",
        name="NHXA",
        description="Nor-Hexane (NC6) (avg)",
        data_type=WITSDataType.LONG,
        length=4,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=13,
        item_number=37
    ),
    "1338": WITSSymbol(
        code="1338",
        name="NHXN",
        description="Nor-Hexane (NC6) (min)",
        data_type=WITSDataType.LONG,
        length=4,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=13,
        item_number=38
    ),
    "1339": WITSSymbol(
        code="1339",
        name="NHXX",
        description="Nor-Hexane (NC6) (max)",
        data_type=WITSDataType.LONG,
        length=4,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=13,
        item_number=39
    ),
    "1340": WITSSymbol(
        code="1340",
        name="CO2A",
        description="Carbon Dioxide (avg)",
        data_type=WITSDataType.LONG,
        length=4,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=13,
        item_number=40
    ),
    "1341": WITSSymbol(
        code="1341",
        name="CO2N",
        description="Carbon Dioxide (min)",
        data_type=WITSDataType.LONG,
        length=4,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=13,
        item_number=41
    ),
    "1342": WITSSymbol(
        code="1342",
        name="CO2X",
        description="Carbon Dioxide (max)",
        data_type=WITSDataType.LONG,
        length=4,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=13,
        item_number=42
    ),
    "1343": WITSSymbol(
        code="1343",
        name="ACET",
        description="Acetylene",
        data_type=WITSDataType.LONG,
        length=4,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=13,
        item_number=43
    ),
}

# WITS Record 14 symbols - Lagged Mud Properties
WITS_RECORD_14_SYMBOLS = {
    "1401": WITSSymbol(
        code="1401",
        name="WID",
        description="Well Identifier",
        data_type=WITSDataType.ASCII,
        length=16,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=14,
        item_number=1
    ),
    "1402": WITSSymbol(
        code="1402",
        name="SKNO",
        description="Sidetrack/Hole Sect No.",
        data_type=WITSDataType.INTEGER,
        length=2,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=14,
        item_number=2
    ),
    "1403": WITSSymbol(
        code="1403",
        name="RID",
        description="Record Identifier",
        data_type=WITSDataType.INTEGER,
        length=2,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=14,
        item_number=3
    ),
    "1404": WITSSymbol(
        code="1404",
        name="SQID",
        description="Sequence Identifier",
        data_type=WITSDataType.LONG,
        length=4,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=14,
        item_number=4
    ),
    "1405": WITSSymbol(
        code="1405",
        name="DATE",
        description="Date",
        data_type=WITSDataType.LONG,
        length=4,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=14,
        item_number=5
    ),
    "1406": WITSSymbol(
        code="1406",
        name="TIME",
        description="Time",
        data_type=WITSDataType.LONG,
        length=4,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=14,
        item_number=6
    ),
    "1407": WITSSymbol(
        code="1407",
        name="ACTC",
        description="Activity Code",
        data_type=WITSDataType.INTEGER,
        length=2,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=14,
        item_number=7
    ),
    "1408": WITSSymbol(
        code="1408",
        name="DRTM",
        description="Depth Returns (meas)",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.METERS,
        fps_units=WITSUnits.FEET,
        record_type=14,
        item_number=8
    ),
    "1409": WITSSymbol(
        code="1409",
        name="DRTV",
        description="Depth Returns (vert)",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.METERS,
        fps_units=WITSUnits.FEET,
        record_type=14,
        item_number=9
    ),
    "1410": WITSSymbol(
        code="1410",
        name="MDIL",
        description="Mud Density In (lagd)",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.KGM3,
        fps_units=WITSUnits.PPG,
        record_type=14,
        item_number=10
    ),
    "1411": WITSSymbol(
        code="1411",
        name="MDOA",
        description="Mud Density Out (avg)",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.KGM3,
        fps_units=WITSUnits.PPG,
        record_type=14,
        item_number=11
    ),
    "1412": WITSSymbol(
        code="1412",
        name="MTIL",
        description="Mud Temperature In (lagd)",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.DEGC,
        fps_units=WITSUnits.DEGF,
        record_type=14,
        item_number=12
    ),
    "1413": WITSSymbol(
        code="1413",
        name="MTOA",
        description="Mud Temperature Out (avg)",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.DEGC,
        fps_units=WITSUnits.DEGF,
        record_type=14,
        item_number=13
    ),
    "1414": WITSSymbol(
        code="1414",
        name="MCIL",
        description="Mud Conductivity In (lagd)",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.MMHO,
        fps_units=WITSUnits.MMHO,
        record_type=14,
        item_number=14
    ),
    "1415": WITSSymbol(
        code="1415",
        name="MCOA",
        description="Mud Conductivity Out (avg)",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.MMHO,
        fps_units=WITSUnits.MMHO,
        record_type=14,
        item_number=15
    ),
    "1416": WITSSymbol(
        code="1416",
        name="HHPA",
        description="Hyd.Sulfide Haz.Pot. (avg)",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=14,
        item_number=16
    ),
    "1417": WITSSymbol(
        code="1417",
        name="HPHA",
        description="Hyd.Sulfide pH (avg)",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=14,
        item_number=17
    ),
    "1418": WITSSymbol(
        code="1418",
        name="HPSA",
        description="Hyd.Sulfide pHS (avg)",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.PERCENT,
        fps_units=WITSUnits.PERCENT,
        record_type=14,
        item_number=18
    ),
    "1419": WITSSymbol(
        code="1419",
        name="GSIL",
        description="Gas In (lagd)",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.PERCENT,
        fps_units=WITSUnits.PERCENT,
        record_type=14,
        item_number=19
    ),
    "1420": WITSSymbol(
        code="1420",
        name="GASA",
        description="Gas (avg)",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.PERCENT,
        fps_units=WITSUnits.PERCENT,
        record_type=14,
        item_number=20
    ),
    "1421": WITSSymbol(
        code="1421",
        name="GASX",
        description="Gas (max)",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.PERCENT,
        fps_units=WITSUnits.PERCENT,
        record_type=14,
        item_number=21
    ),
    "1422": WITSSymbol(
        code="1422",
        name="CO2A",
        description="Carbon Dioxide (avg)",
        data_type=WITSDataType.LONG,
        length=4,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=14,
        item_number=22
    ),
    "1423": WITSSymbol(
        code="1423",
        name="HSA",
        description="Hydrogen Sulfide (avg)",
        data_type=WITSDataType.LONG,
        length=4,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=14,
        item_number=23
    ),
    "1424": WITSSymbol(
        code="1424",
        name="HSX",
        description="Hydrogen Sulfide (max)",
        data_type=WITSDataType.LONG,
        length=4,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=14,
        item_number=24
    ),
}

# WITS Record 15 symbols - Cuttings / Lithology
WITS_RECORD_15_SYMBOLS = {
    "1501": WITSSymbol(
        code="1501",
        name="WID",
        description="Well Identifier",
        data_type=WITSDataType.ASCII,
        length=16,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=15,
        item_number=1
    ),
    "1502": WITSSymbol(
        code="1502",
        name="SKNO",
        description="Sidetrack/Hole Sect No.",
        data_type=WITSDataType.INTEGER,
        length=2,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=15,
        item_number=2
    ),
    "1503": WITSSymbol(
        code="1503",
        name="RID",
        description="Record Identifier",
        data_type=WITSDataType.INTEGER,
        length=2,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=15,
        item_number=3
    ),
    "1504": WITSSymbol(
        code="1504",
        name="SQID",
        description="Sequence Identifier",
        data_type=WITSDataType.LONG,
        length=4,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=15,
        item_number=4
    ),
    "1505": WITSSymbol(
        code="1505",
        name="DATE",
        description="Date",
        data_type=WITSDataType.LONG,
        length=4,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=15,
        item_number=5
    ),
    "1506": WITSSymbol(
        code="1506",
        name="TIME",
        description="Time",
        data_type=WITSDataType.LONG,
        length=4,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=15,
        item_number=6
    ),
    "1507": WITSSymbol(
        code="1507",
        name="ACTC",
        description="Activity Code",
        data_type=WITSDataType.INTEGER,
        length=2,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=15,
        item_number=7
    ),
    "1508": WITSSymbol(
        code="1508",
        name="DSAM",
        description="Depth Sample (meas)",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.METERS,
        fps_units=WITSUnits.FEET,
        record_type=15,
        item_number=8
    ),
    "1509": WITSSymbol(
        code="1509",
        name="DSAV",
        description="Depth Sample (vert)",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.METERS,
        fps_units=WITSUnits.FEET,
        record_type=15,
        item_number=9
    ),
    "1510": WITSSymbol(
        code="1510",
        name="DESC",
        description="Description type",
        data_type=WITSDataType.ASCII,
        length=8,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=15,
        item_number=10
    ),
    "1511": WITSSymbol(
        code="1511",
        name="L1TY",
        description="Lith 1 type",
        data_type=WITSDataType.ASCII,
        length=16,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=15,
        item_number=11
    ),
    "1512": WITSSymbol(
        code="1512",
        name="L1PC",
        description="Lith 1 %",
        data_type=WITSDataType.INTEGER,
        length=2,
        metric_units=WITSUnits.PERCENT,
        fps_units=WITSUnits.PERCENT,
        record_type=15,
        item_number=12
    ),
    "1513": WITSSymbol(
        code="1513",
        name="L1CL",
        description="Lith 1 classification",
        data_type=WITSDataType.ASCII,
        length=16,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=15,
        item_number=13
    ),
    "1514": WITSSymbol(
        code="1514",
        name="L1CO",
        description="Lith 1 color",
        data_type=WITSDataType.ASCII,
        length=16,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=15,
        item_number=14
    ),
    "1515": WITSSymbol(
        code="1515",
        name="L1TX",
        description="Lith 1 texture",
        data_type=WITSDataType.ASCII,
        length=16,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=15,
        item_number=15
    ),
    "1516": WITSSymbol(
        code="1516",
        name="L1HD",
        description="Lith 1 hardness",
        data_type=WITSDataType.ASCII,
        length=16,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=15,
        item_number=16
    ),
    "1517": WITSSymbol(
        code="1517",
        name="L1SZ",
        description="Lith 1 grain size",
        data_type=WITSDataType.ASCII,
        length=16,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=15,
        item_number=17
    ),
    "1518": WITSSymbol(
        code="1518",
        name="L1RD",
        description="Lith 1 roundness",
        data_type=WITSDataType.ASCII,
        length=16,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=15,
        item_number=18
    ),
    "1519": WITSSymbol(
        code="1519",
        name="L1SO",
        description="Lith 1 sorting",
        data_type=WITSDataType.ASCII,
        length=16,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=15,
        item_number=19
    ),
    "1520": WITSSymbol(
        code="1520",
        name="L1MC",
        description="Lith 1 matrix/cement",
        data_type=WITSDataType.ASCII,
        length=16,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=15,
        item_number=20
    ),
    "1521": WITSSymbol(
        code="1521",
        name="L1AC",
        description="Lith 1 accessories",
        data_type=WITSDataType.ASCII,
        length=16,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=15,
        item_number=21
    ),
    "1522": WITSSymbol(
        code="1522",
        name="L1PO",
        description="Lith 1 porosity",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.PERCENT,
        fps_units=WITSUnits.PERCENT,
        record_type=15,
        item_number=22
    ),
    "1523": WITSSymbol(
        code="1523",
        name="L1PE",
        description="Lith 1 permeability",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=15,
        item_number=23
    ),
    "1524": WITSSymbol(
        code="1524",
        name="L2TY",
        description="Lith 2 type",
        data_type=WITSDataType.ASCII,
        length=16,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=15,
        item_number=24
    ),
    "1525": WITSSymbol(
        code="1525",
        name="L2PC",
        description="Lith 2 %",
        data_type=WITSDataType.INTEGER,
        length=2,
        metric_units=WITSUnits.PERCENT,
        fps_units=WITSUnits.PERCENT,
        record_type=15,
        item_number=25
    ),
    "1526": WITSSymbol(
        code="1526",
        name="L2CL",
        description="Lith 2 classification",
        data_type=WITSDataType.ASCII,
        length=16,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=15,
        item_number=26
    ),
    "1527": WITSSymbol(
        code="1527",
        name="L2CO",
        description="Lith 2 color",
        data_type=WITSDataType.ASCII,
        length=16,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=15,
        item_number=27
    ),
    "1528": WITSSymbol(
        code="1528",
        name="L2TX",
        description="Lith 2 texture",
        data_type=WITSDataType.ASCII,
        length=16,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=15,
        item_number=28
    ),
    "1529": WITSSymbol(
        code="1529",
        name="L2HD",
        description="Lith 2 hardness",
        data_type=WITSDataType.ASCII,
        length=16,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=15,
        item_number=29
    ),
    "1530": WITSSymbol(
        code="1530",
        name="L2SZ",
        description="Lith 2 grain size",
        data_type=WITSDataType.ASCII,
        length=16,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=15,
        item_number=30
    ),
    "1531": WITSSymbol(
        code="1531",
        name="L2RD",
        description="Lith 2 roundness",
        data_type=WITSDataType.ASCII,
        length=16,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=15,
        item_number=31
    ),
    "1532": WITSSymbol(
        code="1532",
        name="L2SO",
        description="Lith 2 sorting",
        data_type=WITSDataType.ASCII,
        length=16,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=15,
        item_number=32
    ),
    "1533": WITSSymbol(
        code="1533",
        name="L2MC",
        description="Lith 2 matrix/cement",
        data_type=WITSDataType.ASCII,
        length=16,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=15,
        item_number=33
    ),
    "1534": WITSSymbol(
        code="1534",
        name="L2AC",
        description="Lith 2 accessories",
        data_type=WITSDataType.ASCII,
        length=16,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=15,
        item_number=34
    ),
    "1535": WITSSymbol(
        code="1535",
        name="L2PO",
        description="Lith 2 porosity",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.PERCENT,
        fps_units=WITSUnits.PERCENT,
        record_type=15,
        item_number=35
    ),
    "1536": WITSSymbol(
        code="1536",
        name="L2PE",
        description="Lith 2 permeability",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=15,
        item_number=36
    ),
    "1537": WITSSymbol(
        code="1537",
        name="L3TY",
        description="Lith 3 type",
        data_type=WITSDataType.ASCII,
        length=16,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=15,
        item_number=37
    ),
    "1538": WITSSymbol(
        code="1538",
        name="L3PC",
        description="Lith 3 %",
        data_type=WITSDataType.INTEGER,
        length=2,
        metric_units=WITSUnits.PERCENT,
        fps_units=WITSUnits.PERCENT,
        record_type=15,
        item_number=38
    ),
    "1539": WITSSymbol(
        code="1539",
        name="L3CL",
        description="Lith 3 classification",
        data_type=WITSDataType.ASCII,
        length=16,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=15,
        item_number=39
    ),
    "1540": WITSSymbol(
        code="1540",
        name="L4TY",
        description="Lith 4 type",
        data_type=WITSDataType.ASCII,
        length=16,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=15,
        item_number=40
    ),
    "1541": WITSSymbol(
        code="1541",
        name="L4PC",
        description="Lith 4 %",
        data_type=WITSDataType.INTEGER,
        length=2,
        metric_units=WITSUnits.PERCENT,
        fps_units=WITSUnits.PERCENT,
        record_type=15,
        item_number=41
    ),
    "1542": WITSSymbol(
        code="1542",
        name="L4CL",
        description="Lith 4 classification",
        data_type=WITSDataType.ASCII,
        length=16,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=15,
        item_number=42
    ),
    "1543": WITSSymbol(
        code="1543",
        name="L5TY",
        description="Lith 5 type",
        data_type=WITSDataType.ASCII,
        length=16,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=15,
        item_number=43
    ),
    "1544": WITSSymbol(
        code="1544",
        name="L5PC",
        description="Lith 5 %",
        data_type=WITSDataType.INTEGER,
        length=2,
        metric_units=WITSUnits.PERCENT,
        fps_units=WITSUnits.PERCENT,
        record_type=15,
        item_number=44
    ),
    "1545": WITSSymbol(
        code="1545",
        name="L5CL",
        description="Lith 5 classification",
        data_type=WITSDataType.ASCII,
        length=16,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=15,
        item_number=45
    ),
    "1546": WITSSymbol(
        code="1546",
        name="FOSS",
        description="Fossils",
        data_type=WITSDataType.ASCII,
        length=16,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=15,
        item_number=46
    ),
    "1547": WITSSymbol(
        code="1547",
        name="SHOW",
        description="Composite Show",
        data_type=WITSDataType.ASCII,
        length=16,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=15,
        item_number=47
    ),
    "1548": WITSSymbol(
        code="1548",
        name="BDEN",
        description="Bulk Density",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=15,
        item_number=48
    ),
    "1549": WITSSymbol(
        code="1549",
        name="GCUT",
        description="Cuttings Gas",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.PERCENT,
        fps_units=WITSUnits.PERCENT,
        record_type=15,
        item_number=49
    ),
    "1550": WITSSymbol(
        code="1550",
        name="CCAL",
        description="Calcimetry Calcite %",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.PERCENT,
        fps_units=WITSUnits.PERCENT,
        record_type=15,
        item_number=50
    ),
    "1551": WITSSymbol(
        code="1551",
        name="CDOL",
        description="Calcimetry Dolomite %",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.PERCENT,
        fps_units=WITSUnits.PERCENT,
        record_type=15,
        item_number=51
    ),
    "1552": WITSSymbol(
        code="1552",
        name="CEC",
        description="Cuttings CEC",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=15,
        item_number=52
    ),
    "1553": WITSSymbol(
        code="1553",
        name="CAV",
        description="Cavings %",
        data_type=WITSDataType.INTEGER,
        length=2,
        metric_units=WITSUnits.PERCENT,
        fps_units=WITSUnits.PERCENT,
        record_type=15,
        item_number=53
    ),
    "1554": WITSSymbol(
        code="1554",
        name="SDEN",
        description="Shale Density",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=15,
        item_number=54
    ),
}

# WITS Record 16 symbols - Hydrocarbon Show
WITS_RECORD_16_SYMBOLS = {
    "1601": WITSSymbol(
        code="1601",
        name="WID",
        description="Well Identifier",
        data_type=WITSDataType.ASCII,
        length=16,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=16,
        item_number=1
    ),
    "1602": WITSSymbol(
        code="1602",
        name="SKNO",
        description="Sidetrack/Hole Sect No.",
        data_type=WITSDataType.INTEGER,
        length=2,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=16,
        item_number=2
    ),
    "1603": WITSSymbol(
        code="1603",
        name="RID",
        description="Record Identifier",
        data_type=WITSDataType.INTEGER,
        length=2,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=16,
        item_number=3
    ),
    "1604": WITSSymbol(
        code="1604",
        name="SQID",
        description="Sequence Identifier",
        data_type=WITSDataType.LONG,
        length=4,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=16,
        item_number=4
    ),
    "1605": WITSSymbol(
        code="1605",
        name="DATE",
        description="Date",
        data_type=WITSDataType.LONG,
        length=4,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=16,
        item_number=5
    ),
    "1606": WITSSymbol(
        code="1606",
        name="TIME",
        description="Time",
        data_type=WITSDataType.LONG,
        length=4,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=16,
        item_number=6
    ),
    "1607": WITSSymbol(
        code="1607",
        name="ACTC",
        description="Activity Code",
        data_type=WITSDataType.INTEGER,
        length=2,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=16,
        item_number=7
    ),
    "1608": WITSSymbol(
        code="1608",
        name="SWNO",
        description="Show Number",
        data_type=WITSDataType.INTEGER,
        length=2,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=16,
        item_number=8
    ),
    "1609": WITSSymbol(
        code="1609",
        name="DSTM",
        description="Show Intvl Top Depth (meas)",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.METERS,
        fps_units=WITSUnits.FEET,
        record_type=16,
        item_number=9
    ),
    "1610": WITSSymbol(
        code="1610",
        name="DSTV",
        description="Show Intvl Top Depth (vert)",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.METERS,
        fps_units=WITSUnits.FEET,
        record_type=16,
        item_number=10
    ),
    "1611": WITSSymbol(
        code="1611",
        name="DSBM",
        description="Show Intvl Bott Depth(meas)",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.METERS,
        fps_units=WITSUnits.FEET,
        record_type=16,
        item_number=11
    ),
    "1612": WITSSymbol(
        code="1612",
        name="DSBV",
        description="Show Intvl Bott Depth(vert)",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.METERS,
        fps_units=WITSUnits.FEET,
        record_type=16,
        item_number=12
    ),
    "1613": WITSSymbol(
        code="1613",
        name="WLTY",
        description="Show Lith type",
        data_type=WITSDataType.ASCII,
        length=16,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=16,
        item_number=13
    ),
    "1614": WITSSymbol(
        code="1614",
        name="WLCL",
        description="Show Lith classification",
        data_type=WITSDataType.ASCII,
        length=16,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=16,
        item_number=14
    ),
    "1615": WITSSymbol(
        code="1615",
        name="WLCO",
        description="Show Lith color",
        data_type=WITSDataType.ASCII,
        length=16,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=16,
        item_number=15
    ),
    "1616": WITSSymbol(
        code="1616",
        name="WLTX",
        description="Show Lith texture",
        data_type=WITSDataType.ASCII,
        length=16,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=16,
        item_number=16
    ),
    "1617": WITSSymbol(
        code="1617",
        name="WLHD",
        description="Show Lith hardness",
        data_type=WITSDataType.ASCII,
        length=16,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=16,
        item_number=17
    ),
    "1618": WITSSymbol(
        code="1618",
        name="WLSZ",
        description="Show Lith grain size",
        data_type=WITSDataType.ASCII,
        length=16,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=16,
        item_number=18
    ),
    "1619": WITSSymbol(
        code="1619",
        name="WLRD",
        description="Show Lith roundness",
        data_type=WITSDataType.ASCII,
        length=16,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=16,
        item_number=19
    ),
    "1620": WITSSymbol(
        code="1620",
        name="WLSO",
        description="Show Lith sorting",
        data_type=WITSDataType.ASCII,
        length=16,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=16,
        item_number=20
    ),
    "1621": WITSSymbol(
        code="1621",
        name="WLMC",
        description="Show Lith matrix/cement",
        data_type=WITSDataType.ASCII,
        length=16,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=16,
        item_number=21
    ),
    "1622": WITSSymbol(
        code="1622",
        name="WLAC",
        description="Show Lith accessories",
        data_type=WITSDataType.ASCII,
        length=16,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=16,
        item_number=22
    ),
    "1623": WITSSymbol(
        code="1623",
        name="WLPV",
        description="Show Lith porosity -visible",
        data_type=WITSDataType.ASCII,
        length=16,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=16,
        item_number=23
    ),
    "1624": WITSSymbol(
        code="1624",
        name="WLPM",
        description="Show Lith porosity -meas",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.PERCENT,
        fps_units=WITSUnits.PERCENT,
        record_type=16,
        item_number=24
    ),
    "1625": WITSSymbol(
        code="1625",
        name="WLPE",
        description="Show Lith permeability",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=16,
        item_number=25
    ),
    "1626": WITSSymbol(
        code="1626",
        name="WLST",
        description="Show Lith stain description",
        data_type=WITSDataType.ASCII,
        length=64,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=16,
        item_number=26
    ),
    "1627": WITSSymbol(
        code="1627",
        name="WLFL",
        description="Show Lith fluor description",
        data_type=WITSDataType.ASCII,
        length=64,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=16,
        item_number=27
    ),
    "1628": WITSSymbol(
        code="1628",
        name="WLCT",
        description="Show Lith cut description",
        data_type=WITSDataType.ASCII,
        length=64,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=16,
        item_number=28
    ),
    "1629": WITSSymbol(
        code="1629",
        name="WLGC",
        description="Show Lith cuttings gas",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.PERCENT,
        fps_units=WITSUnits.PERCENT,
        record_type=16,
        item_number=29
    ),
    "1630": WITSSymbol(
        code="1630",
        name="WSAL",
        description="Show titrated salinity",
        data_type=WITSDataType.LONG,
        length=4,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=16,
        item_number=30
    ),
    "1631": WITSSymbol(
        code="1631",
        name="MTHM",
        description="Show Mud Smple Methane",
        data_type=WITSDataType.LONG,
        length=4,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=16,
        item_number=31
    ),
    "1632": WITSSymbol(
        code="1632",
        name="ETHM",
        description="Show Mud Smple Ethane",
        data_type=WITSDataType.LONG,
        length=4,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=16,
        item_number=32
    ),
    "1633": WITSSymbol(
        code="1633",
        name="PRPM",
        description="Show Mud Smple Propane",
        data_type=WITSDataType.LONG,
        length=4,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=16,
        item_number=33
    ),
    "1634": WITSSymbol(
        code="1634",
        name="IBTM",
        description="Show Mud Smple I-Butane",
        data_type=WITSDataType.LONG,
        length=4,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=16,
        item_number=34
    ),
    "1635": WITSSymbol(
        code="1635",
        name="NBTM",
        description="Show Mud Smple N-Butane",
        data_type=WITSDataType.LONG,
        length=4,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=16,
        item_number=35
    ),
    "1636": WITSSymbol(
        code="1636",
        name="IPNM",
        description="Show Mud Smple I-Pentane",
        data_type=WITSDataType.LONG,
        length=4,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=16,
        item_number=36
    ),
    "1637": WITSSymbol(
        code="1637",
        name="NPNM",
        description="Show Mud Smple N-Pentane",
        data_type=WITSDataType.LONG,
        length=4,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=16,
        item_number=37
    ),
    "1638": WITSSymbol(
        code="1638",
        name="EPNM",
        description="Show Mud Smple N-Pentane",
        data_type=WITSDataType.LONG,
        length=4,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=16,
        item_number=38
    ),
    "1639": WITSSymbol(
        code="1639",
        name="IHXM",
        description="Show Mud Smple I-Hexane",
        data_type=WITSDataType.LONG,
        length=4,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=16,
        item_number=39
    ),
    "1640": WITSSymbol(
        code="1640",
        name="NHXM",
        description="Show Mud Smple N-Hexane",
        data_type=WITSDataType.LONG,
        length=4,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=16,
        item_number=40
    ),
    "1641": WITSSymbol(
        code="1641",
        name="WCOM",
        description="Show Comments",
        data_type=WITSDataType.ASCII,
        length=128,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=16,
        item_number=41
    ),
}

# WITS Record 17 symbols - Cementing
WITS_RECORD_17_SYMBOLS = {
    "1701": WITSSymbol(
        code="1701",
        name="WID",
        description="Well Identifier",
        data_type=WITSDataType.ASCII,
        length=16,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=17,
        item_number=1
    ),
    "1702": WITSSymbol(
        code="1702",
        name="SKNO",
        description="Sidetrack/Hole Sect No.",
        data_type=WITSDataType.INTEGER,
        length=2,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=17,
        item_number=2
    ),
    "1703": WITSSymbol(
        code="1703",
        name="RID",
        description="Record Identifier",
        data_type=WITSDataType.INTEGER,
        length=2,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=17,
        item_number=3
    ),
    "1704": WITSSymbol(
        code="1704",
        name="SQID",
        description="Sequence Identifier",
        data_type=WITSDataType.LONG,
        length=4,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=17,
        item_number=4
    ),
    "1705": WITSSymbol(
        code="1705",
        name="DATE",
        description="Date",
        data_type=WITSDataType.LONG,
        length=4,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=17,
        item_number=5
    ),
    "1706": WITSSymbol(
        code="1706",
        name="TIME",
        description="Time",
        data_type=WITSDataType.LONG,
        length=4,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=17,
        item_number=6
    ),
    "1707": WITSSymbol(
        code="1707",
        name="ACTC",
        description="Activity Code",
        data_type=WITSDataType.INTEGER,
        length=2,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=17,
        item_number=7
    ),
    "1708": WITSSymbol(
        code="1708",
        name="DMEA",
        description="Depth Hole (meas)",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.METERS,
        fps_units=WITSUnits.FEET,
        record_type=17,
        item_number=8
    ),
    "1709": WITSSymbol(
        code="1709",
        name="DVER",
        description="Depth Hole (vert)",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.METERS,
        fps_units=WITSUnits.FEET,
        record_type=17,
        item_number=9
    ),
    "1710": WITSSymbol(
        code="1710",
        name="DCGM",
        description="Depth Casing Shoe (meas)",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.METERS,
        fps_units=WITSUnits.FEET,
        record_type=17,
        item_number=10
    ),
    "1711": WITSSymbol(
        code="1711",
        name="DCGV",
        description="Depth Casing Shoe (vert)",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.METERS,
        fps_units=WITSUnits.FEET,
        record_type=17,
        item_number=11
    ),
    "1712": WITSSymbol(
        code="1712",
        name="CPPA",
        description="Cem Pump Pressure (avg)",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.KPA,
        fps_units=WITSUnits.PSI,
        record_type=17,
        item_number=12
    ),
    "1713": WITSSymbol(
        code="1713",
        name="HKLA",
        description="Hookload (avg)",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.KDN,
        fps_units=WITSUnits.KLB,
        record_type=17,
        item_number=13
    ),
    "1714": WITSSymbol(
        code="1714",
        name="BPOS",
        description="Block Position",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.METERS,
        fps_units=WITSUnits.FEET,
        record_type=17,
        item_number=14
    ),
    "1715": WITSSymbol(
        code="1715",
        name="CFIC",
        description="Cem Flow Rate In (calc)",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=17,
        item_number=15
    ),
    "1716": WITSSymbol(
        code="1716",
        name="CFIA",
        description="Cem Flow Rate In (avg)",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=17,
        item_number=16
    ),
    "1717": WITSSymbol(
        code="1717",
        name="CFOA",
        description="Cem Flow Rate Out (avg)",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=17,
        item_number=17
    ),
    "1718": WITSSymbol(
        code="1718",
        name="CFOP",
        description="Cem Flow Out %",
        data_type=WITSDataType.INTEGER,
        length=2,
        metric_units=WITSUnits.PERCENT,
        fps_units=WITSUnits.PERCENT,
        record_type=17,
        item_number=18
    ),
    "1719": WITSSymbol(
        code="1719",
        name="CDIA",
        description="Cem Fluid Dens In (avg)",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.KGM3,
        fps_units=WITSUnits.PPG,
        record_type=17,
        item_number=19
    ),
    "1720": WITSSymbol(
        code="1720",
        name="CDOA",
        description="Cem Fluid Dens Out (avg)",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.KGM3,
        fps_units=WITSUnits.PPG,
        record_type=17,
        item_number=20
    ),
    "1721": WITSSymbol(
        code="1721",
        name="ECDC",
        description="ECD at Casing Shoe",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.KGM3,
        fps_units=WITSUnits.PPG,
        record_type=17,
        item_number=21
    ),
    "1722": WITSSymbol(
        code="1722",
        name="CTIA",
        description="Cem Fluid Temp In (avg)",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.DEGC,
        fps_units=WITSUnits.DEGF,
        record_type=17,
        item_number=22
    ),
    "1723": WITSSymbol(
        code="1723",
        name="CTOA",
        description="Cem Fluid Temp Out (avg)",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.DEGC,
        fps_units=WITSUnits.DEGF,
        record_type=17,
        item_number=23
    ),
    "1724": WITSSymbol(
        code="1724",
        name="CSTG",
        description="Cem Stage Number",
        data_type=WITSDataType.INTEGER,
        length=2,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=17,
        item_number=24
    ),
    "1725": WITSSymbol(
        code="1725",
        name="DDVT",
        description="Cem Depth to DV Tool",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.METERS,
        fps_units=WITSUnits.FEET,
        record_type=17,
        item_number=25
    ),
    "1726": WITSSymbol(
        code="1726",
        name="CTYP",
        description="Cem Fluid Type/Batch",
        data_type=WITSDataType.ASCII,
        length=16,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=17,
        item_number=26
    ),
    "1727": WITSSymbol(
        code="1727",
        name="CCRT",
        description="Cem Cumulative Returns",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.M3,
        fps_units=WITSUnits.BBL,
        record_type=17,
        item_number=27
    ),
    "1728": WITSSymbol(
        code="1728",
        name="CIVL",
        description="Cem Indiv Vol Pumped",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.M3,
        fps_units=WITSUnits.BBL,
        record_type=17,
        item_number=28
    ),
    "1729": WITSSymbol(
        code="1729",
        name="CCVL",
        description="Cem Cement Vol Pumped",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.M3,
        fps_units=WITSUnits.BBL,
        record_type=17,
        item_number=29
    ),
    "1730": WITSSymbol(
        code="1730",
        name="CTVL",
        description="Cem Total Vol Pumped",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.M3,
        fps_units=WITSUnits.BBL,
        record_type=17,
        item_number=30
    ),
    "1731": WITSSymbol(
        code="1731",
        name="CBVL",
        description="Cem Volume to Bump Plug",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.M3,
        fps_units=WITSUnits.BBL,
        record_type=17,
        item_number=31
    ),
    "1732": WITSSymbol(
        code="1732",
        name="CPLG",
        description="Cem No./Status of Plug(s)",
        data_type=WITSDataType.ASCII,
        length=8,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=17,
        item_number=32
    ),
    "1733": WITSSymbol(
        code="1733",
        name="CJTY",
        description="Cem Job Type",
        data_type=WITSDataType.ASCII,
        length=16,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=17,
        item_number=33
    ),
}

# WITS Record 18 symbols - Drill Stem Testing
WITS_RECORD_18_SYMBOLS = {
    "1801": WITSSymbol(
        code="1801",
        name="WID",
        description="Well Identifier",
        data_type=WITSDataType.ASCII,
        length=16,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=18,
        item_number=1
    ),
    "1802": WITSSymbol(
        code="1802",
        name="SKNO",
        description="Sidetrack/Hole Sect No.",
        data_type=WITSDataType.INTEGER,
        length=2,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=18,
        item_number=2
    ),
    "1803": WITSSymbol(
        code="1803",
        name="RID",
        description="Record Identifier",
        data_type=WITSDataType.INTEGER,
        length=2,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=18,
        item_number=3
    ),
    "1804": WITSSymbol(
        code="1804",
        name="SQID",
        description="Sequence Identifier",
        data_type=WITSDataType.LONG,
        length=4,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=18,
        item_number=4
    ),
    "1805": WITSSymbol(
        code="1805",
        name="DATE",
        description="Date",
        data_type=WITSDataType.LONG,
        length=4,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=18,
        item_number=5
    ),
    "1806": WITSSymbol(
        code="1806",
        name="TIME",
        description="Time",
        data_type=WITSDataType.LONG,
        length=4,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=18,
        item_number=6
    ),
    "1807": WITSSymbol(
        code="1807",
        name="ACTC",
        description="Activity Code",
        data_type=WITSDataType.INTEGER,
        length=2,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=18,
        item_number=7
    ),
    "1808": WITSSymbol(
        code="1808",
        name="DSID",
        description="DST identification",
        data_type=WITSDataType.ASCII,
        length=8,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=18,
        item_number=8
    ),
    "1809": WITSSymbol(
        code="1809",
        name="DDTM",
        description="DST Intvl Top Depth (meas)",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.METERS,
        fps_units=WITSUnits.FEET,
        record_type=18,
        item_number=9
    ),
    "1810": WITSSymbol(
        code="1810",
        name="DDTV",
        description="DST Intvl Top Depth (vert)",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.METERS,
        fps_units=WITSUnits.FEET,
        record_type=18,
        item_number=10
    ),
    "1811": WITSSymbol(
        code="1811",
        name="DDBM",
        description="DST Intvl Bott Depth (meas)",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.METERS,
        fps_units=WITSUnits.FEET,
        record_type=18,
        item_number=11
    ),
    "1812": WITSSymbol(
        code="1812",
        name="DDBV",
        description="DST Intvl Bott Depth (vert)",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.METERS,
        fps_units=WITSUnits.FEET,
        record_type=18,
        item_number=12
    ),
    "1813": WITSSymbol(
        code="1813",
        name="DTTI",
        description="DST Tool Time",
        data_type=WITSDataType.LONG,
        length=4,
        metric_units=WITSUnits.HR,
        fps_units=WITSUnits.HR,
        record_type=18,
        item_number=13
    ),
    "1814": WITSSymbol(
        code="1814",
        name="DSTA",
        description="DST State of Well",
        data_type=WITSDataType.INTEGER,
        length=2,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=18,
        item_number=14
    ),
    "1815": WITSSymbol(
        code="1815",
        name="DSPT",
        description="DST Surf Pressure, Tubing",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.KPA,
        fps_units=WITSUnits.PSI,
        record_type=18,
        item_number=15
    ),
    "1816": WITSSymbol(
        code="1816",
        name="DSPC",
        description="DST Surf Pressure, Casing",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.KPA,
        fps_units=WITSUnits.PSI,
        record_type=18,
        item_number=16
    ),
    "1817": WITSSymbol(
        code="1817",
        name="DSTT",
        description="DST Surf Temp, Tubing",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.DEGC,
        fps_units=WITSUnits.DEGF,
        record_type=18,
        item_number=17
    ),
    "1818": WITSSymbol(
        code="1818",
        name="DBHP",
        description="DST Bottom Hole Pressure",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.KPA,
        fps_units=WITSUnits.PSI,
        record_type=18,
        item_number=18
    ),
    "1819": WITSSymbol(
        code="1819",
        name="DBHT",
        description="DST Bottom Hole Temp",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.DEGC,
        fps_units=WITSUnits.DEGF,
        record_type=18,
        item_number=19
    ),
    "1820": WITSSymbol(
        code="1820",
        name="DLFR",
        description="DST Liquid Flow Rate",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=18,
        item_number=20
    ),
    "1821": WITSSymbol(
        code="1821",
        name="DGFR",
        description="DST Gas Flow Rate",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=18,
        item_number=21
    ),
    "1822": WITSSymbol(
        code="1822",
        name="DTFR",
        description="DST Total Flow Rate",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=18,
        item_number=22
    ),
    "1823": WITSSymbol(
        code="1823",
        name="DCLP",
        description="DST Cum Liquid Production",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.M3,
        fps_units=WITSUnits.BBL,
        record_type=18,
        item_number=23
    ),
    "1824": WITSSymbol(
        code="1824",
        name="DCGP",
        description="DST Cum Gas Production",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=18,
        item_number=24
    ),
    "1825": WITSSymbol(
        code="1825",
        name="DCTP",
        description="DST Cum Total Production",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.M3,
        fps_units=WITSUnits.BBL,
        record_type=18,
        item_number=25
    ),
    "1826": WITSSymbol(
        code="1826",
        name="HSA",
        description="Hydrogen Sulfide (avg)",
        data_type=WITSDataType.LONG,
        length=4,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=18,
        item_number=26
    ),
}

# WITS Record 19 symbols - Configuration
WITS_RECORD_19_SYMBOLS = {
    "1901": WITSSymbol(
        code="1901",
        name="WID",
        description="Well Identifier",
        data_type=WITSDataType.ASCII,
        length=16,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=19,
        item_number=1
    ),
    "1902": WITSSymbol(
        code="1902",
        name="SKNO",
        description="Sidetrack/Hole Sect No.",
        data_type=WITSDataType.INTEGER,
        length=2,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=19,
        item_number=2
    ),
    "1903": WITSSymbol(
        code="1903",
        name="RID",
        description="Record Identifier",
        data_type=WITSDataType.INTEGER,
        length=2,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=19,
        item_number=3
    ),
    "1904": WITSSymbol(
        code="1904",
        name="SQID",
        description="Sequence Identifier",
        data_type=WITSDataType.LONG,
        length=4,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=19,
        item_number=4
    ),
    "1905": WITSSymbol(
        code="1905",
        name="DATE",
        description="Date",
        data_type=WITSDataType.LONG,
        length=4,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=19,
        item_number=5
    ),
    "1906": WITSSymbol(
        code="1906",
        name="TIME",
        description="Time",
        data_type=WITSDataType.LONG,
        length=4,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=19,
        item_number=6
    ),
    "1907": WITSSymbol(
        code="1907",
        name="ACTC",
        description="Activity Code",
        data_type=WITSDataType.INTEGER,
        length=2,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=19,
        item_number=7
    ),
    "1908": WITSSymbol(
        code="1908",
        name="DMEA",
        description="Depth Hole (meas)",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.METERS,
        fps_units=WITSUnits.FEET,
        record_type=19,
        item_number=8
    ),
    "1909": WITSSymbol(
        code="1909",
        name="DVER",
        description="Depth Hole (vert)",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.METERS,
        fps_units=WITSUnits.FEET,
        record_type=19,
        item_number=9
    ),
    "1910": WITSSymbol(
        code="1910",
        name="DSNO",
        description="No. Drill String Sections",
        data_type=WITSDataType.INTEGER,
        length=2,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=19,
        item_number=10
    ),
    "1911": WITSSymbol(
        code="1911",
        name="D1OD",
        description="DS Section 1 OD",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=19,
        item_number=11
    ),
    "1912": WITSSymbol(
        code="1912",
        name="D1ID",
        description="DS Section 1 ID",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=19,
        item_number=12
    ),
    "1913": WITSSymbol(
        code="1913",
        name="D1JI",
        description="DS Section 1 Tool Joint ID",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=19,
        item_number=13
    ),
    "1914": WITSSymbol(
        code="1914",
        name="D1JO",
        description="DS Section 1 Tool Joint OD",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=19,
        item_number=14
    ),
    "1915": WITSSymbol(
        code="1915",
        name="D1MA",
        description="DS Section 1 Mass/Length",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=19,
        item_number=15
    ),
    "1916": WITSSymbol(
        code="1916",
        name="D1LE",
        description="DS Section 1 Length",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.METERS,
        fps_units=WITSUnits.FEET,
        record_type=19,
        item_number=16
    ),
    "1917": WITSSymbol(
        code="1917",
        name="D2OD",
        description="DS Section 2 OD",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=19,
        item_number=17
    ),
    "1918": WITSSymbol(
        code="1918",
        name="D2ID",
        description="DS Section 2 ID",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=19,
        item_number=18
    ),
    "1919": WITSSymbol(
        code="1919",
        name="D2JI",
        description="DS Section 2 Tool Joint ID",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=19,
        item_number=19
    ),
    "1920": WITSSymbol(
        code="1920",
        name="D2JO",
        description="DS Section 2 Tool Joint OD",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=19,
        item_number=20
    ),
    "1921": WITSSymbol(
        code="1921",
        name="D2MA",
        description="DS Section 2 Mass/Length",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=19,
        item_number=21
    ),
    "1922": WITSSymbol(
        code="1922",
        name="D2LE",
        description="DS Section 2 Length",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.METERS,
        fps_units=WITSUnits.FEET,
        record_type=19,
        item_number=22
    ),
    "1923": WITSSymbol(
        code="1923",
        name="D3OD",
        description="DS Section 3 OD",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=19,
        item_number=23
    ),
    "1924": WITSSymbol(
        code="1924",
        name="D3ID",
        description="DS Section 3 ID",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=19,
        item_number=24
    ),
    "1925": WITSSymbol(
        code="1925",
        name="D3JI",
        description="DS Section 3 Tool Joint ID",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=19,
        item_number=25
    ),
    "1926": WITSSymbol(
        code="1926",
        name="D3JO",
        description="DS Section 3 Tool Joint OD",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=19,
        item_number=26
    ),
    "1927": WITSSymbol(
        code="1927",
        name="D3MA",
        description="DS Section 3 Mass/Length",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=19,
        item_number=27
    ),
    "1928": WITSSymbol(
        code="1928",
        name="D3LE",
        description="DS Section 3 Length",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.METERS,
        fps_units=WITSUnits.FEET,
        record_type=19,
        item_number=28
    ),
    "1929": WITSSymbol(
        code="1929",
        name="D4OD",
        description="DS Section 4 OD",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=19,
        item_number=29
    ),
    "1930": WITSSymbol(
        code="1930",
        name="D4ID",
        description="DS Section 4 ID",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=19,
        item_number=30
    ),
    "1931": WITSSymbol(
        code="1931",
        name="D4JI",
        description="DS Section 4 Tool Joint ID",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=19,
        item_number=31
    ),
    "1932": WITSSymbol(
        code="1932",
        name="D4JO",
        description="DS Section 4 Tool Joint OD",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=19,
        item_number=32
    ),
    "1933": WITSSymbol(
        code="1933",
        name="D4MA",
        description="DS Section 4 Mass/Length",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=19,
        item_number=33
    ),
    "1934": WITSSymbol(
        code="1934",
        name="D4LE",
        description="DS Section 4 Length",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.METERS,
        fps_units=WITSUnits.FEET,
        record_type=19,
        item_number=34
    ),
    "1935": WITSSymbol(
        code="1935",
        name="D5OD",
        description="DS Section 5 OD",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=19,
        item_number=35
    ),
    "1936": WITSSymbol(
        code="1936",
        name="D5ID",
        description="DS Section 5 ID",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=19,
        item_number=36
    ),
    "1937": WITSSymbol(
        code="1937",
        name="D5JI",
        description="DS Section 5 Tool Joint ID",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=19,
        item_number=37
    ),
    "1938": WITSSymbol(
        code="1938",
        name="D5JO",
        description="DS Section 5 Tool Joint OD",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=19,
        item_number=38
    ),
    "1939": WITSSymbol(
        code="1939",
        name="D5MA",
        description="DS Section 5 Mass/Length",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=19,
        item_number=39
    ),
    "1940": WITSSymbol(
        code="1940",
        name="D5LE",
        description="DS Section 5 Length",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.METERS,
        fps_units=WITSUnits.FEET,
        record_type=19,
        item_number=40
    ),
    "1941": WITSSymbol(
        code="1941",
        name="D6OD",
        description="DS Section 6 OD",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=19,
        item_number=41
    ),
    "1942": WITSSymbol(
        code="1942",
        name="D6ID",
        description="DS Section 6 ID",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=19,
        item_number=42
    ),
    "1943": WITSSymbol(
        code="1943",
        name="D6JI",
        description="DS Section 6 Tool Joint ID",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=19,
        item_number=43
    ),
    "1944": WITSSymbol(
        code="1944",
        name="D6JO",
        description="DS Section 6 Tool Joint OD",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=19,
        item_number=44
    ),
    "1945": WITSSymbol(
        code="1945",
        name="D6MA",
        description="DS Section 6 Mass/Length",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=19,
        item_number=45
    ),
    "1946": WITSSymbol(
        code="1946",
        name="KID",
        description="Kelly ID",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=19,
        item_number=46
    ),
    "1947": WITSSymbol(
        code="1947",
        name="KLEN",
        description="Kelly Length",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.METERS,
        fps_units=WITSUnits.FEET,
        record_type=19,
        item_number=47
    ),
    "1948": WITSSymbol(
        code="1948",
        name="SLEN",
        description="Drill Pipe Stand Length",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.METERS,
        fps_units=WITSUnits.FEET,
        record_type=19,
        item_number=48
    ),
    "1949": WITSSymbol(
        code="1949",
        name="SJNT",
        description="No. Joints/Stand",
        data_type=WITSDataType.INTEGER,
        length=2,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=19,
        item_number=49
    ),
    "1950": WITSSymbol(
        code="1950",
        name="HLNO",
        description="No. Hole Sections",
        data_type=WITSDataType.INTEGER,
        length=2,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=19,
        item_number=50
    ),
    "1951": WITSSymbol(
        code="1951",
        name="H1DI",
        description="Hole Section 1 Diam",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=19,
        item_number=51
    ),
    "1952": WITSSymbol(
        code="1952",
        name="H1LE",
        description="Hole Section 1 Length",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.METERS,
        fps_units=WITSUnits.FEET,
        record_type=19,
        item_number=52
    ),
    "1953": WITSSymbol(
        code="1953",
        name="H2DI",
        description="Hole Section 2 Diam",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=19,
        item_number=53
    ),
    "1954": WITSSymbol(
        code="1954",
        name="H2LE",
        description="Hole Section 2 Length",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.METERS,
        fps_units=WITSUnits.FEET,
        record_type=19,
        item_number=54
    ),
    "1955": WITSSymbol(
        code="1955",
        name="H3DI",
        description="Hole Section 3 Diam",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=19,
        item_number=55
    ),
    "1956": WITSSymbol(
        code="1956",
        name="H3LE",
        description="Hole Section 3 Length",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.METERS,
        fps_units=WITSUnits.FEET,
        record_type=19,
        item_number=56
    ),
    "1957": WITSSymbol(
        code="1957",
        name="H4DI",
        description="Hole Section 4 Diam",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=19,
        item_number=57
    ),
    "1958": WITSSymbol(
        code="1958",
        name="H4LE",
        description="Hole Section 4 Length",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.METERS,
        fps_units=WITSUnits.FEET,
        record_type=19,
        item_number=58
    ),
    "1959": WITSSymbol(
        code="1959",
        name="H5DI",
        description="Hole Section 5 Diam",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=19,
        item_number=59
    ),
    "1960": WITSSymbol(
        code="1960",
        name="P1CA",
        description="Pump 1 Capacity",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=19,
        item_number=60
    ),
    "1961": WITSSymbol(
        code="1961",
        name="P1EF",
        description="Pump 1 Efficiency",
        data_type=WITSDataType.INTEGER,
        length=2,
        metric_units=WITSUnits.PERCENT,
        fps_units=WITSUnits.PERCENT,
        record_type=19,
        item_number=61
    ),
    "1962": WITSSymbol(
        code="1962",
        name="P2CA",
        description="Pump 2 Capacity",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=19,
        item_number=62
    ),
    "1963": WITSSymbol(
        code="1963",
        name="P2EF",
        description="Pump 2 Efficiency",
        data_type=WITSDataType.INTEGER,
        length=2,
        metric_units=WITSUnits.PERCENT,
        fps_units=WITSUnits.PERCENT,
        record_type=19,
        item_number=63
    ),
    "1964": WITSSymbol(
        code="1964",
        name="P3CA",
        description="Pump 3 Capacity",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=19,
        item_number=64
    ),
    "1965": WITSSymbol(
        code="1965",
        name="P3EF",
        description="Pump 3 Efficiency",
        data_type=WITSDataType.INTEGER,
        length=2,
        metric_units=WITSUnits.PERCENT,
        fps_units=WITSUnits.PERCENT,
        record_type=19,
        item_number=65
    ),
    "1966": WITSSymbol(
        code="1966",
        name="RIGC",
        description="Rig Operating Cost/Hour",
        data_type=WITSDataType.INTEGER,
        length=2,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=19,
        item_number=66
    ),
    "1967": WITSSymbol(
        code="1967",
        name="TRRT",
        description="Trip Rate (Dist/Time)",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=19,
        item_number=67
    ),
    "1968": WITSSymbol(
        code="1968",
        name="KLID",
        description="Kill Line ID",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=19,
        item_number=68
    ),
    "1969": WITSSymbol(
        code="1969",
        name="KLJD",
        description="Kill Line Joint ID",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=19,
        item_number=69
    ),
    "1970": WITSSymbol(
        code="1970",
        name="KLJF",
        description="Kill Line Joint Fraction",
        data_type=WITSDataType.INTEGER,
        length=2,
        metric_units=WITSUnits.PERCENT,
        fps_units=WITSUnits.PERCENT,
        record_type=19,
        item_number=70
    ),
    "1971": WITSSymbol(
        code="1971",
        name="KLLE",
        description="Kill Line Length",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.METERS,
        fps_units=WITSUnits.FEET,
        record_type=19,
        item_number=71
    ),
    "1972": WITSSymbol(
        code="1972",
        name="CHID",
        description="Choke Line ID",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=19,
        item_number=72
    ),
    "1973": WITSSymbol(
        code="1973",
        name="CHJD",
        description="Choke Line Joint ID",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=19,
        item_number=73
    ),
    "1974": WITSSymbol(
        code="1974",
        name="CHJF",
        description="Choke Line Joint Fraction",
        data_type=WITSDataType.INTEGER,
        length=2,
        metric_units=WITSUnits.PERCENT,
        fps_units=WITSUnits.PERCENT,
        record_type=19,
        item_number=74
    ),
    "1975": WITSSymbol(
        code="1975",
        name="CHLE",
        description="Choke Line Length",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.METERS,
        fps_units=WITSUnits.FEET,
        record_type=19,
        item_number=75
    ),
    "1976": WITSSymbol(
        code="1976",
        name="DCGM",
        description="Depth Casing Shoe (meas)",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.METERS,
        fps_units=WITSUnits.FEET,
        record_type=19,
        item_number=76
    ),
    "1977": WITSSymbol(
        code="1977",
        name="DCGV",
        description="Depth Casing Shoe (vert)",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.METERS,
        fps_units=WITSUnits.FEET,
        record_type=19,
        item_number=77
    ),
    "1978": WITSSymbol(
        code="1978",
        name="DPTM",
        description="Depth PIT (meas)",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.METERS,
        fps_units=WITSUnits.FEET,
        record_type=19,
        item_number=78
    ),
    "1979": WITSSymbol(
        code="1979",
        name="DPTV",
        description="Depth PIT (vert)",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.METERS,
        fps_units=WITSUnits.FEET,
        record_type=19,
        item_number=79
    ),
    "1980": WITSSymbol(
        code="1980",
        name="FPIT",
        description="Frac Pressure Grad at PIT",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.KGM3,
        fps_units=WITSUnits.PPG,
        record_type=19,
        item_number=80
    ),
    "1981": WITSSymbol(
        code="1981",
        name="CONT",
        description="Drilling Contractor",
        data_type=WITSDataType.ASCII,
        length=16,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=19,
        item_number=81
    ),
    "1982": WITSSymbol(
        code="1982",
        name="RIG",
        description="Rig Name",
        data_type=WITSDataType.ASCII,
        length=16,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=19,
        item_number=82
    ),
    "1983": WITSSymbol(
        code="1983",
        name="RTYP",
        description="Rig Type",
        data_type=WITSDataType.ASCII,
        length=16,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=19,
        item_number=83
    ),
    "1984": WITSSymbol(
        code="1984",
        name="VEN1",
        description="Vendor 1 Name/Service",
        data_type=WITSDataType.ASCII,
        length=32,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=19,
        item_number=84
    ),
    "1985": WITSSymbol(
        code="1985",
        name="VEN2",
        description="Vendor 2 Name/Service",
        data_type=WITSDataType.ASCII,
        length=32,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=19,
        item_number=85
    ),
    "1986": WITSSymbol(
        code="1986",
        name="VEN3",
        description="Vendor 3 Name/Service",
        data_type=WITSDataType.ASCII,
        length=32,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=19,
        item_number=86
    ),
    "1987": WITSSymbol(
        code="1987",
        name="VEN4",
        description="Vendor 4 Name/Service",
        data_type=WITSDataType.ASCII,
        length=32,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=19,
        item_number=87
    ),
    "1988": WITSSymbol(
        code="1988",
        name="VEN5",
        description="Vendor 5 Name/Service",
        data_type=WITSDataType.ASCII,
        length=32,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=19,
        item_number=88
    ),
    "1989": WITSSymbol(
        code="1989",
        name="VEN6",
        description="Vendor 6 Name/Service",
        data_type=WITSDataType.ASCII,
        length=32,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=19,
        item_number=89
    ),
}

# WITS Record 20 symbols - Mud Report
WITS_RECORD_20_SYMBOLS = {
    "2001": WITSSymbol(
        code="2001",
        name="WID",
        description="Well Identifier",
        data_type=WITSDataType.ASCII,
        length=16,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=20,
        item_number=1
    ),
    "2002": WITSSymbol(
        code="2002",
        name="SKNO",
        description="Sidetrack/Hole Sect No.",
        data_type=WITSDataType.INTEGER,
        length=2,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=20,
        item_number=2
    ),
    "2003": WITSSymbol(
        code="2003",
        name="RID",
        description="Record Identifier",
        data_type=WITSDataType.INTEGER,
        length=2,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=20,
        item_number=3
    ),
    "2004": WITSSymbol(
        code="2004",
        name="SQID",
        description="Sequence Identifier",
        data_type=WITSDataType.LONG,
        length=4,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=20,
        item_number=4
    ),
    "2005": WITSSymbol(
        code="2005",
        name="DATE",
        description="Date",
        data_type=WITSDataType.LONG,
        length=4,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=20,
        item_number=5
    ),
    "2006": WITSSymbol(
        code="2006",
        name="TIME",
        description="Time",
        data_type=WITSDataType.LONG,
        length=4,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=20,
        item_number=6
    ),
    "2007": WITSSymbol(
        code="2007",
        name="ACTC",
        description="Activity Code",
        data_type=WITSDataType.INTEGER,
        length=2,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=20,
        item_number=7
    ),
    "2008": WITSSymbol(
        code="2008",
        name="MRDM",
        description="Mud Rept Depth (meas)",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.METERS,
        fps_units=WITSUnits.FEET,
        record_type=20,
        item_number=8
    ),
    "2009": WITSSymbol(
        code="2009",
        name="MRDV",
        description="Mud Rept Depth (vert)",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.METERS,
        fps_units=WITSUnits.FEET,
        record_type=20,
        item_number=9
    ),
    "2010": WITSSymbol(
        code="2010",
        name="MNUM",
        description="Mud Rept Number",
        data_type=WITSDataType.INTEGER,
        length=2,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=20,
        item_number=10
    ),
    "2011": WITSSymbol(
        code="2011",
        name="MTYP",
        description="Mud Rept Mud Type",
        data_type=WITSDataType.ASCII,
        length=16,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=20,
        item_number=11
    ),
    "2012": WITSSymbol(
        code="2012",
        name="MLOC",
        description="Mud Rept Sample Location",
        data_type=WITSDataType.ASCII,
        length=8,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=20,
        item_number=12
    ),
    "2013": WITSSymbol(
        code="2013",
        name="MDAT",
        description="Mud Rept Sample Date",
        data_type=WITSDataType.LONG,
        length=4,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=20,
        item_number=13
    ),
    "2014": WITSSymbol(
        code="2014",
        name="MTIM",
        description="Mud Rept Sample Time",
        data_type=WITSDataType.LONG,
        length=4,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=20,
        item_number=14
    ),
    "2015": WITSSymbol(
        code="2015",
        name="MDEN",
        description="Mud Rept Mud Density",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.KGM3,
        fps_units=WITSUnits.PPG,
        record_type=20,
        item_number=15
    ),
    "2016": WITSSymbol(
        code="2016",
        name="MFV",
        description="Mud Rept Funnel Vis",
        data_type=WITSDataType.INTEGER,
        length=2,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=20,
        item_number=16
    ),
    "2017": WITSSymbol(
        code="2017",
        name="MFVT",
        description="Mud Rept Funnel Vis Temp",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.DEGC,
        fps_units=WITSUnits.DEGF,
        record_type=20,
        item_number=17
    ),
    "2018": WITSSymbol(
        code="2018",
        name="MPV",
        description="Mud Rept Plastic Vis",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=20,
        item_number=18
    ),
    "2019": WITSSymbol(
        code="2019",
        name="MYP",
        description="Mud Rept Yield Point",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=20,
        item_number=19
    ),
    "2020": WITSSymbol(
        code="2020",
        name="MGL1",
        description="Mud Rept Gel - 10 sec",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=20,
        item_number=20
    ),
    "2021": WITSSymbol(
        code="2021",
        name="MGL2",
        description="Mud Rept Gel - 10 min",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=20,
        item_number=21
    ),
    "2022": WITSSymbol(
        code="2022",
        name="MGL3",
        description="Mud Rept Gel - 30 min",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=20,
        item_number=22
    ),
    "2023": WITSSymbol(
        code="2023",
        name="MFIL",
        description="Mud Rept Filtrate",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=20,
        item_number=23
    ),
    "2024": WITSSymbol(
        code="2024",
        name="MCAK",
        description="Mud Rept Filter Cake",
        data_type=WITSDataType.INTEGER,
        length=2,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=20,
        item_number=24
    ),
    "2025": WITSSymbol(
        code="2025",
        name="MHT",
        description="Mud Rept HTHP Temp",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.DEGC,
        fps_units=WITSUnits.DEGF,
        record_type=20,
        item_number=25
    ),
    "2026": WITSSymbol(
        code="2026",
        name="MHP",
        description="Mud Rept HTHP Pressure",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.KPA,
        fps_units=WITSUnits.PSI,
        record_type=20,
        item_number=26
    ),
    "2027": WITSSymbol(
        code="2027",
        name="MHFI",
        description="Mud Rept HTHP Filtrate",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=20,
        item_number=27
    ),
    "2028": WITSSymbol(
        code="2028",
        name="MHCK",
        description="Mud Rept HTHP Filter Cake",
        data_type=WITSDataType.INTEGER,
        length=2,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=20,
        item_number=28
    ),
    "2029": WITSSymbol(
        code="2029",
        name="MSOL",
        description="Mud Rept Solids % (retort)",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.PERCENT,
        fps_units=WITSUnits.PERCENT,
        record_type=20,
        item_number=29
    ),
    "2030": WITSSymbol(
        code="2030",
        name="MWAT",
        description="Mud Rept Water % (retort)",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.PERCENT,
        fps_units=WITSUnits.PERCENT,
        record_type=20,
        item_number=30
    ),
    "2031": WITSSymbol(
        code="2031",
        name="MOIL",
        description="Mud Rept Oil % (retort)",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.PERCENT,
        fps_units=WITSUnits.PERCENT,
        record_type=20,
        item_number=31
    ),
    "2032": WITSSymbol(
        code="2032",
        name="MSAN",
        description="Mud Rept Sand %",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.PERCENT,
        fps_units=WITSUnits.PERCENT,
        record_type=20,
        item_number=32
    ),
    "2033": WITSSymbol(
        code="2033",
        name="MLGS",
        description="Mud Rept Low Grav Sol %",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.PERCENT,
        fps_units=WITSUnits.PERCENT,
        record_type=20,
        item_number=33
    ),
    "2034": WITSSymbol(
        code="2034",
        name="MSCA",
        description="Mud Rept Solids % (calc)",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.PERCENT,
        fps_units=WITSUnits.PERCENT,
        record_type=20,
        item_number=34
    ),
    "2035": WITSSymbol(
        code="2035",
        name="MBRT",
        description="Mud Rept Barite content",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.PERCENT,
        fps_units=WITSUnits.PERCENT,
        record_type=20,
        item_number=35
    ),
    "2036": WITSSymbol(
        code="2036",
        name="MLCM",
        description="Mud Rept LCM content",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.KGM3,
        fps_units=WITSUnits.UNITLESS,
        record_type=20,
        item_number=36
    ),
    "2037": WITSSymbol(
        code="2037",
        name="MMBT",
        description="Mud Rept MBT capacity",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.KGM3,
        fps_units=WITSUnits.UNITLESS,
        record_type=20,
        item_number=37
    ),
    "2038": WITSSymbol(
        code="2038",
        name="MPH",
        description="Mud Rept pH",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=20,
        item_number=38
    ),
    "2039": WITSSymbol(
        code="2039",
        name="MPHT",
        description="Mud Rept pH sample temp",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.DEGC,
        fps_units=WITSUnits.DEGF,
        record_type=20,
        item_number=39
    ),
    "2040": WITSSymbol(
        code="2040",
        name="MPM",
        description="Mud Rept Pm",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=20,
        item_number=40
    ),
    "2041": WITSSymbol(
        code="2041",
        name="MPF",
        description="Mud Rept Pf",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=20,
        item_number=41
    ),
    "2042": WITSSymbol(
        code="2042",
        name="MMF",
        description="Mud Rept Mf",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=20,
        item_number=42
    ),
    "2043": WITSSymbol(
        code="2043",
        name="MRP1",
        description="Mud Rept P1",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=20,
        item_number=43
    ),
    "2044": WITSSymbol(
        code="2044",
        name="MRP2",
        description="Mud Rept P2",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=20,
        item_number=44
    ),
    "2045": WITSSymbol(
        code="2045",
        name="MCHL",
        description="Mud Rept Chlorides",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=20,
        item_number=45
    ),
    "2046": WITSSymbol(
        code="2046",
        name="MCAL",
        description="Mud Rept Calcium",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=20,
        item_number=46
    ),
    "2047": WITSSymbol(
        code="2047",
        name="MMAG",
        description="Mud Rept Magnesium",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=20,
        item_number=47
    ),
    "2048": WITSSymbol(
        code="2048",
        name="MPOT",
        description="Mud Rept Potassium",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=20,
        item_number=48
    ),
    "2049": WITSSymbol(
        code="2049",
        name="MRHT",
        description="Mud Rept Rheometer temp",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.DEGC,
        fps_units=WITSUnits.DEGF,
        record_type=20,
        item_number=49
    ),
    "2050": WITSSymbol(
        code="2050",
        name="M3",
        description="Mud Rept Viscom 3 rpm",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=20,
        item_number=50
    ),
    "2051": WITSSymbol(
        code="2051",
        name="M6",
        description="Mud Rept Viscom 6 rpm",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=20,
        item_number=51
    ),
    "2052": WITSSymbol(
        code="2052",
        name="M100",
        description="Mud Rept Viscom 100 rpm",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=20,
        item_number=52
    ),
    "2053": WITSSymbol(
        code="2053",
        name="M200",
        description="Mud Rept Viscom 200 rpm",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=20,
        item_number=53
    ),
    "2054": WITSSymbol(
        code="2054",
        name="M300",
        description="Mud Rept Viscom 300 rpm",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=20,
        item_number=54
    ),
    "2055": WITSSymbol(
        code="2055",
        name="M600",
        description="Mud Rept Viscom 600 rpm",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=20,
        item_number=55
    ),
    "2056": WITSSymbol(
        code="2056",
        name="MBRI",
        description="Mud Rept Brine %",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.PERCENT,
        fps_units=WITSUnits.PERCENT,
        record_type=20,
        item_number=56
    ),
    "2057": WITSSymbol(
        code="2057",
        name="MALK",
        description="Mud Rept Alkalinity",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=20,
        item_number=57
    ),
    "2058": WITSSymbol(
        code="2058",
        name="MLIM",
        description="Mud Rept Lime content",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.KGM3,
        fps_units=WITSUnits.UNITLESS,
        record_type=20,
        item_number=58
    ),
    "2059": WITSSymbol(
        code="2059",
        name="MELS",
        description="Mud Rept Elect. Stability",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=20,
        item_number=59
    ),
    "2060": WITSSymbol(
        code="2060",
        name="MCCL",
        description="Mud Rept CaCl, Wt %",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.PERCENT,
        fps_units=WITSUnits.PERCENT,
        record_type=20,
        item_number=60
    ),
}

# WITS Record 21 symbols - Bit Report
WITS_RECORD_21_SYMBOLS = {
    "2101": WITSSymbol(
        code="2101",
        name="WID",
        description="Well Identifier",
        data_type=WITSDataType.ASCII,
        length=16,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=21,
        item_number=1
    ),
    "2102": WITSSymbol(
        code="2102",
        name="SKNO",
        description="Sidetrack/Hole Sect No.",
        data_type=WITSDataType.INTEGER,
        length=2,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=21,
        item_number=2
    ),
    "2103": WITSSymbol(
        code="2103",
        name="RID",
        description="Record Identifier",
        data_type=WITSDataType.INTEGER,
        length=2,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=21,
        item_number=3
    ),
    "2104": WITSSymbol(
        code="2104",
        name="SQID",
        description="Sequence Identifier",
        data_type=WITSDataType.LONG,
        length=4,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=21,
        item_number=4
    ),
    "2105": WITSSymbol(
        code="2105",
        name="DATE",
        description="Date",
        data_type=WITSDataType.LONG,
        length=4,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=21,
        item_number=5
    ),
    "2106": WITSSymbol(
        code="2106",
        name="TIME",
        description="Time",
        data_type=WITSDataType.LONG,
        length=4,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=21,
        item_number=6
    ),
    "2107": WITSSymbol(
        code="2107",
        name="ACTC",
        description="Activity Code",
        data_type=WITSDataType.INTEGER,
        length=2,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=21,
        item_number=7
    ),
    "2108": WITSSymbol(
        code="2108",
        name="BNUM",
        description="Bit Number",
        data_type=WITSDataType.ASCII,
        length=8,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=21,
        item_number=8
    ),
    "2109": WITSSymbol(
        code="2109",
        name="BDIA",
        description="Bit Diameter",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=21,
        item_number=9
    ),
    "2110": WITSSymbol(
        code="2110",
        name="BMAN",
        description="Bit Manufacturer",
        data_type=WITSDataType.ASCII,
        length=16,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=21,
        item_number=10
    ),
    "2111": WITSSymbol(
        code="2111",
        name="BNAM",
        description="Bit Name",
        data_type=WITSDataType.ASCII,
        length=16,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=21,
        item_number=11
    ),
    "2112": WITSSymbol(
        code="2112",
        name="BCOD",
        description="Bit IADC Code",
        data_type=WITSDataType.ASCII,
        length=8,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=21,
        item_number=12
    ),
    "2113": WITSSymbol(
        code="2113",
        name="BSER",
        description="Bit Serial Number",
        data_type=WITSDataType.ASCII,
        length=16,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=21,
        item_number=13
    ),
    "2114": WITSSymbol(
        code="2114",
        name="BCST",
        description="Bit Cost",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=21,
        item_number=14
    ),
    "2115": WITSSymbol(
        code="2115",
        name="BJT1",
        description="Bit Jet 1 Diameter",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=21,
        item_number=15
    ),
    "2116": WITSSymbol(
        code="2116",
        name="BJT2",
        description="Bit Jet 2 Diameter",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=21,
        item_number=16
    ),
    "2117": WITSSymbol(
        code="2117",
        name="BJT3",
        description="Bit Jet 3 Diameter",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=21,
        item_number=17
    ),
    "2118": WITSSymbol(
        code="2118",
        name="BJT4",
        description="Bit Jet 4 Diameter",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=21,
        item_number=18
    ),
    "2119": WITSSymbol(
        code="2119",
        name="BJTC",
        description="Bit Center Jet Diameter",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=21,
        item_number=19
    ),
    "2120": WITSSymbol(
        code="2120",
        name="BTFA",
        description="Bit Total Flow Area",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=21,
        item_number=20
    ),
    "2121": WITSSymbol(
        code="2121",
        name="BDPI",
        description="Bit Starting Depth (In)",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.METERS,
        fps_units=WITSUnits.FEET,
        record_type=21,
        item_number=21
    ),
    "2122": WITSSymbol(
        code="2122",
        name="BDPO",
        description="Bit Ending Depth (Out)",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.METERS,
        fps_units=WITSUnits.FEET,
        record_type=21,
        item_number=22
    ),
    "2123": WITSSymbol(
        code="2123",
        name="BDDI",
        description="Bit Run Drilled Distance",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.METERS,
        fps_units=WITSUnits.FEET,
        record_type=21,
        item_number=23
    ),
    "2124": WITSSymbol(
        code="2124",
        name="BDTI",
        description="Bit Run Drilled Time",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=21,
        item_number=24
    ),
    "2125": WITSSymbol(
        code="2125",
        name="BRTI",
        description="Bit Run Reamed Time",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=21,
        item_number=25
    ),
    "2126": WITSSymbol(
        code="2126",
        name="BRPA",
        description="Bit Penetration Rate (avg)",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.MHR,
        fps_units=WITSUnits.FHR,
        record_type=21,
        item_number=26
    ),
    "2127": WITSSymbol(
        code="2127",
        name="BWBA",
        description="Bit Weight-on-Bit (avg)",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.KDN,
        fps_units=WITSUnits.KLB,
        record_type=21,
        item_number=27
    ),
    "2128": WITSSymbol(
        code="2128",
        name="BWBX",
        description="Bit Weight-on-Bit (max)",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.KDN,
        fps_units=WITSUnits.KLB,
        record_type=21,
        item_number=28
    ),
    "2129": WITSSymbol(
        code="2129",
        name="BRMA",
        description="Bit Rotary Speed (avg)",
        data_type=WITSDataType.INTEGER,
        length=2,
        metric_units=WITSUnits.RPM,
        fps_units=WITSUnits.RPM,
        record_type=21,
        item_number=29
    ),
    "2130": WITSSymbol(
        code="2130",
        name="BRMX",
        description="Bit Rotary Speed (max)",
        data_type=WITSDataType.INTEGER,
        length=2,
        metric_units=WITSUnits.RPM,
        fps_units=WITSUnits.RPM,
        record_type=21,
        item_number=30
    ),
    "2131": WITSSymbol(
        code="2131",
        name="BMFA",
        description="Bit Mud Flow Rate (avg)",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.LPM,
        fps_units=WITSUnits.GPM,
        record_type=21,
        item_number=31
    ),
    "2132": WITSSymbol(
        code="2132",
        name="BMDA",
        description="Bit Mud Density (avg)",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.KGM3,
        fps_units=WITSUnits.PPG,
        record_type=21,
        item_number=32
    ),
    "2133": WITSSymbol(
        code="2133",
        name="BSPA",
        description="Bit Standpipe Pressure (avg)",
        data_type=WITSDataType.FLOAT,
        length=4,
        metric_units=WITSUnits.KPA,
        fps_units=WITSUnits.PSI,
        record_type=21,
        item_number=33
    ),
    "2134": WITSSymbol(
        code="2134",
        name="BRUN",
        description="Bit Reason Run",
        data_type=WITSDataType.ASCII,
        length=16,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=21,
        item_number=34
    ),
    "2135": WITSSymbol(
        code="2135",
        name="BPUL",
        description="Bit Reason Pulled",
        data_type=WITSDataType.ASCII,
        length=16,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=21,
        item_number=35
    ),
    "2136": WITSSymbol(
        code="2136",
        name="BGI",
        description="Bit Grade In",
        data_type=WITSDataType.ASCII,
        length=16,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=21,
        item_number=36
    ),
    "2137": WITSSymbol(
        code="2137",
        name="BGO",
        description="Bit Grade Out",
        data_type=WITSDataType.ASCII,
        length=16,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=21,
        item_number=37
    ),
    "2138": WITSSymbol(
        code="2138",
        name="BSHK",
        description="Bit Shock Sub Used ?",
        data_type=WITSDataType.ASCII,
        length=1,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=21,
        item_number=38
    ),
    "2139": WITSSymbol(
        code="2139",
        name="BMM",
        description="Bit Mud Motor Used ?",
        data_type=WITSDataType.ASCII,
        length=1,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=21,
        item_number=39
    ),
    "2140": WITSSymbol(
        code="2140",
        name="BCOM",
        description="Bit Comments",
        data_type=WITSDataType.ASCII,
        length=128,
        metric_units=WITSUnits.UNITLESS,
        fps_units=WITSUnits.UNITLESS,
        record_type=21,
        item_number=40
    ),
}

# Combined dictionary of all WITS symbols
WITS_SYMBOLS = {
    **WITS_RECORD_1_SYMBOLS,
    **WITS_RECORD_2_SYMBOLS,
    **WITS_RECORD_3_SYMBOLS,
    **WITS_RECORD_4_SYMBOLS,
    **WITS_RECORD_6_SYMBOLS,
    **WITS_RECORD_7_SYMBOLS,
    **WITS_RECORD_8_SYMBOLS,
    **WITS_RECORD_9_SYMBOLS,
    **WITS_RECORD_10_SYMBOLS,
    **WITS_RECORD_11_SYMBOLS,
    **WITS_RECORD_12_SYMBOLS,
    **WITS_RECORD_13_SYMBOLS,
    **WITS_RECORD_14_SYMBOLS,
    **WITS_RECORD_15_SYMBOLS,
    **WITS_RECORD_16_SYMBOLS,
    **WITS_RECORD_17_SYMBOLS,
    **WITS_RECORD_18_SYMBOLS,
    **WITS_RECORD_19_SYMBOLS,
    **WITS_RECORD_20_SYMBOLS,
    **WITS_RECORD_21_SYMBOLS,
}


def get_symbol_by_code(code: str) -> Optional[WITSSymbol]:
    """Get a WITS symbol by its 4-digit code."""
    return WITS_SYMBOLS.get(code)


def get_symbols_by_record_type(record_type: int) -> Dict[str, WITSSymbol]:
    """Get all symbols for a specific record type."""
    return {code: symbol for code, symbol in WITS_SYMBOLS.items() 
            if symbol.record_type == record_type}


def get_record_types() -> List[int]:
    """Get list of all available record types."""
    return sorted(set(symbol.record_type for symbol in WITS_SYMBOLS.values()))


def get_record_description(record_type: int) -> str:
    """Get description for a record type."""
    return RECORD_DESCRIPTIONS.get(record_type, f"Record {record_type}")


def search_symbols(query: str) -> Dict[str, WITSSymbol]:
    """Search symbols by name or description."""
    query = query.lower()
    return {
        code: symbol for code, symbol in WITS_SYMBOLS.items()
        if query in symbol.name.lower() or query in symbol.description.lower()
    }
