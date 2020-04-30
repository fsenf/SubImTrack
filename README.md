![Example Track](docs/example-track.jpg)
# SubImTrack - Python Package for Subjective Image Tracking

## Introduction
`SubImTrack` is a small python toolbox for subjective tracking of features (e.g. clouds) in a stack of images. It runs i a `ipython`shell and let you 

* interactively load a stack of images
* select cloud track point via Mouse Click in subsequent images
* and store the resulting track data (time identifier, index positions w.r.t image geometry) in a netcdf file


## Installation
In the following, the steps to install `SubImTrack` are described.

### A dedicated place
It is assumed that your tracking activities start at a dedicated directories, e.g. `tracking`

```bash
mdkir tracking
```

### Via Python Virtual Environment
It is assumed that your python3 installation contains the `venv` module (see https://docs.python.org/3/library/venv.html). For installing the `subimtrack` package in the separate environment, do: 

* go to your tracking dir
```bash
cd tracking
```
* create a separate python environment and activate it
```bash
python3 -m venv python_env
source python_env/bin/activate
```

* install dependencies
```bash
pip install numpy matplotlib xarray Image
```



## Getting Started