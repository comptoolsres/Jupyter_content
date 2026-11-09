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
    # Stucturing LLM Output

    In the [first notebook](A01_Intro_to_Agenitc_AI.ipynb) of this series, we focused on setting up API keys, connecting to NaviGator, and exploring some things we can do with quries to the LLM.

    Now we want to see where we can tie model output to our actual data.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Step 1. Managing Messy Data

    While the data for the `airway` dataset are actually quite nice, that's not always the case. I had Claude generate some more realistic data: [data/messy_metadata.csv](data/messy_metadata.csv). Let's load it and take a look.
    """)
    return


@app.cell
def _():
    import openai
    import os
    import json
    from pathlib import Path
    from dotenv import load_dotenv
    import pypdf
    import sqlite3
    import pandas as pd
    from typing import Literal, Optional
    from pydantic import BaseModel, ConfigDict, Field, ValidationError

    return (
        BaseModel,
        ConfigDict,
        Field,
        Literal,
        Optional,
        Path,
        ValidationError,
        json,
        load_dotenv,
        openai,
        os,
        pd,
    )


@app.cell
def _(pd):
    meta_data = pd.read_csv("data/messy_metadata.csv")

    meta_data
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Notice the conditions and donor lines are inconsistent.

    The goal is to turn the free‑text fields in `messy_metadata.csv` into a clean, structured table:

    * `treatment`: `"dexamethasone"` or `"untreated"`
    * `cell_line`: one of the four airway cell lines (`N061011`, `N080611`, `N052611`, `N61311`)
    * `replicate`: integer replicate number **only if** the original row explicitly states one; otherwise `null`

    We achieve this by:
    1. Defining a Pydantic model that encodes the allowed values and rejects extra keys.
    2. Prompting the model to output **only JSON** that matches the model.
    3. Validating each output; on failure we feed the validation error back to the model and allow up to 3 retries.
    4. Logging token usage so you can see the cost of each attempt.

    Pydantic is a Python library for validating data against models defined with Python types. Here, `CleanRecord` inherits from `BaseModel`: its `Literal` fields restrict `treatment` and `cell_line` to the listed values, `replicate` can be an integer or `None`, and `ConfigDict(extra="forbid")` rejects unexpected fields. Each parsed LLM response is passed to `CleanRecord`, so invalid values or shapes raise a `ValidationError` that the retry loop can send back to the model for correction. See the [Pydantic models](https://docs.pydantic.dev/latest/concepts/models/), [fields](https://docs.pydantic.dev/latest/concepts/fields/), [configuration](https://docs.pydantic.dev/latest/concepts/config/), and [validation errors](https://docs.pydantic.dev/latest/errors/errors/) documentation.

    Type hints (also called type annotations) describe the kinds of values a variable, function parameter, or return value is expected to use. For example, `prompt: str` says that `prompt` should be a string, `system: str | None` allows either a string or `None`, and `-> tuple[dict, dict]` describes the pair returned by `ask_for_json`. Type hints help readers and editor tools understand code, but Python does not generally enforce them by itself at runtime; Pydantic uses these annotations in `CleanRecord` to validate actual data. See the [Python typing documentation](https://docs.python.org/3/library/typing.html) for more.

     The messy sheet contains the same 8 samples as `airway_samples.csv` but with inconsistent wording. This makes it a realistic data‑cleaning exercise.
    """)
    return


@app.cell
def _(
    BaseModel,
    ConfigDict,
    Field,
    Literal,
    Optional,
    Path,
    json,
    load_dotenv,
    openai,
    os,
    pd,
):
    # Load environment variables from the ../.env file in the directory above the current working directory
    load_dotenv('../.env')
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    # Retrieve the key
    BASE_URL = 'https://api.navigator.ai.ufl.edu/v1/'
    model = 'nemotron-3-super-120b-a12b'  # This is the Navigator API base URL
      # Replace with the desired model ID
    def get_client() -> openai.OpenAI:
    # Create an OpenAI client using the API key and base URL
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key:
            raise RuntimeError('OPENAI_API_KEY not set. Export it or put it in a .env file before running.')
        return openai.OpenAI(api_key=api_key, base_url=BASE_URL)

    def strip_reasoning(text: str) -> str:
        """Some models emit 
        blocks; remove them."""
        import re
        return re.sub('', '', text or '', flags=re.DOTALL).strip()

    def ask_for_json(prompt: str, system: str | None=None, model: str=model, temperature: float=0.0, max_tokens: int=512, client: openai.OpenAI | None=None) -> tuple[dict, dict]:
        """Send a prompt and return (parsed_json, full_response_dict)."""
        if client is None:
            client = get_client()
        messages = []
        if system:
            messages.append({'role': 'system', 'content': system})
        messages.append({'role': 'user', 'content': prompt})
        resp = client.chat.completions.create(model=model, messages=messages, temperature=temperature, max_tokens=max_tokens)
        raw = strip_reasoning(resp.choices[0].message.content)
        usage = resp.usage
        try:
            data = json.loads(raw)
        except json.JSONDecodeError as e:
            raise ValueError(f'Model did not return valid JSON: {raw}') from e
        return (data, {'usage': usage, 'raw': raw})

    class CleanRecord(BaseModel):
        treatment: Literal['dexamethasone', 'untreated'] = Field(description='Treatment condition after standardization')
        cell_line: Literal['N061011', 'N080611', 'N052611', 'N61311'] = Field(description='Exact cell‑line identifier')
        replicate: Optional[int] = Field(default=None, description='Replicate number if explicitly given; otherwise null')
        model_config = ConfigDict(extra='forbid')
    DATA_DIR = Path('data')
    messy_path = DATA_DIR / 'messy_metadata.csv'
    df_messy = pd.read_csv(messy_path)
    print('Messy metadata shape:', df_messy.shape)
    df_messy.head()  # a CompletionUsage object
    SYSTEM_PROMPT = 'You are a data‑curator assistant. Convert each row of the\nprovided sample sheet into a JSON object that exactly matches the schema:\n{\n  "treatment": "dexamethasone" | "untreated",\n  "cell_line": "N061011" | "N080611" | "N052611" | "N61311",\n  "replicate": integer | null\n}\nDo NOT add any extra fields or explanatory text. Return ONLY the JSON object.\nIf the row does not contain a replicate number, set replicate to null.\n'

    def build_user_prompt(row: pd.Series) -> str:
        """Create a short, readable description of the messy row."""
    # ----------------------------------------------------------------------
    # Define the strict schema for a clean record
    # Load the messy metadata
    # Prompt template – ask for JSON only
        return f"Sample ID: {row['sample']}\nCondition (raw): {row['condition']}\nDonor line (raw): {row['donor_line']}\nNotes (raw): {row.get('notes', '')}\nReturn the JSON object for this row."  # reject any extra keys  # adjust if your data lives elsewhere

    return (
        CleanRecord,
        DATA_DIR,
        SYSTEM_PROMPT,
        ask_for_json,
        build_user_prompt,
        df_messy,
        get_client,
    )


