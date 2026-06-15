"""Ingestion is idempotent: re-loading the same rows creates no duplicates."""
import sqlite3

from textsql.ingest import load_rows


def _conn():
    c = sqlite3.connect(":memory:")
    c.execute("CREATE TABLE products (product_id INTEGER PRIMARY KEY, name TEXT)")
    return c


def test_dedup_on_repeated_load():
    conn = _conn()
    rows = [{"product_id": 1, "name": "Gadget"}, {"product_id": 2, "name": "Widget"}]

    inserted_first = load_rows(conn, "products", rows, key="product_id")
    inserted_second = load_rows(conn, "products", rows, key="product_id")

    assert inserted_first == 2
    assert inserted_second == 0
    total = conn.execute("SELECT COUNT(*) FROM products").fetchone()[0]
    assert total == 2


def test_partial_overlap_inserts_only_new():
    conn = _conn()
    load_rows(conn, "products", [{"product_id": 1, "name": "Gadget"}], key="product_id")
    inserted = load_rows(
        conn,
        "products",
        [{"product_id": 1, "name": "Gadget"}, {"product_id": 3, "name": "Gizmo"}],
        key="product_id",
    )
    assert inserted == 1
    total = conn.execute("SELECT COUNT(*) FROM products").fetchone()[0]
    assert total == 2
