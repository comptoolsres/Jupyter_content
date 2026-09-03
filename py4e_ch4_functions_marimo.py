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
    # Ch 4: Python Functions

    Chapter 4 of Py4E goes into functions, starting by showing several functions we've already seen, like the `type` function to get a variable's type, the type conversion functions (`float(input)`), etc.

    ## 4.2 Built-in functions

    One of the design goals of Python was to keep the main language, the built-in functions, relatively limited. You can do a fair bit with the built-in functions, but you will almost always need to import additional functions. The idea here is that different people need different functions, so rather than make a bloated language that has everything, allow people to import what they need.

    ## 4.4 Math functions (p. 45)

    Here, we `import math` because we want some functions that are not in the built-in functions of Python.

    ## 4.5 Random numbers (p.46)

    This is an interesting bit on `pseudorandom` numbers--computers cannot make truly random numbers.

    Remember the dot notation: once imported, the functions that are part of a module can be called with the `module.function` format as in `random.random` in this case since both the module and function are called "random".

    Run the next cell several times and notice that you get different numbers each time.
    """)
    return


@app.cell
def _():
    import random
    for i in range(10):
        _x = random.random()
        print(_x)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    In addition to the `random` function, the `random` module has `randint` and several other functions.

    **How would you find out about the functions in the `random` module?**
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 4.6 Adding new functions (p.47)

    Just as in Bash, you can write your own functions.
    """)
    return


@app.cell
def _():
    def print_lyrics():
        print("I'm a lumberjack, and I'm okay.")
        print('I sleep all night and I work all day.')
    print(print_lyrics)
    print(type(print_lyrics))  # print_lyrics is a variable of type function
    print_lyrics()
    return (print_lyrics,)


@app.cell
def _(print_lyrics):
    def repeat_lyrics(): 
        print_lyrics() 
        print_lyrics()
    
    repeat_lyrics()
    return


@app.cell
def _():
    def print_twice(bruce): 
        print(bruce)
        print(bruce)

    print_twice("Spam!")
    return (print_twice,)


@app.cell
def _(print_twice):
    michael = 'Eric, the half a bee.'
    print_twice(michael)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### The importance of variable names

    Hopefully the last example above took some thinking to follow. That is partially because there is very little correspondence between the variable names and their content. This makes it hard to read! This is an example of poor variable name choice!
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 4.10 Fruitful functions and void functions

    Some functions return information (a fruitful function) while others just do something (a void function). For example, the `print_twice` function didn't return anything, it just printed some text twice.

    One important thing to remember with fruitful functions is that unless you do something with the returned value, like store it in a variable, the information is lost.
    """)
    return


@app.cell
def _():
    import math

    math.sqrt(5)
    return (math,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    On the Python interactive prompt or in Jupyter, we see the result of that function call--the square root of 5 is displayed. But **in a script**, that number just disappears unless we do something with it, like store it in a variable.
    """)
    return


@app.cell
def _(math):
    _x = math.sqrt(5)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Similarly, while the `sqrt` function returns something, not all functions return anything. So assigning the return value may give **None**
    """)
    return


@app.cell
def _(print_lyrics):
    lyrics=print_lyrics()
    print ("_________________")
    print(lyrics)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The first two lines are the output of calling the `print_lyrics` function. The variable lyrics however has the value of **None**. Kind of like `True` and `False`, `None` is a special type, the "NoneType":
    """)
    return


@app.cell
def _():
    type(None)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    This will be important later, but `None` is not the same as '0' or undefined.

    ### Returning values from a function

    To return something from a function, use the `return` statement.
    """)
    return


@app.cell
def _():
    def addtwo(a, b):
        added = a + b
        return added
    _x = addtwo(3, 5)
    print(_x)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 4.11 Why Functions? (p.52)

    This is summarized nicely by Py4E:

    >It may not be clear why it is worth the trouble to divide a program into functions. There are several reasons:
    * Creating a new function gives you an opportunity to name a group of statements, which makes your program easier to read, understand, and debug.
    * Functions can make a program smaller by eliminating repetitive code. Later, if you make a change, you only have to make it in one place.
    * Dividing a long program into functions allows you to debug the parts one at a time and then assemble them into a working whole.
    * Well-designed functions are often useful for many programs. Once you write and debug one, you can reuse it.

    I would add: any time you find yourself copying and pasting code from one section of a script into another section, stop yourself and convert that into a function!
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Your turn
    Work on any exercises you haven't finished up.
    Or try Exercises 5 & 6 in Ch 4.
    """)
    return


if __name__ == "__main__":
    app.run()
