"""
WITS decoder for parsing raw WITS frames into structured data.

This module provides the main decoder functionality for converting
WITS ASCII frames into typed Python objects with full validation.
"""

from datetime import datetime
from typing import List, Literal, Optional, Tuple, Union
from loguru import logger

# Always use absolute imports to avoid type conflicts
from ..models import WITSFrame, DecodedData, DecodedFrame, WITSSymbol
from ..models.symbols import get_symbol_by_code, WITS_SYMBOLS


class WITSDecoder:
    """
    Main WITS decoder class for parsing and validating WITS data frames.

    Supports WITS Level 0 (ASCII) format with extensible symbol definitions.
    """

    def __init__(self, use_metric_units: bool = True, strict_mode: bool = False):
        """
        Initialize the WITS decoder.

        Args:
            use_metric_units: If True, use metric units, otherwise use FPS units
            strict_mode: If True, raise errors for unknown symbols, otherwise log warnings
        """
        self.use_metric_units: bool = use_metric_units
        self.strict_mode: bool = strict_mode

    def decode_frame(
        self, raw_frame: str, source: Optional[str] = None
    ) -> DecodedFrame:
        """
        Decode a complete WITS frame into structured data.

        Args:
            raw_frame: Raw WITS frame string (with && and !! markers)
            source: Optional source identifier for the frame

        Returns:
            DecodedFrame containing all decoded data points and any errors

        Raises:
            ValueError: If frame format is invalid and strict_mode is True
        """
        try:
            # Create and validate the WITS frame
            wits_frame = WITSFrame(raw_data=raw_frame, source=source)

            decoded_frame = DecodedFrame(frame=wits_frame)

            # Process each data line
            for line in wits_frame.data_lines:
                try:
                    data_point: DecodedData | None = self._decode_data_line(
                        line, wits_frame.timestamp, source
                    )
                    if data_point:
                        decoded_frame.data_points.append(data_point)
                except Exception as e:
                    error_msg: str = f"Error decoding line '{line}': {str(e)}"
                    decoded_frame.errors.append(error_msg)
                    logger.warning(error_msg)

                    if self.strict_mode:
                        raise ValueError(error_msg) from e

            logger.debug(
                f"Decoded WITS frame with {len(decoded_frame.data_points)} data points "
                f"and {len(decoded_frame.errors)} errors"
            )

            return decoded_frame

        except Exception as e:
            if self.strict_mode:
                raise
            # Return a frame with just the error
            error_frame = DecodedFrame(
                frame=WITSFrame(raw_data=raw_frame, source=source),
                errors=[f"Frame decoding failed: {str(e)}"],
            )
            return error_frame

    def _decode_data_line(
        self, line: str, timestamp: datetime, source: Optional[str]
    ) -> Optional[DecodedData]:
        """
        Decode a single WITS data line.

        Args:
            line: Single data line from WITS frame (e.g., "01083650.40")
            timestamp: Timestamp for the data point
            source: Source identifier

        Returns:
            DecodedData object or None if line couldn't be decoded
        """
        if not line.strip():
            return None

        try:
            # Parse the line into symbol code and value
            if len(line) < 4:
                raise ValueError(f"Line too short: {line}")

            symbol_code: str = line[:4]
            raw_value: str = line[4:].strip()

            if not symbol_code.isdigit():
                raise ValueError(f"Invalid symbol code: {symbol_code}")

            # Look up the symbol definition
            symbol: WITSSymbol | None = get_symbol_by_code(symbol_code)
            if not symbol:
                if self.strict_mode:
                    raise ValueError(f"Unknown symbol code: {symbol_code}")
                else:
                    logger.warning(f"Unknown symbol code: {symbol_code}, skipping")
                    return None

            # Determine the unit to use
            unit: str = (
                symbol.metric_units.value
                if self.use_metric_units
                else symbol.fps_units.value
            )

            # Create the decoded data point
            decoded_data = DecodedData(
                symbol=symbol,
                raw_value=raw_value,
                unit=unit,
                timestamp=timestamp,
                source=source,
            )

            logger.debug(
                f"Decoded {symbol_code} ({symbol.name}): {raw_value} -> {decoded_data.parsed_value} {unit}"
            )

            return decoded_data

        except Exception as e:
            logger.error(f"Failed to decode line '{line}': {str(e)}")
            raise

    def decode_multiple_frames(
        self, frame_data: List[str], source: Optional[str] = None
    ) -> List[DecodedFrame]:
        """
        Decode multiple WITS frames.

        Args:
            frame_data: List of raw WITS frame strings
            source: Optional source identifier

        Returns:
            List of DecodedFrame objects
        """
        results = []
        for i, frame in enumerate(frame_data):
            try:
                decoded: DecodedFrame = self.decode_frame(frame, source)
                results.append(decoded)
            except Exception as e:
                logger.error(f"Failed to decode frame {i}: {str(e)}")
                if self.strict_mode:
                    raise

        return results

    def validate_frame_format(self, raw_frame: str) -> Tuple[bool, Optional[str]]:
        """
        Validate the basic format of a WITS frame without full decoding.

        Args:
            raw_frame: Raw WITS frame string

        Returns:
            Tuple of (is_valid, error_message)
        """
        try:
            WITSFrame(raw_data=raw_frame, source=None)
            return True, None
        except ValueError as e:
            return False, str(e)


