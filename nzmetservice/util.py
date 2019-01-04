# -*- coding: utf-8 -*-
"""
Created on Fri Dec 28 17:36:34 2018

Utility functions
"""

########################################
### Functions


def write_log(text, file):
    f = open(file, 'a')
    f.write("{}\n".format(text))
