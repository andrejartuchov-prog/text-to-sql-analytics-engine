"""Seeded SQLite execution returns rows as dicts."""
from textsql.db import run_query


def test_aggregate_query(conn):
    rows = run_query(
        conn,
        "SELECT SUM(revenue) AS total_revenue FROM sales WHERE sale_date = '2026-06-14'",
    )
    assert rows == [{"total_revenue": 1500.0}]


def test_rows_are_dicts_in_order(conn):
    rows = run_query(conn, "SELECT name FROM products ORDER BY product_id")
    assert rows == [{"name": "Gadget"}, {"name": "Widget"}]
