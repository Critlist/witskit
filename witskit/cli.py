"""
Complete refactored CLI for witskit.

Clean, modular structure with all commands from the original CLI.
"""

import typer
import asyncio
import json
import csv
from typing import Any, Dict, List, Literal, Optional, Union
from pathlib import Path
from rich.console import Console
from rich.table import Table
from rich import print as rprint
from datetime import datetime

from witskit import __version__
from witskit.models.symbols import (
    WITSSymbol, 
    WITSUnits, 
    WITS_SYMBOLS,
    get_record_types,
    get_symbols_by_record_type,
    search_symbols,
    get_record_description,
)
from witskit.models.wits_frame import DecodedFrame
from witskit.models.unit_converter import UnitConverter, ConversionError
from witskit.decoder.wits_decoder import (
    WITSDecoder,
    decode_frame,
    decode_file,
    split_multiple_frames,
    validate_wits_frame,
)
from witskit.transport.tcp_reader import TCPReader
from witskit.transport.requesting_tcp_reader import RequestingTCPReader
from witskit.transport.serial_reader import SerialReader
from witskit.transport.file_reader import FileReader

# Optional SQL storage imports
try:
    from witskit.storage.sql_writer import SQLWriter, DatabaseConfig
    SQL_AVAILABLE = True
except ImportError:
    SQL_AVAILABLE = False

# Create app and console
app = typer.Typer(
    name="witskit",
    help="Modern Python SDK for WITS drilling data processing",
    no_args_is_help=True,
)
console = Console()


# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def print_error(message: str) -> None:
    """Print an error message in red."""
    rprint(f"[red]Error: {message}[/red]")


def print_success(message: str) -> None:
    """Print a success message in green."""
    rprint(f"[green]{message}[/green]")


def print_warning(message: str) -> None:
    """Print a warning message in yellow."""
    rprint(f"[yellow]Warning: {message}[/yellow]")


def print_info(message: str) -> None:
    """Print an info message in cyan."""
    rprint(f"[cyan]{message}[/cyan]")


def version_callback(value: bool) -> None:
    """Show version and exit."""
    if value:
        typer.echo(f"WitsKit Version: {__version__}")
        raise typer.Exit()


# ============================================================================
# MAIN CALLBACK
# ============================================================================

@app.callback()
def main(
    version: bool = typer.Option(
        False,
        "--version",
        "-V",
        help="Show the version and exit.",
        callback=version_callback,
        is_eager=True,
    )
):
    """
    WitsKit - Python SDK for WITS data processing
    """
    pass


# ============================================================================
# DECODE COMMAND
# ============================================================================

