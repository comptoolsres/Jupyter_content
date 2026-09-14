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
    # Flow control: *if*

    As I mentioned in the Bash section, `if` statements are fundamental to just about every programming language. Syntax is all that changes...

    Python emphasizes readability. It has always been the case the people were *told* to indent code to make it more readable, so the developers of Python took that a step further and force indentation, making indentation level, rather than brackets or "`if ... fi`", "`do ... done`", how the boundaries of the statement are defined.
    """)
    return


@app.cell
def _():
    x=5
    if x > 0 :
        print ("x is positive")
    return (x,)


@app.cell
def _(x):
    # The % is the modulus operator, which gets the remainder of a division.

    if x%2 == 0 :
        print('x is even')
    else :
        print('x is odd')
    return


@app.cell
def _():
    x_1 = 5
    y = 10
    if x_1 < y:
        print('x is less than y')
    elif x_1 > y:
        print('x is greater than y')
    else:
        print('x and y are equal')
    return x_1, y


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    You do not need to have an ending `else` (see p. 35):
    """)
    return


@app.cell
def _():
    choice = "d"
    if choice == 'a': 
        print('Bad guess')
    elif choice == 'b': 
        print('Good guess')
    elif choice == 'c':
        print('Close, but not correct')

    print ("Moving on")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    p. 35: **3.5 Chained conditionals**: This statement bears emphasizing:

    > "If one of them is true, the corresponding branch executes, and the statement
    ends. Even if more than one condition is true, only the first true branch executes."

    Keep this in mind when arranging the order of tests.

    p. 36: **3.6: Nested Conditionals**: Generally try to avoid complex nesting.
    """)
    return


@app.cell
def _(x_1, y):
    if x_1 == y:
        print('x and y are equal')
    elif x_1 < y:
        print('x is less than y')
    else:
        print('x is greater than y')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # 3.7 Catching exceptions using try and except

    I **highly** recommend adding try and except liberally to your code. It is far better to fail gracefully with meaningful error messages or options to continue than to crash and burn with Python errors that sometimes make little sense.
    """)
    return


@app.cell
def _():
    _inp = input('Enter Fahrenheit Temperature:')
    try:
        _fahr = float(_inp)
        _cel = (_fahr - 32.0) * 5.0 / 9.0
        print(_cel)
    except:
        print('Please enter a number')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Recovering from exceptions

    Not covered at this point in the text, is one way to try again if the user doesn't enter a number. `while True:` is used a lot and True is *always* True. It may seem odd to use it as a flow control method. But, if we add `break` we can break out of the `while` loop.
    """)
    return


@app.cell
def _():
    while True:
        _inp = input('Enter Fahrenheit Temperature:')
        try:
            _fahr = float(_inp)
            _cel = (_fahr - 32.0) * 5.0 / 9.0
            print(_cel)
            break  # Add the break to exit while after success. 
        except:
            print('Please enter a number')
    print('Done')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Flow control: *assert*

    The *assert* operator is not covered in the text, but I think it's important and this seems like a good place to introduce it.

    Assert is kind of like a simplified if statement and can be used to help catch bugs in your program.

    Here's an example, but don't worry about the code too much. It adds quite a bit we haven't seen.
    """)
    return


@app.cell
def _():
    # Simple captcha
    Answer = 5
    while True:
        _inp = input('What it 2 + 3:')
        try:
            int(_inp)
            break
        except:  # Make sure the user entered a number
            print('Please enter a number')
    assert int(_inp) == Answer, 'Are you sure you are human?'
    print('Welcome human!')  # We've determined we have a numeric answer, now we can check that it is correct
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    You can use assert statements in your code to make sure conditions are met. This can make debugging much easier as it will clue you into where something is not going the way you expect it to rather than just keeping going with bad data.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Flow control: *while* and *for*

    We will come back to this later, but just like in Bash, Python has *while* and *for* loops.
    """)
    return


@app.cell
def _():
    # From section 5.2, p. 58 of PDF.

    n=5
    while n > 0:
        print(n)
        n=n-1 

    print('Blastoff!')
    return


@app.cell
def _():
    # From section 5.6, p. 60 of PDF.

    friends = ['Joseph', 'Glenn', 'Sally'] 
    for friend in friends:
        print('Happy New Year:', friend)
    print('Done!')
    return


if __name__ == "__main__":
    app.run()
