# -*- coding: utf-8 -*-
"""
Created on Mon May 09 14:10:31 2016

@author: amassett
"""

import gdal,ogr
import os
import numpy as np
#%%
location=r'E:\GOULD\Landsat\McCorkhill'#raster path location###
shloc=r'E:\GOULD\Landsat\test\One_timers'#shape location#
shas=['burnt_block_11']#name of the point shapefile without extension .shp It is used for logging###
outputlocation=r"E:\GOULD\Landsat\test\bulk" ##output location
                      
filez = [f for f in os.listdir(location) if f.endswith(".tif")]##select the tif files      
shpA=os.path.join(shloc,(shas[0] + '.shp'))
#shpB=os.path.join(shloc,(shas[1] + '.shp'))
#%%
def get_metadata(fil):
    """extracts information from the filename
    """
    band=fil[26:30]
    date=fil[9:25]
    return band, date        
def extractbypoint(shp,fil,shID,fileout="csv"):         
    """
    """
    calcthis = [] #TODO: should I really use a list here???
    band = os.path.join(location,fil)    
    src_ds = gdal.Open(band) 
    gt = src_ds.GetGeoTransform()
    rb = src_ds.GetRasterBand(1)
    countpnt = 0
    ds = ogr.Open(shp)
    layer = ds.GetLayer()            
    for feature in layer:
        countpnt = countpnt+1
        geom = feature.GetGeometryRef()
        mx,my = geom.GetX(), geom.GetY()  #coord in map units
            #Convert from map to pixel coordinates.
            
        px = int((mx - gt[0]) / gt[1]) #x pixel
        py = int((my - gt[3]) / gt[5]) #y pixel
        try:        
            intval = rb.ReadAsArray(px,py,1,1)
            calcthis.append(intval[0])#####<<<<<--------------------------------intval[0] is the pixel value
        except:
            pass
    src_ds = None
    rb = None
    ds = None
    layer = None ###close the datasets
    out = np.array(calcthis)
    band , date = get_metadata(fil)    
    namepart = "{}_{}_{}.npy".format(date,band,shID)    
    name = os.path.join(outputlocation,namepart)
    np.save(name,out)    

for fil in filez:
    extractbypoint(shpA,fil,"fire_88_block11")

