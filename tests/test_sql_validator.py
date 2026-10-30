
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
    result = validate_sql(
    query,
    allowed_tables={"vendas", "produtos", "clientes"},
)

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



@pytest.mark.parametrize(
    "query",
    [
        "SELECT * FROM read_csv('dados.csv')",
        "SELECT * FROM read_parquet('dados.parquet')",
    ],
)
def test_rejects_external_file_access(query):
    result = validate_sql(query)

    assert result["allowed"] is False



@pytest.mark.parametrize(
    "query",
    [
        "SELECT * FROM vendas",
        "SELECT * FROM produtos",
        "SELECT * FROM clientes",
    ],
)
def test_accepts_authorized_tables(query):
    result = validate_sql(
        query,
        allowed_tables={"vendas", "produtos", "clientes"},
    )

    assert result["allowed"] is True


@pytest.mark.parametrize(
    "query",
    [
        "SELECT * FROM salarios",
        "SELECT * FROM dados_rh",
        "SELECT * FROM usuarios",
    ],
)
def test_rejects_unauthorized_tables(query):
    result = validate_sql(
        query,
        allowed_tables={"vendas", "produtos", "clientes"},
    )

    assert result["allowed"] is False


@pytest.mark.parametrize(
    "query",
    [
        """
        WITH dados AS (
            SELECT * FROM salarios
        )
        SELECT * FROM dados
        """,
        """
        SELECT *
        FROM vendas
        JOIN salarios ON vendas.id = salarios.id
        """,
        """
        SELECT *
        FROM (
            SELECT * FROM dados_rh
        ) AS informacoes
        """,
    ],
)
def test_rejects_unauthorized_tables_in_nested_queries(query):
    result = validate_sql(
        query,
        allowed_tables={"vendas", "produtos", "clientes"},
    )

    assert result["allowed"] is False
