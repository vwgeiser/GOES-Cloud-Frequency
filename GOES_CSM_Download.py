# -*- coding: utf-8 -*-
"""
Created on Sun Jan 21 11:58:26 2024

@author: vwgei
"""

# directory of config C:\Users\vwgei\.config\goes2go
from goes2go import GOES


# ABI Clear Sky Mask Contiguous US
G = GOES(satellite=16, product="ABI-L2-ACMC", domain='C')

sstr = '2018-1-1 00:00'
estr = '2018-12-31 00:00'

# Produce a pandas DataFrame of the available files in a time range
df = G.df(start=sstr, end=estr)

# df.head()

# # Download data for a specified time range
# G.timerange(start=sstr, end=estr)



# # Download recent data for a specific interval
# #G.timerange(recent='30min')