@app.command("decode")
def decode_command(
    data: str = typer.Argument(..., help="WITS frame data or path to file"),
    metric: bool = typer.Option(
        False, "--metric/--fps", help="Use metric units or FPS units (default)"
    ),
    strict: bool = typer.Option(
        False, "--strict", help="Enable strict mode (fail on unknown symbols)"
    ),
    output: Optional[Path] = typer.Option(
        None, "--output", "-o", help="Output file for JSON results"
    ),
    format: str = typer.Option(
        "table", "--format", "-f", help="Output format: table, json, or raw"
    ),
    convert_to_metric: bool = typer.Option(
        False,
        "--convert-to-metric",
        help="Convert all values to metric units after decoding",
    ),
    convert_to_fps: bool = typer.Option(
        False, "--convert-to-fps", help="Convert all values to FPS units after decoding"
    ),
):
    """
    Decode a WITS frame from string or file.

    Examples:
    \b
        # Decode a WITS frame directly
        witskit decode "&&\\n01083650.40\\n011323.38\\n!!"

        # Decode from file
        witskit decode data.wits --output results.json

        # Use metric units instead of FPS (default)
        witskit decode data.wits --metric

        # Decode with FPS units then convert all to metric
        witskit decode data.wits --fps --convert-to-metric
    """

    # Validate conversion options
    if convert_to_metric and convert_to_fps:
        print_error("Cannot convert to both metric and FPS units")
        raise typer.Exit(1)

    # Check if data is a file path
    if Path(data).exists():
        with open(data, "r") as f:
            frame_data = f.read()
        source = str(data)
    else:
        # Treat as direct WITS data
        frame_data = data.replace("\\n", "\n")  # Allow escaped newlines
        source = "cli_input"

    try:
        # Check if file contains multiple frames
        frames = split_multiple_frames(frame_data)

        if len(frames) > 1:
            # Multiple frames - use decode_file
            results = decode_file(
                frame_data, use_metric_units=metric, strict_mode=strict, source=source
            )
            # Combine all data points for display
            all_data_points = []
            all_errors = []
            for result in results:
                all_data_points.extend(result.data_points)
                all_errors.extend(result.errors)

            # Create a combined result object for display
            class CombinedResult:
                def __init__(self, data_points: list, errors: list, source: str) -> None:
                    self.data_points = data_points
                    self.errors = errors
                    self.source = source
                    self.timestamp = datetime.now()

                def to_dict(self) -> dict[str, Any]:
                    return {
                        "timestamp": self.timestamp.isoformat(),
                        "source": self.source,
                        "frames": len(results),
                        "data": {
                            dp.symbol_code: {
                                "name": dp.symbol_name,
                                "description": dp.symbol_description,
                                "value": dp.parsed_value,
                                "raw_value": dp.raw_value,
                                "unit": dp.unit,
                            }
                            for dp in self.data_points
                        },
                        "errors": self.errors,
                    }

            result = CombinedResult(all_data_points, all_errors, source)
        else:
            # Single frame
            result = decode_frame(
                frame_data, use_metric_units=metric, strict_mode=strict, source=source
            )

        # Apply unit conversions if requested
        if convert_to_metric or convert_to_fps:
            conversion_errors = []
            converted_count = 0

            for dp in result.data_points:
                try:
                    symbol = WITS_SYMBOLS.get(dp.symbol_code)
                    if symbol:
                        current_unit = (
                            getattr(WITSUnits, dp.unit, None)
                            if dp.unit != "UNITLESS"
                            else WITSUnits.UNITLESS
                        )
                        target_unit = (
                            symbol.metric_units if convert_to_metric else symbol.fps_units
                        )

                        if current_unit and target_unit and current_unit != target_unit:
                            if UnitConverter.is_convertible(current_unit, target_unit):
                                if isinstance(dp.parsed_value, (int, float)):
                                    converted_value = UnitConverter.convert_value(
                                        float(dp.parsed_value),
                                        current_unit,
                                        target_unit,
                                    )
                                    dp.parsed_value = converted_value
                                    dp.unit = target_unit.value
                                    converted_count += 1
                except Exception as e:
                    conversion_errors.append(f"Failed to convert {dp.symbol_code}: {str(e)}")

            if converted_count > 0:
                units_type = "metric" if convert_to_metric else "FPS"
                print_success(f"Converted {converted_count} values to {units_type} units")

            if conversion_errors:
                print_warning("Conversion warnings:")
                for error in conversion_errors[:5]:
                    rprint(f"[yellow]  • {error}")
                if len(conversion_errors) > 5:
                    rprint(f"[yellow]  ... and {len(conversion_errors) - 5} more")

        # Output results
        if format == "json" or output:
            output_data = result.to_dict() if hasattr(result, 'to_dict') else {
                "timestamp": result.timestamp.isoformat(),
                "source": result.source,
                "data_points": [
                    {
                        "symbol_code": dp.symbol_code,
                        "symbol_name": dp.symbol_name,
                        "parsed_value": dp.parsed_value,
                        "unit": dp.unit,
                        "description": dp.symbol_description,
                    }
                    for dp in result.data_points
                ],
                "errors": result.errors,
            }
            if output:
                with open(output, "w") as f:
                    json.dump(output_data, f, indent=2)
                print_success(f"Results saved to {output}")
            else:
                rprint(json.dumps(output_data, indent=2))

        elif format == "raw":
            for dp in result.data_points:
                rprint(f"{dp.symbol_code}: {dp.parsed_value} {dp.unit}")

        else:  # table format
            if result.data_points:
                table = Table(title="Decoded WITS Data")
                table.add_column("Symbol", style="cyan")
                table.add_column("Name", style="green")
                table.add_column("Value", style="yellow")
                table.add_column("Unit", style="blue")
                table.add_column("Description", style="dim")

                for dp in result.data_points:
                    table.add_row(
                        dp.symbol_code,
                        dp.symbol_name,
                        str(dp.parsed_value),
                        dp.unit,
                        (dp.symbol_description[:50] + "..."
                         if len(dp.symbol_description) > 50
                         else dp.symbol_description),
                    )

                console.print(table)

                # Show metadata
                rprint(f"\n[dim]Source: {result.source}")
                rprint(f"[dim]Timestamp: {result.timestamp}")
                rprint(f"[dim]Data points: {len(result.data_points)}")
                if result.errors:
                    rprint(f"[red]Errors: {len(result.errors)}")
            else:
                print_warning("No data points decoded")

        # Show errors if any
        if result.errors:
            print_error("Errors encountered:")
            for error in result.errors:
                rprint(f"[red]  • {error}")

    except Exception as e:
        print_error(str(e))
        raise typer.Exit(1)


