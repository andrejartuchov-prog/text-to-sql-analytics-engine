"""The guardrail enforces single, read-only SELECTs over known tables."""
import pytest

from textsql.guardrail import validate_sql, UnsafeSQLError, SchemaError


def test_accepts_plain_select(schema):
    # Must not raise.
    validate_sql("SELECT revenue FROM sales WHERE sale_date = '2026-06-14'", schema)


def test_accepts_join_over_known_tables(schema):
    validate_sql(
        "SELECT p.name FROM inventory i "
        "JOIN products p ON p.product_id = i.product_id WHERE i.on_hand = 0",
        schema,
    )


@pytest.mark.parametrize("sql", [
    "INSERT INTO sales (revenue) VALUES (1)",
    "UPDATE sales SET revenue = 0",
    "DELETE FROM sales",
    "DROP TABLE sales",
    "ALTER TABLE sales ADD COLUMN x INTEGER",
    "CREATE TABLE evil (id INTEGER)",
])
def test_rejects_writes_and_ddl(schema, sql):
    with pytest.raises(UnsafeSQLError):
        validate_sql(sql, schema)


def test_rejects_multiple_statements(schema):
    with pytest.raises(UnsafeSQLError):
        validate_sql("SELECT revenue FROM sales; DROP TABLE sales", schema)


def test_rejects_unknown_table(schema):
    with pytest.raises(SchemaError):
        validate_sql("SELECT * FROM secret_table", schema)
