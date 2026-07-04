src/__init__.py
"""Repository Core: Abstract Data Type Generator with LaTeX Support and CLI Interface."""
import os
from typing import Dict, List, Any, Optional, Set, Tuple
from dataclasses import dataclass, field
from pathlib import Path
import logging
import sqlite3
import asyncio
import queue
import threading
import sys
import time
from contextlib import asynccontextmanager
from datetime import timedelta

# ============================================================================
# SECURITY CONTROL PANE: CORE MODULES (Public)
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class SecurityEventRecord:
    """Represents a recorded security event for auditing."""
    id: str  # UUID-like identifier
    timestamp_ms: float = field(default_factory=time.time, repr=False)
    severity: int = 0  # 1=High, 2=Moderate, 3=Low, ...
    category: str = "unknown"
    payload_type: str = ""
    details: Dict[str, Any] = field(default_factory=dict)

class SecurityEventQueue:
    """Thread-safe event queue for recording and processing security events."""
    
    def __init__(self):
        self._queue: asyncio.Queue[SecurityEventRecord] = asyncio.Queue()
        
    async def enqueue(self, record: SecurityEventRecord) -> bool:
        if not await self._queue.put(record):
            raise RuntimeError("Queue full")
        return True
    
    @asynccontextmanager
    async def queue(self):
        """Context manager to manage the event queue."""
        try:
            while True:
                record = None
                try:
                    if not await self._queue.get():  # Blocking get for high-frequency updates
                        continue
                    return
            
                except asyncio.QueueEmpty:
                    break
                
                yield
        
    async def dequeue(self) -> Optional[SecurityEventRecord]:
        """Dequeues from the queue."""
        record = None
        try:
            if not await self._queue.get():  # Blocking get for high-frequency updates
                return None
            
            record = await asyncio.wait_for(
                self._queue.get(), timeout=1.0
            )
            
            # Mark as processed to prevent duplicate processing in the same thread
            self._recorded_ids.add(record.id)
        except asyncio.TimeoutError:
            pass
        
        if not record:
            return None
            
        await self.enqueue(record)
        
        return record
    
    def clear(self):
        """Clears all queued records."""
        while True:
            try:
                self._queue.task_done()
            except Exception as e:
                logging.warning(f"Failed to process queue cleanup: {e}")

class AuditLogger:
    """Thread-safe immutable history store for security events."""
    
    def __init__(self, db_path: str = "src/audit.db"):
        self._db_path = Path(db_path)
        
        # Initialize database connection in background thread to avoid blocking main loop
        async with asyncio.create_task(self.init_db()):
            pass
        
        self._logger = logging.getLogger("SecurityControlPlane")

    def _init_database(self):
        """Initialize SQLite database if it doesn't exist."""
        db_path = Path(f"src/{self._db_path}")
        
        # Remove existing DB to ensure clean state on restart
        if db_path.exists():
            db_path.unlink()
            
        conn = sqlite3.connect(str(db_path))
        cursor = conn.cursor()

        # Create tables for audit history and events
        create_audit_table(cursor, "audit_history")
        
        self._conn = conn
        
    def _create_audit_table(self, table_name: str):
        """Create a database schema."""
        cursor.execute(f"CREATE TABLE IF NOT EXISTS {table_name} (id TEXT PRIMARY KEY, timestamp_ms REAL, severity INTEGER, category TEXT)")

    async def record_event(
        self, 
        event_id: str = "",
        severity: int = 0,
        category: str = "unknown",
        payload_type: str = "",
        details: Dict[str, Any] = field(default_factory=dict)
    ) -> SecurityEventRecord:
        """Records a security event and persists to database."""
        
        # Ensure we don't record the same ID twice in this thread
        if "event_id" not in self._recorded_ids:
            await asyncio.sleep(0.1)  # Small delay for atomicity
            
            new_record = SecurityEventRecord(id=event_id, severity=severity, category=category, payload_type=payload_type, details=details)
            
            async with queue.Queue():
                if not self._recorded_ids.add(new_record.id):
                    return None
                
                await asyncio.wait_for(self._conn.execute(
