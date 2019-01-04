# -*- coding: utf-8 -*-
import os
from re import search, IGNORECASE
from ftplib import FTP


def ftp_transfer(ftp_path, username, password, output_path):
    """
    Function to update the output_path with new netcdf forecast files from the MetService ftp site.

    Parameters
    ----------
    ftp_path : str
        The MetService ftp path.
    username : str
        The username to access the ftp site.
    password : str
        The password to access the ftp site.
    output_path : str
        The path where the netcdf files should be saved.

    Returns
    -------
    None
    """
    #############################################
    ### Get list of files in the output ftp dir

    files1 = [filename for filename in os.listdir(output_path) if search('.nc$', filename, IGNORECASE)]

    #############################################
    ### Get list of files in ftp site and compare to ours

    print('Transfer files from FTP site')
    ftp = FTP(ftp_path)
    ftp.login(user=username, passwd=password)
    ftp.cwd('netcdf_combined')
    ftp_files1 = ftp.mlsd()
    ftp_files2 = [i[0] for i in ftp_files1]
    ftp_files3 = [i for i in ftp_files2 if ('wrf_hourly_precip' in i) or ('NZ_WRF_Selection' in i)]
    ftp_files4 = [i for i in ftp_files3 if i not in files1]

    ##############################################
    ### Download files

    if ftp_files4:
        for f in ftp_files4:
            ftp.retrbinary('RETR ' + f, open(os.path.join(output_path, f), 'wb').write)
        print(str(len(ftp_files4)) + ' files downloaded')
    else:
        print('No files downloaded')