@app.cell
def _(
    CleanRecord,
    DATA_DIR,
    Path,
    SYSTEM_PROMPT,
    ValidationError,
    ask_for_json,
    build_user_prompt,
    df_messy,
    get_client,
    pd,
):
    # ----------------------------------------------------------------------
    # Process each row with retries
    # ----------------------------------------------------------------------
    results = []
    token_log = []

    client = get_client()

    for idx, row in df_messy.iterrows():
        user_prompt = build_user_prompt(row)
        attempt = 0
        while attempt < 3:
            attempt += 1
            try:
                json_obj, meta = ask_for_json(
                    prompt=user_prompt,
                    system=SYSTEM_PROMPT,
                    temperature=0.0,  # deterministic for validation
                )
                # Validate with Pydantic
                record = CleanRecord(**json_obj)
                # Success – store cleaned record and token usage
                results.append(
                    {
                        "original_index": idx,
                        "sample": row["sample"],
                        "treatment": record.treatment,
                        "cell_line": record.cell_line,
                        "replicate": record.replicate,
                    }
                )
                token_log.append(
                    {
                        "row": idx,
                        "attempt": attempt,
                        "prompt_tokens": meta["usage"].prompt_tokens,
                        "completion_tokens": meta["usage"].completion_tokens,
                        "total_tokens": meta["usage"].total_tokens,
                    }
                )
                break  # exit retry loop
            except (ValidationError, ValueError) as e:
                # If we are on the last attempt, record the failure
                if attempt == 3:
                    results.append(
                        {
                            "original_index": idx,
                            "sample": row["sample"],
                            "error": str(e),
                            "last_attempt_prompt": user_prompt,
                            "last_raw_response": meta.get("raw") if "meta" in locals() else None,
                        }
                    )
                    token_log.append(
                        {
                            "row": idx,
                            "attempt": attempt,
                            "error": str(e),
                        }
                    )
                else:
                    # Prepare a feedback message for the next try
                    feedback = f"Your previous output was invalid: {e}. Please correct it and output ONLY a valid JSON object matching the schema."
                    # Replace the user prompt with one that includes the feedback
                    user_prompt = (
                        f"{build_user_prompt(row)}\n\n"
                        f"Feedback from validation: {feedback}"
                    )
                    continue

    # ----------------------------------------------------------------------
    # Assemble the cleaned DataFrame and save
    # ----------------------------------------------------------------------
    df_clean = pd.DataFrame([r for r in results if "error" not in r])
    df_errors = pd.DataFrame([r for r in results if "error" in r])

    outputs_dir = Path("outputs")
    outputs_dir.mkdir(exist_ok=True)
    df_clean.to_csv(outputs_dir / "clean_metadata.csv", index=False)
    df_errors.to_csv(outputs_dir / "cleaning_errors.csv", index=False)
    pd.DataFrame(token_log).to_csv(outputs_dir / "token_usage.csv", index=False)

    print(f"Cleaned rows: {len(df_clean)}")
    print(f"Rows with errors after retries: {len(df_errors)}")
    print("Token usage summary (first few rows):")
    print(pd.DataFrame(token_log).head())

    # ----------------------------------------------------------------------
    # Quick sanity check – compare with the known good metadata
    # ----------------------------------------------------------------------
    good_path = DATA_DIR / "airway_samples.csv"
    df_good = pd.read_csv(good_path)[["run_id", "cell", "dex"]].rename(
        columns={"run_id": "sample", "cell": "cell_line", "dex": "dex_raw"}
    )
    df_good["treatment"] = df_good["dex_raw"].map({"trt": "dexamethasone", "untrt": "untreated"})
    df_good = df_good[["sample", "treatment", "cell_line"]]
    df_good["replicate"] = None  # the airway design has no technical replicates

    comparison_columns = ["sample", "treatment", "cell_line", "replicate"]
    print("\nCleaned metadata:")
    print(df_clean[comparison_columns].sort_values("sample").reset_index(drop=True))
    print("\nReference metadata:")
    print(df_good[comparison_columns].sort_values("sample").reset_index(drop=True))
    return


if __name__ == "__main__":
    app.run()
