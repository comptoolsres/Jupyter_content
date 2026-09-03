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
    # Another look a JOINs

    I've gotten a lot of questions about JOINs, so I think I didn't cover them very well. Here are some additional examples and information.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Examples of JOINs

    This [PySheets page](https://www.pythonsheets.com/notes/python-sqlalchemy.html) has some good examples of sqlalchemy code that may come in handy.

    The examples below combine some of the examples from there and add some additional examples to try to help explain joins and how they work.

    I did change the names to make it a bit easier to follow the examples.

    ## Setup the database:
    """)
    return


@app.cell
def _():
    from sqlalchemy import create_engine
    from sqlalchemy import MetaData
    from sqlalchemy import Table
    from sqlalchemy import Column
    from sqlalchemy import Integer
    from sqlalchemy import String
    from sqlalchemy import select

    db_uri = 'sqlite:///db.sqlite'
    engine = create_engine(db_uri)

    # create table
    meta = MetaData(engine)
    table = Table('user', meta,
       Column('id', Integer, primary_key=True),
       Column('l_name', String),
       Column('f_name', String))
    meta.create_all()

    # insert data via insert() construct
    ins = table.insert().values(
          l_name='Jones',
          f_name='Fred')
    conn = engine.connect()
    conn.execute(ins)

    # insert multiple data
    conn.execute(table.insert(),[
       {'l_name':'Smith','f_name':'Mary'},
       {'l_name':'Lopez','f_name':'Victor'}])

    meta = MetaData(engine, reflect=True)
    email_t = Table('email_addr', meta,
          Column('id', Integer, primary_key=True),
          Column('email',String),
          Column('name',String))
    meta.create_all()

    # ** Note **: This is in this format because I am combining
    #   a couple of examples from the original source. "table" already
    #   has this information, but I left it here to serve as an example
    #   of loading a table from meta.

    # get user table
    user_t = meta.tables['user']

    # insert
    conn = engine.connect()
    conn.execute(email_t.insert(),[
       {'email':'ker@test','name':'Smith'},
       {'email':'yo@test','name':'Lopez'},
       {'email':'fun@name','name':'Johnson'}])
    return MetaData, Table, conn, create_engine, email_t, select, user_t


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Check the data in the tables
    """)
    return


@app.cell
def _(conn, select, user_t):
    # select * from 'user_t'
    _select_st = select([user_t])
    _res = conn.execute(_select_st)
    for _row in _res:
        print(_row)
    return


@app.cell
def _(conn, email_t, select):
    # select * from 'email_t'
    _select_st = select([email_t])
    _res = conn.execute(_select_st)
    for _row in _res:
        print(_row)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Non-overlapping data

    Notice that I have added some non-overlapping data in each of the tables. There is no email for Fred Jones and no user for fun@name, Johnson.

    This will let us see how JOINs work.

    ## JOIN
    Let's start with a simple JOIN. The PySheets page does this in two steps, creating a `join_obj` and then the `sel_st`:
    """)
    return


@app.cell
def _(conn, email_t, select, user_t):
    # join statement
    _join_obj = user_t.join(email_t, email_t.c.name == user_t.c.l_name)
    _sel_st = select([user_t.c.l_name, email_t.c.email]).select_from(_join_obj)
    _res = conn.execute(_sel_st)
    # using select_from
    for _row in _res:
        print(_row)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    You *can* put it all together, but the statements can get long...
    """)
    return


@app.cell
def _(conn, email_t, select, user_t):
    # First, let's rewrite the JOIN above into a single statement
    _sel_st = select([user_t.c.l_name, email_t.c.email]).select_from(user_t.join(email_t, email_t.c.name == user_t.c.l_name))
    # using select_from
    _res = conn.execute(_sel_st)
    for _row in _res:
        print(_row)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # JOIN vs SELECT WHERE

    SELECT WHERE and JOIN can often produce the same results.

    We can "join" the tables together using the columns and selecting the data where the `l_name` in the users table matches the `name` in the email table.

    There is some discussion of this on the "authoritative" source...Wikipedia: https://en.wikipedia.org/wiki/Join_(SQL)
    """)
    return


@app.cell
def _(conn, email_t, select, user_t):
    _sel_st = select([user_t.c.l_name, email_t.c.email]).where(user_t.c.l_name == email_t.c.name)
    _res = conn.execute(_sel_st)
    for _row in _res:
        print(_row)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # But...

    But remember the non-overlapping data? SELECT WHERE can't get us that data.

    A plain JOIN doesn't return that data, but there are many types of joins.

    Remember this picture:

    ![Visual SQL JOINs](https://www.codeproject.com/KB/database/Visual_SQL_Joins/Visual_SQL_JOINS_orig.jpg)

    A regular join is an inner join--we only get the results where the tables overlap.

    ## Outer JOIN
    """)
    return


