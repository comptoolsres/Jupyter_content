import marimo

__generated_with = "0.24.0"
app = marimo.App()


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # SQLAlchemy

    We'll start off using the world.sqlite database again.

    Rather than import all of sqlalchemy and then need to preface each method with the module name, we're importing a lot of individual methods.
    """)
    return


@app.cell
def _():
    #!/usr/bin/env python
    from sqlalchemy import create_engine
    from sqlalchemy import MetaData
    from sqlalchemy import Table, Column
    from sqlalchemy import Integer, String
    from sqlalchemy import sql, select, join, desc

    # Create a Engine object which is our handle into the database.
    engine = create_engine('sqlite:///../world.sqlite')

    # Connect to the database
    conn = engine.connect()

    # Read the metadata from the existing database.
    #  Since the database already exists and has tables defined, we can create Python objects based on these automatically.
    DBInfo=MetaData(engine)
    return (
        Column,
        DBInfo,
        Integer,
        MetaData,
        String,
        Table,
        conn,
        create_engine,
        desc,
        select,
    )


@app.cell
def _(DBInfo, Table, conn, select):
    # Auto-create the city object based on the metadata read into the DBInfo.
    city = Table('city', DBInfo, autoload=True)
    _query = select([city.c.ID, city.c.Name, city.c.Population]).limit(10)
    # Mirroring this command: SELECT Id, Name, Population FROM city LIMIT 10;
    _result = conn.execute(_query)
    for _row in _result:
        print(_row)
    return (city,)


@app.cell
def _(city, conn, select):
    # Mirroring this command: SELECT Id, Name, Population FROM city WHERE Population > 5000000;
    _query = select([city.c.ID, city.c.Name, city.c.Population]).where(city.c.Population > 5000000)
    _result = conn.execute(_query)
    for _row in _result:
        print(_row)
    return


@app.cell
def _(city, conn, desc, select):
    # Mirroring this command: 
    #   SELECT Id, Name, Population FROM city WHERE Population > 5000000 ORDER BY Population DESC LIMIT 10;
    _query = select([city.c.ID, city.c.Name, city.c.Population]).where(city.c.Population > 5000000).order_by(desc(city.c.Population)).limit(10)
    _result = conn.execute(_query)
    for _row in _result:
        print(_row)
    print(_result)
    return


@app.cell
def _(DBInfo, Table, conn, desc, select):
    # Mirroring this command:
    # select Name,Language,Percentage FROM country JOIN countrylanguage ON Code=CountryCode WHERE Language='Portuguese' ORDER BY Percentage DESC;
    country = Table('country', DBInfo, autoload=True)
    countrylanguage = Table('countrylanguage', DBInfo, autoload=True)
    print(select([country.c.Name, countrylanguage.c.Language, countrylanguage.c.Percentage]).select_from(country.join(countrylanguage)).where(countrylanguage.c.Language == 'Portuguese').order_by(desc(countrylanguage.c.Percentage)))
    _query = select([country.c.Name, countrylanguage.c.Language, countrylanguage.c.Percentage]).select_from(country.join(countrylanguage)).where(countrylanguage.c.Language == 'Portuguese').order_by(desc(countrylanguage.c.Percentage))
    _result = conn.execute(_query)
    for _row in _result:
        print(_row)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Inserting

    I made this following the information on this page: https://docs.sqlalchemy.org/en/13/core/tutorial.html#coretutorial-insert-expressions
    """)
    return


@app.cell
def _(city):
    print(city.insert())
    return


@app.cell
def _(city):
    my_insert=city.insert().values(Name='Gainesville', CountryCode='USA',District='TX',Population=16612)
    print(my_insert)
    return (my_insert,)


@app.cell
def _(conn, my_insert):
    _result = conn.execute(my_insert)
    return


@app.cell
def _(city, conn, select):
    _query = select([city.c.ID, city.c.Name, city.c.District, city.c.Population]).where(city.c.Name.like('Gain%'))
    _result = conn.execute(_query)
    for _row in _result:
        print(_row)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Creating database in SQLAlchemy
    """)
    return


@app.cell
def _(create_engine):
    engine_1 = create_engine('sqlite:///test.sqlite', echo=True)
    return (engine_1,)


@app.cell
def _(Column, Integer, MetaData, String, Table):
    from sqlalchemy import ForeignKey
    metadata = MetaData()
    users = Table('users', metadata, Column('id', Integer, primary_key=True), Column('name', String), Column('fullname', String))
    addresses = Table('addresses', metadata, Column('id', Integer, primary_key=True), Column('user_id', None, ForeignKey('users.id')), Column('email_address', String, nullable=False))
    return (metadata,)


@app.cell
def _(engine_1, metadata):
    metadata.create_all(engine_1)
    return


if __name__ == "__main__":
    app.run()
