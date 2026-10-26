import marimo

__generated_with = "0.24.0"
app = marimo.App()


@app.cell
def _():
    import marimo as mo
    from sqlalchemy import (
        Column,
        ForeignKey,
        Integer,
        MetaData,
        String,
        Table,
        create_engine,
        desc,
        select,
    )

    return (
        Column,
        ForeignKey,
        Integer,
        MetaData,
        String,
        Table,
        create_engine,
        desc,
        mo,
        select,
    )


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # SQLAlchemy (2.0 style)

    We'll start off using the world.sqlite database again.

    This marimo notebook uses modern SQLAlchemy 2.x Core patterns.
    """)
    return


@app.cell
def _(MetaData, create_engine):
    # Create an Engine object which is our handle into the database.
    engine = create_engine('sqlite:///../world.sqlite')

    # MetaData holds table definitions reflected from the existing database.
    DBInfo = MetaData()
    return DBInfo, engine


@app.cell
def _(DBInfo, Table, engine, select):
    # Auto-create the city object by reflecting the table from the database.
    city = Table('city', DBInfo, autoload_with=engine)

    # Mirroring this command: SELECT Id, Name, Population FROM city LIMIT 10;
    _query = select(city.c.ID, city.c.Name, city.c.Population).limit(10)
    with engine.connect() as _conn:
        for _row in _conn.execute(_query):
            print(_row)
    return (city,)


@app.cell
def _(city, engine, select):
    # Mirroring this command: SELECT Id, Name, Population FROM city WHERE Population > 5000000;
    _query = select(city.c.ID, city.c.Name, city.c.Population).where(
        city.c.Population > 5000000
    )
    with engine.connect() as _conn:
        for _row in _conn.execute(_query):
            print(_row)
    return


@app.cell
def _(city, desc, engine, select):
    # Mirroring this command:
    #   SELECT Id, Name, Population FROM city WHERE Population > 5000000 ORDER BY Population DESC LIMIT 10;
    _query = (
        select(city.c.ID, city.c.Name, city.c.Population)
        .where(city.c.Population > 5000000)
        .order_by(desc(city.c.Population))
        .limit(10)
    )
    with engine.connect() as _conn:
        _result = _conn.execute(_query)
        for _row in _result:
            print(_row)
    print(type(_result))
    return


@app.cell
def _(DBInfo, Table, desc, engine, select):
    # Mirroring this command:
    # SELECT Name, Language, Percentage FROM country JOIN countrylanguage ON Code=CountryCode
    #   WHERE Language='Portuguese' ORDER BY Percentage DESC;
    country = Table('country', DBInfo, autoload_with=engine)
    countrylanguage = Table('countrylanguage', DBInfo, autoload_with=engine)

    _query = (
        select(country.c.Name, countrylanguage.c.Language, countrylanguage.c.Percentage)
        .select_from(
            country.join(countrylanguage, country.c.Code == countrylanguage.c.CountryCode)
        )
        .where(countrylanguage.c.Language == 'Portuguese')
        .order_by(desc(countrylanguage.c.Percentage))
    )
    print(_query)

    with engine.connect() as _conn:
        for _row in _conn.execute(_query):
            print(_row)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Inserting

    This section uses SQLAlchemy 2.x insert patterns. Writes use `engine.begin()`, which opens a transaction and commits automatically when the block finishes (or rolls back on error).
    """)
    return


@app.cell
def _(city):
    print(city.insert())
    return


@app.cell
def _(city):
    my_insert = city.insert().values(
        Name='Gainesville', CountryCode='USA', District='TX', Population=16612
    )
    print(my_insert)
    return (my_insert,)


@app.cell
def _(engine, my_insert):
    with engine.begin() as _conn:
        _conn.execute(my_insert)
    return


@app.cell
def _(city, engine, select):
    _query = select(
        city.c.ID, city.c.Name, city.c.District, city.c.Population
    ).where(city.c.Name.like('Gain%'))
    with engine.connect() as _conn:
        for _row in _conn.execute(_query):
            print(_row)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Creating a database in SQLAlchemy 2.x
    """)
    return


@app.cell
def _(create_engine):
    test_engine = create_engine('sqlite:///test.sqlite', echo=True)
    return (test_engine,)


@app.cell
def _(Column, ForeignKey, Integer, MetaData, String, Table):
    new_metadata = MetaData()

    users = Table(
        'users',
        new_metadata,
        Column('id', Integer, primary_key=True),
        Column('name', String),
        Column('fullname', String),
    )

    addresses = Table(
        'addresses',
        new_metadata,
        Column('id', Integer, primary_key=True),
        Column('user_id', Integer, ForeignKey('users.id')),
        Column('email_address', String, nullable=False),
    )
    return (new_metadata,)


@app.cell
def _(new_metadata, test_engine):
    new_metadata.create_all(test_engine)
    return


if __name__ == "__main__":
    app.run()
