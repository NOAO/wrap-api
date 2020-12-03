#!/usr/bin/env python

import sys
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
import numpy as np
import math
import requests
import json
import healpy as hp
from pprint import pprint as pp  # pretty print

##############################################################################
# functions to order the vertices of HDU corners in counter-clockwise
# direction, so that their polygon is convex
#
# reference:
# https://algorithmtutor.com/Computational-Geometry/Area-of-a-polygon-given-a-set-of-points/

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return '(' + str(self.x) + ', ' + str(self.y) + ')'
    
def distance(p1, p2):
    d = np.sqrt((p2.x - p1.x)**2 + (p2.y - p1.y)**2)
    return d
    
def average_point_inside(points):
    x = 0
    y = 0
    for point in points:
        x += point.x
        y += point.y
    return Point(x / len(points), y / len(points))

def angle(p1, p2):
    k = (p2.y - p1.y) / distance(p1, p2)

    x2 = p2.x
    x1 = p1.x

    if k >= 0:
        if x2 >= x1: # First Quadrant
            return (2.0 * math.pi - math.asin(k))
        else: # Second Quadrant
            return (math.pi + math.asin(k))
    else:
        if x2 >= x1: # Fourth Quadrant
            return math.asin(-k)
        else: # Third Quadrant
            return (math.pi - math.asin(-k))
        
def sort_angular(points, reference_point):
    return sorted(points, key = lambda point: -angle(point, reference_point))

def sort_radec(ra,dec):
    points = [Point(ra[0],dec[0]), Point(ra[1],dec[1]), Point(ra[2],dec[2]), Point(ra[3],dec[3])]
    reference_point = average_point_inside(points)
    spoints =  sort_angular(points, reference_point)
    ra1s=[]
    dec1s=[]
    for p in spoints:
        ra1s.append(p.x)
        dec1s.append(p.y)
    return np.array(ra1s),np.array(dec1s)


##############################################################################

def gen_exposure_map(fapi,hapi):
    jj = {"outfields" : ["md5sum", "AIRMASS", "G-TRANSP"],
          "search" : [
              ["instrument", "decam"],
              ["proc_type", "instcal"],
              ["prod_type", "image"],
              ["obs_type", "object"],
              ["proposal", "2012B-0001"],
              ["ifilter", "r DECam", "contains"]
          ]}
    res = fapi.search(jj, limit=500000)
    dff = pd.read_json(json.dumps(res[1:]))

    # Now we'll get the information needed from the individual HDUs.
    # This will take longer, because the number of HDUs is nearly two
    # orders of magnitude larger than the number of full files.
    jj = {"outfields" : ["fitsfile",
                         "hdu_idx",
                         "fitsfile__archive_filename",
                         "fitsfile__exposure",
                         "fitsfile__ifilter",
                         "CENRA1",
                         "CENDEC1",
                         "COR1RA1",
                         "COR2RA1",
                         "COR3RA1",
                         "COR4RA1",
                         "COR1DEC1",
                         "COR2DEC1",
                         "COR3DEC1",
                         "COR4DEC1",
                         "FWHM",
                         "AVSKY", ],
          "search" : [
              ["fitsfile__caldat", "2018-09-01", "2020-09-01"] ,
              ["fitsfile__instrument", "decam"],
              ["fitsfile__proc_type", "instcal"],
              ["fitsfile__prod_type", "image"],
              ["fitsfile__obs_type", "object"],
              ["fitsfile__proposal", "2012B-0001"],
              ["fitsfile__ifilter", "r DECam", "contains"]
          ]}
    
    res = hapi.search(jj, limit=5000000)
    df2 = pd.read_json(json.dumps(res[1:]))

    dfm = pd.merge(dff,df2,left_on='md5sum',right_on='fitsfile')
    dfmc = dfm.dropna()

    apix = 0.263 # arcsec/pixel
    sky = dfmc['AVSKY']/dfmc['fitsfile__exposure'] # sky rate
    tau = dfmc['G-TRANSP']**2/(dfmc['FWHM']*apix/0.9)**2/(sky/3.)

    a = plt.hist(tau,bins=200,range=(0,1))
    plt.xlabel('tau')

    tau_trim = np.clip(tau,0,1) # tau should be between 0 and 1

    # Making the depth map <a id="depth" />


    # Pull out the HDU corners
    ratab = [np.array([row[0],row[1],row[2],row[3]])
             for row in dfmc[['COR1RA1','COR2RA1','COR3RA1','COR4RA1']].values]
    dectab = [np.array([row[0],row[1],row[2],row[3]])
              for row in dfmc[['COR1DEC1','COR2DEC1','COR3DEC1','COR4DEC1']].values]


    adectab_s = [sort_radec(ra1,dec1) for ra1,dec1 in zip(ratab,dectab)]
    vectab = [hp.ang2vec(ra1,dec1,lonlat=True) for ra1, dec1 in radectab_s]    

    # Define the Healpix map
    nside = 4096
    print('Resolution is {:5.2f} arcmin'.format(hp.nside2resol(nside,arcmin=True)))
    map = np.zeros(hp.nside2npix(nside)) # raw exposure map
    tmap = map.copy() # teff map

    # Loop over HDUs (slow!)
    for vec,exptime,tau1 in zip(vectab,dfmc['fitsfile__exposure'],tau_trim):
        try:
            ipix = hp.query_polygon(nside,vec)
            map[ipix] += exptime
            tmap[ipix] += tau1 * exptime
        except:
            pass

    # Show the map
    fig = plt.figure(figsize=(15,15))
    hp.orthview(tmap,rot=(20,-30),fig=1,cmap='inferno',half_sky=True,min=0,max=1000)

    # Zooming in
    hp.gnomview(tmap,reso=0.75,cmap='inferno',rot=(8,-44),min=0,max=1000)
    
    return tmap 


##############################################################################


def main():
    parser = argparse.ArgumentParser(
        #version='1.0.0',
        description='Generate exposure map for a survey (from: Knut Olsen)',
        epilog='EXAMPLE: %(prog)s a b"'
        )
    parser.add_argument('--outdir',
                        help='Directory to download files into. (must exist)' )
    args = parser.parse_args()

    fapi =  helpers.api.FitsFile()
    hapi =  helpers.api.Hdu()

    map = gen_exposure_map(fapi,hapi)

if __name__ == '__main__':
    main()