# Convenience functions for direct usage
def decode_frame(
    raw_frame: str,
    use_metric_units: bool = True,
    strict_mode: bool = False,
    source: Optional[str] = None,
) -> DecodedFrame:
    """
    Convenience function to decode a single WITS frame.

    Args:
        raw_frame: Raw WITS frame string
        use_metric_units: If True, use metric units, otherwise use FPS units
        strict_mode: If True, raise errors for unknown symbols
        source: Optional source identifier

    Returns:
        DecodedFrame containing decoded data points
    """
    decoder = WITSDecoder(use_metric_units=use_metric_units, strict_mode=strict_mode)
    return decoder.decode_frame(raw_frame, source)


def validate_wits_frame(raw_frame: str) -> bool:
    """
    Convenience function to validate WITS frame format.

    Args:
        raw_frame: Raw WITS frame string

    Returns:
        True if valid, False otherwise
    """
    decoder = WITSDecoder()
    is_valid, _ = decoder.validate_frame_format(raw_frame)
    return is_valid


def get_available_symbols() -> dict[str, WITSSymbol]:
    """
    Get all available WITS symbols.

    Returns:
        Dictionary mapping symbol codes to WITSSymbol objects
    """
    return WITS_SYMBOLS.copy()


def split_multiple_frames(data: str) -> List[str]:
    """
    Split a string containing multiple WITS frames into individual frames.

    Args:
        data: Raw string potentially containing multiple WITS frames

    Returns:
        List of individual WITS frame strings
    """
    frames = []
    lines: List[str] = data.strip().split("\n")
    current_frame = []

    for line in lines:
        line: str = line.strip()
        if not line:
            continue

        if line.startswith("&&"):
            # Start of new frame
            if current_frame:  # Save previous frame if exists
                frames.append("\n".join(current_frame))
            current_frame: List[str] = [line]
        elif line.startswith("!!"):
            # End of current frame
            current_frame.append(line)
            frames.append("\n".join(current_frame))
            current_frame = []
        elif current_frame:  # Data line within a frame
            current_frame.append(line)

    # Handle case where last frame doesn't end with !!
    if current_frame and current_frame[0].startswith("&&"):
        frames.append("\n".join(current_frame))

    return frames


def decode_file(
    file_data: str,
    use_metric_units: bool = True,
    strict_mode: bool = False,
    source: Optional[str] = None,
) -> List[DecodedFrame]:
    """
    Decode a file containing one or more WITS frames.

    Args:
        file_data: Raw file content
        use_metric_units: If True, use metric units, otherwise use FPS units
        strict_mode: If True, raise errors for unknown symbols
        source: Optional source identifier

    Returns:
        List of DecodedFrame objects
    """
    decoder = WITSDecoder(use_metric_units=use_metric_units, strict_mode=strict_mode)
    frames: List[str] = split_multiple_frames(file_data)

    if not frames:
        raise ValueError("No valid WITS frames found in data")

    results = []
    for i, frame_data in enumerate(frames):
        try:
            decoded: DecodedFrame = decoder.decode_frame(
                frame_data, source or f"frame_{i+1}"
            )
            results.append(decoded)
        except Exception as e:
            logger.error(f"Failed to decode frame {i+1}: {str(e)}")
            if strict_mode:
                raise

    return results
