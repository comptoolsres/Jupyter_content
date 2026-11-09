import marimo

__generated_with = "0.24.2"
app = marimo.App()


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Writing our own minimal agent

    ## What is an AI Agent?

    There are many deffinitions of what an AI agent is. At the most basic level, an AI agent is software that combines a LLM with tools. Rather than just generate answers to prompts, an agent has tools that it can use to actually **do** things!

    In the next notebook, we'll look at using a pre-made agent, but before we do that, let's write our own.

    ## Step 1. Tool definitions and the basic agent loop
    We will create three read‑only tools that let the model inspect and query the `airway.db` SQLite database:

    * `list_tables()` – returns the names of all tables
    * `describe_table(name)` – returns the column names and types for a given table
    * `run_sql(query)` – executes a read‑only SQL query (SELECT only) and returns up to 50 rows as a list of dictionaries

    We'll also write the agent loop.

    ### The agent loop:
    1. Send the user's question together with the tool definitions to the model.
    2. If the model decides to call a tool, execute it, feed the result back, and repeat.
    3. When the model returns a final text answer (no tool calls), we display it.
    """)
    return


@app.cell
def _():
    import json
    import sqlite3
    from typing import Any, Dict, List
    from dotenv import load_dotenv
    import os
    import openai

    # Load environment variables from the ../.env file in the directory above the current working directory
    load_dotenv("../.env")

    # Retrieve the key
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    BASE_URL = "https://api.navigator.ai.ufl.edu/v1/" # This is the Navigator API base URL
    model = "nemotron-3-super-120b-a12b"  # Replace with the desired model ID

    # Create an OpenAI client using the API key and base URL
    def get_client() -> openai.OpenAI:
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise RuntimeError(
                "OPENAI_API_KEY not set. Export it or put it in a .env file before running."
            )
        return openai.OpenAI(api_key=api_key, base_url=BASE_URL)

    return Any, Dict, List, get_client, json, sqlite3


@app.cell
def _(get_client):
    # Load environment variables (OPENAI_API_KEY) if needed
    client = get_client()
    MODEL = "nemotron-3-super-120b-a12b"  # matches the model list from the airway notebook【1†L20-L22】

    # Path to the SQLite database built in the data‑preparation script
    DB_PATH = "data/airway.db"
    return DB_PATH, MODEL, client


@app.cell
def _(Any, DB_PATH, Dict, List, sqlite3):
    # Define the functions for the tools

    def list_tables() -> List[str]:
        """Return the names of all tables in the database."""
        with sqlite3.connect(f"file:{DB_PATH}?mode=ro", uri=True) as con:
            cur = con.execute("SELECT name FROM sqlite_master WHERE type='table'")
            return [row[0] for row in cur.fetchall()]

    def describe_table(table_name: str) -> List[Dict[str, Any]]:
        """Return column information for a given table."""
        if table_name not in list_tables():
            raise ValueError(f"Table '{table_name}' does not exist.")
        with sqlite3.connect(f"file:{DB_PATH}?mode=ro", uri=True) as con:
            cur = con.execute(f"PRAGMA table_info({table_name})")
            return [{"name": row[1], "type": row[2], "nullable": not row[3],
                     "default": row[4], "primary_key": bool(row[5])} for row in cur.fetchall()]

    def run_sql(query: str, limit: int = 50) -> List[Dict[str, Any]]:
        """
        Execute a read‑only SQL query and return up to `limit` rows.
        Only SELECT statements are allowed; any other statement raises an error.
        """
        q = query.strip()
        if not q.upper().startswith("SELECT"):
            raise ValueError("Only SELECT queries are permitted for safety.")
        # Append a LIMIT clause if the user didn't provide one (still respects their LIMIT if present)
        if "LIMIT" not in q.upper():
            q = f"{q} LIMIT {limit}"
        with sqlite3.connect(f"file:{DB_PATH}?mode=ro", uri=True) as con:
            con.row_factory = sqlite3.Row
            cur = con.execute(q)
            rows = [dict(row) for row in cur.fetchall()]
        return rows

    return describe_table, list_tables, run_sql


@app.cell
def _():
    # Create a list of tool definitions for the agent to use

    tools = [
        {
            "type": "function",
            "function": {
                "name": "list_tables",
                "description": "List the names of all tables in the database.",
                "parameters": {"type": "object", "properties": {}, "additionalProperties": False},
            },
        },
        {
            "type": "function",
            "function": {
                "name": "describe_table",
                "description": "Return column names and types for a given table.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "table_name": {
                            "type": "string",
                            "description": "Name of the table to describe",
                        }
                    },
                    "required": ["table_name"],
                    "additionalProperties": False,
                },
            },
        },
        {
            "type": "function",
            "function": {
                "name": "run_sql",
                "description": "Execute a read‑only SQL SELECT query and return up to 50 rows.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "query": {
                            "type": "string",
                            "description": "A SELECT statement to run against the database",
                        }
                    },
                    "required": ["query"],
                    "additionalProperties": False,
                },
            },
        },
    ]
    return (tools,)


@app.cell
def _(MODEL, client, describe_table, json, list_tables, run_sql, tools):
    # ---- The agent loop ----
    def run_agent(question: str, max_steps: int = 10) -> str:
        """
        Run the agent loop for a single question.
        Returns the final answer string and prints each step.
        """
        messages = [
            {
                "role": "system",
                "content": (
                    "You are a helpful data‑analysis assistant. "
                    "When you need information about the database, you must use the provided tools. "
                    "Do not guess answers; always query the database first. "
                    "When you have enough information, give a concise final answer."
                ),
            },
            {"role": "user", "content": question},
        ]

        step = 0
        while step < max_steps:
            step += 1
            print(f"\n=== Step {step} ===")
            # Ask the model, giving it access to the tools
            response = client.chat.completions.create(
                model=MODEL,
                messages=messages,
                tools=tools,
                tool_choice="auto",  # let the model decide
                temperature=0.0,
            )
            msg = response.choices[0].message
            print(f"Model message: {msg}")

            # If the model wants to call tools, execute them
            if msg.tool_calls:
                # Append the assistant's message (with tool_calls) to the conversation
                messages.append(msg)

                for tool_call in msg.tool_calls:
                    name = tool_call.function.name
                    args = json.loads(tool_call.function.arguments)
                    print(f"→ Calling tool: {name}({args})")
                    try:
                        if name == "list_tables":
                            result = list_tables()
                        elif name == "describe_table":
                            result = describe_table(**args)
                        elif name == "run_sql":
                            result = run_sql(**args)
                        else:
                            raise ValueError(f"Unknown tool: {name}")
                    except Exception as e:
                        result = {"error": str(e)}
                    print(f"← Tool result: {result}")

                    # Feed the tool result back as a tool message
                    messages.append(
                        {
                            "role": "tool",
                            "tool_call_id": tool_call.id,
                            "name": name,
                            "content": json.dumps(result, default=str),
                        }
                    )
                # Continue the loop to let the model process the tool results
                continue
            else:
                # No tool calls → we have a final answer
                final_answer = msg.content
                print("\n=== Final answer ===")
                print(final_answer)
                return final_answer

        return "Agent stopped after reaching max steps without a final answer."

    return (run_agent,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Part B – Questions in plain English

    Use the `run_agent` function defined above to answer the example questions.

    After each answer, write the equivalent SQL yourself and check that the agent’s result matches your own query.
    """)
    return


