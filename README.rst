nzmetservice - A Python package for handling  New Zealand MetService forecast data
==================================================================================

The nzmetservice package contains various functions for downloading, processing, and handling of New Zealand MetService forecast data.
This package is not associated with the MetService.

.. Documentation
.. --------------
.. The primary documentation for the package can be found `here <http://eto.readthedocs.io>`_.

Installation
------------
nzmetservice can be installed via pip or conda::

  pip install nzmetservice

or::

  conda install -c mullenkamp nzmetservice

The core dependencies are `Pandas <http://pandas.pydata.org/pandas-docs/stable/>`_ and `xarray <http://xarray.pydata.org>`_.

Usage
-----
ftp_transfer
~~~~~~~~~~~~
The ftp_transfer functions does as the name implies. It looks at the output_path on your local drive then compares it to the MetService ftp site and downloads what is on the ftp site that isn't in the output_path.
It can be loaded in from the basic module:

.. code:: python

  from nzmetservice import ftp_transfer

And feed it with the necessary parameters:

.. code:: python

  ftp_transfer(ftp_path, username, password, output_path)

You will likely want to create a scheduled task to run a script containing this function once an hour.

Selection and processing
~~~~~~~~~~~~~~~~~~~~~~~~
The other two functions are simple selection and conversion tools.

.. code:: python

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
  ### Examples

  ms1 = select_bounds(nc1_path, min_lat, max_lat, min_lon, max_lon)

  ms_df = to_df(ms1, to_rate=True)
