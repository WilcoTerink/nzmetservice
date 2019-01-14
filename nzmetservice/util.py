# -*- coding: utf-8 -*-
"""
Created on Fri Dec 28 17:36:34 2018

Utility functions
"""
import xarray as xr

########################################
### Functions


def write_log(text, file):
    f = open(file, 'a')
    f.write("{}\n".format(text))


def to_proj4(ds):
    """
    Function to create a proj4 formated string from a MetService netcdf. Not correct!

    Parameters
    ----------
    ds : Dataset
        MetService Dataset.

    Returns
    -------
    str
        Proj4 formatted
    """
    ### Open the nc file
    attrs1 = ds.attrs

    if attrs1['projection_name'] == 'Lambert Conformal':
        proj_base = '+proj=lcc +lat_1={lat1} +lat_2={lat2} +lat_0={lat0} +lon_0={lon0} +R={radius} +no_defs'
        lat0 = (attrs1['true_lat_1'] + attrs1['true_lat_2'])/2
        proj4 = proj_base.format(lat1=attrs1['true_lat_1'], lat2=attrs1['true_lat_2'], lat0=lat0, lon0=attrs1['standard_lon'], radius=attrs1['earth_radius_m'])
    else:
        raise ValueError('The projection is not Lambert Conformal')

    return proj4
