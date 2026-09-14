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
    # Ch 9: Dictionaries

    The index in a list is an integer, additionally, all indexes are consecutively occupied and order matters. That is great for some data. But other data make more sense to index by something else.

    Dictionaries provide a key-value pair where the index, or key, can be a variety of types and is associated with a value. There is no inherent order to a dictionary.

    The text shows the `dict()` function to create an empty dictionary, you can also just use {} or start by assigning a key-value pair.
    """)
    return


@app.cell
def _():
    _eng2sp = dict()
    type(_eng2sp)
    return


@app.cell
def _():
    test={}
    type(test)
    return


@app.cell
def _():
    test2={'one':'uno'}
    type(test2)
    return


@app.cell
def _():
    _eng2sp = {'one': 'uno', 'two': 'dos', 'three': 'tres'}
    print(_eng2sp)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Exercise 1 (p. 111)

    The `words.txt` file is in `/blue/bsc4452/share/Class_Files/Py4E_files/code3`.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 9.1 Dictionary as a set of counters

    Cool stuff here...
    """)
    return


@app.cell
def _():
    _word = 'brontosaurus'
    d = {}  # Seems easier to me than dict()
    for _c in _word:
        if _c not in d:
            d[_c] = 1
        else:
            d[_c] = d[_c] + 1
    print(d)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Notice the insertion order being retained!

    ### `get`
    """)
    return


@app.cell
def _():
    counts = { 'chuck' : 1 , 'annie' : 42, 'jan': 100}
    print(counts.get('jan', 0))

    print(counts.get('tim', "Tim isn't here"))  # get takes a key and default value
    return


@app.cell
def _():
    _word = 'brontosaurus'
    d_1 = dict()
    for _c in _word:
        d_1[_c] = d_1.get(_c, 0) + 1
    print(d_1)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 9.3 Looping and dictionaries (p. 114)

    Here's the example in the text:
    """)
    return


@app.cell
def _():
    counts_1 = {'chuck': 1, 'annie': 42, 'jan': 100}
    for _key in counts_1:
        print(_key, counts_1[_key])
    return (counts_1,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    But what if we wanted the output to be sorted alphabetically?

    The text makes a list of the keys, sorts that, and loops over the list:
    """)
    return


@app.cell
def _(counts_1):
    lst = list(counts_1.keys())
    print(lst)
    lst.sort()
    for _key in lst:
        print(_key, counts_1[_key])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    But Python has a `sorted()` function that makes this easier...
    """)
    return


@app.cell
def _(counts_1):
    for _key in sorted(counts_1):
        print(_key, counts_1[_key])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    We can also sort by values:
    """)
    return


@app.cell
def _(counts_1):
    counts_1['matt'] = 0
    for _key in sorted(counts_1, key=counts_1.__getitem__):
        print(_key, counts_1[_key])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 9.4 Advanced text parsing (p. 115)

    Take a look at this.

    Note the `string.punctuation`:
    """)
    return


@app.cell
def _():
    import string
    string.punctuation
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Check out `count2.py`
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Ch 10: Tuples

    I don't use these a lot, but there are some good things in this chapter.

    One is the idea of tuple assignment...

    ## Section 10.3 Tuple assignment
    """)
    return


@app.cell
def _():
    m = ['have', 'fun']
    _x, _y = m
    print(_x)
    print(_y)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    This is frequently used with functions that return multiple values!
    """)
    return


@app.cell
def _():
    def powers(x):
        square = _x ** 2
        cube = _x ** 3
        quad = _x ** 4
        return (square, cube, quad)
    _x, _y, _z = powers(2)
    print(_x, _y, _z)
    return (powers,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    As noted at the start of the chapter, you don't need to have the parentheses around the x,y,z to create tuple--stylistically, the "pythonic" way is to not use them in this case
    """)
    return


@app.cell
def _(powers):
    # Be careful with number of variables on the left
    _x, _y, _z, a = powers(4)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Section 10.4: Dictionaries and tuples

    This goes into the `items` method of dictionaries that returns a list of tuples:
    """)
    return


@app.cell
def _():
    d_2 = {'a': 10, 'b': 1, 'c': 22}
    t = list(d_2.items())
    print(t)
    print(t[0])
    print('\n-------------------\n')
    t = d_2.items()
    # Note the list() above and what happens without it
    print(t)
    print(t[0])
    return (d_2,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 10.5 Multiple assignment with dictionaries (p. 125)

    This section shows the reasoning behind a common Python construct...Combining `items` with tuple multiple assignment and a `for` loop (interestingly, we don't need, but can use, the `list()` here):
    """)
    return


@app.cell
def _(d_2):
    for _key, val in d_2.items():
        print(val, _key)
    return


if __name__ == "__main__":
    app.run()
