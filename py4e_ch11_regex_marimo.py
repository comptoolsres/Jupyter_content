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
    # Ch 11: Regular Expressions

    Back to the good old regex!!

    As we've seen with `import math` earlier, Python keeps things relatively stripped down, so in order to use regular expressions, you need to `import re` the regular expression module.
    """)
    return


@app.cell
def _():
    # Search for lines that start with 'From'
    import re
    _hand = open('data/mbox-short.txt')
    for _line in _hand:
        _line = _line.rstrip()
        if re.search('^From:', _line):
    # Code: http://www.py4e.com/code3/re02.py
            print(_line)
    return (re,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Much of this chapter is a review of regular expressions and how to implement them in Python. Have a look over the content and play with the examples.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # 11.2 Extracting data using regular expressions

    Modify `re07.py`, reproduced below, to print a list of unique email addresses from the file.
    """)
    return


@app.cell
def _(re):
    _hand = open('data/mbox-short.txt')
    for _line in _hand:
        _line = _line.rstrip()
        x = re.findall('[a-zA-Z0-9]\\S+@\\S+[a-zA-Z]', _line)
        if len(x) > 0:
            print(x)
    return


if __name__ == "__main__":
    app.run()
