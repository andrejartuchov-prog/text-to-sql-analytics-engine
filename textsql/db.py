"""SQLite demo database: seed + read-only query (stdlib sqlite3, zero services).

The production design targets PostgreSQL; the self-contained demo uses SQLite so
the example runs with no external services.
"""
from __future__ import annotations
import sqlite3
from typing import Dict, List


def connect_seeded(seed_sql: str) -> sqlite3.Connection:
    """Return an in-memory SQLite connection seeded from a SQL script."""
    conn = sqlite3.connect(":memory:")
    conn.executescript(seed_sql)
    return conn


def run_query(conn: sqlite3.Connection, sql: str) -> List[Dict]:
    """Execute a SELECT and return rows as a list of dicts (column -> value)."""
    cursor = conn.execute(sql)
    columns = [d[0] for d in cursor.description]
    return [dict(zip(columns, row)) for row in cursor.fetchall()]
