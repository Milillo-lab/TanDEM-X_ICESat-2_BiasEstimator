#!/usr/bin/env python
# coding: utf-8

# # <left style="font-size:1.0em;">**About this Code**</left>
# 
# 
# 
# 
# <div style="text-align:justify; font-size:1.2em;">
#     
# This code extracts the TanDEM-X DEM height along with other Radar features having horizontal resolution of 2×10-4 arc degrees or 12m by running 3×3 window around the raster cell in which ICESat-2 data point is lying and evaluating the average of all values in the window. Same code may be repeated to update the CSV file by extracting different Radar features. 
#    
# The second code explains about the data filter which is applied to filter out the outliers in the dataset to further feed into the neural network.
# </div> 
# 

# In[ ]:


import os
import pandas as pd
import geopandas as gpd
from datetime import datetime, timedelta
import rasterio
from rasterio.merge import merge
from shapely.geometry import Point
from pathlib import Path


# In[ ]:


'''To define base data folder consiting of date wise folder having TanDEM-X DEM along with 
other Radar features tiff files'''

base_folder ="/data_folder/"  

# CSV file consisting of ICESat-2 data points along with the nearest date of acqusition of TanDEM-X data
csv_path = "/ICESat-2_data.csv"

base_f =  Path(base_folder)
base_name = base_f.parent.name

raster_groups = {}
for folder_name in os.listdir(base_folder):
    if os.path.isdir(os.path.join(base_folder, folder_name)):
        # Extracting date given in the folder name   
        date_str = folder_name.split("_")[-1][:8]
        if date_str.isdigit():
            # Reading tiff files of a particular Radar feature like DEM, LIA, Coherence.
            raster_groups.setdefault(date_str, []).append(os.path.join(base_folder, folder_name, "DEM.tiff"))
        

csv_df = pd.read_csv(csv_path, low_memory=False)

# Function to extract date and time from decimal years
def decimal_year_to_datetime(decimal_year):
    year = int(decimal_year)
    remainder = decimal_year - year
    start_of_year = datetime(year, 1, 1)
    days_in_year = 366 if (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0) else 365
    exact_date = start_of_year + timedelta(days=remainder * days_in_year)
    return exact_date

csv_df.loc[:,'exact_date'] = csv_df['t_dem_(yrs)'].apply(decimal_year_to_datetime)


#Pandas df is converted into geodataframe and geometry of points are defined
geometry = [Point(xy) for xy in zip(csv_df['lon_(deg)'], csv_df['lat_(deg)'])]
points_gdf = gpd.GeoDataFrame(csv_df, geometry=geometry)
points_gdf.set_crs(epsg=4326, inplace=True)

# Defining the column name in dataframe
points_gdf['TanDEM_X'] = pd.NA

for date_str, raster_files in raster_groups.items():
    raster_date = datetime.strptime(date_str, "%Y%m%d")
    previous_date = raster_date - timedelta(days=1)
    previous_date_str = previous_date.strftime("%Y%m%d")
   
    '''Condition is given to match the nearest date of the tiff file folder with the exact_date extracted 
    from the CSV file''' 
    if previous_date.date() in points_gdf['exact_date'].dt.date.values:
        filtered_points = points_gdf[points_gdf['exact_date'].dt.date == previous_date.date()]
    elif raster_date.date() in points_gdf['exact_date'].dt.date.values:
        filtered_points = points_gdf[points_gdf['exact_date'].dt.date == raster_date.date()]
    if not filtered_points.empty:
       # points overlapping the tiff files of the same dates are mosaiced before the running the 3×3 window
        rasters = [rasterio.open(fp) for fp in raster_files]
        mosaic, out_transform = merge(rasters)
        
       
        mosaic_meta = rasters[0].meta.copy()
        mosaic_meta.update({
            "height": mosaic.shape[1],
            "width": mosaic.shape[2],
            "transform": out_transform
        })
        temp_mosaic_path = "/temp_mosaic.tiff" # Temporary mosaic file is created
        with rasterio.open(temp_mosaic_path, "w", **mosaic_meta) as dest:
            dest.write(mosaic)
        
             
        with rasterio.open(temp_mosaic_path) as src:
            nodata_value = src.nodata if src.nodata is not None else -9999
            for idx, point in filtered_points.iterrows():
                lon, lat = point['lon_(deg)'], point['lat_(deg)']
                # row and col of the raster cell is identified in the tiff file in which the ICESat-2 data point is lying
                row, col = src.index(lon, lat)
                # A 3×3 window is made around this raster cell
                window_size = 1  
                row_start, row_end = row - window_size, row + window_size + 1
                col_start, col_end = col - window_size, col + window_size + 1

                try:
                    window = src.read(1, window=((row_start, row_end), (col_start, col_end)))
                    # Only valid values are extracted in the window 
                    valid_values = window[window != nodata_value]
                    # Average value is calculated for the valid values inside the window
                    dem_avg = np.mean(valid_values) if valid_values.size > 0 else np.nan
                except Exception:
                    dem_avg = np.nan
      
                if pd.isna(points_gdf.at[idx, 'TanDEM-X_DEM']): 
                    points_gdf.at[idx, 'TanDEM-X_DEM'] = dem_avg
points_gdf = points_gdf.drop(['exact_date'], axis=1)
points_gdf.to_csv('/updated_CSV.csv', index=False) # Saving the updated CSV file


# Code for applying data filter


df = pd.read_csv("/updated_input.csv")

df['dem_diff_Tdx_Tdxpolar'] = df['TanDEM-X_DEM']-df['TanDEM-X_polar']

# Defining filter function for filtering out the outliers in the input dataset
def filter_df(df,dem_height,dem_diff,coh,hoa,amp,slope_min,slope_max):
    # To remove the data points in the sea ice region
    filtered_df = df[(df['TanDEM-X_DEM'] >=dem_height)] 
    # To remove the data points having large difference between the raw DEM elevation and Polar DEM elevation (Calibrated)
    filtered_df_1 = filtered_df[(filtered_df['dem_diff_Tdx_Tdxpolar']).between(-dem_diff,dem_diff)]
    # To remove the low coherence data points
    filtered_df_2 = filtered_df_1[(filtered_df_1['Coherence'])>=coh] 
    # To filter out low HOA data points
    filtered_df_3 = filtered_df_2[filtered_df_2['HOA'] > hoa]
    # To filter out the data points laying in high slope regions
    filtered_df_4 = filtered_df_3[((filtered_df_3['Slope'] >= slope_min)&(filtered_df_3['Slope'] <= slope_max))]
    
    # Applying inter-quartile range to the penetration bias values
    Q1 = filtered_df_5['Penetration_bias'].quantile(0.25)
    Q3 = filtered_df_5['Penetration_bias'].quantile(0.75)
    IQR = Q3 - Q1

    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR

    filtered_df_5 = filtered_df_4[(filtered_df_4['Penetration_bias'] >= lower_bound) & (filtered_df_4['Penetration_bias'] <= upper_bound)]
    
    
    return (filtered_df_5)

'''To filter out the input data input variables to this function is given as filter_df(df,100,5,0.3,30,0,20)'''

