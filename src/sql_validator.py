
import sqlglot
from sqlglot import exp


def validate_sql(query: str) -> dict:
    """Permite somente uma consulta SQL de leitura do tipo SELECT."""

    if not query or not query.strip():
        return {
            "allowed": False,
            "reason": "A consulta está vazia.",
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

    return {
        "allowed": True,
        "reason": "Consulta de leitura aprovada.",
    }
