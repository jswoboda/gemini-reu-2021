#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 29 02:14:43 2021

@author: wrightig
# Adapted from Juha Vierinen: http://www.radio-science.net/2017/08/eclipse-visualizations-using-python.html
"""
#!/usr/bin/env python
#
# Calculate the totality of the eclipse.
#
import cartopy.crs as ccrs
import cartopy.feature as cf
import ephem
import numpy as n
import matplotlib.pyplot as plt
from celluloid import Camera

# numerically approximate eclipse fraction
def intersection(r0,r1,d,n_s=100):
    A1=n.zeros([n_s,n_s])
    A2=n.zeros([n_s,n_s])
    I=n.zeros([n_s,n_s])
    x=n.linspace(-2.0*r0,2.0*r0,num=n_s)
    y=n.linspace(-2.0*r0,2.0*r0,num=n_s)
    xx,yy=n.meshgrid(x,y)
    A1[n.sqrt((xx+d)**2.0+yy**2.0) < r0]=1.0
    n_sun=n.sum(A1)
    A2[n.sqrt(xx**2.0+yy**2.0) < r1]=1.0
    S=A1+A2
    I[S>1]=1.0
    eclipse=n.sum(I)/n_sun
    return(eclipse)
# calculate the fraction that sun is eclipsed at given altitudes, latitude, and longitude
#
# returns eclipse fraction (0..1) and time (seconds after t0) 
def get_eclipse(t0,n_t=1,dt=60.0,alts=[100e3],lats=[69.0],lons=[16.02]):
    # Location
    obs = ephem.Observer()
    n_alts=len(alts)
    n_lats=len(lats)
    n_lons=len(lons)
    
    p=n.zeros([n_t,n_alts,n_lats,n_lons])
    times=n.arange(n_t)*dt
    dts=[]
    for ti,t in enumerate(times):
        print("Time %1.2f (s)"%(t))
        for ai,alt in enumerate(alts):
            for lai,lat in enumerate(lats):
                for loi,lon in enumerate(lons):
                    #obs.lon, obs.lat = '-1.268304', '51.753101'#'16.02', '78.15' # ESR
                    obs.lon, obs.lat = '%1.2f'%(lon), '%1.2f'%(lat) # ESR
                    obs.elevation=alt
                    obs.date= t0#(ephem.date(ephem.date(t0)+t*ephem.second))
                    sun, moon = ephem.Sun(), ephem.Moon()
                    
                    # Output list
                    results=[]
                    seps=[]
                    sun.compute(obs)
                    moon.compute(obs)
                    r_sun=(sun.size/2.0)/3600.0
                    r_moon=(moon.size/2.0)/3600.0
                    s=n.degrees(ephem.separation(sun,moon))
                    percent_eclipse=0.0
                    # if loi==0:
                    #     print(lai,sun.az,sun.alt,moon.az,moon.alt,s)
                    if s <= (r_moon+r_sun):
#                        print("eclipsed")
                        if s < 1e-3:
                            percent_eclipse=1.0
                        else:
                            percent_eclipse=intersection(r_moon,r_sun,s,n_s=100)-.15# to match simple mask

                                        
                    if n.degrees(sun.alt) <= r_sun:
                        if n.degrees(sun.alt) <= -r_sun:
                            percent_eclipse=1.0
                        else:
                            percent_eclipse=1.0-((n.degrees(sun.alt)+r_sun)/(2.0*r_sun))*(1.0-percent_eclipse)
                    

                    p[ti,ai,lai,loi]=percent_eclipse
        dts.append(obs.date)
    return(p,times,dts)



def plot_map(p,lons,lats,t0,alt=0,lat_0=40,lon_0=-60):
    fig = plt.figure(figsize=(8,8))
    plt.style.use('dark_background')

    m = plt.axes(projection=ccrs.NearsidePerspective(central_latitude=75,central_longitude=-100,satellite_height= 65785831))
    # draw coastlines, state and country boundaries, edge of map.
    m.coastlines()
    m.add_feature(cf.BORDERS)
    
    lon,lat=n.meshgrid(lons,lats)
    # compute map proj coordinates.
    # draw filled contours.
    cs = m.pcolormesh(lon,lat,1.0-p[0,0,:,:],vmin=0,vmax=1.0,cmap="inferno",transform=ccrs.PlateCarree())


    plt.title(ephem.date(t0).datetime().strftime("%d %B, %Y  %H:%M:00")+ " UTC", fontsize=20)
    fname="eclipse-%f.png"%(float(t0))
    plt.savefig(fname)
    plt.show()
    return m

t0=ephem.date((2021,6,10,9,50,1))
lons=360-n.linspace(0,360,400)
lats=n.linspace(-90,90,400)
for i in range(49):
    ec=get_eclipse(t0=t0+ephem.second*120*i,alts=[0e3],n_t=1,lats=lats,lons=lons)
    plot_map(ec[0],t0=t0+ephem.second*120*i,lats=lats,lons=lons)
    
    
    
    
