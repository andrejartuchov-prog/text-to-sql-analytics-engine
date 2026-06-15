"""Config loading: schema + KPIs + model parsed from YAML into a typed Config."""


def test_loads_schema_tables(config):
    assert set(config.schema.table_names()) == {"branches", "products", "sales", "inventory"}


def test_loads_columns(config):
    assert config.schema.columns("sales") == [
        "sale_id", "product_id", "branch_id", "sale_date", "qty", "revenue"
    ]
    assert config.schema.has_column("inventory", "on_hand")
    assert not config.schema.has_column("inventory", "no_such_column")


def test_loads_model_and_kpis(config):
    assert config.model == "claude-opus-4-8"
    assert "total_revenue" in config.kpis