# ============================================================================
# CONVERT COMMAND
# ============================================================================

@app.command("convert")
def convert_command(
    value: float = typer.Argument(..., help="Value to convert"),
    from_unit: str = typer.Argument(..., help="Source unit (e.g., PSI, KPA, MHR, FHR)"),
    to_unit: str = typer.Argument(..., help="Target unit (e.g., PSI, KPA, MHR, FHR)"),
    precision: int = typer.Option(
        3, "--precision", "-p", help="Decimal places in result"
    ),
    show_formula: bool = typer.Option(
        False, "--formula", "-f", help="Show conversion formula and factor"
    ),
    list_units: bool = typer.Option(
        False, "--list-units", "-l", help="List all available units"
    ),
):
    """
    Convert values between drilling industry units.

    Examples:
    \b
        # Convert drilling rate
        witskit convert 30 MHR FHR

        # Convert pressure
        witskit convert 2500 PSI KPA --precision 2

        # Convert temperature
        witskit convert 150 DEGF DEGC
    """

    if list_units:
        _show_available_units()
        return

    try:
        # Parse units
        try:
            from_wits_unit = getattr(WITSUnits, from_unit.upper())
        except AttributeError:
            print_error(f"Unknown source unit: {from_unit}")
            rprint("[dim]Use --list-units to see available units")
            raise typer.Exit(1)

        try:
            to_wits_unit = getattr(WITSUnits, to_unit.upper())
        except AttributeError:
            print_error(f"Unknown target unit: {to_unit}")
            rprint("[dim]Use --list-units to see available units")
            raise typer.Exit(1)

        # Check if conversion is supported
        if not UnitConverter.is_convertible(from_wits_unit, to_wits_unit):
            print_error(f"Conversion from {from_unit} to {to_unit} is not supported")
            rprint("[dim]These units are not in the same category")
            raise typer.Exit(1)

        # Perform conversion
        result = UnitConverter.convert_value(value, from_wits_unit, to_wits_unit)
        formatted_result = round(result, precision)

        # Display result
        table = Table(title="Unit Conversion Result")
        table.add_column("From", style="cyan")
        table.add_column("To", style="green")
        table.add_column("Result", style="yellow")
        
        table.add_row(
            f"{value} {from_unit}",
            f"{to_unit}",
            f"{formatted_result:.{precision}f}",
        )
        
        console.print(table)

        # Show formula if requested
        if show_formula:
            factor = UnitConverter.get_conversion_factor(from_wits_unit, to_wits_unit)
            if factor:
                if factor == 1.0:
                    rprint(f"\n[dim]Formula: {from_unit} = {to_unit} (same unit)")
                elif from_wits_unit == WITSUnits.DEGC and to_wits_unit == WITSUnits.DEGF:
                    rprint(f"\n[dim]Formula: °F = (°C × 9/5) + 32")
                elif from_wits_unit == WITSUnits.DEGF and to_wits_unit == WITSUnits.DEGC:
                    rprint(f"\n[dim]Formula: °C = (°F - 32) × 5/9")
                else:
                    rprint(f"\n[dim]Formula: {to_unit} = {from_unit} × {factor}")

        # Show category info
        category = UnitConverter.get_unit_category(from_wits_unit)
        rprint(f"\n[dim]Category: {category}")

    except ConversionError as e:
        print_error(f"Conversion error: {str(e)}")
        raise typer.Exit(1)
    except Exception as e:
        print_error(f"Error: {str(e)}")
        raise typer.Exit(1)


