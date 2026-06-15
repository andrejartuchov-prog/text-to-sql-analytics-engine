"""End-to-end pipeline with a mocked LLM: question -> SQL -> guarded exec -> explain.

No network and no live database: the LLM is the FixedLLM double from conftest and
the data is the seeded in-memory SQLite.
"""
import pytest

from textsql.engine import answer
from textsql.guardrail import UnsafeSQLError
from textsql.db import run_query
from conftest import FixedLLM


def test_total_sales_question(schema, conn):
    sql = "SELECT SUM(revenue) AS total_revenue FROM sales WHERE sale_date = '2026-06-14'"
    llm = FixedLLM(sql)

    result = answer("What were total sales on 2026-06-14?", schema=schema, conn=conn, llm=llm)

    assert result.sql == sql
    assert result.rows == [{"total_revenue": 1500.0}]
    assert "1500" in result.explanation
    # the schema-aware prompt was actually handed to the adapter
    assert llm.last_prompt and "sales" in llm.last_prompt


def test_out_of_stock_question(schema, conn):
    sql = (
        "SELECT p.name FROM inventory i "
        "JOIN products p ON p.product_id = i.product_id WHERE i.on_hand = 0"
    )
    result = answer("Which products are out of stock?", schema=schema, conn=conn, llm=FixedLLM(sql))

    assert result.rows == [{"name": "Widget"}]
    assert "Widget" in result.explanation


def test_unsafe_generated_sql_is_blocked_before_execution(schema, conn):
    with pytest.raises(UnsafeSQLError):
        answer("delete everything", schema=schema, conn=conn, llm=FixedLLM("DROP TABLE sales"))

    # the destructive statement never ran: the table is intact
    assert run_query(conn, "SELECT COUNT(*) AS n FROM sales") == [{"n": 3}]