@app.cell
def _(conn, email_t, select, user_t):
    # Outer join (inferred to be a left join-- user_t is 1st, so left)
    _join_obj = user_t.outerjoin(email_t, user_t.c.l_name == email_t.c.name)
    _sel_st = select([user_t.c.l_name, email_t.c.email]).select_from(_join_obj)
    _res = conn.execute(_sel_st)
    for _row in _res:
        print(_row)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Notice the 1st line of the output:

    `('Jones', None)`

    We get the name from the left table (user_t), but there isn't a corresponding entry in the email_t table, so we get "None".
    """)
    return


@app.cell
def _(conn, email_t, select, user_t):
    # Outer join, same as above but using the isouter syntax
    _join_obj = user_t.join(email_t, user_t.c.l_name == email_t.c.name, isouter=True)
    _sel_st = select([user_t.c.l_name, email_t.c.email]).select_from(_join_obj)
    _res = conn.execute(_sel_st)
    for _row in _res:
        print(_row)
    return


@app.cell
def _(conn, email_t, select, user_t):
    # Full join
    _join_obj = user_t.join(email_t, user_t.c.l_name == email_t.c.name, full=True)
    _sel_st = select([user_t.c.l_name, email_t.c.email]).select_from(_join_obj)
    _res = conn.execute(_sel_st)
    for _row in _res:
        print(_row)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Hmmm...RIGHT and FULL OUTER JOINs are not currently supported

    That's too bad.

    We can fake a RIGHT join by switching the order of tables...
    """)
    return


@app.cell
def _(conn, email_t, select, user_t):
    # Cheating to make a right join...switch the tables around...
    _join_obj = email_t.outerjoin(user_t, user_t.c.l_name == email_t.c.name)
    _sel_st = select([user_t.c.l_name, email_t.c.email]).select_from(_join_obj)
    _res = conn.execute(_sel_st)
    for _row in _res:
        print(_row)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    This is actually what [this blog post](https://weblogs.sqlteam.com/jeffs/2007/04/19/full-outer-joins/) suggests doing for readability.

    There is also the question of why you would want a FULL JOIN...again, the above posts suggests against it.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Another but...

    In searching how to write JOINs in SQLAlchemy, you may have run across two (or more) methods of making SQL quries in the first place...

    Sometimes, you will find something line we have with `select`:

    ```python
    sel_st = select([user_t.c.l_name, email_t.c.email]).where(user_t.c.l_name==email_t.c.name)
    ```

    Sometimes, you will find something more like:

    ```python
    s.query(Employee).filter(Employee.name.startswith("C")).one().name
    ```

    Turns out these are the difference between the SQL expression language and ORM. There's a good post on this [here](https://groups.google.com/forum/#!topic/sqlalchemy/IXins449qOo).
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Another example using the world.sqlite database

    Let's look at another example of joins, using the ORM version of things with `query`.

    First we need to load the database:
    """)
    return


@app.cell
def _(MetaData, Table, create_engine):
    #!/usr/bin/env python
    from sqlalchemy import sql, join
    engine_1 = create_engine('sqlite:///../data/world.sqlite')
    DBInfo = MetaData(engine_1)
    conn_1 = engine_1.connect()
    city = Table('city', DBInfo, autoload=True)
    country = Table('country', DBInfo, autoload=True)
    countrylanguage = Table('countrylanguage', DBInfo, autoload=True)
    return conn_1, country, countrylanguage, engine_1


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    When we first looked at this data, we used this command as an example of a join in SQL:

    ```sql
    sqlite> select Name,Language,Percentage FROM country JOIN countrylanguage ON Code=CountryCode WHERE Language='Portuguese' ORDER BY Percentage DESC;
    Name        Language    Percentage
    ----------  ----------  ----------
    Portugal    Portuguese  99.0
    Brazil      Portuguese  97.5
    Luxembourg  Portuguese  13.0
    Andorra     Portuguese  10.8
    Guinea-Bis  Portuguese  8.1
    Paraguay    Portuguese  3.2
    Macao       Portuguese  2.3
    France      Portuguese  1.2
    Canada      Portuguese  0.7
    United Sta  Portuguese  0.2
    Cape Verde  Portuguese  0.0
    East Timor  Portuguese  0.0
    sqlite>
    ```
    """)
    return


@app.cell
def _(country, countrylanguage, engine_1):
    from sqlalchemy.orm import sessionmaker
    Session = sessionmaker(bind=engine_1)
    session = Session()
    _res = session.query(country.c.Name, countrylanguage.c.Language, countrylanguage.c.Percentage).join(countrylanguage).filter(countrylanguage.c.Language == 'Portuguese')
    for _row in _res:
        print(_row)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    One thing to note that I discovered in debugging this--yes it took a couple of hours to write this--is that because there is only one foreign key between the tables, we don't need to specify country.c.Code==countrycode.c.CountryCode...SQLAlchemy knows to make this linkage.

    And using the SQL Expression select version...
    """)
    return


@app.cell
def _(conn_1, country, countrylanguage, select):
    _join_obj = country.join(countrylanguage)
    _sel_st = select([country.c.Name, countrylanguage.c.Language, countrylanguage.c.Percentage]).select_from(_join_obj).where(countrylanguage.c.Language == 'Portuguese')
    _res = conn_1.execute(_sel_st)
    for _row in _res:
        print(_row)
    return


if __name__ == "__main__":
    app.run()
