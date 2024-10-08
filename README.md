# pygmt_clinic

> Jupyter Notebook demonstration of PyGMT

### Setup

In the Anaconda terminal.

Create an environment with fixed dependencies, then activate:

```bash
conda env create -f environment.yml
conda activate pygmt
```

Start the Jupyter server

```bash
jupyter-lab
```

Navigate to the "pygmt_intro" folder and start "pygmt_intro.ipynb".


### Initial environment creation

The environment was initially created with:

```bash
conda create -c conda-forge -n pygmt python=3.12 pygmt pandas jupyterlab matplotlib
```

This command installs the latest compatible versions of each of the packages.
Once created, the pinned versions can be exported with:

```bash
conda env export > environment.yml
```

This file can be modified to remove the "prefix" and any local repository mirrors.

At one point, I had issues downloading the dependency files.
Conda advised that I delete some from the `pkgs` folder.
The following command removed all files from the past 3 days.

```bash
find /c/Users/my_username/.conda/pkgs/ -mtime -3 -exec rm -rf {} \;
```
