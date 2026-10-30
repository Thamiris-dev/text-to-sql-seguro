
import pytest

from src.sql_validator import validate_sql


@pytest.mark.parametrize(
    "query",
    [
        "SELECT * FROM vendas LIMIT 100",
        "SELECT nome, preco FROM produtos WHERE preco > 100 LIMIT 100",
        "SELECT COUNT(*) FROM clientes LIMIT 100",
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
    result = validate_sql(
    query,
    allowed_tables={"vendas", "produtos", "clientes"},
)

    assert result["allowed"] is False


@pytest.mark.parametrize(
    "query",
    [
        "SELECT * FROM vendas; DROP TABLE vendas",
        "SELECT * FROM vendas; DELETE FROM vendas",
    ],
)
def test_rejects_multiple_statements(query):
    result = validate_sql(
    query,
    allowed_tables={"vendas", "produtos", "clientes"},
)

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
    result = validate_sql(
    query,
    allowed_tables={"vendas", "produtos", "clientes"},
)

    assert result["allowed"] is False



@pytest.mark.parametrize(
    "query",
    [
        "SELECT * FROM vendas LIMIT 100",
        "SELECT * FROM produtos LIMIT 100",
        "SELECT * FROM clientes LIMIT 100",
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


@pytest.mark.parametrize(
    "query",
    [
        "SELECT * FROM vendas LIMIT 50",
        "SELECT * FROM produtos LIMIT 100",
    ],
)
def test_accepts_queries_within_row_limit(query):
    result = validate_sql(
        query,
        allowed_tables={"vendas", "produtos", "clientes"},
        max_rows=100,
    )

    assert result["allowed"] is True


def test_rejects_queries_exceeding_row_limit():
    result = validate_sql(
        "SELECT * FROM vendas LIMIT 500",
        allowed_tables={"vendas", "produtos", "clientes"},
        max_rows=100,
    )

    assert result["allowed"] is False


def test_rejects_queries_without_limit():
    result = validate_sql(
        "SELECT * FROM vendas",
        allowed_tables={"vendas", "produtos", "clientes"},
        max_rows=100,
    )

    assert result["allowed"] is False


@pytest.mark.parametrize(
    "query",
    [
        "SELECT * FROM vendas LIMIT 0",
        "SELECT * FROM vendas LIMIT -1",
        "SELECT * FROM vendas LIMIT ALL",
        "SELECT * FROM vendas LIMIT '100'",
    ],
)
def test_rejects_invalid_row_limits(query):
    result = validate_sql(
        query,
        allowed_tables={"vendas", "produtos", "clientes"},
        max_rows=100,
    )

    assert result["allowed"] is False

def test_rejects_invalid_max_rows():
    result = validate_sql(
        "SELECT * FROM vendas LIMIT 10",
        allowed_tables={"vendas", "produtos", "clientes"},
        max_rows=-1,
    )

    assert result["allowed"] is False


@pytest.mark.parametrize(
    "max_rows",
    [
        0,
        -1,
        100.5,
        True,
        "100",
    ],
)
def test_rejects_invalid_max_rows_values(max_rows):
    result = validate_sql(
        "SELECT * FROM vendas LIMIT 10",
        allowed_tables={"vendas", "produtos", "clientes"},
        max_rows=max_rows,
    )

    assert result["allowed"] is False