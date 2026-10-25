import marimo

__generated_with = "0.24.0"
app = marimo.App()


@app.cell
def _():
    import marimo as mo
    from sqlalchemy import create_engine, MetaData, Table, select, desc

    return mo, create_engine, MetaData, Table, select, desc


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
# SQLAlchemy (2.0 style)

We'll start off using the world.sqlite database again.

This marimo notebook uses modern SQLAlchemy 2.x Core patterns.
"""
    )
    return


@app.cell
def _(MetaData, create_engine):
    engine = create_engine("sqlite:///../world.sqlite")
    metadata = MetaData()
    return engine, metadata


@app.cell
def _(Table, engine, metadata, select):
    city = Table("city", metadata, autoload_with=engine)
    query = select(city.c.ID, city.c.Name, city.c.Population).limit(10)
    with engine.connect() as conn:
        for row in conn.execute(query):
            print(row)
    return city


@app.cell
def _(city, engine, select):
    query = select(city.c.ID, city.c.Name, city.c.Population).where(city.c.Population > 5_000_000)
    with engine.connect() as conn:
        for row in conn.execute(query):
            print(row)
    return


@app.cell
def _(city, desc, engine, select):
    query = (
        select(city.c.ID, city.c.Name, city.c.Population)
        .where(city.c.Population > 5_000_000)
        .order_by(desc(city.c.Population))
        .limit(10)
    )
    with engine.connect() as conn:
        for row in conn.execute(query):
            print(row)
    return


@app.cell
def _(Table, desc, engine, metadata, select):
    country = Table("country", metadata, autoload_with=engine)
    countrylanguage = Table("countrylanguage", metadata, autoload_with=engine)

    query = (
        select(country.c.Name, countrylanguage.c.Language, countrylanguage.c.Percentage)
        .select_from(country.join(countrylanguage, country.c.Code == countrylanguage.c.CountryCode))
        .where(countrylanguage.c.Language == "Portuguese")
        .order_by(desc(countrylanguage.c.Percentage))
    )

    print(query)
    with engine.connect() as conn:
        for row in conn.execute(query):
            print(row)

    return city, country, countrylanguage


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
## Inserting

This section uses SQLAlchemy 2.x insert patterns with explicit transaction handling.
"""
    )
    return


@app.cell
def _(city):
    print(city.insert())
    return


@app.cell
def _(city):
    my_insert = city.insert().values(
        Name="Gainesville", CountryCode="USA", District="TX", Population=16612
    )
    print(my_insert)
    return my_insert


@app.cell
def _(engine, my_insert):
    with engine.begin() as conn:
        conn.execute(my_insert)
    return


@app.cell
def _(city, engine, select):
    query = select(city.c.ID, city.c.Name, city.c.District, city.c.Population).where(city.c.Name.like("Gain%"))
    with engine.connect() as conn:
        for row in conn.execute(query):
            print(row)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("## Creating a database in SQLAlchemy 2.x")
    return


@app.cell
def _(create_engine):
    engine_1 = create_engine("sqlite:///test.sqlite", echo=True)
    return engine_1


@app.cell
def _():
    from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey

    metadata = MetaData()

    users = Table(
        "users",
        metadata,
        Column("id", Integer, primary_key=True),
        Column("name", String),
        Column("fullname", String),
    )

    addresses = Table(
        "addresses",
        metadata,
        Column("id", Integer, primary_key=True),
        Column("user_id", Integer, ForeignKey("users.id")),
        Column("email_address", String, nullable=False),
    )

    return metadata, users, addresses


@app.cell
def _(engine_1, metadata):
    metadata.create_all(engine_1)
    return


if __name__ == "__main__":
    app.run()
