"""Idempotent ingestion: load rows into a table, de-duplicated by a key column.

Re-loading the same rows is a no-op (dedup by the key column), so seeding the
demo database is repeatable.
"""
from __future__ import annotations
import sqlite3
from typing import Dict, List


def load_rows(conn: sqlite3.Connection, table: str, rows: List[Dict], key: str) -> int:
    """Insert `rows` into `table`, skipping any whose `key` value already exists.

    Idempotent: loading the same rows twice must not create duplicates.
    Returns the number of rows actually inserted on this call.
    """
    inserted = 0
    for row in rows:
        exists = conn.execute(
            f"SELECT 1 FROM {table} WHERE {key} = ?", (row[key],)
        ).fetchone()
        if exists:
            continue
        columns = list(row)
        placeholders = ", ".join("?" for _ in columns)
        conn.execute(
            f"INSERT INTO {table} ({', '.join(columns)}) VALUES ({placeholders})",
            [row[c] for c in columns],
        )
        inserted += 1
    conn.commit()
    return inserted
