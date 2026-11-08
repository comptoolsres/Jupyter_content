"""build_course_data.py: builds airway.db and messy_metadata.csv from the exported CSVs."""
import random
import sqlite3
import pandas as pd

random.seed(42)

counts = pd.read_csv("data/airway_counts.csv")
samples = pd.read_csv("data/airway_samples.csv")
genes = pd.read_csv("data/genes.csv")

# Long-format counts for SQL
counts_long = counts.melt(id_vars="gene_id", var_name="run_id", value_name="count")

with sqlite3.connect("data/airway.db") as con:
    samples.to_sql("samples", con, if_exists="replace", index=False)
    genes.to_sql("genes", con, if_exists="replace", index=False)
    counts_long.to_sql("counts", con, if_exists="replace", index=False)
    con.execute("CREATE INDEX IF NOT EXISTS idx_counts_gene ON counts(gene_id)")
    con.execute("CREATE INDEX IF NOT EXISTS idx_counts_run ON counts(run_id)")

# Messy metadata: simulate an inconsistent hand-typed sample sheet
trt_variants = ["Dex", "dexamethasone 1uM", "DEX treated", "dex+", "1 uM Dexameth."]
ctl_variants = ["untrt", "ctrl", "Untreated", "vehicle", "none", "control (EtOH)"]
cell_variants = lambda c: random.choice([c, c.lower(), f"line {c}", c.replace("N", "N-")])

rows, key = [], []
for _, s in samples.iterrows():
    treated = s["dex"] == "trt"
    rows.append({
        "sample": s["run_id"],
        "condition": random.choice(trt_variants if treated else ctl_variants),
        "donor_line": cell_variants(s["cell"]),
        "notes": random.choice(["", "rerun", "lib prep batch 2", "QC ok", ""]),
    })
    key.append({"sample": s["run_id"],
                "treatment": "dexamethasone" if treated else "untreated",
                "cell_line": s["cell"]})

pd.DataFrame(rows).to_csv("data/messy_metadata.csv", index=False)
pd.DataFrame(key).to_csv("data/messy_metadata_answer_key.csv", index=False)
print("Done:", len(counts_long), "count rows;", len(rows), "samples")
