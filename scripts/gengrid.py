from gemini3d.grid.tilted_dipole import tilted_dipole3d
from gemini3d.grid.cartesian import cart3d
from plotgrid import plotoutline3D, plotoutline2D
from matplotlib.pyplot import show


# %% generate a 3D grid

cfg = {
'glat' :56,
'glon':294,
'xdist' : 2500e3,     #         ! eastward distance (meters)
'ydist' : 5200e3,      #         ! northward distance (meters)
'alt_min' : 80e3,      #        ! minimum altitude (meters)
'alt_max' : 900e3,      #       ! maximum altitude (meters)
 'alt_scale' : [10.9e3, 8e3, 500e3, 150e3],#  ! altitude grid scales (meters)xg['x1']
'lxp' : 15,            #       ! number of x-cells
'lyp' : 55,            #       ! number of y-cells
'Bincl' : 90,                  #! geomagnetic inclination
'nmf' : 5e11,
'nme' : 2e11
}
xg = cart3d(cfg)

# %% plot the 3D grid outline

plotoutline3D(xg)
# %% generate a 2D grid
# cfg = {
#     "dtheta": 11,
#     "dphi": 105,
#     "lp": 128,
#     "lq": 256,
#     "lphi": 1,
#     "altmin": 80e3,
#     "glat": 56,
#     "glon": 120,
#     "gridflag": 0,
#     "openparm": 50,
# }


# %% plot the 2D grid
# plotoutline2D(xg1)

show()
