# -*- coding: utf-8 -*-
"""
Created on Thu Feb 15 18:14:41 2018

@author: amassett
"""
import math
import numpy as np
import os
import datetime as dt
import matplotlib.pyplot as plt
location=r"E:\WA\Validation_RSE_after_Reviews"

def select_bands(location,band,sample="fire"):
    """band="3"
    """
    if sample=="fire":
        fire=[f for f in os.listdir(location) if (f[9:10]==band and f.endswith("fire.npy"))]
        return fire
    if sample=="control":
        control=[f for f in os.listdir(location) if (f[9:10]==band and f.endswith("control.npy"))]
        return control
    if sample=="both":    
        control=[f for f in os.listdir(location) if (f[9:10]==band and f.endswith("control.npy"))]
        fire=[f for f in os.listdir(location) if (f[9:10]==band and f.endswith("fire.npy"))]
        return fire, control

def get_date(band):
    dates={}
    temp = select_bands(location,band)
    for i in temp:
        dates[i[:8]]=i
    return dates

def get_vspi(log="1"):
    b5 = get_date("5")
    b7 = get_date("7")
    inter=-318.81978991
    slope=0.78393920
    factor=(1/(np.sqrt((slope**2)+1)))
    vspi={}
    for date in b5.keys():
        arr5 = np.load(os.path.join(location,b5[date]))
        arr7 = np.load(os.path.join(location,b7[date]))
        arr5[arr5==0]=np.nan
        arr5[arr7==0]=np.nan
        arr7[arr5==0]=np.nan        
        arr7[arr7==0]=np.nan
        index=(((arr7-(slope*arr5)-inter)*factor))        
        vspi[date]=["_",np.nanmean(index),np.nanstd(index)]
        if log=="1":
            print("date: {}; mean: {}; std: {}\n".format(date,round(np.nanmean(index),2),round(np.nanstd(index)),2))
    return vspi    
def get_nbr(log="0"):
    b5 = get_date("5")
    b4 = get_date("4")
    nbr={}
    for date in b5.keys():
        arr5 = np.load(os.path.join(location,b5[date]))
        arr4 = np.load(os.path.join(location,b4[date]))
        arr5[arr5==0]=np.nan
        arr5[arr4==0]=np.nan
        arr4[arr5==0]=np.nan        
        arr4[arr4==0]=np.nan
        index=(arr4-arr5)/(arr5+arr4)#(((b7-(slope*b5)-inter)*factor))        
        nbr[date]=["_",np.nanmean(index),np.nanstd(index)]
        if log=="1":
            print("date: {}; mean: {}; std: {}\n".format(date,round(np.nanmean(index),2),round(np.nanstd(index)),2))
    return nbr

def get_ndvi():
    b3 = get_date("3")
    b4 = get_date("4")
    ndvi={}
    for date in b3.keys():
        arr3 = np.load(os.path.join(location,b3[date]))
        arr4 = np.load(os.path.join(location,b4[date]))
        arr3=arr3.astype(np.float32)
        arr3[arr3==0]=np.nan
        arr3[arr4==0]=np.nan
        arr4[arr3==0]=np.nan        
        arr4[arr4==0]=np.nan
        index=(arr4-arr3)/(arr3+arr4)#(((b7-(slope*b5)-inter)*factor))        
        ndvi[date]=["_",np.nanmean(index),np.nanstd(index)]
    return ndvi

  
vspi = get_vspi()
nbr = get_nbr()  
ndvi = get_ndvi()

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