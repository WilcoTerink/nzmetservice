# -*- coding: utf-8 -*-
import xarray as xr
#import numpy as np
#from util import to_proj4

################################
### Parameters

lat_coord='south_north'
lon_coord='west_east'


##################################


#def add_xy_coords(nc):
#    """
#
#    """
#    x1 = xr.open_dataset(nc)
#    x2  = x1.copy()
#    x1.close()
#
#    proj4 = to_proj4(x2)
#
#    nlat = x2.dims[lat_coord]
#    nlon = x2.dims[lon_coord]
#    x_res = int(x2.attrs['dx_m'])
#    y_res = int(x2.attrs['dy_m'])
#
#    lat = np.arange(nlat, dtype='int32') * y_res
#    lon = np.arange(nlon, dtype='int32') * x_res
#
#    x2.coords[lat_coord] = ((lat_coord), lat)
#    x2.coords[lon_coord] = ((lon_coord), lon)


def select_bounds(ms_nc, min_lat, max_lat, min_lon, max_lon):
    """
    Function to select out a bounding box of lat of lon (and to remove negative lon).

    Parameters
    ----------
    ms_nc : str
        Path to the MetService netcdf file.
    min_lat : int, float, or None
        The minimum lat to extract in WGS84 decimal degrees.
    max_lat : int, float, or None
        The maximum lat to extract in WGS84 decimal degrees.
    min_lon : int, float, or None
        The minimum lon to extract in WGS84 decimal degrees.
    max_lon : int, float, or None
        The maximum lon to extract in WGS84 decimal degrees.

    Returns
    -------
    xarray Dataset
        With the same data structure and attributes as the original netcdf
    """
    ms1 = xr.open_dataset(ms_nc)
    ms2 = ms1.where((ms1.longitude >= min_lon) & (ms1.longitude <= max_lon) & (ms1.latitude >= min_lat) & (ms1.latitude <= max_lat), drop=True)
    ms1.close()
    if (ms2.longitude <= 0).any():
        ms2 = ms2.where(ms1.longitude > 0, drop=True)

    return ms2


def to_df(ms_nc, to_rate=False):
    """
    Function to take a MetService netcdf file and convert it to a pandas DataFrame. Optionally to convert the precipitation values to an hourly rate.

    Parameters
    ----------
    ms_nc : str or xarray dataset
        Path to the MetService netcdf file or an xarray dataset object.
    to_rate : bool
        Should the accumulated precipitation be converted to an hourly rate?

    Returns
    -------
    DataFrame
    """
    if isinstance(ms_nc, xr.Dataset):
        ms1 = ms_nc
    elif isinstance(ms_nc, str):
        ms1 = xr.open_dataset(ms_nc)
    df1 = ms1.to_dataframe()
    ms1.close()
    df1.reset_index(level=['south_north', 'west_east'], drop=True, inplace=True)
    df1 = df1[df1.longitude > 0].reset_index()
    df1.time = df1.time.dt.round('H').values
    df1.rename(columns={'precipitation_amount': 'precip_accum'}, inplace=True)
    rem1 = df1.time.unique()[0]
    if to_rate:
        rem2 = df1.time.unique()[-1]
        df1a = df1[df1.time != rem2].copy()
        df1 = df1[df1.time != rem1]
        df1['other'] = df1a.precip_accum.values
        df1['precip_rate'] = df1['precip_accum'] - df1['other']
        df1.drop(['precip_accum', 'other'], axis=1, inplace=True)
    else:
        df1 = df1[df1.time != rem1]

    df1.set_index(['time', 'latitude', 'longitude'], inplace=True)

    return df1

