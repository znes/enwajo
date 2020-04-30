
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
  python model.py
```

Results will be written to a directory `results`. After optimisation you
can run

```
  python plotting.py
```

to generate plots that will be stored in the plots directory `plots`.

##  Mathematical model


## Cite as
