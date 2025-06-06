"""
Command-line interface for witskit.

A CLI tool for decoding, processing, and analyzing WITS drilling data.
"""

import typer
from typing import Optional
from pathlib import Path
from rich.console import Console
from rich.table import Table
from rich import print as rprint
import json

try:
    from decoder.wits_decoder import WITSDecoder, decode_frame
    from models.symbols import WITS_SYMBOLS
except ImportError:
    import sys
    import os
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from decoder.wits_decoder import WITSDecoder, decode_frame
    from models.symbols import WITS_SYMBOLS

app = typer.Typer(
    name="witskit",
    help="🛠️ Modern Python SDK for WITS drilling data processing",
    no_args_is_help=True
)
console = Console()


@app.command("decode")
def decode_command(
    data: str = typer.Argument(..., help="WITS frame data or path to file"),
    metric: bool = typer.Option(True, "--metric/--fps", help="Use metric units (default) or FPS units"),
    strict: bool = typer.Option(False, "--strict", help="Enable strict mode (fail on unknown symbols)"),
    output: Optional[Path] = typer.Option(None, "--output", "-o", help="Output file for JSON results"),
    format: str = typer.Option("table", "--format", "-f", help="Output format: table, json, or raw")
):
    """
    Decode a WITS frame from string or file.
    
    Examples:
    \b
        # Decode a WITS frame directly
        witskit decode "&&\\n01083650.40\\n011323.38\\n!!"
        
        # Decode from file
        witskit decode data.wits --output results.json
        
        # Use FPS units instead of metric
        witskit decode data.wits --fps
    """
    
    # Check if data is a file path
    if Path(data).exists():
        with open(data, 'r') as f:
            frame_data = f.read()
        source = str(data)
    else:
        # Treat as direct WITS data
        frame_data = data.replace('\\n', '\n')  # Allow escaped newlines
        source = "cli_input"
    
    try:
        # Decode the frame
        result = decode_frame(
            frame_data, 
            use_metric_units=metric, 
            strict_mode=strict, 
            source=source
        )
        
        # Output results
        if format == "json":
            output_data = result.to_dict()
            if output:
                with open(output, 'w') as f:
                    json.dump(output_data, f, indent=2)
                rprint(f"✅ Results saved to {output}")
            else:
                rprint(json.dumps(output_data, indent=2))
        
        elif format == "raw":
            for dp in result.data_points:
                rprint(f"{dp.symbol_code}: {dp.parsed_value} {dp.unit}")
        
        else:  # table format
            if result.data_points:
                table = Table(title="🛠️ Decoded WITS Data")
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
                        dp.symbol_description[:50] + "..." if len(dp.symbol_description) > 50 else dp.symbol_description
                    )
                
                console.print(table)
                
                # Show metadata
                rprint(f"\n[dim]Source: {result.source}")
                rprint(f"Timestamp: {result.timestamp}")
                rprint(f"Data points: {len(result.data_points)}")
                if result.errors:
                    rprint(f"[red]Errors: {len(result.errors)}")
            else:
                rprint("[yellow]⚠️ No data points decoded")
        
        # Show errors if any
        if result.errors:
            rprint(f"\n[red]❌ Errors encountered:")
            for error in result.errors:
                rprint(f"[red]  • {error}")
    
    except Exception as e:
        rprint(f"[red]❌ Error: {str(e)}")
        raise typer.Exit(1)


