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
    # Ch 6: Strings

    Chapter 6 covers strings. I'll cover a few things here, but am hoping not to spend a lot of time on strings in class. Read the chapter, look over this, play with examples and **ask questions**.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 6.1 A string is a sequence (p. 67)

    ### 0-indexing

    The first big thing to learn about stings (and lists) in Python is that they are indexed starting at 0, so the first element in a string or list is the 0<sup>th</sup> element.

    0-indexing in very common in coding languages, but not universal. It takes some getting used to and results in a type of error known as an [off-by-one error](https://en.wikipedia.org/wiki/Off-by-one_error) when you forget. Do your best to remember and try to write code that tests itself to avoid this kind of error sneaking in and creating incorrect results.
    """)
    return


@app.cell
def _():
    # Traversing through a string with a loop: while version
    _fruit = 'banana'
    _index = 0
    while _index < len(_fruit):
        _letter = _fruit[_index]
        print(_index, '-->', _letter)
        _index = _index + 1
    return


@app.cell
def _():
    # Or using a for loop
    _fruit = 'banana'
    for char in _fruit:
        _letter = char
        print(_letter)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 6.4 String slices (p. 69)

    Image 6.1 in the text was used to illustrate indexes for strings. I've redrawn an image from another text that I think helps illustrate string slices.

    ![Python slice illustration](https://raw.githubusercontent.com/comptoolsres/comptoolsres.github.io/master/images/python_string_slices.png)
    """)
    return


@app.cell
def _():
    s="BANANA"
    print("1:", s[0])
    print("2:", s[1:3])
    print("3:", s[3:])
    print("4:", s[:2])
    print("5:", s[-4:-2])
    print("6:", s[-1])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 6.5 Strings are immutable (p. 70)

    Strings, and some other variable types, are immutable--they cannot be changed.

    The example here shows one way around this by making a new variable with the new string, but it may be easier to re-assign the variable:
    """)
    return


@app.cell
def _():
    greeting = 'Hello, world!'
    return (greeting,)


@app.cell
def _(greeting):
    greeting_1 = 'J' + greeting[1:]
    print(greeting_1)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Unlike the example in the text, which has no effect on the original string, in the example above, the original string is erased, and a completely new string is defined. If the goal is to celebrate Jello, mission accomplished either way--it's up to you which makes more sense for what your script is doing.

    One advantage of reassigning is it that we don't need a new variable name.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 6.7 The `in` operator (p.71)

    Handy to know!
    """)
    return


@app.cell
def _():
    'a' in 'banana'
    return


@app.cell
def _():
    'z' in 'banana'
    return


@app.cell
def _():
    'Gator' in 'Go Gators!'
    return


@app.cell
def _():
    'Seminole' in 'Go Gators!'
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 6.9 String methods (p. 71)

    **This is kind of an important section, so look at the text.**

    This is the first introduction to the idea of Python *objects* and *methods*. Objects are instances of the class that defines them. We will learn more about classes, objects and methods as we go.

    The `dir` function can help you see what can be done to an object--what methods it has.
    """)
    return


@app.cell
def _():
    stuff='Hello, world!'
    print(type(stuff))
    dir(stuff)
    return


@app.cell
def _():
    help(str.upper)
    return


@app.cell
def _():
    word='banana'
    print(word.upper())
    return (word,)


@app.cell
def _(word):
    _index = word.find('a')
    print(_index)
    return


@app.cell
def _():
    _line = '  Here we go  '
    _line.strip()
    return


@app.cell
def _():
    # You can combine methods too...
    # But order matters!!!
    _line = 'Here we go'
    print(_line.startswith('h'))
    print(_line.lower().startswith('h'))
    print(_line.startswith('h').lower())
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 6.10 Parsing strings (p. 74)

    Have a look, but we will learn more about using regular expressions with the `re` module later.

    ## 6.11 Format operator (p. 74)

    This still works, but we will find that the newer f-strings feature in Python are easier to use.
    Here are some of the examples from this section re-written using f-strings. Generally easier to write and read!
    """)
    return


@app.cell
def _():
    camels = 42
    f'I have spotted {camels} camels.'
    return


@app.cell
def _():
    years = 3
    num_spotted = 0.1
    animal = 'camels'
    f'In {years} years I have spotted {num_spotted} {animal}.'
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    We can also do lots more formatting with f-strings. E.g. control number of decimals printed.
    """)
    return


@app.cell
def _():
    import math
    print(f'The value of pi is: {math.pi}')

    print(f'The value of pi is approximately: {math.pi:.2f}')
    return


if __name__ == "__main__":
    app.run()
