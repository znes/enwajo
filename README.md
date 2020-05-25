
# enwajo - Energy Water Jordan Model

## Installation

### Windows

### Linux

Installation on Linux is straighforward with *pip* using the
`requirements.txt`. Create a virtualenv, activate and install the requirements with
the following commands:


```
  virtualenv -p python3 enwajo-env
  source enwajo-env/bin/activate
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
  python model.py scenarios/enwajo
```

The first commandline argument provides the path to the scenario directory
containing the input data. The following folder structure is required for this
scenario directory:

```
example-scenarios
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
