import numpy as np
from matplotlib.pyplot import figure
import typing as T


def plotoutline2D(xg):
    """plot an outline of a 2D grid in mlat and altitude"""

    mlat = np.degrees(np.pi/4 - xg["theta"])
    alt = xg["alt"]

    fg = figure(dpi=100)
    ax = fg.gca()

    ax.plot(mlat[0, :, 0], alt[0, :, 0] / 1e3)
    ax.plot(mlat[-1, :, 0], alt[-1, :, 0] / 1e3)
    ax.plot(mlat[:, 0, 0], alt[:, 0, 0] / 1e3)
    ax.plot(mlat[:, -1, 0], alt[:, -1, 0] / 1e3)
    ax.set_xlabel("mlat")
    ax.set_ylabel("alt")


def plotoutline3D(xg):
    """plot 3D grid outline"""

    mlon = xg["glon"]
    mlat = xg['glat']
    alt = xg["alt"]

    fg = figure(dpi=150,figsize=(5, 5))
    ax = fg.gca(projection="3d")

    ax.plot(mlon[0, :, 0], mlat[0, :, 0], alt[0, :, 0] / 1e3,color='red')
    ax.plot(mlon[-1, :, 0], mlat[-1, :, 0], alt[-1, :, 0] / 1e3,color='red')
    ax.plot(mlon[0, :, -1], mlat[0, :, -1], alt[0, :, -1] / 1e3,color='red')
    ax.plot(mlon[-1, :, -1], mlat[-1, :, -1], alt[-1, :, -1] / 1e3,color='red')

    ax.plot(mlon[:, 0, 0], mlat[:, 0, 0], alt[:, 0, 0] / 1e3,color='red')
    ax.plot(mlon[:, -1, 0], mlat[:, -1, 0], alt[:, -1, 0] / 1e3,color='red')
    ax.plot(mlon[:, 0, -1], mlat[:, 0, -1], alt[:, 0, -1] / 1e3,color='red')
    ax.plot(mlon[:, -1, -1], mlat[:, -1, -1], alt[:, -1, -1] / 1e3,color='red')

    ax.plot(mlon[0, 0, :], mlat[0, 0, :], alt[0, 0, :] / 1e3,color='red')
    ax.plot(mlon[0, -1, :], mlat[0, -1, :], alt[0, -1, :] / 1e3,color='red')
    ax.plot(mlon[-1, -1, :], mlat[-1, -1, :], alt[-1, -1, :] / 1e3,color='red')
    ax.plot(mlon[-1, 0, :], mlat[-1, 0, :], alt[-1, 0, :] / 1e3,color='red')

    ax.set_xlabel("glon")
    ax.set_ylabel("glat")
    ax.set_zlabel("alt [km]")
