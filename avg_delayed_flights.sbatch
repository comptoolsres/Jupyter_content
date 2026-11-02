#!/bin/bash
#SBATCH --job-name=avg_delayed
#SBATCH --account=bsc4452
#SBATCH --qos=bsc4452
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --mem=8gb
#SBATCH --time=00:30:00
#SBATCH --output=avg_delayed_%j.log

# Usage: sbatch avg_delayed_flights.sbatch /path/to/flight_data_2024.csv [arrival|departure]
# Writes <input name>_avg_delayed.csv to the directory you submit from.

set -euo pipefail

INPUT=${1:?Usage: sbatch avg_delayed_flights.sbatch INPUT.csv [arrival|departure]}
TYPE=${2:-arrival}
OUTPUT="$(basename "${INPUT%.csv}")_avg_delayed.csv"

# Run from the project directory so uv uses its environment (marimo, pandas)
cd /blue/bsc4452/magitz/Jupyter_content
OUTDIR=${SLURM_SUBMIT_DIR:-$PWD}

uv run python flight_data.mo.py --input "$INPUT" --output "$OUTDIR/$OUTPUT" --type "$TYPE"
echo "Wrote $OUTDIR/$OUTPUT"
