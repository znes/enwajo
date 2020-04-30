

# Modelling and Optimization with Python (Anaconda)



New to programming? 

Python is free and easy to learn if you know where to start! This guide will help you to get started quickly.

## Anaconda for Data Scientists

Directly from the platform and without involving DevOps, data scientists can develop and deploy AI and machine learning models rapidly into production. Anaconda provides the tools needed to easily:


•	Collect data from files, databases, and data lakes

•	Manage environments with Conda (all package dependencies are taken care of at the time of download)

•	Share, collaborate on, and reproduce projects

•	Deploy projects into production with the single click of a button

Data scientists that work in silos struggle to add value for their organization. That is why Anaconda created an integrated, end-to-end data experience.

Anaconda is a free and open-source distribution of the Python and R programming languages for scientific computing, that aims to simplify package management and deployment. Package versions are managed by the package management system conda.


## Installing python (anaconda)

install the Python 3 interpreter on your computer. This is the program that reads Python programs and carries out their instructions; you need it before you can do any Python programming.

make sure to download the latest version of anaconda and python, in this link you will find easy installation instructions:

https://docs.anaconda.com/anaconda/install/windows/


You can confirm that Anaconda is installed and working with Anaconda Navigator or conda.
Click Start, search, or select Anaconda Navigator from the menu.

If you prefer using a command line interface (CLI), you can use conda to verify the installation using Anaconda Prompt on Windows.

![github](/images/conda.PNG)

after installing and opening Anaconda:

Anaconda navigator windows appears **Anaconda Navigator** is a desktop graphical user interface (GUI) included in Anaconda distribution that allows you to launch applications and easily manage conda packages, environments, and channels without using command-line commands. Navigator can search for packages on Anaconda Cloud or in a local Anaconda Repository.

![github](/images/navi.PNG)

## Spyder

The simplest way to run ,edit or write code is with spyder. There are many ways to launch it .

If you are using the Anaconda Navigator, you simply can click the spyder icon.

or

If you have a terminal window open, simply launch spyder by typing ``spyder`` and pressing enter.

You may get a pop-up window saying that spyder is not the latest version, which is just because the version within Anaconda is a few revisions behind.

![github](/images/spyder.PNG)


1.)	Editor window: here you can (open, read, run, write, edit, etc) your code.
2.)	The upper right-hand side is used for a help browser, a variable explorer, and a file explorer. You can change which panes are visible and their layout within the window.
3.)	Python console window: where you can see the result of your program and also the history.

You can begin working with spyder immediately in the console window. It works, essentially, the same way that it works on the command line. The big difference is that spyder can inspect the contents of the Python engine and can-do things like display variables and their contents within the variable explorer.

**moreover you can use Jupyter Notebooks the same way** ,Jupyter Notebooks are an increasingly popular system that combine your code, descriptive text, output, images, and interactive interfaces into a single notebook file that is edited, viewed, and used in a web browser.


##  making virtual environment in Anaconda :
Once you installed Anaconda successfully you can start Anaconda. Therefore, you have to open your shell:
1.) Click Start

2.) In the Search or Run line, type ``cmd`` (short for command) or ``anaconda Prompt`` , and press Enter

3.) write ``python`` to show which version of python and anaconda that you use

After following the steps, Windows command line should be shown

![github](/images/promrt.PNG)



Anaconda uses virtual environments. These are separate spaces on your computer that you can use to install specific python packages. You can create multiple environments where you can use different versions of python, versions of packages etc (depending on your use-case).

To create an environment, do the following:
In the same anaconda prompt write:

``conda create -n example python=3.7.6``

after processing type (y) and enter to download

This will create an environment with the name example and the python version 3.7.6

As shown below Before you install any packages into your environment, you will need to activate your virtual environment on windows you can do this by:

``conda activate example``

To deactivate use:

``conda deactivate``

![github](/images/env.PNG)



the example below show that we activate and deactivate (example environment)

![github](/images/example.PNG)



Now back to example environment by typing ``conda activate example`` and installing spyder for this environment
1.)	Write ``conda install spyder`` to install spyder
2.)	Write ``spyder`` to open the program in **example environment**

## Installing packages and solvers :




#### Packages 
in computer programming, Packages are a software libraries written for the Python programming language for data manipulation and analysis ,extract and create data ,Optimization and other scientific purposes .



in the same anaconda command prompt write:

``conda install -c conda-forge pyomo``

to install pyomo package

``conda install pandas``

to install pandas package

``conda install -c conda-forge matplotlib``

to install matplotlib package

``conda install -c anaconda xlrd``

to install xlrd Package

``conda install -c conda-forge toml``

to install toml package

``conda install gurobi``

to install gurobi optimizer 

.

.

.


``conda install ‘package-name’``

to add any other package 

also visit 

https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-pkgs.htmlor 

or search in the internet for more commands and packages .




#### Solvers  
 Solvers are powerful packages help to solve large-scale linear programming ,quadratic programming, quadratically constrained programming, mixed integer programming, and other related problems .

#### some examples 

``conda install gurobi``

to install gurobi optimizer 

 
``conda install -c conda-forge glpk``

to install glpk solver


![github](/images/pyomo.PNG)

**to install cbc solver for windows** 

use this link https://oemof.readthedocs.io/en/stable/installation_and_setup.html
and look for windows solver

1) Check your architecture first (32/64 bit)
2) In Anaconda Prompt’ type: ``pip install oemof``
3) Downloaded CBC (64 or 32 bit)
4) Unpacked CBC to your model folder 
5) Restarrt windows 

![github](/images/cbcsolver.PNG)




## Another way to install packages and solvers on Jupyter notebook

After installing Anaconda, we can also install Jupyter notebook on the new environment as we have done with Spyder

To install packages and solvers 
   
1.)	open Jupyter from anaconda prompt (be aware of your environment)

2.)	open file > new notebook > Python 3

write one of this command and click run to install pyomo Package:

``conda install -c conda-forge pyomo``

``conda install -c conda-forge/label/cf201901 pyomo``

``conda install -c conda-forge/label/cf202003 pyomo``

![github](/images/jupyter1.PNG)

3.)	write one of this command and click run to install glpk solver :                                                                                                                      

``conda install -c conda-forge glpk``

``conda install -c conda-forge/label/gcc7 glpk``

``conda install -c conda-forge/label/broken glpk``

``conda install -c conda-forge/label/cf201901 glpk``

``conda install -c conda-forge/label/cf202003 glpk``

![github](/images/jupyter2.png)


This method is valid for all other packages and solver 

All used  anaconda Prompt commands are here also valid  

After doing the steps close the window even without saving.
