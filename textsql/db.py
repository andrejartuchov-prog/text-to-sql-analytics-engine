"""SQLite demo database: seed + read-only query (stdlib sqlite3, zero services).

The production design targets PostgreSQL; the self-contained demo uses SQLite so
the example runs with no external services.

STUB — production code intentionally incomplete (RED). Executor implements.
"""
from __future__ import annotations
import sqlite3
from typing import Dict, List


def connect_seeded(seed_sql: str) -> sqlite3.Connection:
    """Return an in-memory SQLite connection seeded from a SQL script."""
    # STUB: connection without the seed applied -> query tests are RED.
    return sqlite3.connect(":memory:")


def run_query(conn: sqlite3.Connection, sql: str) -> List[Dict]:
    """Execute a SELECT and return rows as a list of dicts (column -> value)."""
    # STUB: empty result -> tests are RED.
    return []
