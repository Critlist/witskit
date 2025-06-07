"""
SQL writer implementation for storing WITS data in timeseries databases.

This module provides a robust SQL storage backend with support for SQLite,
PostgreSQL, and MySQL databases, optimized for timeseries drilling data.
"""

import json
import asyncio
from datetime import datetime
from typing import List, Optional, Dict, Any, AsyncGenerator
from pathlib import Path
from dataclasses import dataclass
from contextlib import asynccontextmanager

try:
    from sqlalchemy import select, func, and_, or_, desc
    from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
    from sqlalchemy.orm import selectinload
    import aiosqlite
    SQLALCHEMY_AVAILABLE = True
except ImportError:
    SQLALCHEMY_AVAILABLE = False

from .base import BaseStorage
from .schema import (
    Base, WITSFrame, WITSDataPoint, WITSSymbolDefinition, WITSSourceInfo,
    create_database_engine, create_tables, get_session_factory
)
from ..models.wits_frame import DecodedFrame, DecodedData
from ..models.symbols import WITS_SYMBOLS


@dataclass
class DatabaseConfig:
    """Configuration for database connection."""
    
    # Database type and connection
    database_type: str  # sqlite, postgresql, mysql
    database_url: str   # Full connection URL
    
    # SQLite specific
    sqlite_path: Optional[str] = None
    
    # PostgreSQL/MySQL specific
    host: Optional[str] = None
    port: Optional[int] = None
    username: Optional[str] = None
    password: Optional[str] = None
    database: Optional[str] = None
    
    # Connection settings
    echo_sql: bool = False
    pool_size: int = 5
    max_overflow: int = 10
    
    @classmethod
    def sqlite(cls, path: str = "wits_data.db", echo: bool = False) -> "DatabaseConfig":
        """Create SQLite configuration."""
        return cls(
            database_type="sqlite",
            database_url=f"sqlite+aiosqlite:///{path}",
            sqlite_path=path,
            echo_sql=echo
        )
    
    @classmethod
    def postgresql(
        cls, 
        host: str = "localhost",
        port: int = 5432,
        username: str = "postgres",
        password: str = "",
        database: str = "wits_data",
        echo: bool = False
    ) -> "DatabaseConfig":
        """Create PostgreSQL configuration."""
        url = f"postgresql+asyncpg://{username}:{password}@{host}:{port}/{database}"
        return cls(
            database_type="postgresql",
            database_url=url,
            host=host,
            port=port,
            username=username,
            password=password,
            database=database,
            echo_sql=echo
        )
    
    @classmethod
    def mysql(
        cls,
        host: str = "localhost", 
        port: int = 3306,
        username: str = "root",
        password: str = "",
        database: str = "wits_data",
        echo: bool = False
    ) -> "DatabaseConfig":
        """Create MySQL configuration."""
        url = f"mysql+aiomysql://{username}:{password}@{host}:{port}/{database}"
        return cls(
            database_type="mysql",
            database_url=url,
            host=host,
            port=port,
            username=username,
            password=password,
            database=database,
            echo_sql=echo
        )


