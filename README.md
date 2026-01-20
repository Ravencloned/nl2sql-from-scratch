# NL2SQL From Scratch (Gemini)

This repository contains an **end-to-end Natural Language → SQL (NL2SQL) system** built as part of a **GenAI Prototyping Intern assignment**.

The goal of this project is **not** to build a flashy chatbot or use heavy frameworks, but to demonstrate **clear system thinking, correct GenAI usage, and strong engineering judgment**.

The entire pipeline is implemented in a **single, linear Python script** so that every step is **visible, inspectable, and easy to reason about**.

---

##  Project Objective

Enable a user to ask a **natural language question** about a relational database and receive a **correct, human-readable answer**, while:

* Explicitly grounding the database schema
* Treating LLM output as **untrusted input**
* Avoiding prebuilt chains, agents, or abstractions
* Prioritizing **clarity and correctness over cleverness**

This project updates and extends the teaching style of the tutorial:

> *“Mastering Natural Language to SQL with LangChain and LangSmith (NL2SQL)”*

…but **reimplements everything from scratch** without relying on LangChain internals.

---

##  System Design Philosophy

This project was intentionally designed with the following principles:

### 1. Clarity over Abstraction

* No prebuilt NL2SQL chains
* No agents
* No hidden logic
* Every step is written explicitly in Python

### 2. Linear, Notebook-Style Execution

* Everything lives in a **single file (`main.py`)**
* Execution flows top-to-bottom
* A reviewer can read the file **in one sitting**

### 3. Minimal, Explicit LLM Usage

The LLM (Gemini) is used **only where it is actually needed**:

* Natural language → SQL generation
* Rephrasing raw SQL results into a human-readable answer

All other steps are deterministic code.

### 4. SQL is Treated as Untrusted Output

LLMs can hallucinate or generate unsafe queries. Therefore:

* Generated SQL is **validated before execution**
* Only `SELECT` queries are allowed
* Destructive keywords are explicitly blocked
* Multiple SQL statements are rejected

### 5. Inspectability

At runtime, the script prints:

* The user question
* The extracted database schema
* The constructed prompt
* The generated SQL
* The SQL execution result
* The final natural-language answer

Nothing is hidden.

---

##  System Pipeline (Step-by-Step)

The system follows a clear 7-step pipeline:

1. **User Question**
   A natural language question (e.g. *"What is the total revenue generated from all orders?"*)

2. **Database Connection**
   Connects to a local SQLite database

3. **Schema Grounding**
   Extracts table and column information using `PRAGMA table_info`

4. **Prompt Construction**
   Builds a strict, schema-grounded prompt for the LLM

5. **NL → SQL Generation (Gemini)**
   Gemini generates a single SQL `SELECT` query

6. **SQL Validation**
   Ensures the query is safe before execution

7. **SQL Execution + Answer Rephrasing**
   Executes the query and converts results into a natural-language answer

---

## Database Schema

The SQLite database (`data/sample.db`) contains **five realistic transactional tables**:

* `customers`
* `products`
* `orders`
* `order_items`
* `payments`

This schema is intentionally non-trivial to demonstrate realistic joins, aggregations, and business questions.

---

##  Repository Structure

```
nl2sql-from-scratch/
│
├── main.py              # Complete NL2SQL pipeline (single script)
├── requirements.txt     # Python dependencies
├── .gitignore           # Excludes .env and cache files
├── data/
│   └── sample.db        # SQLite database
└── README.md            # Project documentation
```

---

## Environment Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Set Up Environment Variables

Create a `.env` file in the project root:

```env
GEMINI_API_KEY=your_api_key_here
```

> ⚠️ The `.env` file is intentionally **not committed** to GitHub.

### 3. Run the Project

```bash
python main.py
```

---

##  Example Run

**Input Question:**

```
What is the total revenue generated from all orders?
```

**Generated SQL:**

```sql
SELECT SUM(amount) FROM payments
```

**Final Answer:**

```
The total revenue generated from all orders is $2,900.00.
```

---

## 🔍 Why This Project Matters

This repository is designed to demonstrate:

* Correct GenAI usage boundaries
* Awareness of LLM failure modes
* Security-conscious design
* Strong prompt engineering fundamentals
* Clean Git hygiene and reproducibility

Rather than optimizing for features, the project optimizes for **understandability and trust**.

---

##  Possible Extensions (Not Implemented Intentionally)

The following features were **deliberately not implemented** to avoid scope creep:

* Conversational memory
* Chat UI
* Agents or planners
* Vector databases
* Multi-turn query loops

These could be added in the future, but were out of scope for this assignment.

---

##  Summary

This project presents a **clean, minimal, and correct** implementation of an NL2SQL system that prioritizes:

* Transparency
* Safety
* Correctness
* Engineering judgment

It is intentionally simple — and intentionally rigorous.
