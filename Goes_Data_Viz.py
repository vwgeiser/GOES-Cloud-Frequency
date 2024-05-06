# -*- coding: utf-8 -*-
"""
Created on Sun Jan 21 12:10:41 2024

@author: vwgei
"""

# from goes2go import GOES
from datetime import datetime
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import metpy  # noqa: F401
import numpy as np

import xarray as xr
import netCDF4

# def calculate_degrees(file_id):
    
#     # Read in GOES ABI fixed grid projection variables and constants
#     x_coordinate_1d = file_id.variables['x'][:]  # E/W scanning angle in radians
#     y_coordinate_1d = file_id.variables['y'][:]  # N/S elevation angle in radians
#     projection_info = file_id.variables['goes_imager_projection']
#     lon_origin = projection_info.attrs['longitude_of_projection_origin']
#     H = projection_info.attrs['perspective_point_height']+projection_info.attrs['semi_major_axis']
#     r_eq = projection_info.attrs['semi_major_axis']
#     r_pol = projection_info.attrs['semi_minor_axis']
    
#     # Create 2D coordinate matrices from 1D coordinate vectors
#     x_coordinate_2d, y_coordinate_2d = np.meshgrid(x_coordinate_1d, y_coordinate_1d)
    
#     # Equations to calculate latitude and longitude
#     lambda_0 = (lon_origin*np.pi)/180.0  
#     a_var = np.power(np.sin(x_coordinate_2d),2.0) + (np.power(np.cos(x_coordinate_2d),2.0)*(np.power(np.cos(y_coordinate_2d),2.0)+(((r_eq*r_eq)/(r_pol*r_pol))*np.power(np.sin(y_coordinate_2d),2.0))))
#     b_var = -2.0*H*np.cos(x_coordinate_2d)*np.cos(y_coordinate_2d)
#     c_var = (H**2.0)-(r_eq**2.0)
#     r_s = (-1.0*b_var - np.sqrt((b_var**2)-(4.0*a_var*c_var)))/(2.0*a_var)
#     s_x = r_s*np.cos(x_coordinate_2d)*np.cos(y_coordinate_2d)
#     s_y = - r_s*np.sin(x_coordinate_2d)
#     s_z = r_s*np.cos(x_coordinate_2d)*np.sin(y_coordinate_2d)
    
#     # Ignore numpy errors for sqrt of negative number; occurs for GOES-16 ABI CONUS sector data
#     np.seterr(all='ignore')
    
#     abi_lat = (180.0/np.pi)*(np.arctan(((r_eq*r_eq)/(r_pol*r_pol))*((s_z/np.sqrt(((H-s_x)*(H-s_x))+(s_y*s_y))))))
#     abi_lon = (lambda_0 - np.arctan(s_y/(H-s_x)))*(180.0/np.pi)
    
#     return abi_lat, abi_lon

# https://unidata.github.io/python-gallery/examples/mapping_GOES16_TrueColor.html#using-other-projections

#  D:\GOES_data_CM\2022\104\04\OR_ABI-L2-ACMC-M6_G16_s20221040456172_e20221040458545_c20221040500052.nc

# Open the NetCDF file
nc_file_path = r"D:\GOES_data_CM\2021\305\00\OR_ABI-L2-ACMC-M6_G16_s20213050001170_e20213050003543_c20213050004318.nc"
ds = xr.open_dataset(nc_file_path)

# profile = ds.profile

# print(profile)

# abi_lat, abi_lon = calculate_degrees(ds)

# Scan's start time, converted to datetime object
scan_start = datetime.strptime(ds.time_coverage_start, '%Y-%m-%dT%H:%M:%S.%fZ')

# Scan's end time, converted to datetime object
scan_end = datetime.strptime(ds.time_coverage_end, '%Y-%m-%dT%H:%M:%S.%fZ')

# File creation time, convert to datetime object
file_created = datetime.strptime(ds.date_created, '%Y-%m-%dT%H:%M:%S.%fZ')

# The 't' variable is the scan's midpoint time
midpoint = str(ds['t'].data)[:-8]
scan_mid = datetime.strptime(midpoint, '%Y-%m-%dT%H:%M:%S.%f')

print('Scan Start    : {}'.format(scan_start))
print('Scan midpoint : {}'.format(scan_mid))
print('Scan End      : {}'.format(scan_end))
print('File Created  : {}'.format(file_created))
print('Scan Duration : {:.2f} minutes'.format((scan_end-scan_start).seconds/60))

# Use the `ACM` variable as a 'hook' to get the CF metadata.
dat = ds.metpy.parse_cf('BCM')

geos = dat.metpy.cartopy_crs

# We also need the x (north/south) and y (east/west) axis sweep of the ABI data
x = dat.x
y = dat.y

# ds['ACM'][:] = 3

fig = plt.figure(figsize=(15, 12))

# Create axis with Geostationary projection
ax = fig.add_subplot(1, 1, 1, projection=geos)

# b = ds.BCM

# Add the RGB image to the figure. The data is in the same projection as the
# axis we just created.
# 'turbo_r'
ax.imshow(ds.BCM, origin='upper',
          extent=(x.min(), x.max(), y.min(), y.max()), transform=geos, cmap='Greys')

# Add Coastlines and States
ax.coastlines(resolution='50m', color='grey', linewidth=.50)
ax.add_feature(ccrs.cartopy.feature.STATES, linewidth=.50)

plt.title('GOES-16 Cloud Mask', loc='left', fontweight='bold', fontsize=15)
plt.title('{}'.format(scan_start.strftime('%d %B %Y %H:%M UTC ')), loc='right')

plt.show()
