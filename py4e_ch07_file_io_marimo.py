import marimo

__generated_with = "0.24.0"
app = marimo.App()


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell
def _():
    import subprocess

    return (subprocess,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Ch 7: Files

    **Tip:** There is a copy of the code and other files from the Py4E book at `/blue/bsc4452/share/Class_Files/Py4E_files/code3`. The `mbox.txt` and `mbox-short.txt` files are also in the `data/` folder of this repository.

    ## 7.2 Opening files (p. 80)

    This section has the following figure (7.2 on p. 80):

    ![File handle image](https://raw.githubusercontent.com/comptoolsres/comptoolsres.github.io/refs/heads/main/images/py4e_fig7.2_file_handles.png)

    As noted in the text, **if** the `open` command is successful, what is returned is not the actual data, but a **file handle** to the file which can be used to read the data. The figure also shows **some** of the methods available for this object, like open, close, read, write.

    A file handle is the first we will see of this kind of structure, but will become more common in our work. We are not getting the actual file content, but a way to access that content. As you look around the internet, you will often see `fh` used for the variable name as an abbreviation of 'file handle'.
    """)
    return


@app.cell
def _():
    # Note that we need to add the data/ path since the mbox.txt is not in the current directory, but in the data folder.
    _fhand = open('data/mbox.txt')
    return


@app.cell
def _():
    # And the example of a failed open command
    _fhand = open('stuff.txt')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    We already saw `try` adn `except` write a try/except statement to tell the user that the file cannot be found on failure.
    """)
    return


@app.cell
def _():
    # To do: write a try/except statement to tell user that the file cannot be found
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### New line characters

    One more thing to note about this section is that the `\n` new line character (which we should remember from the RegEx section) takes on different forms in different operating systems. While Mac (since the early 2000s) and Linux use one format, Windows uses another. This can cause problems for parsing text files. Your text editor can usually save with specified new line characters (and you should choose Linux for this course) and there is also a command line tool, `dos2unix`, that can automate the conversion of files.

    It is surprisingly common to have users run into trouble with this. If you think everything *should* be working and it isn't, check the line breaks!

    ## 7.4 Reading files (p. 82)

    Look at `open.py`.
    """)
    return


@app.cell
def _():
    _fhand = open('data/mbox-short.txt')
    count = 0
    for _line in _fhand:
        count = count + 1
    # Code: http://www.py4e.com/code3/open.py
    print('Line Count:', count)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    `open.py` reads the file line by line, which is usually a good thing.

    Sometimes, it can be helpful to have the whole file in memory, see the `fhand.read()` function on p. 82 of the PDF for an example of how to do this.

    The example on p. 83 demonstrates one "feature" of `read()`, but is a little unclear. Py4E states "...each call to `read` exhausts the resource". What this means is that once you are at the end of the file, either using the file handle to read through line by line, or after reading the whole file at once, you can't easily go back through the file again.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 7.5 Searching through a file (p. 83)

    Notice the extra blank lines between the lines found. This is because the line itself has a new line character and that is printed in addition to the default new line after each print.
    """)
    return


@app.cell
def _():
    _fhand = open('data/mbox-short.txt')
    count_1 = 0
    for _line in _fhand:
        if _line.startswith('From:'):
            print(_line)
    return (count_1,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Py4E uses the `line.rstrip()` function to remove white space from the *right* side of the string to remove the line break. I typically use `line.strip()` to remove whitespace from either side.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Quick quiz**: What is the value of `count` at the end of this script?
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 7.6 Letting the user choose the file name (p. 85)

    This section shows one way to allow the user to choose, or run the same script on different input files without having to change the script itself.

    Another way to do this is using command line arguments in scripts. We saw how programs in Bash use command line arguments. We can do similar things with our scripts in python.

    ## Command line arguments: `argparse`

    That's all well and good, but requires a user to be sitting there to type the name of the file to run the script on.

    But what if we submit the script to a scheduler? Or we have 1,000 files to process? Do you want to type 1,000 file names???
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    `argparse` is the recommended command-line argument parser for python 3. There's a good [tutorial here](https://docs.python.org/3/howto/argparse.html).

    I made a version of the `search7.py` script called `search7.argparse.py` located in this repository.

    But here it is for clarity:
    ```python
    #!/usr/bin/env python3

    import argparse

    parser = argparse.ArgumentParser(
                description="Count the Subject: lines in a mbox file")
    parser.add_argument("file",
                help="File to count Subject: lines")
    args=parser.parse_args()

    try:
        fhand = open(args.file)
    except:
        print('File cannot be opened:', args.file)
        exit()
    count = 0
    for line in fhand:
        if line.startswith('Subject:'):
            count = count + 1
    print('There were', count, 'subject lines in', args.file)
    ```

    One aspect of Jupyter we haven't explored yet is the ability to run Bash commands using the `!`. So, we can run the script from withing Jupyter:
    """)
    return


@app.cell
def _(subprocess):
    #! python search7.argparse.py data/mbox-short.txt
    subprocess.call(['python', 'search7.argparse.py', 'data/mbox-short.txt'])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    We can look more at `argparse` later, but this is a valuable tool to learn as it allows you to pass arguments into your script from the command line.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 7.8 Writing files (p. 87)

    Writing to files is like reading them--we need to get a file handle.

    There are two types of file handles for writing, Py4E warns you about how writing clears out the old data, but doesn't tell you about the other type...appending.

    Kind of like the `>` redirect in Bash, `open('output.txt', 'w')` opens the file for writing, which clears the contents of the file and then starts writing what you ask.

    The `>>` double redirect equivalent in Python is `open('output.txt', 'a')` (**a** for **a**ppend).
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### `write` only rakes 1 argument

    With `print`, we've combined multiple things with commas for a single output line. e.g:
    """)
    return


@app.cell
def _(count_1):
    print('The current value of count is: ', count_1)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    But that doesn't work with write. e.g:
    """)
    return


@app.cell
def _(count_1):
    fout = open('output.txt', 'w')
    fout.write('The current value of count is: ', count_1)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    To me, this is a frustrating limitation, but there is a relatively easy work around. This is demonstrated on p. 88 without really explainging why this is handy. Re-writing for our example, we get:
    """)
    return


@app.cell
def _(count_1):
    fout_1 = open('output.txt', 'w')
    line1 = 'The current value of count is: ' + str(count_1)
    fout_1.write(line1)
    return (fout_1,)


@app.cell
def _(fout_1):
    fout_1.close()  # Always good practice to close your file when done!
    return


if __name__ == "__main__":
    app.run()
