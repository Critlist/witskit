"""
Abstract base class for WITS data storage backends.
"""

from abc import ABC, abstractmethod
from typing import List, Optional, AsyncGenerator
from datetime import datetime

from ..models.wits_frame import DecodedFrame, DecodedData


class BaseStorage(ABC):
    """
    Abstract base class for WITS data storage backends.

    Defines the interface that all storage implementations must follow.
    """

    @abstractmethod
    async def initialize(self) -> None:
        """
        Initialize the storage backend (create tables, connections, etc.).
        """
        pass

    @abstractmethod
    async def store_frame(self, frame: DecodedFrame) -> None:
        """
        Store a single decoded WITS frame.

        Args:
            frame: The decoded WITS frame to store
        """
        pass

    @abstractmethod
    async def store_frames(self, frames: List[DecodedFrame]) -> None:
        """
        Store multiple decoded WITS frames in a batch.

        Args:
            frames: List of decoded WITS frames to store
        """
        pass

    @abstractmethod
    async def query_frames(
        self,
        start_time: Optional[datetime] = None,
        end_time: Optional[datetime] = None,
        source: Optional[str] = None,
        symbol_codes: Optional[List[str]] = None,
        limit: Optional[int] = None,
    ) -> AsyncGenerator[DecodedFrame, None]:
        """
        Query stored WITS frames with optional filters.

        Args:
            start_time: Optional start time filter
            end_time: Optional end time filter
            source: Optional source identifier filter
            symbol_codes: Optional list of symbol codes to filter by
            limit: Optional limit on number of results

        Yields:
            DecodedFrame: Matching frames from storage
        """
        pass

    @abstractmethod
    async def query_data_points(
        self,
        symbol_codes: List[str],
        start_time: Optional[datetime] = None,
        end_time: Optional[datetime] = None,
        source: Optional[str] = None,
        limit: Optional[int] = None,
    ) -> AsyncGenerator[DecodedData, None]:
        """
        Query specific data points with timeseries filtering.

        Args:
            symbol_codes: List of symbol codes to retrieve
            start_time: Optional start time filter
            end_time: Optional end time filter
            source: Optional source identifier filter
            limit: Optional limit on number of results

        Yields:
            DecodedData: Matching data points from storage
        """
        pass

    @abstractmethod
    async def get_available_symbols(self, source: Optional[str] = None) -> List[str]:
        """
        Get list of available symbol codes in storage.

        Args:
            source: Optional source filter

        Returns:
            List of symbol codes available in storage
        """
        pass

    @abstractmethod
    async def get_time_range(
        self, source: Optional[str] = None
    ) -> tuple[Optional[datetime], Optional[datetime]]:
        """
        Get the time range of data in storage.

        Args:
            source: Optional source filter

        Returns:
            Tuple of (earliest_time, latest_time) or (None, None) if no data
        """
        pass

    @abstractmethod
    async def close(self) -> None:
        """
        Close connections and cleanup resources.
        """
        pass