class SQLWriter(BaseStorage):
    """
    SQL-based storage backend for WITS data.
    
    Provides efficient storage and querying of WITS timeseries data
    with support for multiple database backends.
    """
    
    def __init__(self, config: DatabaseConfig):
        """
        Initialize SQL writer with database configuration.
        
        Args:
            config: Database configuration
        """
        if not SQLALCHEMY_AVAILABLE:
            raise ImportError(
                "SQLAlchemy and database drivers not available. "
                "Install with: pip install witskit[sql]"
            )
        
        self.config = config
        self.engine = None
        self.session_factory = None
        self._initialized = False
    
    async def initialize(self) -> None:
        """Initialize database connection and create tables."""
        # Create async engine
        self.engine = create_async_engine(
            self.config.database_url,
            echo=self.config.echo_sql,
            pool_size=self.config.pool_size,
            max_overflow=self.config.max_overflow
        )
        
        # Create session factory
        self.session_factory = async_sessionmaker(
            self.engine, 
            class_=AsyncSession,
            expire_on_commit=False
        )
        
        # Create tables
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        
        # Initialize symbol definitions from WITS_SYMBOLS
        await self._initialize_symbols()
        
        self._initialized = True
    
    async def _initialize_symbols(self) -> None:
        """Initialize symbol definitions in database."""
        async with self.session_factory() as session:
            # Check if symbols already exist
            result = await session.execute(select(func.count(WITSSymbolDefinition.symbol_code)))
            count = result.scalar()
            
            if count == 0:
                # Insert all WITS symbols
                symbol_objs = []
                for code, symbol in WITS_SYMBOLS.items():
                    symbol_obj = WITSSymbolDefinition(
                        symbol_code=code,
                        name=symbol.name,
                        description=str(symbol.description),
                        data_type=symbol.data_type.value,
                        fps_unit=symbol.fps_units.value if symbol.fps_units else None,
                        metric_unit=symbol.metric_units.value if symbol.metric_units else None,
                        record_type=symbol.record_type
                    )
                    symbol_objs.append(symbol_obj)
                
                session.add_all(symbol_objs)
                await session.commit()
    
    @asynccontextmanager
    async def get_session(self):
        """Get database session context manager."""
        if not self._initialized:
            await self.initialize()
        
        async with self.session_factory() as session:
            try:
                yield session
            except Exception:
                await session.rollback()
                raise
            finally:
                await session.close()
    
    async def store_frame(self, frame: DecodedFrame) -> None:
        """Store a single decoded WITS frame."""
        await self.store_frames([frame])
    
    async def store_frames(self, frames: List[DecodedFrame]) -> None:
        """Store multiple decoded WITS frames in a batch."""
        if not frames:
            return
        
        async with self.get_session() as session:
            frame_objs = []
            data_point_objs = []
            
            for decoded_frame in frames:
                # Create frame object
                frame_obj = WITSFrame(
                    timestamp=decoded_frame.timestamp,
                    source=decoded_frame.source,
                    raw_data=decoded_frame.frame.raw_data,
                    created_at=datetime.utcnow()
                )
                frame_objs.append(frame_obj)
                session.add(frame_obj)
                
                # Flush to get frame ID
                await session.flush()
                
                # Create data point objects
                for data_point in decoded_frame.data_points:
                    # Determine value storage
                    numeric_value = None
                    string_value = None
                    
                    if isinstance(data_point.parsed_value, (int, float)):
                        numeric_value = float(data_point.parsed_value)
                    elif data_point.parsed_value is not None:
                        string_value = str(data_point.parsed_value)
                    
                    data_point_obj = WITSDataPoint(
                        frame_id=frame_obj.id,
                        symbol_code=data_point.symbol_code,
                        timestamp=data_point.timestamp,
                        source=data_point.source,
                        raw_value=data_point.raw_value,
                        numeric_value=numeric_value,
                        string_value=string_value,
                        unit=data_point.unit,
                        created_at=datetime.utcnow()
                    )
                    data_point_objs.append(data_point_obj)
            
            # Bulk insert data points
            session.add_all(data_point_objs)
            
            # Update source statistics
            await self._update_source_stats(session, frames)
            
            await session.commit()
    
    async def _update_source_stats(self, session: AsyncSession, frames: List[DecodedFrame]) -> None:
        """Update source statistics."""
        # Group frames by source
        source_stats = {}
        for frame in frames:
            source = frame.source or "unknown"
            if source not in source_stats:
                source_stats[source] = {
                    'frame_count': 0,
                    'data_point_count': 0,
                    'latest_timestamp': frame.timestamp
                }
            
            source_stats[source]['frame_count'] += 1
            source_stats[source]['data_point_count'] += len(frame.data_points)
            if frame.timestamp > source_stats[source]['latest_timestamp']:
                source_stats[source]['latest_timestamp'] = frame.timestamp
        
        # Update or create source info records
        for source, stats in source_stats.items():
            result = await session.execute(
                select(WITSSourceInfo).where(WITSSourceInfo.source == source)
            )
            source_info = result.scalar_one_or_none()
            
            if source_info:
                source_info.last_seen = stats['latest_timestamp']
                source_info.total_frames += stats['frame_count']
                source_info.total_data_points += stats['data_point_count']
            else:
                source_info = WITSSourceInfo(
                    source=source,
                    first_seen=stats['latest_timestamp'],
                    last_seen=stats['latest_timestamp'],
                    total_frames=stats['frame_count'],
                    total_data_points=stats['data_point_count'],
                    is_active=True
                )
                session.add(source_info)
    
    async def query_frames(
        self,
        start_time: Optional[datetime] = None,
        end_time: Optional[datetime] = None,
        source: Optional[str] = None,
        symbol_codes: Optional[List[str]] = None,
        limit: Optional[int] = None
    ) -> AsyncGenerator[DecodedFrame, None]:
        """Query stored WITS frames with optional filters."""
        async with self.get_session() as session:
            query = select(WITSFrame).options(
                selectinload(WITSFrame.data_points).selectinload(WITSDataPoint.symbol_def)
            )
            
            # Apply filters
            conditions = []
            if start_time:
                conditions.append(WITSFrame.timestamp >= start_time)
            if end_time:
                conditions.append(WITSFrame.timestamp <= end_time)
            if source:
                conditions.append(WITSFrame.source == source)
            
            if conditions:
                query = query.where(and_(*conditions))
            
            # Filter by symbol codes if specified
            if symbol_codes:
                query = query.join(WITSDataPoint).where(
                    WITSDataPoint.symbol_code.in_(symbol_codes)
                ).distinct()
            
            # Order by timestamp
            query = query.order_by(WITSFrame.timestamp)
            
            # Apply limit
            if limit:
                query = query.limit(limit)
            
            result = await session.execute(query)
            frames = result.unique().scalars().all()
            
            # Convert to DecodedFrame objects
            for frame in frames:
                decoded_frame = await self._convert_to_decoded_frame(frame)
                if symbol_codes:
                    # Filter data points by symbol codes
                    decoded_frame.data_points = [
                        dp for dp in decoded_frame.data_points
                        if dp.symbol_code in symbol_codes
                    ]
                yield decoded_frame
    
    async def query_data_points(
        self,
        symbol_codes: List[str],
        start_time: Optional[datetime] = None,
        end_time: Optional[datetime] = None,
        source: Optional[str] = None,
        limit: Optional[int] = None
    ) -> AsyncGenerator[DecodedData, None]:
        """Query specific data points with timeseries filtering."""
        async with self.get_session() as session:
            query = select(WITSDataPoint).options(
                selectinload(WITSDataPoint.symbol_def)
            ).where(WITSDataPoint.symbol_code.in_(symbol_codes))
            
            # Apply filters
            conditions = []
            if start_time:
                conditions.append(WITSDataPoint.timestamp >= start_time)
            if end_time:
                conditions.append(WITSDataPoint.timestamp <= end_time)
            if source:
                conditions.append(WITSDataPoint.source == source)
            
            if conditions:
                query = query.where(and_(*conditions))
            
            # Order by timestamp
            query = query.order_by(WITSDataPoint.timestamp)
            
            # Apply limit
            if limit:
                query = query.limit(limit)
            
            result = await session.execute(query)
            data_points = result.scalars().all()
            
            # Convert to DecodedData objects
            for dp in data_points:
                yield await self._convert_to_decoded_data(dp)
    
    async def get_available_symbols(self, source: Optional[str] = None) -> List[str]:
        """Get list of available symbol codes in storage."""
        async with self.get_session() as session:
            query = select(WITSDataPoint.symbol_code).distinct()
            
            if source:
                query = query.where(WITSDataPoint.source == source)
            
            result = await session.execute(query)
            return [row[0] for row in result.fetchall()]
    
    async def get_time_range(self, source: Optional[str] = None) -> tuple[Optional[datetime], Optional[datetime]]:
        """Get the time range of data in storage."""
        async with self.get_session() as session:
            query = select(
                func.min(WITSDataPoint.timestamp),
                func.max(WITSDataPoint.timestamp)
            )
            
            if source:
                query = query.where(WITSDataPoint.source == source)
            
            result = await session.execute(query)
            min_time, max_time = result.first()
            return min_time, max_time
    
    async def _convert_to_decoded_frame(self, frame: WITSFrame) -> DecodedFrame:
        """Convert database frame to DecodedFrame object."""
        from ..models.wits_frame import WITSFrame as ModelWITSFrame
        
        # Create original frame object
        original_frame = ModelWITSFrame(
            raw_data=frame.raw_data,
            timestamp=frame.timestamp,
            source=frame.source
        )
        
        # Convert data points
        data_points = []
        for dp in frame.data_points:
            decoded_data = await self._convert_to_decoded_data(dp)
            data_points.append(decoded_data)
        
        return DecodedFrame(
            frame=original_frame,
            data_points=data_points,
            errors=[]  # Errors not stored in DB for now
        )
    
    async def _convert_to_decoded_data(self, dp: WITSDataPoint) -> DecodedData:
        """Convert database data point to DecodedData object."""
        # Get symbol from WITS_SYMBOLS
        symbol = WITS_SYMBOLS.get(dp.symbol_code)
        if not symbol:
            raise ValueError(f"Unknown symbol code: {dp.symbol_code}")
        
        # Determine parsed value
        parsed_value = dp.numeric_value if dp.numeric_value is not None else dp.string_value
        
        return DecodedData(
            symbol=symbol,
            raw_value=dp.raw_value,
            parsed_value=parsed_value,
            unit=dp.unit,
            timestamp=dp.timestamp,
            source=dp.source
        )
    
    async def close(self) -> None:
        """Close database connections."""
        if self.engine:
            await self.engine.dispose()
            self.engine = None
            self.session_factory = None
            self._initialized = False