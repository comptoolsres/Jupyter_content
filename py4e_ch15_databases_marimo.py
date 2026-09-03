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
    # Ch 15: Databases and SQL

    Chapter 15 of Py4E gets into databases and the first sections are a good place to start.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 15.1 What is a database? (p. 181)
    I do like Charles Severance's (the Py4E author) idea that, at its foundation
    >"a database is a file that is organized for storing data."
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Charles goes on to liken databases to Python dictionaries, except that they **store their data on disk** rather than in a data structure in memory. This allows a database to store more data.

    Databases are designed not only to store data, but to access that data--and access it quickly! Indexing the stored data is one method used by database systems to speed up data access.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Database Systems
    ### Also called Relational Database Managements Systems (RDMS)
     * Usually server-based
     * Client-Server model
     * Performance and Scalability
     * ACID (Atomicity, Consistency, Isolation, Durability)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Databases can range from the example we'll use below, which requires nothing more than the Python install we've been using all along, to supercomputer sized systems used by large corporations. More than just a file, databases are managed by their own software, and often that software runs on a server.

    While we will use SQLite for this class, which is designed to be light-weight and can be embedded in other applications (like your web browser as Py4E points out), the same concepts scale up to larger databases and server-based systems.

    Why use a server? For one, as databases grow, their files grow. Also, more compute power is needed to quickly access that data. So, for larger databases, larger computers, typically servers are needed--*this can also scale to clusters of computers*. Also, larger databases tend to be used by more than one person at a time. Server-based databases are typically set up with a **client-server model**, where the database is running on a server that users do not actively log into. Users connect to the server using the client. This allows the server to be dedicated to processing client queries and allows the server to be setup to manage concurrent use from multiple users. If multiple users try to change the same file on a computer at the same time, file corruption can happen. Using the client-server model prevents this.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Common Database Systems

     * [SQLite](https://sqlite.org/index.html)
         * Free
         * Small
         * Not server-based
     * [MySQL](https://www.mysql.com/)
         * Free (Community Server)
         * Relatively common and robust
     * [PostgreSQL](https://www.postgresql.org/)
         * Free
         * Geospatial extensions
     * [Oracle](https://www.oracle.com/index.html)
         * Commercial
         * UF Licensed
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Desktop databases software
     * FileMaker
     * Microsoft Access
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### NOSQL (Non SQL, or Not Only SQL) Databases
     * [MongoDB](https://www.mongodb.com/)
        * A document-based DB
        * MongoDB stores data in flexible, JSON-like documents, meaning fields can vary from document to document and data structure can be changed over time
     * [Cassandra](http://cassandra.apache.org/)
         * A wide column DB
     * [neo4j](https://neo4j.com/)
         * A graph-based DB
         ![neo4j graph representation](https://s3.amazonaws.com/dev.assets.neo4j.com/wp-content/uploads/20170731095054/Property-Graph-Concepts-Simple.svg)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Tables

    ### Revisiting [Browman & Woo (2018)](https://www.tandfonline.com/doi/full/10.1080/00031305.2017.1375989)

    ![Figure 2 of Browman & Woo 2018, showing examples of spreadsheets that violate best practices](https://www.tandfonline.com/cms/asset/a2e180fa-d5e2-41d2-a5ab-bb19a4844e1b/utas_a_1375989_f0002_b.jpg)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    We've worked with tables a lot already in class. Every problem set has had a table of data, we've parsed tables reading line-by-line, we've loaded tables into Pandas dataframes, and we had a reading ([Browman and Woo 2018)](https://www.tandfonline.com/doi/full/10.1080/00031305.2017.1375989)) that made recommendations for how to best store data in tables (spreadsheets are essentially tables of data).

    Databases extend tables.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 15.4 Creating a database table (p. 182)

    Python has SQLite built in, you just need to import it.
    """)
    return


@app.cell
def _():
    import sqlite3
    _conn = sqlite3.connect('music.sqlite')
    _cur = _conn.cursor()
    _cur.execute('DROP TABLE IF EXISTS Tracks')
    _cur.execute('CREATE TABLE Tracks (title TEXT, plays INTEGER)')
    # Code: http://www.py4e.com/code3/db1.py
    _conn.close()
    return (sqlite3,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## A lot going on here...

    ```python
    conn = sqlite3.connect('music.sqlite')
    cur = conn.cursor()
    ```
     * Makes a connection, called `conn` in this case, to our database
     * Connection, because databases are often on a server
         * Note that we now have a file called music.sqlite in the current folder
     * Call the `cursor()` method on the connection--similar to `open()` on a file
     * `cur` is similar to a file handle or web socket
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Py4E Figure 15.2: A database cursor
    ![Py4E Figure 15.2: A database cursor](https://www.py4e.com/images/cursor.svg)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ```python
    cur.execute('DROP TABLE IF EXISTS Tracks')
    cur.execute('CREATE TABLE Tracks (title TEXT, plays INTEGER)')
    ```

     * Use the `cur` cursor to execute commands on the connected DB
     * `DROP` (delete) the table "Tracks" if is exists
     * `CREATE` a table "Tracks" with two columns:
         * "title", a text column
         * "plays", an integer column
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Data types

     * Databases typically are very strict about types--the LinkedIn Learning introduction talked about how careful selection of data types and size limits allows databases to be more efficient.
     * SQLite, our DBMS, is an exception:
     >SQLite is "typeless". This means that you can store any kind of data you want in any column of any table, regardless of the declared datatype of that column...This behavior is a feature, not a bug. ... The strong typing system found in most other SQL engines and codified in the SQL language spec is a misfeature. [SQLite Datatypes Page](https://www.sqlite.org/datatypes.html)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Some MySQL data types

    |Data Type| Description|
    |-------|---------------|
    |INTEGER|An integer|
    |FLOAT| Real numbers, including scientific notation|
    |DATE|YYYY-MM-DD|
    |DATETIME|YYYY-MM-DD HH:MM:SS|
    |TEXT| Strings up to 65535 characters|
    |TINYTEXT|Strings up to 255 characters|
    |BLOB|Binary Large Object (e.g., images)|
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Let's add data to our music database
    """)
    return


@app.cell
def _(sqlite3):
    _conn = sqlite3.connect('music.sqlite')
    _cur = _conn.cursor()
    _cur.execute('INSERT INTO Tracks (title, plays) VALUES (?, ?)', ('Thunderstruck', 20))
    _cur.execute('INSERT INTO Tracks (title, plays) VALUES (?, ?)', ('My Way', 15))
    _conn.commit()
    print('Tracks:')
    _cur.execute('SELECT title, plays FROM Tracks')
    for row in _cur:
        print(row)
    _cur.execute('DELETE FROM Tracks WHERE plays < 100')
    _cur.close()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## This looks complicated

    ```python
    cur.execute('INSERT INTO Tracks (title, plays) VALUES (?, ?)',
        ('Thunderstruck', 20))
    ```
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ```python
    conn.commit()
    ```
    From [StackOverflow](https://stackoverflow.com/questions/2847999/why-the-need-to-commit-explicitly-when-doing-an-update)
    > The DB-API spec requires that connecting to the database begins a new transaction, by default. You must `commit` to confirm any changes you make, or `rollback` to discard them.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ```python
    cur.execute('SELECT title, plays FROM Tracks')
    for row in cur:
        print(row)
    ```

    > ('Thunderstruck', 20)

    >  ('My Way', 15)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ```python
    cur.execute('DELETE FROM Tracks WHERE plays < 100')
    ```
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 15.5 Structured Query Language summary (p. 185)

    * Structured Query Language was developed to standardize database interactions among vendors.
       * But there are differences
    * Upper case by convention, but not needed--mostly for readability, which **is* important!
    * We will cover some basics as we go, but...
       * But we will largely use a Python module that converts Python methods to SQL for us

    After Sections 15.5, Py4E continues using the `sqlite3` module for most things, writing SQL in raw text. While this works, one of the issues is that if your project grows, or you move and decide to change the DBMS, those small differences among SQL implementations on different DBMSs often breaks your code--the code here woks for sqlite, but may not work for MySQL or Oracle.

    Another issue is that you are learning another language--SQL. We are still learning Python and the "Pythonic" way of doing things. Wouldn't it be great if we could abstract the details of SQL and write Python code to do our database actions?

    There is (or maybe are...)! SQLAlchemy is this tool--a module that abstracts SQL management, uses a unified language to translate to a large number of common 'dialects' for each DBMS, and more.

    So...we will leave Py4E for now. It is probably worth looking through and reading some of the text, not focusing on the code. Look at the figures and think about how these relate to the figures in the LinkedIn Learning introduction. All of this is similar. And we will do similar things too, but with different code.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
 
    """)
    return


if __name__ == "__main__":
    app.run()
