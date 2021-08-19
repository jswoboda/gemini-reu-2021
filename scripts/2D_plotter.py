#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul  6 14:02:48 2021

@author: wrightig
"""
#!/usr/bin/env python3
"""
@author: zettergm
"""

import gemini3d.read
import os
from plotcurv import plotcurv2D
from matplotlib.pyplot import show, savefig,figure, style
import gemini3d.coord
from celluloid import Camera
import iri2016 as iri
from gemini3d.grid.convert import geomag2geog
from gemini3d.grid.gridmodeldata import model2magcoords
import numpy as np
import datetime
import xarray as x
# load some sample data (2D)
direc = "/home/wrightig/simulations/ion_sim"

cfg = gemini3d.read.config(direc)
xg = gemini3d.read.grid(direc)
element="ne"
glat=0
time =  datetime.datetime(2011, 3, 12,5,0,0)

# grid data
files=os.listdir(direc)
sfiles=[file for file in files if file.endswith('.h5')]
numberfiles=len(sfiles)
results_dir='/home/wrightig/REU/presentation_diurnal/'+element+'/'

if not os.path.isdir(results_dir):
    os.makedirs(results_dir)
altstuff=np.linspace(80000,1079868.45,80)

for i in range(numberfiles-10,numberfiles):
    dat = gemini3d.read.frame(direc, cfg["time"][i])
    #alti, mloni, mlati, parmi,l = model2magcoords(xg, dat[element], 24, 1, 24)
    style.use("dark_background")
    
    title= "Electron density (e/m^3) "+'  '+str((cfg["time"][i] + datetime.timedelta(hours=9)).time())+' Local'
    plotcurv2D(xg, dat[element],lalt=1024, llat=1024, label=title, vcmax=3e12)#,vcmin=100, vcmax=10e3)#,title,ilon=0, llon=1)#,lalt=512, llat=512)#,vcmax=3.5e12)#,vcmin=800)
    #mloni=mloni+258.64
    #mlati=mlati+96.9
    #savefig(results_dir+element+'_'+str(cfg["time"][i])+'_'+str(i).zfill(3)+'.png',dpi=200)
    show()

# gloniri, glatiri=geomag2geog(np.radians(np.repeat(mloni[0],512)), np.radians(mlati+90))
# frames=[]
# for i in range(512):
#     frames.append(iri.IRI(time, [150,600,4], glatiri[i], gloniri[i]))
                                  
# sim=x.concat(frames,'mlat')
# fg = figure()
# ax = fg.gca()
# plot=ax.pcolormesh(sim.glat, sim.alt_km, sim.ne.T, shading="nearest",vmax=3.5e12)
# ax.set_title("Electron Dens "+str(time))
# ax.set_xlabel("glat")
# ax.set_ylabel("altitude [km]")
# fg.colorbar(plot, ax=ax)