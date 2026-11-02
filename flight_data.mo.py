import marimo

__generated_with = "0.25.2"
app = marimo.App()


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Average delayed flights per month

    Calculates the average number of delayed flights for each calendar month from
    BTS on-time performance data
    ([source](https://www.transtats.bts.gov/DL_SelectFields.asp)).

    **Workflow note:** the subsample file below is only for initial set up. Once
    the notebook works, point `data_file` at the full data file for each year.

    A flight counts as *delayed* when it was 15 or more minutes late
    (`ArrDel15` / `DepDel15` equal to 1). Delayed flights are counted per
    year-month, then averaged across the years present in the file. With a
    single-year file the "average" is simply that year's count for each month.
    """)
    return


@app.cell
def _():
    import pandas as pd

    return (pd,)


@app.cell
def _(mo):
    # Override with CLI args, e.g.:
    #   marimo run flight_data.mo.py -- --input data.csv --output out.csv --type departure
    #   python flight_data.mo.py --input data.csv --output out.csv
    # Defaults below use the subsample file (initial set up only).
    _args = mo.cli_args()
    data_file = _args.get(
        "input", "/blue/bsc4452/share/Class_Files/data/flight_data_by_year/subsample_100_GNV.csv"
    )
    output_file = _args.get("output", "avg_delayed_flights_per_month.csv")
    delay_type = _args.get("type", "arrival")  # "arrival" (ArrDel15) or "departure" (DepDel15)
    return data_file, delay_type, output_file


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Load the data

    Only the columns needed are read, which keeps memory use low for the full
    yearly files. `index_col=False` handles the trailing comma BTS puts on the
    header line.
    """)
    return


@app.cell
def _(data_file, delay_type, pd):
    delay_col = "ArrDel15" if delay_type == "arrival" else "DepDel15"
    df = pd.read_csv(data_file, usecols=["Year", "Month", delay_col], index_col=False)
    df.head()
    return delay_col, df


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Calculate

    Count delayed flights per year-month (filling in months with zero delays),
    then average across years for each calendar month.
    """)
    return


@app.cell
def _(delay_col, df, pd):
    _delayed = df[delay_col].eq(1).groupby([df["Year"], df["Month"]]).sum()
    years = sorted(df["Year"].unique())
    _full_index = pd.MultiIndex.from_product([years, range(1, 13)], names=["Year", "Month"])
    _delayed = _delayed.reindex(_full_index, fill_value=0)

    result = (
        _delayed.groupby("Month").mean()
        .rename("Avg_Delayed_Flights").round(2).reset_index()
    )
    result
    return result, years


@app.cell(hide_code=True)
def _(mo, years):
    mo.md(f"## Save results\n\nData covers {len(years)} year(s): {years[0]}–{years[-1]}.")
    return


@app.cell
def _(mo, output_file, result):
    result.to_csv(output_file, index=False)
    mo.md(f"Saved to `{output_file}`")
    return


if __name__ == "__main__":
    app.run()
