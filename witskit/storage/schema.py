"""
SQLAlchemy schema definitions for WITS data storage.

This module defines the database tables optimized for timeseries storage
of WITS drilling data with proper indexing for efficient queries.
"""

from datetime import datetime
from typing import Optional
from sqlalchemy import (
    Column, String, Float, Integer, DateTime, Text, Index, 
    ForeignKey, BigInteger, Boolean, create_engine
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

Base = declarative_base()


class WITSSymbolDefinition(Base):
    """
    Table for storing WITS symbol definitions (metadata).
    
    This normalizes symbol information to avoid duplication in the data tables.
    """
    __tablename__ = "wits_symbols"
    
    symbol_code = Column(String(4), primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    description = Column(Text)
    data_type = Column(String(1), nullable=False)  # A, F, S, L
    fps_unit = Column(String(50))
    metric_unit = Column(String(50))
    record_type = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationship to data points
    data_points = relationship("WITSDataPoint", back_populates="symbol_def")


class WITSFrame(Base):
    """
    Table for storing WITS frame metadata.
    
    Each frame represents a complete WITS transmission with timestamp and source.
    """
    __tablename__ = "wits_frames"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    timestamp = Column(DateTime, nullable=False, index=True)
    source = Column(String(255), index=True)
    raw_data = Column(Text)  # Store original raw frame data
    frame_count = Column(Integer, default=1)  # For batch processing tracking
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationship to data points
    data_points = relationship("WITSDataPoint", back_populates="frame", cascade="all, delete-orphan")
    
    # Composite index for time-based queries
    __table_args__ = (
        Index('idx_frames_timestamp_source', 'timestamp', 'source'),
        Index('idx_frames_created_source', 'created_at', 'source'),
    )


class WITSDataPoint(Base):
    """
    Table for storing individual WITS data points (timeseries data).
    
    This is the main table for querying drilling parameters over time.
    Optimized for timeseries queries with proper indexing.
    """
    __tablename__ = "wits_data_points"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    frame_id = Column(Integer, ForeignKey('wits_frames.id'), nullable=False, index=True)
    symbol_code = Column(String(4), ForeignKey('wits_symbols.symbol_code'), nullable=False, index=True)
    timestamp = Column(DateTime, nullable=False, index=True)
    source = Column(String(255), index=True)
    
    # Value storage - use appropriate type based on data
    raw_value = Column(String(255))  # Always store raw string value
    numeric_value = Column(Float)    # Parsed numeric value (if applicable)
    string_value = Column(Text)      # Parsed string value (if applicable)
    
    unit = Column(String(50))
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    frame = relationship("WITSFrame", back_populates="data_points")
    symbol_def = relationship("WITSSymbolDefinition", back_populates="data_points")
    
    # Indexes optimized for timeseries queries
    __table_args__ = (
        # Primary timeseries index: symbol + time
        Index('idx_timeseries_primary', 'symbol_code', 'timestamp'),
        
        # Source-specific timeseries 
        Index('idx_timeseries_source', 'symbol_code', 'source', 'timestamp'),
        
        # Time range queries
        Index('idx_timestamp_range', 'timestamp', 'symbol_code'),
        
        # Frame-based queries
        Index('idx_frame_symbol', 'frame_id', 'symbol_code'),
        
        # Latest value queries
        Index('idx_latest_values', 'symbol_code', 'source', 'timestamp'),
    )


class WITSSourceInfo(Base):
    """
    Table for tracking data source metadata and statistics.
    """
    __tablename__ = "wits_sources"
    
    source = Column(String(255), primary_key=True)
    description = Column(Text)
    first_seen = Column(DateTime, default=datetime.utcnow)
    last_seen = Column(DateTime, default=datetime.utcnow)
    total_frames = Column(BigInteger, default=0)
    total_data_points = Column(BigInteger, default=0)
    is_active = Column(Boolean, default=True)
    
    # Metadata about the source
    connection_type = Column(String(50))  # tcp, serial, file
    connection_details = Column(Text)     # JSON string with connection info
    
    __table_args__ = (
        Index('idx_source_activity', 'is_active', 'last_seen'),
    )


def create_database_engine(database_url: str, echo: bool = False):
    """
    Create SQLAlchemy engine for the given database URL.
    
    Args:
        database_url: Database connection URL (sqlite:///path.db, postgresql://...)
        echo: Whether to log SQL queries
        
    Returns:
        SQLAlchemy Engine instance
    """
    engine = create_engine(database_url, echo=echo)
    return engine


def create_tables(engine):
    """
    Create all tables in the database.
    
    Args:
        engine: SQLAlchemy Engine instance
    """
    Base.metadata.create_all(engine)


def get_session_factory(engine):
    """
    Create a session factory for the given engine.
    
    Args:
        engine: SQLAlchemy Engine instance
        
    Returns:
        SQLAlchemy sessionmaker factory
    """
    return sessionmaker(bind=engine) 