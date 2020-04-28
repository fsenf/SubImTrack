#!/usr/bin/env python

import sys, os, glob
import numpy as np
import pylab as pl

import ImageTracking
from ImageTracking import ImageTracking
from PIL import Image

######################################################################
######################################################################



if __name__ == '__main__':

    # ----------------------------------------------------------------
    # CHANGE THESE PARAMETERS FOR YOUR NEEDS--------------------------
    # ----------------------------------------------------------------


    # set directory name for track data output .......................
#    fout = '/vols/talos/home/fabian/data/life_cycles/dust_conv'
    fout = '/vols/talos/home/fabian/data/life_cycles/case_20150611'

    # fout = '/home/fabs/TROPOS/data/track'

    # indicate the range of string in your filename 
    # where the time information is, e.g. myfile_20120612_1000.png
    # has time information at [7:20] -> tlim = (7, 20)
#    tlim = (11, 24)
#    tlim = (13, 28)
    tlim = (7, 20)


    # ================================================================
    # END OF PARAMETER list ==========================================
    # ================================================================



    # select start file  ---------------------------------------------
    fname = sys.argv[1]
    fdir = os.path.dirname(fname)
    fext = os.path.splitext(fname)[1]
    # ================================================================

    
    # create file list -----------------------------------------------
    flist = sorted(glob.glob('%s/*%s' % (fdir, fext)))

    npos = flist.index(fname)
    
    nimg = 11 # number of images to hold in storage
    # ================================================================

    

    # open the image to get its shape --------------------------------
    img = Image.open(fname)
    rmax, cmax = img.size
    del img
    # ================================================================


    # prepare settings -----------------------------------------------
    s = {}
    s['trackdata_path'] = fout
    s['xlim'] = (0, rmax)
    s['ylim'] = (cmax, 0)
    s['tlim'] = tlim
    # ================================================================

    # do the manual tracking -----------------------------------------
    mt = ImageTracking(flist, **s)

    mt.load_set(npos, nimg = nimg)

    mt.plot(nimg / 2)
    # ================================================================
