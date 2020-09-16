
# enwajo - Energy Water Jordan Model

## Installation

### Windows

#### Install python

- Download and install Python 3.7.6 from https://www.python.org/ftp/python/3.7.6/python-3.7.6-amd64.exe
- Make sure to enable option "Add Python 3.7 to PATH"
- Use the standard installation option
- Follow the install wizard instructions
- At the end of the wizard, use the option to "Disable path length limit", if available


#### Install model

- Download Source Code as a zip file from: https://github.com/znes/enwajo/releases .
Unzip it to a location of your choosing.
- Install the necessary packages with double clicking on install.py .
- To test the installation:
  - Run the model with double clicking on run.py
  - Follow the instructions in the console output
  - When prompted choose a scenario folder, e.g. scenarios/example1

If you have any problems on the way, create an issue at:
https://github.com/znes/enwajo/issues

##  Mathematical model

The description of the mathematical equations can be found in the `docs/`
directory. To generate the pdf file pandoc can be used:

```
  pandoc docs/model-description.md -t latex -o docs/model-description.pdf
```

Units within the model can be defined by the user. However, make sure that
units are consistent. For example use:

* MW (installed capacities)
* MWh (energy related values like the demand)
* $/MWh (carrier or variable cost).

## Cite as

Hilpert, S. & Wingenbach, C. & Dettner, F. (2020). EnWaJo - Energy Water Model Jordan
