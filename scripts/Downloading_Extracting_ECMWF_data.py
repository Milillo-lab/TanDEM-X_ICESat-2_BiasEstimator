#!/usr/bin/env python
# coding: utf-8

# # <left style="font-size:1.0em;">**About this Code**</left>
# 
# 
# 
# 
# <div style="text-align:justify; font-size:1.2em;">
#     
# This code details about the downloading the desired ECMWF parameters from the website by using API. Firstly the NetCDF files of a desired parameter is downloaded for each unique date of the TanDEM-X acquistion given in the CSV file. Then all the NetCDF files are converted into tiff files in EPSG 4326 map projection for the entire Antarctica region. Further, the selected parameter values are extracted for data points corresponding to each unique date and file is updated for each parameter.  
# </div>
# 
# 

# In[ ]:


import cdsapi
import os
import requests
import numpy as np
import xarray as xr 
import rioxarray as rio 
import yarl
import re
import netCDF4 as nc
from os import walk
from osgeo import gdal
import glob
import netCDF4 as nc
import numpy as np
import rasterio
from rasterio.transform import from_origin
from pathlib import Path


# In[ ]:


# Reading the CSV file containing ICESat-2 and TanDEM-X elevation data for data points
df = pd.read_csv('/file.csv') 

# Function defined for changing the decimal years into date and time format for downloading the precise data of a parameter
def decimal_year_to_datetime(decimal_year): 
    year = int(decimal_year)
    remainder = decimal_year - year
    start_of_year = datetime(year, 1, 1)
    days_in_year = 366 if (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0) else 365
    exact_date = start_of_year + timedelta(days=remainder * days_in_year)
    return exact_date

# Extracting exact date time of the datapoints in the CSV file
df['exact_datetime'] = df['t_dem_(yrs)'].apply(decimal_year_to_datetime)

#Determinig the unique values of exact date time
exact_datetime = np.array(df['exact_datetime'].unique())
datetime_index = pd.to_datetime(exact_datetime)

# Extracting year, month, day and time from the unique dates to feed into the website API code
year = (datetime_index.year).tolist()
month = (datetime_index.month).tolist()
day = (datetime_index.day).tolist()
time_1 = datetime_index.time

def round_to_nearest_hour(t):
    if t.minute >= 30:
        new_hour = (t.hour + 1) % 24 
        return f"{new_hour:02}:00"
    else:
        return f"{t.hour:02}:00"

time = [round_to_nearest_hour(t) for t in time_1]

# to define target folder for downloading NetCDF files of the selected parameter
LOCATION_ERA5 = Path("/target_folder/") 

# ECMWF website API
client = cdsapi.Client()
for i, (x, y, z, r) in enumerate(zip(year, month, day, time)):
    
    dataset = "reanalysis-era5-single-levels"
    request = {
    "product_type": ["reanalysis"],
    "variable": ["parameter"],
    "year": x,
    "month": y,
    "day": z,
    "time": r,
    "data_format": "netcdf",
    "download_format": "unarchived",
    "area": [-60, -180, -90, 180]
    }

    target = LOCATION_ERA5 / f"download_{i}.nc"

   
    client.retrieve(dataset, request).download(str(target))

# Code to save NetCDF files into tiff files

# Reading a single dataset to extract the variable keys in the file
dataset = nc.Dataset('target_folder/download_0.nc')
total = len(exact_datetime)
keys = list(dataset.variables.keys())
i = 0
while i < total: # while loop for all the NetCDF files in the folder
    #Reading the NetCDF files in the folder
    file_path = f'/Netcdf_files/download_{i}.nc'

    
    with nc.Dataset(file_path, 'r') as dataset:
        #Extracting the parameter variable in the file
        para = dataset.variables[keys[5]][:]
        lat = dataset.variables['latitude'][:]
        lon = dataset.variables['longitude'][:]

        # Defining the resolution of the tiff file which is 0.25 arc degrees as per ECMWF website
        resolution = (lat[1] - lat[0], lon[1] - lon[0])
        transform = from_origin(lon.min(), lat.min(), resolution[1], resolution[0])

        #Defining the meta data
        metadata = {
            'driver': 'GTiff',
            'height': para.shape[1],  
            'width': para.shape[2],
            'count': 1,
            'dtype': str(para.dtype),  
            'crs': 'EPSG:4326',
            'transform': transform,
        }

        #Extracting data
        for time_step in range(para.shape[0]):
            para_data = para[time_step, :, :]

            # Inverting arrays to maintain the proper orientation in the tiff file 
            para_data = np.flipud(para_data)

            # Saving the output tiff files
            output_file = f'target_folder/Tiff_files/{keys[5]}_{i}.tiff'

           
            with rasterio.open(output_file, 'w', **metadata) as dst:
                dst.write(para_data, 1)
    
    i += 1
    
# Code to extract the values of the Environmental feature for the data points in the CSV file

tiff_folder = 'target_folder/Tiff_files/' # To define directory of tiff files of a feature


# Extracting unique from the CSV file for which environmental features are already downloaded
unique_years = df['t_dem_(yrs)'].unique()
para_values = []


for i, year in enumerate(unique_years):
    tiff_path = os.path.join(tiff_folder, f'parameter_{i}.tiff') # parameter name is to be given as per the tiff file name
    if os.path.exists(tiff_path):
        
        df_year = df[df['t_dem_(yrs)'] == year]
        
       
        geometry_year = [Point(xy) for xy in zip(df_year['lon_(deg)'], df_year['lat_(deg)'])]
        # All the data points of a particular year are considered
        geo_df_year = gpd.GeoDataFrame(df_year, geometry=geometry_year) 
        geo_df_year.crs = "EPSG:4326"
        
        '''For each data point, the corresponding raster value is sampled from TIFF files organized 
        sequentially by unique years within the specified folder path''' 
        with rasterio.open(tiff_path) as src:
            geo_df_year['parameter_name'] = [
                x[0] for x in src.sample([(point.x, point.y) for point in geo_df_year.geometry])
            ]
        
       
        para_values.extend(geo_df_year['parameter_name'].tolist()) # To give proper name of the parameter
    else:
        print(f"File {tiff_path} does not exist.")


df['parameter_name'] = para_values[:len(df)] # Defining the parameter name as a df column


print(df)

'''The above code shall be repeated to update the CSV file for all the desired ECMWF atmospheric features
downloaded from the website'''


'''Additional code for calculating wind speed and wind direction because on the ECMWF website 
there are horizontal (u) and vertical (v) components are available'''

# Vector mean of wind speed is calculated after extracting horizontal and vertical components of the wind speed by applying the above code
df['wind_speed_(m/s)'] = np.sqrt(df['wind_speed_u']**2 + df['wind_speed_v']**2)
v_comp = np.array(df['wind_speed_v'])
u_comp = np.array(df['wind_speed_u'])
#Wind direction is calculated
df['wind_direction_(in_degrees)_w.r.t_East'] = np.degrees(np.arctan2(v_comp, u_comp))

