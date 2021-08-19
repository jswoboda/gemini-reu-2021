#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 21 18:15:25 2021

@author: wrightig
"""
import cartopy.crs as ccrs
import cartopy.feature as cf

import ephem
import matplotlib.pyplot as plt

import numpy as np

from datetime import datetime, timedelta
#radius of obscuration
Ro=4200





def ec_glon(t):
    if t<=39120:
        glon=-1.83080595E-10*t**3+1.64481294E-5*t**2-4.58703077E-1*t+4.01939187E3
    else:
        glon=-3.70904106E-8*t**3+4.55216041E-3*t**2-1.86213961E2*t+2.53904684E6

    return glon

def ec_glat(t):
    if t<=39600:
        glat=-7.19671597E-7*t**2+6.30138989E-2*t-1.27831497E3

    else:
        glat=-4.87899687E-6*t**2+3.82669565E-1*t-7.41458916E3
    return glat
#path interperolated from https://eclipse.gsfc.nasa.gov/SEpath/SEpath2001/SE2021Jun10Apath.html

lon=360-np.linspace(0,360,400)
lat=np.linspace(-90,90,400)
lon2d, lat2d = np.meshgrid(lon, lat)
def get_eclipse(t0,n_t=1,dt=60.0,alts=[100e3],lats=[69.0],lons=[16.02]):
    # Location
    obs = ephem.Observer()
    n_alts=len(alts)
    n_lats=len(lats)
    n_lons=len(lons)
    
    p=np.zeros([n_t,n_alts,n_lats,n_lons])
    times=np.arange(n_t)*dt
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
                    s=np.degrees(ephem.separation(sun,moon))
                    percent_eclipse=0.0
                    # if loi==0:
#                     #     print(lai,sun.az,sun.alt,moon.az,moon.alt,s)
#                     if s <= (r_moon+r_sun):
# #                        print("eclipsed")
#                         if s < 1e-3:
#                             percent_eclipse=intersection(r_moon,r_sun,s,n_s=100)
#                         else:
#                             percent_eclipse=intersection(r_moon,r_sun,s,n_s=100)

                                        
                    if np.degrees(sun.alt) <= r_sun:
                        if np.degrees(sun.alt) <= -r_sun:
                            percent_eclipse=1.0
                        else:
                            percent_eclipse=1.0-((np.degrees(sun.alt)+r_sun)/(2.0*r_sun))*(1.0-percent_eclipse)
                    

                    p[ti,ai,lai,loi]=percent_eclipse
        dts.append(obs.date)
    return(p,times,dts)

def distance_chkr(lat1,lon1,lat2,lon2):
    R=6373.0

    lat1=np.radians(lat1)
    lon1=np.radians(lon1)
    lat2=np.radians(lat2)
    lon2=np.radians(lon2)
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = np.sin(dlat / 2)**2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon / 2)**2
    c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1 - a))

    distance = R * c
    return distance



def mask(dists):
    mask=dists
    
    for ix,iy in np.ndindex(mask.shape):
        if abs(mask[ix,iy]) >= Ro:
            mask[ix,iy]=1
        else:
            mask[ix,iy]=.15+.85*mask[ix,iy]/Ro
    return mask
        
def position(t, t_f = 67740 , t_i = 61215, phi_i = 258, theta_i = 57, phi_f = 255, theta_f = 85):
    del_phi = phi_f - phi_i
    del_theta = theta_f - theta_i
    del_t=t_f-t_i
    phi= phi_i + del_phi/del_t*(t-t_i)
    theta=theta_i+del_theta/del_phi*(phi-phi_i)
    return theta, phi


#go from ~9:50-11:30 UT time, 40 time steps
t=np.linspace(9.8*3600,11.5*3600,40)

for i in range(len(t)):
    plt.figure(figsize=(25, 10))
    ax = plt.axes(projection=ccrs.NearsidePerspective(central_latitude=75,central_longitude=-100, satellite_height= 65785831))
    ax.clear()
    ax.coastlines()
    ax.add_feature(cf.BORDERS)

    distances = distance_chkr(lat2d,lon2d,ec_glat(t[i]),ec_glon(t[i]))
    p=mask(distances)
    plt.title(label="June 10, 2021:  "+str(timedelta(seconds=int(t[i])))+" UTC", fontsize=24,pad=.2)
    juha=get_eclipse(t0=ephem.date((2021,6,10))+ephem.second*t[i],alts=[0],lats=lat,lons=lon)
    ax.pcolormesh(lon2d, lat2d, np.multiply(p,1.0-juha[0][0,0,:,:]),transform=ccrs.PlateCarree(),vmin=0,vmax=1,cmap='inferno')

    plt.savefig('/home/wrightig/frame_'+str(i).zfill(3)+'.png')
    plt.show()








