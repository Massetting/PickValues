# -*- coding: utf-8 -*-
"""
Created on Mon May 09 14:10:31 2016

@author: amassett
"""

import gdal,ogr
import os
from multiprocessing import Pool

location=r'E:\NSW\indices'#raster path location###
shloc=r'E:\ArcWorkspace\nsw'#shape location#
shas=['control1','control2']#name of the point shapefile without extension .shp It is used for logging###

def extractbypoint(shpID):          
        shpfile=shpID + '.shp'
        shp=os.path.join(shloc,shpfile)                                
        newDir=os.path.join(location,shpID) ##output location
        if not os.path.exists(newDir):
            os.mkdir(newDir)                        
        filez = [f for f in os.listdir(location) if f.endswith(".tif")]##select the tif files      
        filename={}
        for fil in filez:
            calcthis=[]
            filename[fil]=os.path.join(location,fil)
            band=filename[fil]
            src_ds=gdal.Open(band) 
            gt=src_ds.GetGeoTransform()
            rb=src_ds.GetRasterBand(1)
            countpnt=0
            ds=ogr.Open(shp)
            layer=ds.GetLayer()            
            for feature in layer:
                countpnt=countpnt+1
                geom = feature.GetGeometryRef()
                mx,my=geom.GetX(), geom.GetY()  #coord in map units
            #Convert from map to pixel coordinates.
            #Only works for geotransforms with no rotation.
                px = int((mx - gt[0]) / gt[1]) #x pixel
                py = int((my - gt[3]) / gt[5]) #y pixel
                intval=rb.ReadAsArray(px,py,1,1)
                calcthis.append(intval[0])#####<<<<<--------------------------------intval[0] is the pixel value
            src_ds=None
            rb=None###close the datasets
        

        ##NOTE if you want to use multiprocessing you should save calcthis to a file
if __name__ == '__main__':
    pool = Pool()       
    pool.map(extractbypoint, shas)#Multiprocess of the iteration:    for i in shas: extractbypoint(i)###just works as a for loop 
    quit()