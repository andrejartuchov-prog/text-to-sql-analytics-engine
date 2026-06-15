"""The NL->SQL prompt must be schema-aware and carry the user's question."""
from textsql.prompt import build_prompt

QUESTION = "What were total sales on 2026-06-14?"


def test_prompt_contains_the_question(schema):
    assert QUESTION in build_prompt(QUESTION, schema)


def test_prompt_lists_every_table(schema):
    p = build_prompt(QUESTION, schema)
    for table in ("branches", "products", "sales", "inventory"):
        assert table in p, f"prompt omits table {table}"


def test_prompt_is_schema_aware_about_columns(schema):
    p = build_prompt(QUESTION, schema)
    # at least the columns the question/answer depend on must be present
    for column in ("revenue", "sale_date", "on_hand"):
        assert column in p, f"prompt omits column {column}"
