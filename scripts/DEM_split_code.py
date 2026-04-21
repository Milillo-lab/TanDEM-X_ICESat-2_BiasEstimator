#!/usr/bin/env python
# coding: utf-8

# In[ ]:


X = filtered_df[features]
y = filtered_df[target]
groups = filtered_df['DEM_id']

gss = GroupShuffleSplit(n_splits=1, test_size=0.2, random_state=42)

#Splitting Training and Test set based on DEM_id
train_val_idx, test_idx = next(gss.split(X, y, groups=groups))

X_train_val = X.iloc[train_val_idx]
y_train_val = y.iloc[train_val_idx]

X_test = X.iloc[test_idx]
y_test = y.iloc[test_idx]

groups_train_val = groups.iloc[train_val_idx]

#Splitting Training and Validation set based on DEM_id
gss2 = GroupShuffleSplit(n_splits=1, test_size=0.2, random_state=42)

train_idx, val_idx = next(gss2.split(X_train_val, y_train_val, groups=groups_train_val))

X_train = X_train_val.iloc[train_idx]
y_train = y_train_val.iloc[train_idx]

X_val = X_train_val.iloc[val_idx]
y_val = y_train_val.iloc[val_idx]

