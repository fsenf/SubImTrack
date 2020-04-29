#!/usr/bin/env ipython

import sys, os, glob
import numpy as np
import pylab as pl

from .ImageTracking import ImageTracking
from PIL import Image

######################################################################
######################################################################


def run( config, fname ):
    '''
    Run the ImageTracking Class.


    Parameters
    ----------
    config : dict
        configuration entries

        'fout' : directory where track data is stored
        'tlim' : range in filename where time info is stored 


    Returns
    -------
    mt : ImageTracking Class
        contains track data as attributes and methods for tracking
    '''

    # ================================================================
    # START OF PARAMETER list ========================================
    # ================================================================


    # set directory name for track data output .......................
    fout = config.get('fout', 'test/trackdata')


    # indicate the range of string in your filename 
    # where the time information is, e.g. myfile_20120612_1000.png
    # has time information at [7:20] -> tlim = (7, 20)
    tlim = config.get('tlim', (7, 20) )


    # ================================================================
    # END OF PARAMETER list ==========================================
    # ================================================================



    # select start file  ---------------------------------------------
    fdir = os.path.dirname( fname )
    fbase = os.path.basename( fname )
    fext = os.path.splitext( fname )[1]
    # ================================================================


    # test time string here ------------------------------------------
    print('PAY ATTENTION!')
    print('Is this your correct time string? ', fbase[tlim[0]:tlim[1]] )
    print('... if YES: fine!')
    print('... if NO: restart tracking with changed tlim')
    print()
    
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

    mt.plot(nimg // 2)
    # ================================================================

    return mt
