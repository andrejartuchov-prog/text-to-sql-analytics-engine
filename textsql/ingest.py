"""Idempotent ingestion: load rows into a table, de-duplicated by a key column.

STUB — production code intentionally incomplete (RED). Executor implements.
"""
from __future__ import annotations
import sqlite3
from typing import Dict, List


def load_rows(conn: sqlite3.Connection, table: str, rows: List[Dict], key: str) -> int:
    """Insert `rows` into `table`, skipping any whose `key` value already exists.

    Idempotent: loading the same rows twice must not create duplicates.
    Returns the number of rows actually inserted on this call.
    """
    # STUB: insert nothing -> idempotency/dedup test is RED.
    return 0
