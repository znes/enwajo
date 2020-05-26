
# Modelling and Optimization with Python (Anaconda)

New to modelling and programming? Python is free and easy to learn
if you know where to start! This guide will help you to get started quickly.

## Anaconda for Data Scientists

Anaconda is a free and open-source distribution of the programming languages
Python and R for scientific computing, which aims to simplify package management
and deployment. Package versions are managed by the package management system
`conda`.

## Installing Python on Windows with Anaconda

Before you can do any Python programming and/or using models written in
Python you need to install the Python3 interpreter on your computer. 

Make sure to download the latest version of Anaconda. Follow the link below to find
easy installation instructions for windows:

https://docs.anaconda.com/anaconda/install/windows/

You can confirm that Anaconda is installed and working with Anaconda Navigator or
with the `conda` command in the command line. Using Windows, click `Start` and select Anaconda Navigator from the menu. If you prefer using a command line
interface (CLI), you can use the `conda` command to verify the installation
using Anaconda Prompt on Windows.

![Find Navigator](/docs/images/conda.PNG)

**Anaconda Navigator** is a desktop graphical user interface (GUI) included in the Anaconda
distribution, which allows you to launch applications and easily manage conda packages,
environments, and channels without using command line commands.
With the Navigator you can search for packages on Anaconda Cloud or
in a local Anaconda Repository.

![Conda Navigator](/docs/images/navi.PNG)

Although Anaconda can be managed from the Anaconda Navigator, it is highly
recommended using the command line tool. Especially when installing a solver (see below)
the command line will be essential. Therefore, the following description is
given for command line usage.

##  Creating a virtual environment with Anaconda

Anaconda uses so-called *virtual environments* to manage your Python ????. These *environments* represent separate spaces??? on your computer, which are used to install specific Python packages. You can create multiple *environments* in which you can use different versions of Python, versions of packages etc. depending the respective application.

Once you have installed Anaconda successfully you can start. For this,
you have to open your shell????:

1. On Windows click `Start`
2. In the Search or Run line, type ``cmd`` (short for command) or ``anaconda Prompt`` and press Enter
3. Write ``python`` to show which version of Python and Anaconda is used.

After following 1-2-3, the command line should show:

![github](/docs/images/promrt.PNG)


To create an environment (with the name *example*), write in the Anaconda prompt:

```
  conda create -n example python=3.7.6
```

Following instructions, including typing `y` (for yes, proceed with download) and pressing Enter will create an environment with the name example in the Python version 3.7.6. As shown below, before installing any packages into your environment, you will need to activate your virtual environment in Windows:

```
  conda activate example
```

To deactivate use:

```
  conda deactivate
```

![github](/docs/images/env.PNG)

The example below shows how to activate and deactivate an environment (*example* environment).

![github](/docs/images/example.PNG)

## Installing packages and solvers

#### Packages

Packages are software libraries written for the Python programming language, which can be utilized in a number of contexts including data processing and analysis, writing and reading data as well as
solving optimisation problems.

To install any package (here as an example the package *pyomo*) write in the Anaconda command prompt

```
  conda install -c conda-forge pyomo
```

This installs from the channel conda-forge the package *pyomo*.


#### Solvers  

Solvers are powerful software libraries to solve large-scale linear programming,
quadratic programming, quadratically constrained programming, mixed integer
programming and other problems.

To install the (proprietary) gurobi solver run:

``conda install gurobi``

One open source solver is the GLPK solver, which you can install with:

``conda install -c conda-forge glpk``


![github](/docs/images/pyomo.PNG)

There are various commercial and open-source solvers that can be used.

One of the recommended open source solvers is the CBC (Coin-or branch and cut) solver. But sometimes its worth comparing the results of different solvers (e.g. GLPK).

1. Downloaded CBC from here ([64](http://ampl.com/dl/open/cbc/cbc-win64.zip) or [32](http://ampl.com/dl/open/cbc/cbc-win32.zip) bit)
2. Download GLPK from 
3. Unpacked CBC/GLPK to any folder (e.g. C:/Users/Somebody/my_programs)
4. Add the path of the executable files of both solvers to the PATH variable using this [tutorial](https://www.computerhope.com/issues/ch000549.htm)
5. Restart Windows


## Writing Python Code: *Spyder*

The simplest way to run, edit or write code is by using *Spyder*. *Spyder*
is an interactive programming environment for Python. There are many ways to install and
launch it. If you are using the Anaconda Navigator, you simply can click the *Spyder* icon.

**Alternatively** you can open a terminal window and simply launch *Spyder*
by typing ``spyder`` and pressing enter.

*You may get a pop-up window saying that spyder is not the latest version,
which is just because the version within Anaconda is a few revisions behind.*


### Spyder
![github](/docs/images/spyder.PNG)

1.	In the Editor window you can open, read, run, write, edit, etc. your code.
2.	In the upper right-hand you can chose between a help browser, a variable explorer or a file explorer. You can change which panels are visible and their layout within the window.
3.	In the Python console window you can see the result of your program as well as the history.

You can start working with spyder immediately in the console window. Essentially, it works like Python
inside the command line. The big difference is that spyder can inspect the contents of the Python engine and e.g. display variables and their contents within the variable explorer.
