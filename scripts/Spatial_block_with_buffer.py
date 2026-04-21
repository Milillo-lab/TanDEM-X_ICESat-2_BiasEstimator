#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from scipy.spatial import cKDTree

X = filtered_df[features]
y = filtered_df[target]

'''Block size is decided based on the auto correlation observed in penetration bias values along
the ICESat-2 tracks. In this dataset autocorreation between the datapoints decreases between
10-15 km.'''

block_size = 11000  

filtered_df['block_x'] = (filtered_df['x_3031'] // block_size).astype(int)
filtered_df['block_y'] = (filtered_df['y_3031'] // block_size).astype(int)

# Specific block id is alloted to each data point"
filtered_df['block_id'] = filtered_df['block_x'].astype(str) + "_" + filtered_df['block_y'].astype(str)

# block of data points are segregated based on block_id
blocks = filtered_df['block_id'].unique()

# Train and Test data split
train_blocks, test_blocks = train_test_split(
    blocks, test_size=0.2, random_state=42
)

train_df = filtered_df[filtered_df.block_id.isin(train_blocks)]
test_df  = filtered_df[filtered_df.block_id.isin(test_blocks)]

train_blocks_unique = train_df['block_id'].unique()

# Train and Validation data split
train_blocks_final, val_blocks = train_test_split(
    train_blocks_unique, test_size=0.2, random_state=42
)

train_df_final = train_df[train_df.block_id.isin(train_blocks_final)]
val_df = train_df[train_df.block_id.isin(val_blocks)]

''' A buffer is made to filter out all the training dataset lies in this buffer to minimize the spatial correlation
between the train, validation and test sets'''
buffer_dist = 3000   

coords_train = train_df_final[['x_3031','y_3031']].values
coords_test  = test_df[['x_3031','y_3031']].values
coords_val   = val_df[['x_3031','y_3031']].values


tree_test = cKDTree(coords_test)
tree_val  = cKDTree(coords_val)

# training points close to test
near_test = tree_test.query_ball_point(coords_train, r=buffer_dist)

# training points close to validation
near_val = tree_val.query_ball_point(coords_train, r=buffer_dist)

mask_test = np.array([len(i) == 0 for i in near_test])
mask_val  = np.array([len(i) == 0 for i in near_val])

# Final mask extended from validation and test data
mask_final = mask_test & mask_val

# Filtered training data
train_df_buffered = train_df_final.iloc[mask_final]

# Final training data
X_train = train_df_buffered[features]
y_train = train_df_buffered[target]

# Final validation data
X_val = val_df[features]
y_val = val_df[target]

# Final test data
X_test = test_df[features]
y_test = test_df[target]
tree_train = cKDTree(train_df_buffered[['x_3031','y_3031']].values)


