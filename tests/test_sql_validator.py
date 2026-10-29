
import pytest

from src.sql_validator import validate_sql


@pytest.mark.parametrize(
    "query",
    [
        "SELECT * FROM vendas",
        "SELECT nome, preco FROM produtos WHERE preco > 100",
        "SELECT COUNT(*) FROM clientes",
    ],
)
def test_accepts_read_only_select_queries(query):
    result = validate_sql(query)

    assert result["allowed"] is True


@pytest.mark.parametrize(
    "query",
    [
        "DELETE FROM vendas",
        "UPDATE produtos SET preco = 0",
        "DROP TABLE clientes",
        "INSERT INTO clientes (nome) VALUES ('Teste')",
    ],
)
def test_rejects_data_modification_queries(query):
    result = validate_sql(query)

    assert result["allowed"] is False


@pytest.mark.parametrize(
    "query",
    [
        "SELECT * FROM vendas; DROP TABLE vendas",
        "SELECT * FROM vendas; DELETE FROM vendas",
    ],
)
def test_rejects_multiple_statements(query):
    result = validate_sql(query)

    assert result["allowed"] is False


@pytest.mark.parametrize(
    "query",
    [
        "",
        "   ",
        "not a SQL query",
    ],
)
def test_rejects_empty_or_invalid_queries(query):
    result = validate_sql(query)

    assert result["allowed"] is False
