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
    # Data Visualization in Pandas

    We don't normally think about using Pandas for data visualization, and it is not the best general purpose graphing solution. But Pandas does have some very nice ways of summarizing and visualizing data!

    We used this Iris data in one of the earlier assignments. Note also that csv stands for comma separated values, but `read_csv` can use uther separators, tab in this case.
    """)
    return


@app.cell
def _():
    import pandas as pd

    df = pd.read_csv('/blue/bsc4452/share/Class_Files/data/Iris/Iris.data.txt', sep='\t')

    df.head()
    return (df,)


@app.cell
def _(df):
    # Summarize the data in the dataframe with .describe()

    df.describe()
    return


@app.cell
def _(df):
    # Visualize ranges, correlations, density plots of values with scatter_matrix

    from pandas.plotting import scatter_matrix

    # Make a scatter matrix of fans, width, thick, leaf.length, and curve
    scatter_matrix(df[['fans', 'width', 'thick', 'leaf.length', 'curve']], 
                   alpha=0.2, figsize=(6, 6), diagonal='kde')
    return


@app.cell
def _(df):
    df.plot.scatter(x='leaf.length', y='curve', color='orange')
    return


@app.cell
def _(df):
    # Setup a dictionary to translate species names to colors
    colors = {'I.mariae':'red', 'I.petrana':'blue', 
              'I.atropurpurea':'green', 'I.atrofusca':'black'}

    df.plot.scatter(x='leaf.length', y='curve',
                    s=df['width']*100, alpha=0.5, 
                    color=df['species'].apply(lambda x: colors[x]),
                    ylim=(-1,4))
    return


if __name__ == "__main__":
    app.run()
