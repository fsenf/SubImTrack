# A Short Manual on `subimtrack`
It is assumed that you have started the image tracking in a `ipython`shell (see Getting Started in [Readme](../Readme.md)).

## Explanation of Visualization
![Example Track](example-track.jpg)

The example shows you an natural color Meteosat image. The ground is shown in greenish colors, the sea would appear dark, and clouds are either white or cyanish depending on the amount of cloud ice in the top levels.

You also see the current track point as **red circle**.

Moreover, previous and subsequent track points are provided as **white circles**.


## Typical Workflow
You will typically choose the following workflow:

1. create a manual track
2. store the track
3. continue with item 1. (make the next track and store it)

### Creating a track
The following steps are reasonable:

* Zoom into the region of Interest (Strg + Mouse Window)
* Create a Track Point (Left Mouse Button)
* _( Delete Wrong Track (Backspace) )_
* Proceed to next image (Arrow Down)
* _( Or go the previous one (Arrow Up)_
* Create a Track Point

* Finally store the track (Right Mouse Button)


## Key- and Mouse-Bindings for Tracking
The `subimtrack.run`command starts an interactive matplotlib window. You will interact with that window using mouse and keyboard.

### Mouse-Bindings

| **Mouse Buttons**   | **Action**  | 
|---|---|
| Left Mouse Button    |  Sets the Track Point |
| Middle Mouse Button  |  Deletes the Full Track |
| Right Mouse Button   |  Saves the Track in a netcdf File / Starts a new Track |

### Key-Bindings

* Tracking

| **Shortcut Keys**   | **Action**  | 
|---|---|
| Arrow Down    |  Next Image |
| Arrow Up      |  Previous Image |
| Backspace     |  Remove Track Point |

* Zoom

| **Shortcut Keys**   | **Action**  | 
|---|---|
| Strg + Mouse  |  Create a Zoom Window |
| Esc           |  Reset Zoom to Full Image |

* Experimental (default `nstep = 5`)

| **Shortcut Keys**   | **Action**  | 
|---|---|
| Page Down    |  +`nstep` Next Image  |
| Page Up      |  -`nstep` Previous Image |
| +     |  double `nstep` |
| -     |  half `nstep` |

 

## Throughts on Post-Processing
Finally, you will have a simplistic set of track data stored. For instance,

```bash
> ncdump -h SubImTrack/test/tracks/track_20120608T1050Z_P222x397.nc 
netcdf track_20120608T1050Z_P222x397 {
dimensions:
	time = 3 ;
	string14 = 14 ;
variables:
	char time(time, string14) ;
		time:_Encoding = "utf-8" ;
	double column_index(time) ;
		column_index:_FillValue = NaN ;
	double row_index(time) ;
		row_index:_FillValue = NaN ;
}
```
* the filename contains the start point information 
* `time` : contains your time identifier string which you might need to parse 
* `column_index`and `row_index` : contain the respective row and column indices as float values

You need to read a geo-reference information that **exactly** fits with your image to translate the indices into longitude and latitude values. 