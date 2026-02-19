import re
import logging
from groq import Groq
from app.config import GROQ_API_KEY, GROQ_MODEL
from app.database import get_schema, execute_query
from app.agents.base import Agent

logger = logging.getLogger(__name__)

SYSTEM_PROMPT = """You are an expert PostgreSQL SQL query generator.
Given the following database schema:

{schema}

Generate a SQL query for the user's question.

Rules:
- Output ONLY the raw SQL query, nothing else
- No markdown, no explanation, no code blocks, no backticks
- Use the llm schema prefix for all tables (e.g., llm.heartattack_data)
- For the glaucoma table, use llm."glaucoma_Data" (quoted, case-sensitive)
- Only generate SELECT queries (never INSERT, UPDATE, DELETE, DROP, etc.)
- Use double quotes around column names that have mixed case (e.g., "PatientID")
- If the question is ambiguous, make a reasonable assumption and generate the best query
- Limit results to 100 rows unless the user asks for a specific count or aggregation"""


class Text2SQLAgent(Agent):
    def __init__(self):
        super().__init__("Text2SQL Agent")
        self._client = Groq(api_key=GROQ_API_KEY)
        self._schema: str | None = None

    def _get_schema(self) -> str:
        if self._schema is None:
            self._schema = get_schema()
            logger.info("Schema loaded:\n%s", self._schema)
        return self._schema

    def _generate_sql(self, user_input: str, schema: str, history: list[tuple[str, str]] = None) -> str:
        messages = [
            {"role": "system", "content": SYSTEM_PROMPT.format(schema=schema)}
        ]

        if history:
            for user_msg, assistant_msg in history[-5:]:
                messages.append({"role": "user", "content": user_msg})
                messages.append({"role": "assistant", "content": assistant_msg})

        messages.append({"role": "user", "content": user_input})

        response = self._client.chat.completions.create(
            model=GROQ_MODEL,
            messages=messages,
            temperature=0.0,
            max_tokens=1024,
        )

        sql = response.choices[0].message.content.strip()
        sql = self._clean_sql(sql)
        logger.info("Generated SQL: %s", sql)
        return sql

    def _clean_sql(self, sql: str) -> str:
        """Strip markdown fences and validate it's a SELECT query."""
        sql = re.sub(r"^```(?:sql)?\s*", "", sql)
        sql = re.sub(r"\s*```$", "", sql)
        sql = sql.strip().rstrip(";") + ";"

        first_word = sql.strip().split()[0].upper() if sql.strip() else ""
        if first_word not in ("SELECT", "WITH"):
            raise ValueError(f"Only SELECT queries are allowed. Got: {first_word}")

        return sql

    def _execute_query(self, sql: str) -> tuple[list[str], list[list]]:
        return execute_query(sql)

    def _format_response(self, sql: str, columns: list[str], rows: list[list]) -> str:
        if not rows:
            return "The query returned no results."

        row_count = len(rows)
        if row_count == 1 and len(columns) == 1:
            return f"The result is: **{rows[0][0]}**"

        return f"Found {row_count} result{'s' if row_count != 1 else ''}."

    def run(self, user_input: str, history: list[tuple[str, str]] = None) -> dict:
        try:
            schema = self._get_schema()
            sql = self._generate_sql(user_input, schema, history)
            columns, rows = self._execute_query(sql)
            response_text = self._format_response(sql, columns, rows)

            return {
                "response": response_text,
                "sql": sql,
                "columns": columns,
                "results": rows,
                "error": None,
            }
        except ValueError as e:
            logger.warning("Validation error: %s", e)
            return {
                "response": f"I can't process that request: {e}",
                "sql": None,
                "columns": [],
                "results": [],
                "error": str(e),
            }
        except Exception as e:
            logger.exception("Agent error")
            return {
                "response": f"An error occurred: {e}",
                "sql": None,
                "columns": [],
                "results": [],
                "error": str(e),
            }
