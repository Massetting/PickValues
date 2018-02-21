# -*- coding: utf-8 -*-
"""
Created on Thu Feb 15 18:14:41 2018

@author: amassett
"""

import numpy as np
import os
import datetime as dt
import matplotlib.pyplot as plt
location=r"E:\GOULD\Landsat\test\bulk"
ff=[f for f in os.listdir(location) if f.endswith(".npy")]
def get_date(filestring):
    year=int(filestring[:4])
    month=int(filestring[5:7])
    day=int(filestring[8:10])
    date=dt.date(year,month,day)
    return date
def loadnpy(filestring,parentfolder=location):
    array=np.load(os.path.join(parentfolder,filestring))
    return array    
arrays={}
for f in ff:
    arrays[f]=loadnpy(f)
delete=[f for f in arrays.keys() if arrays[f].shape==(0,)]
delete1=[f for f in arrays.keys() if np.all(arrays[f]==-999)]    

def delete_row(list_to_be_deleted):
    """deletes from loaded dictionary and from disk based on a list of filestrings.
    """
    for  k in list_to_be_deleted:
        del arrays[k]
        os.remove(os.path.join(location,k))
    
delete_row([f for f in arrays.keys() if arrays[f].shape==(0,)])#delete empty numpy arrrays:they are empty because the point shapefile was out of range.
delete_row([f for f in arrays.keys() if np.all(arrays[f]==-999)] )#delete numpy arrays filled with nodata, which is -999; those come from an inrange extent for the coordinates of the points, but an empty
dates=[]    
means=[]    
std=[]
for i,k in arrays.items():

    if arrays[i][arrays[i]==-999].shape[0]==0:
        date=get_date(i)
        dates.append(date)
        means.append(np.mean(arrays[i]))
        std.append(np.std(arrays[i]))
        


  

#%%

fig,ax=plt.subplots()
#ax=fig.add_subplot()
def elev(age,mod="percent_cover"):
    if mod=="percent_cover":    
        x=1.78*(1-np.exp(-0.142*age))
        return (x/2.2)
    if mod=="fuel_load_s+ns":    
        x=(1-np.exp(-0.15*age))
        return (x*0.8)        
    

init=dt.date(2003, 1, 1)
plotdt=[]
ploty=[]
plotstdy=[]
for d,vs in vspi.items():
    if  int(d[0:4])>=2003:
        curr=dt.date(int(d[0:4]), int(d[4:6]), int(d[6:8]))
        delta=curr-init
        years=delta.days/30.0#math.ceil(delta.days/365.0)
        plotdt.append(years)
        ploty.append((490-vs[1])/590)
        plotstdy.append(vs[2]/590)
ax.errorbar(plotdt, ploty, plotstdy, linestyle='None', marker='^')
plotdt=[]
ploty=[]
plotstdy=[]
for d,vs in nbr.items():
    if  int(d[0:4])>=2003:
        curr=dt.date(int(d[0:4]), int(d[4:6]), int(d[6:8]))
        delta=curr-init
        years=delta.days/30.0#math.ceil(delta.days/365.0)
        plotdt.append(years)
        ploty.append((((0.25+vs[1])/(0.25+0.37))))
        plotstdy.append((vs[2]/(0.25+0.37)))
ax.errorbar(plotdt, ploty, plotstdy, linestyle='None', marker='.')        

plotdt=[]
ploty=[]
plotstdy=[]
for d,vs in ndvi.items():
    if  int(d[0:4])>=2003:
        curr=dt.date(int(d[0:4]), int(d[4:6]), int(d[6:8]))
        delta=curr-init
        years=delta.days/30.0#math.ceil(delta.days/365.0)
        plotdt.append(years)
        ploty.append((((vs[1]-0.25)/(0.78-0.25))))
        plotstdy.append(((vs[2]/(0.78-0.25))))        
ax.errorbar(plotdt, ploty, plotstdy, linestyle='None', marker='.')

x=[f for f in range(0,100)]    
cover=[]
for i in sorted(plotdt):
    cover.append(elev(i,mod="fuel_load_s+ns"))

ax.plot(sorted(plotdt),cover) 
 
plt.show()    
#%%
fig,ax=plt.subplots()
#x=[f for f in range(0,100)]    
def elev(age,mod="percent_cover"):
    if mod=="percent_cover":    
        x=1.78*(1-np.exp(-0.142*age))
        return (x/2.2)
    if mod=="fuel_load_s+ns":    
        x=9.92*(1-np.exp(-0.057*age))
        return (x)  

plotdt=[]
ploty=[]
plotstdy=[]
for d,vs in vspi.items():
    if  int(d[0:4])>=2003:
        curr=dt.date(int(d[0:4]), int(d[4:6]), int(d[6:8]))
        delta=curr-init
        years=delta.days/30.0#math.ceil(delta.days/365.0)
        plotdt.append(years)
        ploty.append((490-vs[1])/590)
        plotstdy.append(vs[2]/590)
cover=[]
for i in plotdt:
    cover.append(elev(i,mod="fuel_load_s+ns"))
vsp=(round(np.corrcoef(ploty,cover)[1,0],2))

ax.scatter(cover,ploty,marker="s",color="r")
ax.set_xlabel('bulk density')
ax.set_ylabel('indices')
#plt.show()




plotdt=[]
ploty=[]
plotstdy=[]
for d,vs in nbr.items():
    if  int(d[0:4])>=2003:
        curr=dt.date(int(d[0:4]), int(d[4:6]), int(d[6:8]))
        delta=curr-init
        years=delta.days/30.0#math.ceil(delta.days/365.0)
        plotdt.append(years)
        ploty.append((((0.25+vs[1])/(0.25+0.37))))
        plotstdy.append((vs[2]/(0.25+0.37)))

nb=(round(np.corrcoef(ploty,cover)[1,0],2))
ax.scatter(cover,ploty,marker=".",color="g")
#plt.show()




plotdt=[]
ploty=[]
plotstdy=[]
for d,vs in ndvi.items():
    if  int(d[0:4])>=2003:
        curr=dt.date(int(d[0:4]), int(d[4:6]), int(d[6:8]))
        delta=curr-init
        years=delta.days/30.0#math.ceil(delta.days/365.0)
        plotdt.append(years)
        ploty.append((((vs[1]-0.25)/(0.78-0.25))))
        plotstdy.append(((vs[2]/(0.78-0.25))))  
nd=(round(np.corrcoef(ploty,cover)[1,0],2))
ax.scatter(cover,ploty,marker="^",color="b")
ax.text(-1.5,0.8,"coeff of corr: \n VSPI: {} \n NBR: {}\n NDVI: {}".format(vsp,nb,nd),bbox={'facecolor':'white', 'alpha':0.5, 'pad':10})

handles, labels = ax.get_legend_handles_labels()
ax.legend(handles, labels)
plt.show()



#%%