@app.command("symbols")
def symbols_command(
    search: Optional[str] = typer.Option(None, "--search", "-s", help="Search symbols by name or description"),
    record_type: Optional[int] = typer.Option(None, "--record", "-r", help="Filter by record type"),
    list_records: bool = typer.Option(False, "--list-records", "-l", help="List all available record types")
):
    """
    List available WITS symbols with their definitions.
    
    This command provides access to the complete WITS specification with 742+ symbols
    across 20+ record types including drilling, logging, and completion data.
    
    Examples:
    \b
        # List all available record types
        witskit symbols --list-records
        
        # Search for depth-related symbols
        witskit symbols --search depth
        
        # Show symbols for record type 1 (General Time-Based)
        witskit symbols --record 1
        
        # Search within a specific record type
        witskit symbols --record 8 --search resistivity
    """
    from models.symbols import (get_record_types, get_record_description, 
                                get_symbols_by_record_type, search_symbols)
    
    # List all record types
    if list_records:
        rprint("📊 [bold cyan]WITS Record Types\n")
        
        table = Table(title="Available WITS Record Types")
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
            "Marine": [24, 25]
        }
        
        category_map = {}
        for cat, records in categories.items():
            for record in records:
                category_map[record] = cat
        
        for rt in sorted(get_record_types()):
            symbols_count = len(get_symbols_by_record_type(rt))
            category = category_map.get(rt, "Other")
            table.add_row(
                str(rt),
                get_record_description(rt),
                str(symbols_count),
                category
            )
        
        console.print(table)
        
        total_symbols = len(WITS_SYMBOLS)
        total_records = len(get_record_types())
        rprint(f"\n📈 [bold green]Total: {total_records} record types, {total_symbols} symbols")
        rprint(f"[dim]Use --record <number> to see symbols for a specific record type")
        return
    
    # Filter symbols
    if search and record_type:
        # Search within specific record type
        record_symbols = get_symbols_by_record_type(record_type)
        search_lower = search.lower()
        symbols_to_show = {
            code: symbol for code, symbol in record_symbols.items()
            if (search_lower in symbol.name.lower() or 
                search_lower in symbol.description.lower() or
                search_lower in code)
        }
        title = f"Record {record_type} Symbols matching '{search}'"
    elif search:
        symbols_to_show = search_symbols(search)
        title = f"All Symbols matching '{search}'"
    elif record_type:
        symbols_to_show = get_symbols_by_record_type(record_type)
        title = f"Record {record_type}: {get_record_description(record_type)}"
    else:
        symbols_to_show = WITS_SYMBOLS
        title = "All WITS Symbols"
    
    if not symbols_to_show:
        rprint("[yellow]⚠️ No symbols found matching criteria")
        rprint("[dim]Try using --list-records to see available record types")
        return
    
    # Create table
    table = Table(title=f"📊 {title} ({len(symbols_to_show)} found)")
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
            description
        )
    
    console.print(table)
    
    # Show helpful hints
    if len(symbols_to_show) > 50:
        rprint(f"\n[dim]💡 Large result set. Use --search to filter or --record to focus on specific record types")
    
    if record_type:
        rprint(f"\n[dim]📖 Record {record_type} contains {len(symbols_to_show)} symbols for {get_record_description(record_type)}")
    else:
        rprint(f"\n[dim]📖 Showing {len(symbols_to_show)} of {len(WITS_SYMBOLS)} total symbols across {len(get_record_types())} record types")


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
        with open(data, 'r') as f:
            frame_data = f.read()
    else:
        frame_data = data.replace('\\n', '\n')
    
    try:
        from decoder.wits_decoder import validate_wits_frame
        
        is_valid = validate_wits_frame(frame_data)
        if is_valid:
            rprint("✅ [green]Valid WITS frame format")
        else:
            rprint("❌ [red]Invalid WITS frame format")
            raise typer.Exit(1)
    
    except Exception as e:
        rprint(f"❌ [red]Validation error: {str(e)}")
        raise typer.Exit(1)


@app.command("demo")
def demo_command():
    """
    Run a demonstration with sample WITS data.
    """
    rprint("🛠️ [bold cyan]WITS Kit Demo")
    rprint("Decoding sample drilling data...\n")
    
    # Sample WITS frame with common drilling parameters
    sample_frame = """&&
01083650.40
011323.38
011412.5
012112.5
!!"""
    
    rprint("[dim]Sample WITS frame:")
    for line in sample_frame.split('\n'):
        if line.strip():
            rprint(f"[dim]  {line}")
    rprint()
    
    # Decode it
    result = decode_frame(sample_frame, source="demo")
    
    if result.data_points:
        table = Table(title="📊 Decoded Sample Data")
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
                dp.symbol_description
            )
        
        console.print(table)
        
        rprint(f"\n✅ [green]Successfully decoded {len(result.data_points)} parameters")
        
        if result.errors:
            rprint(f"⚠️ [yellow]{len(result.errors)} warnings/errors:")
            for error in result.errors:
                rprint(f"[yellow]  • {error}")
    else:
        rprint("❌ [red]No data could be decoded")


if __name__ == "__main__":
    app()
