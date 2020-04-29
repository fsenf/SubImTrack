#!/usr/bin/env python


import sys, os

import numpy as np
import pylab as pl
import copy

import matplotlib.widgets
import xarray as xr
from PIL import Image

######################################################################
######################################################################

def debug_run(func):

    def func_wrapper(*args, **kwargs):

        try:
           return func(*args, **kwargs)

        except Exception as e:

            print(e)
            return None

    return func_wrapper


######################################################################
######################################################################


class ImageTracking(object):
    
    # some default values ...
    tlim = (12, 25)
    xlim = (0,620)
    ylim = (480,0)
    page_step = 6

    # ................................................................
    def __init__(self, flist,
                 tlim = tlim,
                 xlim = xlim, 
                 ylim = ylim, 
                 trackdata_path = './trackdata' ):
        
        self.flist = flist
        self.nlist = len( flist )
        self.trackdata_path  =  trackdata_path 

        
        # initialization of plotting stuff ...........................
        pl.ion()

        self.fig = pl.figure(figsize = (15.5, 12.))
        self.ax =  self.fig.add_subplot(111)
        self.xlim = xlim
        self.ylim = ylim
        self.reset_zoom()
 

        # init of interactive stuff ..................................
        self.rect = matplotlib.widgets.RectangleSelector(
            self.ax, self.zoom,
            drawtype='box', useblit=True,
            button=[1], # just use left button
            rectprops = dict(edgecolor='white', facecolor='white', alpha = 0.1))
        
        self.rect.set_active(False)
        self.connect()
        
        
        # init of data output stuff ..................................
        self.init_track()
        self.tracks = {}
        self.track_number = 0
        self.tlim = tlim
       
        return
    

    # ................................................................
    def plot(self, n):

        print((n, self.nmax))

        if (self.nimg == 0): 
            print('First Image Reached')
        elif (self.nimg == self.nlist - 1):
            print('Last Image Reached')
        else:
            if n >= self.nmax:
                dn = n - self.nmax + 1
                print('Please wait for loading')
                self.load_set(self.nend + dn, self.nimg)
                n = self.nimg // 2 - 1
    
            elif n < 0:
                print('Please wait for loading')
                self.load_set(self.nstart + n, self.nimg)
                n = self.nimg // 2 

        # get name of the next loaded image
        self.nstep = n
        self.fname = self.loaded_images[n]
        self.basename = os.path.basename( self.fname )

   
        # and also extract the timestring
        t1, t2 = self.tlim
        self.timestr = self.basename[t1 : t2]


        print(('...plotting image number ', self.nstep))

        # get old limits and clean axis
        xlim = self.ax.get_xlim()
        ylim = self.ax.get_ylim()
        self.ax.cla()

        # do threshold-based plotting
        self.ax.imshow(self.data[n], interpolation='nearest')


        # set limits again to preserve zoom
        self.ax.set_xlim(xlim)
        self.ax.set_ylim(ylim)

        # set time as title
        self.ax.set_title(self.fname)

        self.line, = self.ax.plot([],[],'o-',color=([1,1,1]))
        self.actual, = self.ax.plot([],[],'o', color=([1,0,0]))        
        
        self.draw_track()
                                
        self.fig.canvas.draw()
        
        return

    # ................................................................

    def load_set(self, npos, nimg = 100):

        '''
        This routine will load images from file list and convert it 
        into rgb data for interactive plotting.
        '''

        # set start and end position in file list ....................

        dn = nimg // 2
        nmax = len(self.flist)

        nstart = int( np.max( [0,    npos - dn] ) )
        nend   = int( np.min( [nmax, npos + dn + 1] ) )

        # get list for loading files ................................. 
        load_list = self.flist[nstart:nend]
        self.loaded_images = load_list


        rgb_list = []
        for fname in load_list:
            print(fname)
            img = Image.open(fname)

            rgb_list.append(np.array(img))

        
        s = rgb_list[0].shape
        Nt = len(rgb_list)
        self.data = np.vstack(rgb_list).reshape(Nt, *s)
        del rgb_list


        # save vriable as class attributes
        self.nimg = len(load_list)
        self.nmax = len(load_list)
        self.npos = npos
        self.nstart = nstart
        self.nend = nend


        return

    # ................................................................
    def connect(self, event = 'all'):


        if event in ['all', 'mouse']:
            self.mouse = self.fig.canvas.mpl_connect(
                    'button_press_event',  self.clickevent  )

        if event in ['all', 'key']:
            self.key = self.fig.canvas.mpl_connect(
                    'key_press_event',  self.keyevent  )

        return


    # ................................................................
    def disconnect(self, event):

        self.fig.canvas.mpl_disconnect( event )

        return

    # ................................................................
    @debug_run
    def clickevent(self, event):


        if event.button == 1:
            self.proceed_track(event)
            
        if event.button == 2:
            self.del_track(event)

        if event.button == 3:
            self.end_track(event)


    # ................................................................
    @debug_run
    def keyevent(self, event):

        print((event.key))

        if event.key == 'control':
            
            self.disconnect(self.mouse)
            self.rect.set_active(True)

        elif event.key == 'escape':
            self.reset_zoom()

        elif event.key in ['down']:
            self.nstep += 1
            self.plot(self.nstep)
            
        elif event.key in ['up']:
            self.nstep -= 1
            self.plot(self.nstep)

        elif event.key in ['+']:
            self.page_step *=2
            print(('... new page step:',  self.page_step))
            
        elif event.key in ['-']:
             self.page_step /=2
             print(('... new page step:',  self.page_step))

        elif event.key in ['pagedown']:
            self.nstep += self.page_step
            self.plot(self.nstep)
            
        elif event.key in ['pageup']:
            self.nstep -= self.page_step
            self.plot(self.nstep)

        elif event.key in ['backspace']:
            self.remove_trackpoint()

            

    # ................................................................

    def reset_zoom(self):

        self.ax.set_xlim(self.xlim)
        self.ax.set_ylim(self.ylim)
        

        self.fig.canvas.draw()
    # ................................................................
    
    def read(self, track):
        
        ks = sorted(track.keys())

        xsin = {}
        ysin = {}

        for k in ks:
            xsin[k] = track[k][0]
            ysin[k] = track[k][1]


        self.xs.update(xsin)
        self.ys.update(ysin)

        return 

    # ................................................................

    def zoom(self, eclick, erelease):
        xc, yc = eclick.xdata, eclick.ydata
        xr, yr = erelease.xdata, erelease.ydata

        if xc > xr:
            x1 = xr
            x2 = xc
        else:
            x1 = xc
            x2 = xr

        if yc > yr:
            y1 = yr
            y2 = yc
        else:
            y1 = yc
            y2 = yr

            

        self.ax.set_xlim(x1, x2)
        self.ax.set_ylim(y2, y1)
        

        self.fig.canvas.draw()

        self.rect.set_active(False)
        self.connect('mouse')
    # ................................................................

    def track_list(self):
    
        ks = list(self.xs.keys())
        
        x = []
        y = []
        for k in sorted(ks):
            x.append(self.xs[k])
            y.append(self.ys[k])            
        
        return x, y
    # ................................................................
    
    def init_track(self):

        self.xs = {}
        self.ys = {}
        
        return

    # ................................................................
 
    def proceed_track(self, event):

        t = self.timestr

        self.xs[t] = event.xdata
        self.ys[t] = event.ydata

        self.draw_track()       
        
        return
    # ................................................................
 
    def remove_trackpoint(self):

        t = self.timestr

        if t in self.xs:
            del self.xs[t]

        if t in self.ys:
            del self.ys[t]

        self.draw_track()       
        
        return
    # ................................................................

    def del_track(self, event):
        
        self.init_track()
        self.draw_track()
        
        print('...track deleted')
        
        return
    # ................................................................    
    
    def end_track(self, event):

        self.save_tracks()
        self.init_track()    
        self.draw_track()  
        
        print('...save track')
            
        return 
    # ................................................................

    def save_tracks(self):      
        
        ts = sorted(self.xs.keys())
        xs = np.array([ self.xs[t] for t in ts])
        ys = np.array([ self.ys[t] for t in ts])
        

        # make xarray dataset
        coords       = dict( time = ts )
        column_index = xr.DataArray(xs, coords = coords, dims = ('time') )
        row_index    = xr.DataArray(ys, coords = coords, dims = ('time') )
        track_data   = xr.Dataset( dict( column_index = column_index, 
                                         row_index = row_index ) ) 

        
        t0 = ts[0]
        x0, y0 = xs[0], ys[0]
      
        fdir = self.trackdata_path
        trackfile = '%s/track_%s_P%.0fx%.0f.nc' % (fdir, t0, x0, y0)
        self.trackfile = trackfile

        print(('... save track data to %s' % trackfile))
        track_data.to_netcdf(trackfile)

        self.tracks[self.track_number] = track_data
        self.track_number += 1
    
        return
    # ................................................................
    
    def draw_track(self):
        
        # full path
        x, y = self.track_list()
        self.line.set_data(x,y)

        t = self.timestr

        # actual track point
        if t in self.xs:
            self.actual.set_data(self.xs[t],self.ys[t])
        else:
            self.actual.set_data([],[]) 

        self.line.figure.canvas.draw()
        
        return

######################################################################
######################################################################
    
