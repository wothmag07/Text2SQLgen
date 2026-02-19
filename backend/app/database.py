import psycopg2
from app.config import DATABASE_URL


def get_connection():
    return psycopg2.connect(DATABASE_URL)


def get_schema() -> str:
    """Extract database schema from the llm schema for LLM context."""
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT table_name, column_name, data_type
                FROM information_schema.columns
                WHERE table_schema = 'llm'
                ORDER BY table_name, ordinal_position;
            """)
            rows = cur.fetchall()
    finally:
        conn.close()

    if not rows:
        return "No tables found in the 'llm' schema."

    schema_parts = []
    current_table = None
    for table_name, column_name, data_type in rows:
        if table_name != current_table:
            if current_table is not None:
                schema_parts.append("")
            schema_parts.append(f"Table: llm.{table_name}")
            schema_parts.append("Columns:")
            current_table = table_name
        schema_parts.append(f"  - {column_name} ({data_type})")

    return "\n".join(schema_parts)


def execute_query(sql: str) -> tuple[list[str], list[list]]:
    """Execute a SQL query and return (column_names, rows)."""
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(sql)
            columns = [desc[0] for desc in cur.description]
            rows = cur.fetchall()
            return columns, [list(row) for row in rows]
    finally:
        conn.close()
