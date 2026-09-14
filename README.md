# Jupyter Notebook Content
## [Computational Tools for Research](https://comptoolsres.github.io/)

Matt Gitzendanner

This repo contains the Jupyter Notebook portions of my notes for the class. These are then served via the free [mybinder.org](https://mybinder.org/) site.

View in Binder:  [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/comptoolsres/Jupyter_content.git/master)

## Fall 2026: Added Marimo option

See more information on Marimo here [https://marimo.io/](https://marimo.io/).

On HiPerGator, you can launch a Marimo session fom the Interactive Apps menu. But first you need to do a little setup:

There is more information [here](https://docs.rc.ufl.edu/software/uv/), but follow these steps:

1. Make a symlink for your uv cache folder, **you will need to change "GROUP" to your group name, e.g. "bsc4452"**: 

        mkdir /blue/GROUP/$USER/cache
        ln -l /blue/GROUP/$USER/cache .cache/uv
2. Clone this repo to your /blue directory
3. Set up the uv environment

        ml conda
        uv sync

Now when you launch a Marimo session, you can enter the path to this repo in the "Path to a uv Project" box in Open OnDemand. E.g. `/blue/bsc4452/$USER/Jupyter_content`