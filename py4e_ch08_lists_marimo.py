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
    # Lists

    I've mentioned the list data type before, but today we'll dive in a bit deeper.

    You can define a list with square brackets [ ] around a list of items:
    """)
    return


@app.cell
def _():
    numbers=[10,20,30,40]
    phrases=['crunchy frog', 'ram bladder', 'lark vomit']
    return (phrases,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Don't blame me...I'm copying from Py4E!

    ## Section 8.2: Lists are mutable

    Unlike strings, where letters can't be changed, lists can be:
    """)
    return


@app.cell
def _(phrases):
    print(phrases)
    phrases[1]='sheep guts'
    print(phrases)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Just like we did with strings, you can ask is something is `in` a list:
    """)
    return


@app.cell
def _(phrases):
    'sheep guts' in phrases
    return


@app.cell
def _(phrases):
    'ram bladder' in phrases # We replaced it, so not there anymore
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    If you try to access an element that doesn't exist, you get an `IndexError`. A good place to use `try:` and `except:`:
    """)
    return


@app.cell
def _():
    cheeses = ['Cheddar', 'Edam', 'Gouda']
    print(cheeses[2])
    print(cheeses[3])
    return (cheeses,)


@app.cell
def _(cheeses):
    try:
        print(cheeses[3])
    except:
        print("There are only", len(cheeses),"cheeses!")
    return


@app.cell
def _():
    crazy_list=['spam', 1, ['Brie', 'Roquefort', 'Pol le Veq'], [1, 2, 3]]
    len(crazy_list)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Section 8.6 List methods

    The `.append` method adds a new element ot the end of a list:
    """)
    return


@app.cell
def _():
    _t = ['a', 'b', 'c']
    _t.append('d')
    print(_t)
    return


@app.cell
def _():
    _t = ['d', 'c', 'e', 'b', 'a']
    _t.sort()
    print(_t)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Adding to a list...

    You cannot add to an arbitrary point in a list. For example, I have a list `nums=[0,1,2,3]` and I want to add 10 at `nums[10]`
    """)
    return


@app.cell
def _():
    nums=[0,1,2,3]
    nums[10]=10
    return (nums,)


@app.cell
def _(nums):
    # Even insert, which should insert 'x' at the nums[10] doesn't work 
    nums.insert(10,'x')  
    print(nums)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### A hidden warning...
    At the end of 8.6, Py4E notes that "most list methods are void; they modify the list and return `None`. Note the important difference in these two:
    """)
    return


@app.cell
def _():
    _t = ['d', 'c', 'e', 'b', 'a']
    _t.sort()  # t.sort modifies the list itself
    print(_t)
    print('\n-----------\n')
    _t = ['d', 'c', 'e', 'b', 'a']
    _t = _t.sort()
    print(_t)  # the .sort method returns None!!
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Other list methods

    `.pop()` -- get the value of the last element in the list and remove it

    `.pop(n)` -- get the value of the n<sup>th</sup> element in the list and remove it

    `del my_list[n]` -- delete the n<sup>th</sup> element in the list

    `.remove('the')` -- delete "the" from the list

    And some other handy ones:
    """)
    return


@app.cell
def _():
    nums_1 = [3, 41, 12, 9, 74, 15]
    print('Len:', len(nums_1))
    print('Max:', max(nums_1))
    print('Min:', min(nums_1))
    print('Sum:', sum(nums_1))
    print('Average:', sum(nums_1) / len(nums_1))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Section 8.10 Parsing lines

    This is about 50% of the scripts I write--read through a file, parse out the information I want, do something with that information.

    Look at `search5.py`.

    ## Section 8.11 & 8.12: Object, values and aliasing

    The information in 8.11 is the background to 8.12, and the moral of the story is that with mutable object, like lists, be careful about unintentionally aliasing.

    Here's the example:
    """)
    return


@app.cell
def _():
    a=[1,2,3]
    b=a
    print(b is a)
    print(a)
    print(b)
    return a, b


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    So far so good! But let's change `b[0]`:
    """)
    return


@app.cell
def _(b):
    b[0]=17
    print(b)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    What's the problem???

    Look at `a`:
    """)
    return


@app.cell
def _(a):
    print(a)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    What??? I didn't change `a[0]`!!!

    But you *actually* told Python with `b=a` is that **`a` and `b` point to the same place in memory**. Then you used `b` to change the value of the 0<sup>th</sup> element of the list at that place in memory--that also changes `a`!
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### How to avoid this??

    The text shows you the problem, but not the solution...at least not until the debugging section later.
    """)
    return


@app.cell
def _():
    a_1 = [1, 2, 3]
    b_1 = a_1[:]  # Use slices
    b_1[0] = 17
    print(a_1)
    print(b_1)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Now, rather than saying `b` points to the same place in memory as `a`, you are saying `b` is a new list with all the elements of `a`.

    This also applies to functions that modify lists. If you pass a list into a function, and it modifies the list, the original list is modified.
    """)
    return


if __name__ == "__main__":
    app.run()
