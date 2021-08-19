#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 21 10:28:36 2021

@author: wrightig
"""


import gemini3d.read
import os
from plotcurv import plotcurv3D
from matplotlib.pyplot import show, savefig,figure
import gemini3d.coord
from matplotlib import pyplot
from celluloid import Camera
import iri2016 as iri




# load some sample data (3D)
direc = "/home/wrightig/eq_retry"
# Read cfg to get time stamps
cfg = gemini3d.read.config(direc)
# grid data
xg = gemini3d.read.grid(direc)
element="ne"
index=0 


files=os.listdir(direc)
sfiles=[file for file in files if file.endswith('.h5')]
numberfiles=len(sfiles)
results_dir='/home/wrightig/REU/'+element+'s'+'/'

if not os.path.isdir(results_dir):
    os.makedirs(results_dir)

fig = figure()
camera = Camera(fig)
# loops through all output files in direc and makes animation afterward
for i in range(numberfiles):
    title= element+'  '+str(cfg["time"][i])
    dat=gemini3d.read.frame(direc, cfg["time"][i])
    #llat lalt llon control resolution of interperolation. dangerous for RAM if too high!
    plotcurv3D(xg, dat[element], cfg,coords='geog',label=title, llat=64,lalt=64,llon=64)
    camera.snap()
    savefig(results_dir+element+'_'+str(cfg["time"][i])+'_'+str(i).zfill(3)+'.png')
    
    show()
animation = camera.animate()
animation.save(results_dir+'animation.mp4')





