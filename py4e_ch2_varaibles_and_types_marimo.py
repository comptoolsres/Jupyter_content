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
    # Py4E: Ch 2: Variables, expressions, and statements

    ## A note on change in format

    The previous sections of this website were written in Markdown and converted to static HTML pages to be served via GitHub with [Jekyll](https://jekyllrb.com/), a [Ruby](https://www.ruby-lang.org/en/)-based framework, using the [Documentation theme](https://idratherbewriting.com/documentation-theme-jekyll/).

    For the Bash section, that worked Ok, and there are not great tools to mix interactive code demonstration with nicely formatted descriptions on the web.

    As we move into the Python section of the course, there is a tool made for this: Jupyter Notebooks. As such, most of the rest of the course content will be presented as Jupyter Notebooks. GitHub does a decent job of rendering static versions of notebooks on the web (though it does fail at times), but one neat thing about notebooks is that they can remain fully interactive for you in the right environment.

    ### Some methods of running the notebooks interactively:

    * Clone the [repository](https://github.com/comptoolsres/Jupyter_content) to your space on HiPerGator, log into [Open OnDemand](https://ondemand.rc.ufl.edu/), launch a Jupyter session, and open the notebooks and play with the code.
      * One advantage of this is that you can run `git pull` periodically to get updated content.

    * The Google Colaboratory runs Notebooks. You can [open this notebook here](https://colab.research.google.com/github/comptoolsres/Jupyter_content/blob/master/py4e_ch2_varaibles_and_types.ipynb) or load the whole repository from the File menu > Open Notebook, select the GitHub tab and paste the URL to the repository: https://github.com/comptoolsres/Jupyter_content
      * This will work for most of the things we do in class and may be easier than using HiPerGator for some. There are a few data files too large for the git repo, but I try to provide another source to download those.

    * View the notebooks in Binder: [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/comptoolsres/Jupyter_content.git/main)
      *Binder can take a minute or two to start up, which can get a bit frustrating at times.

    * VSCode can run Jupyter Notebooks, [either on your own computer](https://code.visualstudio.com/docs/python/jupyter-support) or even remotely on HiPerGator
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Py4E Ch 2: Variables, expressions, and statements

    ### 2.1 Values and types

    #### Implicit vs explicit typing
    Like Bash, Python uses *implicit typing* of variables. This is also sometimes called "duck typing". That is, if it looks like an integer, it's an integer. Variables are typed based on the values they store at the time.

    The opposite of implicit typing is *explicit typing* where you, as the coder, must declare--when you define the variable--what type of values it will hold. C, C++ and others rely on explicit typing--this tends to be the case for compiled programs as the machine code needs to be compiled to properly store the value before the data are present. This forces coders to be more explicit about what they plan to do with a variable, but can also be limiting when you might want to not be explicit ahead of time.

    Implicit typing is handy for programmers because you don't need to think about what type of data the variable will hold...except that you kind of do, because different types do different things when you operate on them.
    """)
    return


@app.cell
def _():
    # Getting the type of a value
    print(type('Hello, World!'))
    print(type(17))
    print(type(3.2))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Here are some common variable types and examples of the data they correspond to:

    Type |	Example
    -----|---------
    Integer	|42
    Float (real)|	3.14
    Boolean	|True
    String	|Hello
    List	|[1,4,"text",5]
    Tuple	|(42,"Answer")
    Dictionary |	{"Name" : "Matt", "Fingers" : 10}
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 2.2 Variables

    Notice the difference between how variables are created and referenced in Bash and Python.

    On the creation side, spacing is not as important as it was in Bash (remember it didn't work if there were spaces on either side of the `=` sign). The Python convention is to put spaces on both sides of the `=` sign, but it will work with or without them.

    In Bash, we assigned a value with something like `x=7` and then referenced the variable (i.e. get its current value) with something like `echo $x`--adding the `$` before the variable name. Most programming languages use some character, often the `$`, before variable names to help differentiate variables from other text. Python is different in that it does not use any special characters. While this can be nice, and aids readability, as we will see, this can create other problems. A good text editor with syntax coloring will help you out here too!
    """)
    return


@app.cell
def _():
    # From 2.2 Variables; p. 20 of Py4E
    message = 'And now for something completely different'
    n = 17
    pi = 3.1415926535897931
    return message, n, pi


@app.cell
def _(message, n, pi):
    print(message)
    print(n)
    print ("Pi is:", pi)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    As noted above, with nothing to specify something as a variable, we do need to make some adjustments. In Bash, we could have done something like:

    ```Bash
    [magitz@login8 ~]$ pi=3.14
    [magitz@login8 ~]$ echo "Pi is: $pi"
    Pi is: 3.14
    ```

    Let's try that in Python:
    """)
    return


@app.cell
def _():
    print("Pi is: pi")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Not quite what we were after! There are a number of ways of getting what we want and there have even been some recently added methods for newer versions of Python. Below are three (of several) methods and in the following block how tht is extended to add additional variables.
    """)
    return


@app.cell
def _(pi):
    print("Pi is:", pi)  # Maybe the most traditional way. Can get complex with many variables
    print("Pi is: %s" %(pi)) # Format specifiers: each specifier is replaced with the value of the variables in the order listed at the end.  
    print(f"Pi is: {pi}")  # The new "f-strings" format in Python 3.6 and above.
    return


@app.cell
def _(n, pi):
    # Adding additional information to the print statements
    # for each format shown in the cell above
    print("Pi is:", pi, ". The value of n is:", n)
    print("Pi is: %s. The value of n is: %d" %(pi, n))
    print(f"Pi is: {pi}. The value of n is: {n}")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    I will generally try to use the f-strings format for print statements as I think it is the clearest and best habit to get into using.

    ## 2.3 Variable names and keywords

    There are many (conflicting) opinions on variable naming. Consistency wins, but the [PEP8 Style Guide](https://www.python.org/dev/peps/pep-0008/) says that variable and function names should be `lower_case_with_underscores` connecting multiple words.

    Keep reading through the chapter, lots of good information...
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 2.10 Asking the user for input

    We saw how to get input in Bash, here are some examples using the input() function
    """)
    return


@app.cell
def _():
    inp=input()
    print(inp)
    return


@app.cell
def _():
    _name = input('What is your name?\n')
    print('Hi', _name, ', nice to meet you!')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Notice the spaces that `print()` puts between the things we told it to  (the space between the name and the comma). That can also be controlled (we just need to put spaces where we do want them):
    """)
    return


@app.cell
def _():
    _name = input('What is your name?\n')
    print('Hi ', _name, ', nice to meet you!', sep='')
    return


@app.cell
def _():
    prompt = 'What...is the airspeed velocity of an unladen swallow?\n'
    speed = input(prompt)
    int(speed)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Your turn...
    In a group, work on **Exercise 3** at the end of Chapter 2 of Py4E (p. 30 in the PDF).

    If you finish that, do **Exercise 5**.
    """)
    return


if __name__ == "__main__":
    app.run()