def _show_available_units() -> None:
    """Display all available units organized by category."""
    rprint("[bold cyan]Available WITS Units\n")

    unit_categories = {
        "Drilling Rates": [WITSUnits.MHR, WITSUnits.FHR],
        "Pressures": [WITSUnits.KPA, WITSUnits.PSI, WITSUnits.BAR],
        "Flow Rates": [WITSUnits.LPM, WITSUnits.GPM, WITSUnits.M3PM, WITSUnits.BPM],
        "Lengths": [WITSUnits.METERS, WITSUnits.FEET, WITSUnits.MILLIMETERS, WITSUnits.INCHES],
        "Densities": [WITSUnits.KGM3, WITSUnits.PPG],
        "Temperatures": [WITSUnits.DEGC, WITSUnits.DEGF],
        "Weights/Forces": [WITSUnits.KDN, WITSUnits.KLB, WITSUnits.KGM, WITSUnits.LBF],
        "Torques": [WITSUnits.KNM, WITSUnits.KFLB],
        "Volumes": [WITSUnits.M3, WITSUnits.BBL],
        "Other": [WITSUnits.UNITLESS],
    }

    for category, units in unit_categories.items():
        table = Table(title=category)
        table.add_column("Unit Code", style="cyan")
        table.add_column("Description", style="green")
        
        for unit in units:
            table.add_row(unit.name, unit.value)
        
        console.print(table)
        rprint()

    rprint("[dim]Example: witskit convert 30 MHR FHR")
    rprint("[dim]Example: witskit convert 2500 PSI KPA --precision 2")


# ============================================================================
# SYMBOLS COMMAND
# ============================================================================

@app.command("symbols")
def symbols_command(
    search: Optional[str] = typer.Option(
        None, "--search", "-s", help="Search symbols by name or description"
    ),
    record_type: Optional[int] = typer.Option(
        None, "--record", "-r", help="Filter by record type"
    ),
    list_records: bool = typer.Option(
        False, "--list-records", "-l", help="List all available record types"
    ),
) -> None:
    """
    List available WITS symbols with their definitions.

    This command provides access to the complete WITS specification with 724 symbols
    across 20+ record types including drilling, logging, and completion data.
    """
    
    if list_records:
        # Show all record types
        table = Table(title="WITS Record Types")
        table.add_column("Record", style="cyan", width=8)
        table.add_column("Description", style="white", width=40)
        table.add_column("Symbols", style="green", width=8)
        table.add_column("Category", style="yellow", width=15)

        # Categorize records for better organization
        categories = {
            "Drilling": [1, 2, 3, 4],
            "Tripping": [5, 6],
            "Surveying": [7],
            "MWD/LWD": [8, 9],
            "Evaluation": [10, 12, 13, 14, 15, 16],
            "Operations": [11, 17, 18],
            "Configuration": [19, 20, 21],
            "Reporting": [22, 23],
            "Marine": [24, 25],
        }

        category_map = {}
        for cat, records in categories.items():
            for record in records:
                category_map[record] = cat

        for rt in sorted(get_record_types()):
            symbols_count = len(get_symbols_by_record_type(rt))
            category = category_map.get(rt, "Other")
            table.add_row(
                str(rt), get_record_description(rt), str(symbols_count), category
            )

        console.print(table)

        total_symbols = len(WITS_SYMBOLS)
        total_records = len(get_record_types())
        rprint(f"\n[bold green]Total: {total_records} record types, {total_symbols} symbols")
        rprint(f"[dim]Use --record <number> to see symbols for a specific record type")
        return

    # Filter symbols
    if search:
        symbols_to_show = search_symbols(search)
        if record_type:
            symbols_to_show = {
                code: symbol
                for code, symbol in symbols_to_show.items()
                if symbol.record_type == record_type
            }
            title = f"Record {record_type} Symbols matching '{search}'"
        else:
            title = f"All Symbols matching '{search}'"
    elif record_type:
        symbols_to_show = get_symbols_by_record_type(record_type)
        title = f"Record {record_type}: {get_record_description(record_type)}"
    else:
        symbols_to_show = WITS_SYMBOLS
        title = "All WITS Symbols"

    if not symbols_to_show:
        print_warning("No symbols found matching criteria")
        if search:
            rprint("[dim]Try a different search term or use broader keywords")
        rprint("[dim]Use --list-records to see available record types")
        return

    # Create table
    table = Table(title=f"{title} ({len(symbols_to_show)} found)")
    table.add_column("Code", style="cyan", width=6)
    table.add_column("Rec", style="dim cyan", width=4)
    table.add_column("Name", style="green", width=12)
    table.add_column("Type", style="blue", width=4)
    table.add_column("Metric", style="yellow", width=10)
    table.add_column("FPS", style="yellow", width=10)
    table.add_column("Description", style="dim", width=45)

    for code, symbol in sorted(symbols_to_show.items()):
        description = symbol.description
        if len(description) > 40:
            description = description[:37] + "..."

        table.add_row(
            code,
            str(symbol.record_type),
            symbol.name,
            symbol.data_type.value,
            symbol.metric_units.value,
            symbol.fps_units.value,
            description,
        )

    console.print(table)

    # Show helpful hints
    if len(symbols_to_show) > 50:
        rprint(f"\n[dim]Large result set. Use --search to filter or --record to focus on specific record types")

    if record_type:
        rprint(f"\n[dim]Record {record_type} contains {len(symbols_to_show)} symbols")
    else:
        rprint(f"\n[dim]Showing {len(symbols_to_show)} of {len(WITS_SYMBOLS)} total symbols")


