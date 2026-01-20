import os
import sqlite3
import re
from typing import List, Tuple

from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()


# ============================================================
# STEP 0: Gemini Configuration
# ============================================================

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
GEMINI_MODEL = "models/gemini-flash-latest"



# ============================================================
# STEP 1: Database Connection
# ============================================================

DB_PATH = "data/sample.db"


def connect_db(db_path: str) -> sqlite3.Connection:
    return sqlite3.connect(db_path)


# ============================================================
# STEP 2: Schema Extraction (Explicit Grounding)
# ============================================================

def extract_schema(conn: sqlite3.Connection) -> str:
    cursor = conn.cursor()

    cursor.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%';"
    )
    tables = [row[0] for row in cursor.fetchall()]

    schema_description = []

    for table in tables:
        cursor.execute(f"PRAGMA table_info({table});")
        columns = cursor.fetchall()

        cols = ", ".join(
            [f"{col[1]} ({col[2]})" for col in columns]
        )

        schema_description.append(f"Table {table}: {cols}")

    return "\n".join(schema_description)


# ============================================================
# STEP 3: Prompt Construction
# ============================================================

def build_prompt(user_question: str, schema: str) -> str:
    return f"""
You are an expert data analyst.

Given the following SQLite database schema:
{schema}

Write a SINGLE valid SQLite SELECT query that answers the question below.
Rules:
- Use ONLY the tables and columns provided.
- Use SELECT only.
- No explanations.
- No markdown.
- No comments.

Question:
{user_question}
""".strip()


# ============================================================
# STEP 4: NL → SQL (Gemini Boundary)
# ============================================================

def generate_sql(prompt: str) -> str:
    model = genai.GenerativeModel(GEMINI_MODEL)

    response = model.generate_content(
        prompt,
        generation_config={
            "temperature": 0.0,
            "max_output_tokens": 512
        }
    )

    raw_output = response.text.strip()
    sql = re.sub(r"```sql|```", "", raw_output).strip()

    print("\n--- GENERATED SQL ---")
    print(sql)

    return sql


# ============================================================
# STEP 5: SQL Validation (Treat as Untrusted)
# ============================================================

def validate_sql(sql: str) -> None:
    normalized = sql.strip().lower()

    forbidden_keywords = [
        "insert", "update", "delete", "drop", "alter",
        "truncate", "create", "replace", "attach", "detach"
    ]

    if not normalized.startswith("select"):
        raise ValueError("Only SELECT queries are allowed.")

    for keyword in forbidden_keywords:
        if keyword in normalized:
            raise ValueError(f"Forbidden SQL keyword detected: {keyword}")

    if ";" in normalized[:-1]:
        raise ValueError("Multiple SQL statements detected.")

    print("\n--- SQL VALIDATION PASSED ---")


# ============================================================
# STEP 6: SQL Execution
# ============================================================

def execute_sql(
    conn: sqlite3.Connection, sql: str
) -> Tuple[List[str], List[tuple]]:
    cursor = conn.cursor()
    cursor.execute(sql)

    rows = cursor.fetchall()
    columns = [desc[0] for desc in cursor.description]

    print("\n--- SQL EXECUTION RESULT ---")
    print("Columns:", columns)
    print("Rows:", rows)

    return columns, rows


# ============================================================
# STEP 7: Result → Natural Language Answer
# ============================================================

def rephrase_answer(
    question: str,
    columns: List[str],
    rows: List[tuple]
) -> str:
    if not rows:
        return "No results found for the given question."

    preview = "\n".join(
        [", ".join(map(str, row)) for row in rows[:5]]
    )

    prompt = f"""
User question:
{question}

Columns:
{columns}

Rows:
{preview}

Write a concise, clear natural language answer.
Do not mention SQL, databases, or tables.
""".strip()

    model = genai.GenerativeModel(GEMINI_MODEL)

    response = model.generate_content(
        prompt,
        generation_config={
            "temperature": 0.2,
            "max_output_tokens": 200
        }
    )

    answer = response.text.strip()

    print("\n--- FINAL ANSWER ---")
    print(answer)

    return answer


# ============================================================
# STEP 8: Main Execution Spine (Linear, Readable)
# ============================================================

def main():
    user_question = "What is the total revenue generated from all orders?"

    print("\n=== USER QUESTION ===")
    print(user_question)

    conn = connect_db(DB_PATH)

    schema = extract_schema(conn)
    print("\n=== DATABASE SCHEMA ===")
    print(schema)

    prompt = build_prompt(user_question, schema)
    print("\n=== CONSTRUCTED PROMPT ===")
    print(prompt)

    sql = generate_sql(prompt)
    validate_sql(sql)

    columns, rows = execute_sql(conn, sql)

    rephrase_answer(user_question, columns, rows)

    conn.close()


if __name__ == "__main__":
    main()
