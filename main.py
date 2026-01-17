"""
NL2SQL From Scratch
===================

This file implements a step-by-step Natural Language to SQL (NL2SQL) pipeline.

IMPORTANT DESIGN PRINCIPLES:
- Linear execution (not agent-based)
- No hidden chains or magic helpers
- Every step is explicit and inspectable
- SQL is treated as untrusted output
- Clarity > cleverness

The goal is NOT to build a production system.
The goal is to make the NL2SQL reasoning process visible.
"""

# ============================================================
# Step 1: Load environment and dependencies
# ============================================================

import sqlite3
from pathlib import Path
from typing import List, Tuple

# (LLM-related imports will be added later)


# ============================================================
# Step 2: Connect to the SQLite database
# ============================================================

DB_PATH = Path("data/sample.db")

def connect_to_db(db_path: Path) -> sqlite3.Connection:
    """
    Create a connection to the SQLite database.
    """
    if not db_path.exists():
        raise FileNotFoundError(f"Database not found at {db_path}")
    return sqlite3.connect(db_path)


# ============================================================
# Step 3: Inspect and extract database schema
# ============================================================

def get_schema_text(conn: sqlite3.Connection) -> str:
    """
    Extract table and column information from the database
    and convert it into a text format suitable for LLM grounding.
    """
    # Placeholder — logic will be implemented in Step 4
    return ""


# ============================================================
# Step 4: Construct the SQL generation prompt
# ============================================================

def build_sql_prompt(
    user_question: str,
    schema_text: str,
) -> str:
    """
    Build the prompt that will be sent to the LLM
    to generate a SQL query.
    """
    # Placeholder — logic will be implemented in Step 5
    return ""


# ============================================================
# Step 5: Generate SQL using the LLM
# ============================================================

def generate_sql(prompt: str) -> str:
    """
    Call the LLM to generate a SQL query.
    The output of this function is UNTRUSTED text.
    """
    # Placeholder — logic will be implemented in Step 6
    return ""


# ============================================================
# Step 6: Validate generated SQL
# ============================================================

def validate_sql(sql_query: str) -> None:
    """
    Perform basic validation on the generated SQL query.
    This function should raise an error if the SQL is unsafe.
    """
    # Placeholder — logic will be implemented in Step 7
    pass


# ============================================================
# Step 7: Execute SQL against the database
# ============================================================

def execute_sql(
    conn: sqlite3.Connection,
    sql_query: str,
) -> List[Tuple]:
    """
    Execute the validated SQL query and return raw rows.
    """
    # Placeholder — logic will be implemented in Step 8
    return []


# ============================================================
# Step 8: Rephrase SQL result into natural language
# ============================================================

def rephrase_answer(
    user_question: str,
    sql_query: str,
    sql_result: List[Tuple],
) -> str:
    """
    Convert raw SQL results into a human-readable answer.
    """
    # Placeholder — logic will be implemented in Step 9
    return ""


# ============================================================
# Step 9: Main execution flow (Notebook-style)
# ============================================================

def main():
    print("=== NL2SQL From Scratch ===")

    # Example user input (will later be interactive)
    user_question = "How many orders are there?"

    print(f"\nUser Question:\n{user_question}")

    # Connect to DB
    conn = connect_to_db(DB_PATH)
    print("\nConnected to database.")

    # Extract schema
    schema_text = get_schema_text(conn)
    print("\nExtracted Schema:")
    print(schema_text)

    # Build prompt
    prompt = build_sql_prompt(user_question, schema_text)
    print("\nPrompt sent to LLM:")
    print(prompt)

    # Generate SQL
    sql_query = generate_sql(prompt)
    print("\nGenerated SQL:")
    print(sql_query)

    # Validate SQL
    validate_sql(sql_query)
    print("\nSQL validation passed.")

    # Execute SQL
    result = execute_sql(conn, sql_query)
    print("\nRaw SQL Result:")
    print(result)

    # Rephrase answer
    answer = rephrase_answer(user_question, sql_query, result)
    print("\nFinal Answer:")
    print(answer)

    conn.close()


# ============================================================
# Entry point
# ============================================================

if __name__ == "__main__":
    main()