# ============================================================================
# VALIDATE COMMAND
# ============================================================================

@app.command("validate")
def validate_command(
    data: str = typer.Argument(..., help="WITS frame data or path to file")
):
    """
    Validate WITS frame format without decoding.

    Examples:
    \b
        # Validate a WITS frame
        witskit validate "&&\\n01083650.40\\n!!"

        # Validate from file
        witskit validate data.wits
    """
    
    # Check if data is a file path
    if Path(data).exists():
        with open(data, "r") as f:
            frame_data = f.read()
    else:
        frame_data = data.replace("\\n", "\n")

    try:
        is_valid = validate_wits_frame(frame_data)
        if is_valid:
            print_success("Valid WITS frame format")
        else:
            print_error("Invalid WITS frame format")
            raise typer.Exit(1)

    except Exception as e:
        print_error(f"Validation error: {str(e)}")
        raise typer.Exit(1)


# ============================================================================
# STREAM COMMAND (Simplified version)
# ============================================================================

@app.command("stream")
def stream_command(
    source: str = typer.Argument(
        ...,
        help="Data source: tcp://host:port, serial:///dev/ttyUSB0, or file://path/to/file.wits",
    ),
    metric: bool = typer.Option(
        False, "--metric/--fps", help="Use metric units or FPS units (default)"
    ),
    max_frames: Optional[int] = typer.Option(
        None, "--max-frames", "-n", help="Maximum number of frames to process"
    ),
    output: Optional[Path] = typer.Option(
        None, "--output", "-o", help="Output file for results"
    ),
    format: str = typer.Option(
        "table", "--format", "-f", help="Output format: table, json, or raw"
    ),
):
    """
    Stream and decode WITS data from various sources.

    Examples:
    \b
        # Stream from TCP server
        witskit stream tcp://192.168.1.100:12345

        # Stream from file (for testing)
        witskit stream file://sample.wits

        # Limit to 10 frames
        witskit stream tcp://localhost:8686 --max-frames 10
    """
    
    # Parse the source URL
    reader = None
    try:
        if source.startswith("tcp://"):
            url_part = source[6:]
            if ":" not in url_part:
                raise ValueError("TCP source must include port: tcp://host:port")
            host, port_str = url_part.rsplit(":", 1)
            port = int(port_str)
            
            reader = TCPReader(host, port)
            print_info(f"Connecting to TCP {host}:{port}...")
            
        elif source.startswith("file://"):
            file_path = source[7:]
            if not Path(file_path).exists():
                raise ValueError(f"File not found: {file_path}")
            reader = FileReader(file_path)
            print_info(f"Reading from file {file_path}...")
            
        elif source.startswith("serial://"):
            print_error("Serial support not yet implemented in refactored CLI")
            print_info("Use the original CLI: python -m witskit.cli stream")
            raise typer.Exit(1)
        else:
            raise ValueError("Source must start with tcp://, serial://, or file://")

        # Stream and process frames
        print_success("Starting WITS Stream Processing")
        rprint(f"Source: {source}")
        if max_frames:
            rprint(f"Processing up to {max_frames} frames")
        rprint("[dim]Press Ctrl+C to stop streaming...[/dim]\n")
        
        frame_count = 0
        all_results = []
        
        try:
            for frame in reader.stream():
                if max_frames and frame_count >= max_frames:
                    break
                    
                try:
                    result = decode_frame(frame, use_metric_units=metric, source=source)
                    frame_count += 1
                    all_results.append(result)
                    
                    # Display frame
                    if format == "raw":
                        for dp in result.data_points:
                            rprint(f"{dp.symbol_code}: {dp.parsed_value} {dp.unit}")
                    else:
                        rprint(f"[green]Frame {frame_count}:[/green] {len(result.data_points)} data points")
                        
                except Exception as e:
                    print_warning(f"Failed to decode frame {frame_count + 1}: {e}")
                    
        except KeyboardInterrupt:
            rprint("\n[yellow]Stream interrupted by user[/yellow]")
            
        finally:
            if reader:
                reader.close()
                
        # Save results if output specified
        if output and all_results:
            output_data = {
                "source": source,
                "frames": frame_count,
                "data": [
                    {
                        "frame": i + 1,
                        "data_points": [
                            {
                                "symbol_code": dp.symbol_code,
                                "symbol_name": dp.symbol_name,
                                "value": dp.parsed_value,
                                "unit": dp.unit,
                            }
                            for dp in result.data_points
                        ]
                    }
                    for i, result in enumerate(all_results)
                ]
            }
            with open(output, "w") as f:
                json.dump(output_data, f, indent=2)
            print_success(f"Saved {frame_count} frames to {output}")
            
        rprint(f"\n[green]Processed {frame_count} frames total[/green]")
        
    except Exception as e:
        print_error(f"Stream error: {e}")
        raise typer.Exit(1)


