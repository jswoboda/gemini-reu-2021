#!/usr/bin/env python3
"""
@author: zettergm
"""

from __future__ import annotations
import typing as T

from matplotlib.pyplot import figure, title, tight_layout, savefig, subplots
import xarray
from gemini3d.grid.convert import geomag2geog
from gemini3d.grid.gridmodeldata import model2magcoords, model2geogcoords
from math import pi
import numpy as np

def plotcurv3D(
    xg: dict[str, T.Any],
    parm: xarray.DataArray,
    cfg: dict[str, T.Any],
    lalt: int = 256,
    llon: int = 256,
    llat: int = 256,
    coords: str = 'geomag',
    label: str = None
):
    """plot dipole data vs. alt,lon,lat"""
    if coords == 'geomag':
        # grid data; wasteful and should only do a slice at a time???
        alti, mloni, mlati, parmi = model2magcoords(xg, parm, lalt, llon, llat)
        
        # define slices indices
        altref = 300e3
        ialt = abs(alti - altref).argmin()
        lonavg = np.median(mloni)
        ilon = abs(mloni - lonavg).argmin()
        latavg = np.median(mlati)
        ilat = abs(mlati - latavg).argmin()
        

        
        # plot various slices through the 3D domain
        fg, axs = subplots(1,3,figsize=(12,4))
        if title != None:
             fg.suptitle(label)
        

        
        ax = axs[0]
        ax.title.set_text('mlat = '+str(round(mlati[ilat],1)))
        h = ax.pcolormesh(mloni, alti / 1e3, parmi[:, :, ilat], shading="nearest")
        ax.set_xlabel("mlon")
        ax.set_ylabel("alt")
        fg.colorbar(h, ax=ax)
    
        ax = axs[1]
        ax.title.set_text('alt = '+str(round(alti[ialt]/1000,1)))
        h = ax.pcolormesh(mloni, mlati, parmi[ialt, :, :].transpose(), shading="nearest")
        ax.set_xlabel("mlon")
        ax.set_ylabel("mlat")
        fg.colorbar(h, ax=ax)
    
        ax = axs[2]
        ax.title.set_text('mlon = '+str(round(mloni[ilon],1)))
        ax.pcolormesh(mlati, alti / 1e3, parmi[:, ilon, :], shading="nearest")
        ax.set_xlabel("mlat")
        ax.set_ylabel("alt")
        fg.colorbar(h, ax=ax)
        tight_layout(pad=1.2, w_pad=.25)
    elif coords == 'geog':
        # grid data; wasteful and should only do a slice at a time???
        #alti, mloni, mlati, parmi = model2magcoords(xg, parm, lalt, llon, llat)
        alti, gloni, glati, parmi = model2geogcoords(xg, parm, lalt, llon, llat)
        # define slices indices
        altref = 300e3
        ialt = abs(alti - altref).argmin()
        lonavg = cfg["glon"]
        ilon = abs(gloni - lonavg).argmin()
        latavg = cfg["glat"]
        ilat = abs(glati - latavg).argmin()
        
        # plot various slices through the 3D domain

        
        fg, axs = subplots(1,3,figsize=(12,4))
        if title != None:
             fg.suptitle(label)
        
        ax = axs[0]
        ax.title.set_text('glat = '+str(round(glati[ilat],1)))
        h = ax.pcolormesh(gloni, alti / 1e3, parmi[:, :, ilat], shading="nearest")
        ax.set_xlabel("glon")
        ax.set_ylabel("alt")
        fg.colorbar(h, ax=ax)
    
        ax = axs[1]
        ax.title.set_text('alt = '+str(round(alti[ialt]/1000,1)))
        h = ax.pcolormesh(gloni, glati, parmi[ialt, :, :].transpose(), shading="nearest")
        ax.set_xlabel("glon")
        ax.set_ylabel("glat")
        fg.colorbar(h, ax=ax)
        
       
        ax = axs[2]
        ax.title.set_text('glon = '+str(round(gloni[ilon],1)))
        h = ax.pcolormesh(glati, alti/1e3, parmi[:, ilon, :], shading="nearest")
        ax.set_xlabel("glat")
        ax.set_ylabel("alt")
        fg.colorbar(h, ax=ax)
        tight_layout(pad=1.2, w_pad=.25)
        
    
    else:
        print('"'+coords+'" coordinate input not recognized')
# alt,lon plot for 2D dipole data
def plotcurv2D(xg: dict[str, T.Any], parm: xarray.DataArray, lalt: int = 512, llat: int = 512, label = None, vcmin=None, vcmax=None):
    # grid data
    alti, mloni, mlati, parmi,l = model2magcoords(xg, parm, lalt, 1, llat)

    # define slices indices, for 2D there is only one longitude index
    ilon = 0

    # plot the meridional slice
    fg = figure()
    if title != None:
        title(label, fontsize=16, pad=20)
        
        
    ax = fg.gca()
    ax.set_ylim(top=700,bottom=100)
    h = ax.pcolormesh(mlati, alti / 1e3, parmi[:, ilon, :], shading="nearest",vmin=vcmin,vmax=vcmax)
    ax.set_xlabel("mlat",fontsize=14)
    ax.set_ylabel("alt",fontsize=14)
    cbar=fg.colorbar(h, ax=ax)
    cbar.ax.get_yaxis().labelpad = 15
    cbar.ax.set_ylabel('', rotation=270)