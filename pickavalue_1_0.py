# -*- coding: utf-8 -*-
"""
Created on Mon May 09 14:10:31 2016

@author: amassett
"""

import gdal,ogr
import os
from multiprocessing import Pool
import numpy as np

location=r'E:\WA'#raster path location###
shloc=r'E:\WA\gis_2017'#shape location#
shas=['cooke_point','controlcookepoints']#name of the point shapefile without extension .shp It is used for logging###
outputlocation=r"E:\WA\Validation_RSE_after_Reviews" ##output location
                      
filez = [f for f in os.listdir(location) if f.endswith(".tif")]##select the tif files      
shpA=os.path.join(shloc,(shas[0] + '.shp'))
shpB=os.path.join(shloc,(shas[1] + '.shp'))

def get_metadata(fil):
    """extracts information from the filename
    """
    band=fil[9:10]
    date=fil[:8]
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
        intval = rb.ReadAsArray(px,py,1,1)
        calcthis.append(intval[0])#####<<<<<--------------------------------intval[0] is the pixel value
    src_ds = None
    rb = None
    ds = None
    layer = None ###close the datasets
    out = np.array(calcthis)
    band , date = get_metadata(fil)    
    namepart = "{}_{}_{}.npy".format(date,band,shID)    
    name = os.path.join(outputlocation,namepart)
    np.save(name,out)    
    #arr = np.ma.array(calcthis)
    #std = np.std(arr)
    #mean = np.std(arr)   
    
    #return mean,std    


    #TODO: export to file
    #if fileout=="csv":
     #   pass


def apply_to_file(fil):
    """Just so that the function gets only one argument for multiprocessing
    """
    extractbypoint(shpA,fil,shID = "fire")
    extractbypoint(shpB,fil,shID = "control")
        ##NOTE if you want to use multiprocessing you should save calcthis to a file
if __name__ == '__main__':
    pool = Pool(6)       
    pool.map(apply_to_file, filez)#Multiprocess of the iteration:    for i in shas: extractbypoint(i)###just works as a for loop 
    quit()