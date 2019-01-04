# -*- coding: utf-8 -*-
"""
Created on Fri Dec 28 17:36:34 2018

Utility functions
"""
import pandas as pd
import statsmodels.api as sm
import numpy as np

########################################
### Functions


def autocorr_est(df, limit=0.05, nlags=400):
    auto_dict = {}
    for name, values in df.iteritems():
        a1 = sm.tsa.stattools.acf(values, nlags=nlags, fft=True, missing='drop')
        days = np.argmax(a1 < limit)
        auto_dict.update({name: days})
    return auto_dict


def tsreg(ts, freq=None, interp=None, maxgap=None, **kwargs):
    """
    Function to regularize a time series DataFrame.
    The first three indeces must be regular for freq=None!!!

    Parameters
    ----------
    ts : DataFrame
        DataFrame with a time series index.
    freq : str
        Either specify the known frequency of the data or use None and
    determine the frequency from the first three indices.
    interp : str or None
        Either None if no interpolation should be performed or a string of the interpolation method.
    **kwargs
        kwargs passed to interpolate.
    """

    if freq is None:
        freq = pd.infer_freq(ts.index[:3])
    ts1 = ts.asfreq(freq)
    if isinstance(interp, str):
        ts1 = ts1.interpolate(interp, limit=maxgap, **kwargs)

    return ts1

