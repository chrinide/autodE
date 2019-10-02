[![DOI](https://zenodo.org/badge/196085570.svg)](https://zenodo.org/badge/latestdoi/196085570) [![Build Status](https://travis-ci.org/duartegroup/cgbind.svg?branch=master)](https://travis-ci.org/duartegroup/autodE) [![codecov](https://codecov.io/gh/duartegroup/autodE/branch/master/graph/badge.svg)](https://codecov.io/gh/duartegroup/autodE) [![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
![alt text](autode/common/llogo.png)
***
## Introduction

**autode** is a Python module designed for the automated calculation of reaction
profiles from just SMILES strings of reactant(s) and product(s).

***

## Installation

If the requirements are already satisfied to install **autodE** as a module
```
python setup.py install
```
**Note**: Using **autode** with PSI4 is not advised due to (1) Instability with radicals, (2) No analytic gradients in 
PCM calculations (3) No semi-empirical/tight-binding calculations.

### Dependencies
* Python > v. 3.5
* [matplotlib](https://anaconda.org/conda-forge/matplotlib)
* [PSI4](http://www.psicode.org)
* [ORCA](https://sites.google.com/site/orcainputlibrary/home) v. 4.1 (optional)
* [XTB](https://www.chemie.uni-bonn.de/pctc/mulliken-center/software/xtb/xtb) v. 6.1 (optional)

The Python dependencies are listed in requirements.txt best satisfied using a conda install (Miniconda or Anaconda) i.e.
```
conda create -n autode_env --file requirements.txt
conda activate autode_env
```

***

## Usage

Broadly, **atuodE** is invoked by first setting appropriate parameters in config.py, or specifying in a python script. 
Then, initialising _Reactant_ and _Product_ objects, generating a _Reaction_ object from those and invoking a method 
e.g. _locate_transtion_state()_ or _calculate_reaction_profile()_.

See _examples/_ for example usage.
