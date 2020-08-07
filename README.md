
# enwajo - Energy Water Jordan Model

## Installation

### Windows

#### Install python and a new virtual environment

- Download and install Python 3.7.6 from https://www.python.org/ftp/python/3.7.6/python-3.7.6-amd64.exe
  - Follow the install wizard instructions
  - Make sure to enable option "Add Python 3.7 to PATH"
  - Use the standard installation option
  - At the end of the wizard, use the option to "Disable path length limit", if available
- Open the Windows Command Prompt
- Create a new folder called *enwajo*:
  `mkdir enwajo`
- Enter that folder: `cd enwajo`
- Install virtualenv (package for python): `pip install virtualenv`
- Create a virtual environment for python in your enwajo folder: `virtualenv venv`
- Activate that environment: `venv\Scripts\activate.bat`
- Now you shoud see a "(venv)" in the command prompt.

#### Install model

- Download Source Code as a zip file and unzip it into you *enwajo* folder from: https://github.com/znes/enwajo/releases
- Go to the root folder of the new repository (where this README resides) with `cd`
- Install necessary packages listed in requirements.txt (make sure to have your environemt activated): `pip install -r requirements.txt`
- Download cbc-solver from http://ampl.com/dl/open/cbc/cbc-win64.zip and unzip in the rootfolder of the model repository (where this README resides)
- Run the model file: `python model.py scenarios/test-scenario`

### Linux

Installation on Linux is straightforward with *pip* using the
`requirements.txt`. Create a virtual environment, activate and install the requirements with
the following commands:


```
  virtualenv -p python3 venv
  source venv/bin/activate
  pip install -r requirements.txt
```

The open source solver CBC can be installed from the official
package lists:

```
sudo apt-get install coinor-cbc
```

## Configure

The `config.toml` file allows to set parameters of the model such as the
solver, constraints and temporal parameters.

## Run the model and analyse results

Run the model from this directory by running:

```
  python model.py scenarios/test-scenario
```

The first command line argument provides the path to the scenario directory
containing the input data. The following folder structure is required for this
scenario directory:

```
example-scenario
  |-- input/
    |--input.xlxs
  |--config.toml
```

##  Mathematical model

The description of the mathematical equations can be found in the `docs/`
directory. To generate the pdf file pandoc can be used:

```
  pandoc docs/model-description.md -t latex -o docs/model-description.pdf
```

## Cite as
