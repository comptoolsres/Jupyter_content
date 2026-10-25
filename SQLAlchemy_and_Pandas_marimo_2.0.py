import marimo

__generated_with = "0.24.0"
app = marimo.App()


@app.cell
def _():
    import marimo as mo
    return mo,


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
# Pandas and SQLAlchemy (2.0 style)

Pandas has several functions to work with databases via SQLAlchemy.

This can be an easier way to get data from a database and to pass data into a database.

Let's start with loading the `world.sqlite` database we've been using.
""")
    return


@app.cell
def _():
    from sqlalchemy import create_engine, MetaData, Table, select

    engine = create_engine('sqlite:////blue/bsc4452/share/Class_Files/data/world.sqlite')
    metadata = MetaData()
    conn = engine.connect()
    return MetaData, Table, conn, create_engine, engine, metadata, select


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
The cell below also mirrors the SQLAlchemy notebook and creates the `city` object from reflected metadata,
builds the `query` variable, and executes it.
""")
    return


@app.cell
def _(Table, engine, metadata, select):
    city = Table('city', metadata, autoload_with=engine)
    query = select(city.c.ID, city.c.Name, city.c.Population).limit(10)
    with engine.connect() as conn:
        result = conn.execute(query)
        for row in result:
            print(row)
    print(type(query))
    return query,


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
## Reading SQL query results into a Pandas data frame

Here's how we can put the result into a pandas data frame.
The selectable and connection are the required arguments for `read_sql`.
In this example, we also set the ID column as the index.
""")
    return


@app.cell
def _(query):
    import pandas as pd
    return pd,


@app.cell
def _(engine, pd, query):
    with engine.connect() as conn:
        df = pd.read_sql(query, conn, index_col='ID')
    df.head()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
## Writing a Pandas data frame to a database

In the next example, we'll use the `shipping_tables.xlsx` table that we used in the
[Pandas_messy_data notebook](Pandas_messy_data.ipynb).

First, we'll get the data into data frames.
""")
    return


@app.cell
def _(pd):
    orders = pd.read_excel('shipping_tables.xlsx', header=1, usecols='B:F')
    orders.head()
    return orders,


@app.cell
def _(pd):
    from openpyxl import load_workbook

    wb = load_workbook(filename='shipping_tables.xlsx')
    sheet = wb['shipping_rates']
    lookup_table = sheet.tables['ship_cost']
    data = sheet[lookup_table.ref]

    rows_list = []
    for row in data:
        cols = []
        for col in row:
            cols.append(col.value)
        rows_list.append(cols)

    ship_rates = pd.DataFrame(data=rows_list[1:], index=None, columns=rows_list[0])
    ship_rates.head()
    return ship_rates,


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
Now we have two Pandas data frames and can create a database and add the data.
""")
    return


@app.cell
def _(create_engine, orders, ship_rates):
    engine = create_engine('sqlite:///shipping.sqlite')

    with engine.begin() as conn:
        orders.to_sql('orders', conn, if_exists='replace', index=False)
        ship_rates.to_sql('ship_rates', conn, if_exists='replace', index=False)

    with engine.connect() as conn:
        print(conn.exec_driver_sql('SELECT * FROM orders LIMIT 5').fetchall())

    return


if __name__ == "__main__":
    app.run()