# ============================================================================
# SQL QUERY COMMAND (Simplified version)
# ============================================================================

@app.command("sql-query")
def sql_query_command(
    database: str = typer.Argument(
        ..., help="Database URL (sqlite:///path.db, postgresql://...)"
    ),
    symbols: Optional[str] = typer.Option(
        None, "--symbols", "-s", help="Comma-separated symbol codes (e.g., 0108,0113)"
    ),
    limit: Optional[int] = typer.Option(
        1000, "--limit", "-l", help="Maximum number of records"
    ),
    list_symbols: bool = typer.Option(
        False, "--list-symbols", help="List available symbols in database"
    ),
):
    """
    Query stored WITS data from SQL database.

    Examples:
    \b
        # List available symbols
        witskit sql-query sqlite:///drilling_data.db --list-symbols

        # Query specific symbols
        witskit sql-query sqlite:///drilling_data.db --symbols "0108,0113"
    """
    
    if not SQL_AVAILABLE:
        print_error("SQL functionality not available. Install with: pip install witskit[sql]")
        raise typer.Exit(1)
        
    print_info("SQL query functionality is simplified in the refactored CLI")
    print_info("For full SQL features, use: python -m witskit.cli sql-query")
    
    # Basic implementation would go here
    # For now, refer to original CLI
    raise typer.Exit()


# ============================================================================
# DEMO COMMAND
# ============================================================================

@app.command("demo")
def demo_command() -> None:
    """
    Run a demonstration with sample WITS data.
    """
    rprint("[bold cyan]WITS Kit Demo[/bold cyan]")
    rprint("Decoding sample drilling data...\n")

    # Sample WITS frame with common drilling parameters
    sample_frame = """&&
01083650.40
011323.38
011412.5
012112.5
!!"""

    rprint("[dim]Sample WITS frame:")
    for line in sample_frame.split("\n"):
        if line.strip():
            rprint(f"[dim]  {line}")
    rprint()

    # Decode it
    result = decode_frame(sample_frame, source="demo")

    if result.data_points:
        table = Table(title="Decoded Sample Data")
        table.add_column("Symbol", style="cyan")
        table.add_column("Name", style="green")
        table.add_column("Value", style="yellow")
        table.add_column("Unit", style="blue")
        table.add_column("Description", style="dim")

        for dp in result.data_points:
            table.add_row(
                dp.symbol_code,
                dp.symbol_name,
                str(dp.raw_value),
                dp.unit,
                dp.symbol_description,
            )

        console.print(table)

        print_success(f"Successfully decoded {len(result.data_points)} parameters")

        if result.errors:
            print_warning(f"{len(result.errors)} warnings/errors:")
            for error in result.errors:
                rprint(f"[yellow]  • {error}")

        rprint("\n[bold]Try these commands:[/bold]")
        rprint("• [cyan]witskit decode 'sample.wits'[/cyan] - Decode from file")
        rprint("• [cyan]witskit stream file://sample.wits[/cyan] - Stream from file")
        rprint("• [cyan]witskit stream tcp://localhost:12345[/cyan] - Stream from TCP")
        rprint("• [cyan]witskit symbols --search depth[/cyan] - Search symbols")
        rprint("• [cyan]witskit convert 3650.40 M F[/cyan] - Convert meters to feet")
    else:
        print_error("No data could be decoded")


if __name__ == "__main__":
    app()