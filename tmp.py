import plotly.graph_objects as go
import pandas as pd
import numpy as np
from numpy import pi, sin, cos
import pymap3d as pm


def lon_lat_r_to_sphere(lon, lat, r):
    x = np.multiply(np.cos(lon), np.sin(lat))
    y = np.multiply(np.sin(lon), np.sin(lat))
    z = np.cos(lat)
    return x, y, z


lon, lat = [0 for _ in range(360)], [i for i in range(360)]
lon1, lat1 = [i for i in range(360)], [90 for _ in range(360)]
lon2, lat2 = [35 + i/ 10000 for i in range(100)], [90 - (31 + i / 1000) for i in range(100)]
x, y, z = lon_lat_r_to_sphere(np.deg2rad(lon), np.deg2rad(lat), 1)
x1, y1, z1 = lon_lat_r_to_sphere(np.deg2rad(lon1), np.deg2rad(lat1), 1)
x2, y2, z2 = lon_lat_r_to_sphere(np.deg2rad(lon2), np.deg2rad(lat2), 1)


def spheres(size, clr1, clr2, dist=0):
    # Set up 100 points. First, do angles
    theta = np.linspace(-pi, pi, 100)
    phi = np.linspace(0, pi, 100)

    # Set up coordinates for points on the sphere
    x0 = dist + size * np.outer(cos(theta), sin(phi))
    y0 = size * np.outer(sin(theta), sin(phi))
    z0 = size * np.outer(np.ones(100), cos(phi))
    x0.ravel()
    y0.ravel()
    z0.ravel()

    # Set up trace
    trace = go.Surface(x=x0, y=y0, z=z0, colorscale=[[0, clr1], [1, clr2]])
    trace.update(showscale=False)

    return trace


noaxis = dict(showbackground=False,
              showgrid=False,
              showline=False,
              showticklabels=False,
              ticks='',
              title='',
              zeroline=False)

layout = dict(
    yaxis=noaxis,
    xaxis=noaxis,
    zaxis=noaxis
)
scene = dict(
    yaxis=noaxis,
    xaxis=noaxis,
    zaxis=noaxis
)

trace = spheres(1, "#000000", "#000000", 0)

spherical_earth_map = np.load(r"c:\users\yair\downloads\map_sphere.npy")
xm, ym, zm = spherical_earth_map.T
trace1 = go.Scatter3d(x=xm, y=ym, z=zm, mode='lines')
trace2 = go.Scatter3d(x=x, y=y, z=z, mode="lines")
trace3 = go.Scatter3d(x=x1, y=y1, z=z1, mode="lines")
trace4 = go.Scatter3d(x=x2, y=y2, z=z2, mode="lines")
# trace2 = go.Scatter3d(x=x, y=y, z=z)

fig = go.Figure(data=[trace, trace1, trace2, trace3, trace4])
fig.update_layout(scene=scene)
fig.show()
