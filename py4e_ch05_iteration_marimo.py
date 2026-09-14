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
    # Ch 5: Iteration

    ## 5.1 Updating variables (p. 57)

    One shortcut not mentioned for incrementing and decrementing variables is the `+=` and `-=` notation.
    """)
    return


@app.cell
def _():
    x = 10
    x = x + 1
    print(f'x has been incremented to {x}.')
    x = x - 1
    print(f'x has been decremented to {x}.')
    return (x,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 5.2 The `while` statement (p. 57)

    As a reminder from the Bash section, here's the diagram of a `while` statement or loop.

    ![Diagram of a while statement](https://raw.githubusercontent.com/comptoolsres/comptoolsres.github.io/refs/heads/main/images/while_loop.png)
    """)
    return


@app.cell
def _():
    n = 5
    while n > 0:
        print(n)
        n = n - 1
    print('Blastoff!')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Much of the rest of this section should be very familiar to you from Bash!

    Here is the diagram of the `for` loop.

    ![Diagram of for loop](https://raw.githubusercontent.com/comptoolsres/comptoolsres.github.io/refs/heads/main/images/for_loop.png)

    Compare the Bash for loop to the Python for loop:

    **Bash**
    ```Bash
    for i in {1..30}
    do
      echo $i
    done
    ```

    **Python**
    ```Python
    for i in range(30):
        print(i)
    ```

    or even **C**:
    ```C
    for (i=1; i<30; i++)
    {
      printf("%d\n", i);
    }
    ```

    All produce essentially the same thing, and all should be relatively easy to look at and see what is happening. In general, the Python one would be the easiest to read--again, the focus by the developers on readability of the code.

    One small detail...These all give *slightly* different results.. Bash will print the numbers 1 to 30 inclusive. Python will print 0 to 29. And C will print 1 to 29. The devil is in the details...
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 5.6.1 Counting and summing loops (p. 61)

    This section outlines common uses of loops.

    A couple of things to add...

    In the text, they mention initializing a variable ahead of the loop, running the loop, and looking at the variable afterword.

    Let's look at what happens if you forget to initialize the variable ahead of time:
    """)
    return


@app.cell
def _():
    # Example 1 of not initializing the variable ahead of time
    for _itervar in [3, 41, 12, 9, 74, 15]:
        total = total + _itervar
    print('Total: ', total)
    return (total,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    In this case `total` is not defined. Remember that in Bash, an undefined variable would happily be used as a blank, and the above would interpret it as 0 and give you the right number. That can be dangerous, and in this case Python complains and makes you define `total`.

    Another example is particularly important for Jupyter notebooks where you can jump around, re-execute cells, skip cells, etc.
    """)
    return


@app.cell
def _(x):
    for _itervar in [1, 2, 3]:
        x_1 = x + _itervar
    print(f'Total: {x_1}')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    This is an example of what the text calls a **logic error**. Python happily did what we asked. But 1+2+3 is not 16!! How did it make this mistake??

    Well, if you look way up at the first code block in this notebook, we used the variable `x` there and it is still defined as 10. So, when we run this code, the first iteration gives 10+1.

    Within a notebook, all variables remain in memory until the kernel is restarted. Keep that in mind!
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
 
    """)
    return


if __name__ == "__main__":
    app.run()
