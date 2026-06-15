"""Config-driven Text-to-SQL analytics engine.

NL question -> schema-aware SQL (LLM) -> safe read-only execution -> result rows
+ a business explanation grounded strictly in those rows (no invented numbers).
"""
__all__ = [
    "load_config",
    "Config",
    "Schema",
    "build_prompt",
    "validate_sql",
    "UnsafeSQLError",
    "SchemaError",
    "connect_seeded",
    "run_query",
    "load_rows",
    "explain",
    "answer",
    "Answer",
]
