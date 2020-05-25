
# Modelling and Optimization with Python (Anaconda)

New to modelling and programming? Python is free and easy to learn
if you know where to start! This guide will help you to get started quickly.

## Anaconda for Data Scientists

Anaconda is a free and open-source distribution of the programming languages
Python and R for scientific computing, that aims to simplify package management
and deployment. Package versions are managed by the package management system
`conda`.

## Installing Python on Windows with Anaconda

First, you need to install the Python3 interpreter on your computer. You need
it before you can do any Python programming and/or using models written in
Python.

Make sure to download the latest version of Anaconda. In the link you will find
easy installation instructions for windows:

https://docs.anaconda.com/anaconda/install/windows/

You can confirm that Anaconda is installed and working with Anaconda Navigator or
with the `conda` command in the commandline.  On windows, click `Start` and search,
or select Anaconda Navigator from  the menu. If you prefer using a command line
interface (CLI), you can use the `conda` command to verify the installation
using Anaconda Prompt on Windows.

![Find Navigator](/docs/images/conda.PNG)

**Anaconda Navigator** is a desktop graphical user interface (GUI) included in Anaconda
distribution that allows you to launch applications and easily manage conda packages,
environments, and channels without using command-line commands.
With the Navigator you can search for packages on Anaconda Cloud or
in a local Anaconda Repository.

![Conda Navigator](/docs/images/navi.PNG)


Though Anaconda can be managed from the Anaconda Navigator, we highly
recommand using the commandline tool. Espacially when installing solver (see below)
the commandline will be essential. Therefore, the following description is
given for the command line usag.

##  Create an virtual environment with Anaconda

Anaconda uses so called *virtual environments* to manage your Python. These *environments* are like separate spaces on your computer that you can use to install specific Python packages. You can create multiple environments where you can use different versions of python, versions of packages etc (depending on your use-case).

Once you installed Anaconda successfully you can start Anaconda. Therefore,
you have to open your shell:

1. On Windows click `Start`
2. In the Search or Run line, type ``cmd`` (short for command) or ``anaconda Prompt`` , and press Enter
3. Write ``python`` to show which version of python and anaconda that you use.

After following the steps, the command line should be shown:

![github](/docs/images/promrt.PNG)


To create an environment (with the name *my-env*), write in the Anaconda prompt:

```
  conda create -n my-env python=3.7.6
```

After processing type `y` and press Enter to download. This will create an environment with the name example and the python version 3.7.6. As shown below before you install any packages into your environment, you will need to activate your virtual environment on windows:

```
  conda activate my-env
```

To deactivate use:

```
  conda deactivate
```

![github](/docs/images/env.PNG)

The example below shows that we activate and deactivate (*example* environment)

![github](/docs/images/example.PNG)

Now back to example environment by typing ``conda activate example`` and installing
*Spyder* for this environment

1.	Write ``conda install spyder`` to install spyder.
2.	Write ``spyder`` to open the program in **my-env**.

## Installing packages and solvers

#### Packages

Packages are software libraries written for the Python programming language for
all sorts of things including data manipulation and analysis, writing and reading data as well as
solving optimisation problems.

In Anaconda command prompt write:

```
  conda install -c conda-forge pyomo
```

To install any package

``conda install ‘package-name’``

##### Examples
To install pyomo package for optimisation

``conda install pyomo``

To install pandas package

``conda install -c conda-forge matplotlib``

To install matplotlib package

``conda install -c anaconda xlrd``

To install xlrd Package

``conda install -c conda-forge xlrd``

To install toml package

``conda install toml``

To install plotly optimizer

``conda install -c plotly``


#### Solvers  

Solvers are powerful software programs to solve large-scale linear programming,
quadratic programming, quadratically constrained programming, mixed integer
programming, and other problems.

To install the (propriatary) gurobi solver run:

``conda install gurobi``

One open source solver is the GLPK solver, which you can install with:

``conda install -c conda-forge glpk``


![github](/docs/images/pyomo.PNG)


**To install open source *CBC* solver for windows** use this
link https://oemof.readthedocs.io/en/stable/installation_and_setup.html
and look for windows solver

1. Check your architecture first (32/64 bit)
2. In Anaconda Prompt’ type: ``pip install oemof``
3. Downloaded CBC (64 or 32 bit)
4. Unpacked CBC to your model folder
5. Restart Windows


## Writing Python Code: *Spyder*

The simplest way to run, edit or write code is by using *Spyder*. Spyder
is a interactive programming environment for Python. There are many ways to install and
launch it. If you are using the Anaconda Navigator, you simply can click the *Spyder* icon.

**Alternatively** you can open a terminal window and simply launch spyder
by typing ``spyder`` and pressing enter.

*You may get a pop-up window saying that spyder is not the latest version,
which is just because the version within Anaconda is a few revisions behind.*


### Spyder
![github](/docs/images/spyder.PNG)

1.	Editor window: here you can (open, read, run, write, edit, etc) your code.
2.	The upper right-hand side is used for a help browser, a variable explorer, and a file explorer. You can change which panes are visible and their layout within the window.
3.	Python console window: where you can see the result of your program and also the history.

You can begin working with spyder immediately in the console window. Essentially, it works like python
inside the command line. The big difference is that spyder can inspect the contents of the Python engine and can-do things like display variables and their contents within the variable explorer.