@app.cell
def _(run_agent):
    # Example 1: "Which 10 genes have the highest mean counts in dex-treated samples?"
    q1 = (
        "Which 10 genes have the highest mean counts in dex-treated samples? "
        "Please give the gene ID, gene name, and the mean count."
    )
    ans1 = run_agent(q1)
    return


@app.cell
def _(run_agent):
    # Example 2: "How many protein‑coding genes have zero counts in every sample?"
    q2 = (
        "How many protein‑coding genes have zero counts in every sample? "
        "Return just the number."
    )
    ans2 = run_agent(q2)
    return


@app.cell
def _(run_agent):
    # Example 3: "For each cell line, what is the total count of reads across all genes and samples?"
    q3 = (
        "For each cell line, what is the total count of reads across all genes and samples? "
        "Show the cell line and the total."
    )
    ans3 = run_agent(q3)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Part C – Trying to break the agent

    Ask questions that are ambiguous, ask for something the tools cannot do,
    or provoke a tool error. Observe how the agent reacts and whether it
    recovers or asks for clarification.
    """)
    return


@app.cell
def _(run_agent):
    # Ambiguous question – the model must ask for clarification
    ambiguous = "What is the average expression?"
    print(run_agent(ambiguous))
    return


@app.cell
def _(run_agent):
    # Request a disallowed operation (UPDATE)
    disallowed = "Please update the count of gene ENSG00000000003 for sample SRR1039508 to 1000."
    print(run_agent(disallowed))
    return


@app.cell
def _(run_agent):
    # Ask for something outside the schema (e.g., file system access)
    outside = "List the files in the current directory."
    print(run_agent(outside))
    return


@app.cell
def _(run_agent):
    # Question that causes a SQL error (syntax error)
    bad_sql = "Why is the query 'SELECT * FROM' invalid?"
    print(run_agent(bad_sql))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
 
    """)
    return


if __name__ == "__main__":
    app.run()
