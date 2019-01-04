# -*- coding: utf-8 -*-
"""
Created on Tue Oct  9 11:22:22 2018

@author: michaelek
"""
import pandas as pd
from nzmetservice import select_bounds, to_df, datasets

pd.options.display.max_columns = 10

#####################################
### Parameters

min_lat = -47
max_lat = -40
min_lon = 166
max_lon = 175
nc1_path = datasets.get_path('wrf_hourly_precip_nz8km_test')

####################################
### Import

ms1 = select_bounds(nc1_path, min_lat, max_lat, min_lon, max_lon)

ms_df = to_df(ms1, True).dropna().reset_index()
























































