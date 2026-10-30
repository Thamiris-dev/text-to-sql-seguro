
import sqlglot
from sqlglot import exp


def validate_sql(
    query: str,
    allowed_tables: set[str] | None = None,
) -> dict:
    """Permite somente consultas SELECT em tabelas autorizadas."""

    if not query or not query.strip():
        return {
            "allowed": False,
            "reason": "A consulta está vazia.",
        }

    if not allowed_tables:
        return {
            "allowed": False,
            "reason": "Nenhuma tabela autorizada foi configurada.",
        }

    try:
        statements = sqlglot.parse(query, read="duckdb")
    except sqlglot.errors.ParseError:
        return {
            "allowed": False,
            "reason": "A consulta SQL é inválida.",
        }

    if len(statements) != 1 or statements[0] is None:
        return {
            "allowed": False,
            "reason": "Somente uma instrução SQL é permitida.",
        }

    statement = statements[0]

    if not isinstance(statement, exp.Query):
        return {
            "allowed": False,
            "reason": "Somente consultas de leitura são permitidas.",
        }

    external_functions = {
        "READ_CSV",
        "READ_CSV_AUTO",
        "READ_PARQUET",
        "READ_JSON",
        "READ_JSON_AUTO",
        "PARQUET_SCAN",
        "CSV_SCAN",
        "GLOB",
    }

    for function in statement.find_all(exp.Func):
        if function.sql_name().upper() in external_functions:
            return {
                "allowed": False,
                "reason": "Acesso a arquivos externos não é permitido.",
            }

    authorized_tables = {
        table.lower() for table in allowed_tables
    }

    for table in statement.find_all(exp.Table):
        if table.db or table.catalog:
            return {
                "allowed": False,
                "reason": "Acesso a tabelas qualificadas não é permitido.",
            }

        if table.name.lower() not in authorized_tables:
            return {
                "allowed": False,
                "reason": f"A tabela '{table.name}' não está autorizada.",
            }

    return {
        "allowed": True,
        "reason": "Consulta de leitura aprovada.",
    }
