![Example Track](docs/example-track.jpg)
# SubImTrack - Python Package for Subjective Image Tracking

## Introduction
`SubImTrack` is a small python toolbox for subjective tracking of features (e.g. clouds) in a stack of images. It runs in an `ipython` shell and let you 

* interactively load a stack of images
* select cloud track points via Mouse Click in subsequent images
* and store the resulting track data (time identifier, index positions w.r.t image geometry) in a netcdf file

**Why should someone like to track clouds?**

* weather application: 
  * Imagine a developing thunderstorm that brings hazards to the regions where it moves along. It would be really good to monitor such dangerous clouds during their evolution.
* climate science: 
  * Clouds reflect sunlight back to space (They appear white in satellite images). Thus their lifetime might have an impact on the Earths energy balance.

The mentioned examples are best done if automated tracking approaches. However, when rearchers start to develop new approaches they need a high quality test data base. For this, `subimtrack` can be used. 


## Installation
In the following, the steps to install `SubImTrack` are described.

### A dedicated place
It is assumed that your tracking activities start at a dedicated directory, e.g. `tracking`

```bash
mkdir tracking
```

### Via Python Virtual Environment
It is assumed that your python3 installation contains the `venv` module 
(see https://docs.python.org/3/library/venv.html). For installing the 
`subimtrack` package in the separate environment, do: 

* go to your tracking dir
```bash
cd tracking
```

* create a separate python environment and activate it
```bash
python3 -m venv python_env

# conda deactivate   # you might need to deactivate your conda env
source python_env/bin/activate
```

* install dependencies
```bash
pip install wheel numpy matplotlib xarray Image ipython
```

* get the repository (good for testing)
```bash
git clone https://github.com/fsenf/SubImTrack.git
```

* locally install it
```bash
cd SubImTrack
pip install --upgrade .
```


## Getting Started
### Prepare for Image Tracking
It is assumed that you prepare images (a temporal sequence with a unique identifier for time in the filename, 
e.g. with the format `%Y%m%d-%H%M`) in a separate folder. 

For testing, the `subimtrack` package provides some Meteosat Images. You find the images here:

```bash
> ls -1 SubImTrack/test/images/
msevi-20120608T1000Z-hsand-rss-meu.jpg
msevi-20120608T1005Z-hsand-rss-meu.jpg
msevi-20120608T1010Z-hsand-rss-meu.jpg
...
```

### Start Tracking on Images
We start tracking of features in images.

* initialize env and start `ipython`
```bash
# conda deactivate   # you might need to deactivate your conda env
cd tracking
source python_env/bin/activate
ipython
```

* import `subimtrack` package
```ipython
In [1]: import subimtrack                                                                                                                         
```

* configure tracking
```ipython
In [2]: config = dict( fout = 'SubImTrack//test/tracks/', tlim = (6,20))                                                                          
```

* keywords:
  * `fout` : `string`, output path for track files (in netcdf format)
  * `tlim` : `tuple`, setting start and end index of the time identifier in the filename (see message when tracking is started) 
             

* set filename of the start image
```ipython
In [3]: start_image  = 'SubImTrack//test/images/msevi-20120608T1100Z-hsand-rss-meu.jpg'                                                           
```

* start the tracking
```ipython
In [4]: subimtrack.run( config, start_image)                                                                                                      
PAY ATTENTION!
Is this your correct time string?  20120608T1100Z
... if YES: fine!
... if NO: restart tracking with changed tlim

SubImTrack//test/images/msevi-20120608T1035Z-hsand-rss-meu.jpg
SubImTrack//test/images/msevi-20120608T1040Z-hsand-rss-meu.jpg
SubImTrack//test/images/msevi-20120608T1045Z-hsand-rss-meu.jpg
SubImTrack//test/images/msevi-20120608T1050Z-hsand-rss-meu.jpg
SubImTrack//test/images/msevi-20120608T1055Z-hsand-rss-meu.jpg
SubImTrack//test/images/msevi-20120608T1100Z-hsand-rss-meu.jpg
SubImTrack//test/images/msevi-20120608T1105Z-hsand-rss-meu.jpg
SubImTrack//test/images/msevi-20120608T1110Z-hsand-rss-meu.jpg
SubImTrack//test/images/msevi-20120608T1115Z-hsand-rss-meu.jpg
SubImTrack//test/images/msevi-20120608T1120Z-hsand-rss-meu.jpg
SubImTrack//test/images/msevi-20120608T1125Z-hsand-rss-meu.jpg
(5, 11)
('...plotting image number ', 5)
Out[4]: <subimtrack.ImageTracking.ImageTracking at 0x7f09b559a828>

```

You should see a window that pops up and shows your image. You can interact with the image window to perform your subjective tracking. See [docs/Manual.md](docs/Manual.md).


## Known Bug
* _Problem_: Resizing the matplotlib window sometimes disconnects the interactive application
  * Don't resize the window
* _Problem_: Exception appears when the end / begin of the image stack is approached several times (E. g. keep going to press <Down Arrow> at the end of the image stack)
