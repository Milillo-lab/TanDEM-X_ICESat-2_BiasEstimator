#!/usr/bin/env python
# coding: utf-8

# In[ ]:


#To read the h5 file having DNN model architecture

import h5py

with h5py.File('/file.h5', 'r') as hf: # Opening .h5 file
        model_weights_group = hf['model_weights']
        for layer_name in model_weights_group.keys():
            layer_group = model_weights_group[layer_name]
            for weight_name in layer_group.keys():
                weight_dataset = layer_group[weight_name]
                print(f"Layer: {layer_name}, Weight: {weight_name}") # Printing the model_weights of each layer
        optimizer_weights_group = hf['optimizer_weights']
        for layer_name in optimizer_weights_group.keys():
            layer_group = optimizer_weights_group[layer_name]
            for optimizer_weight in layer_group.keys():
                optimizer_dataset = layer_group[optimizer_weight]
                print(f"Layer: {layer_name}, Weight: {optimizer_weight}") # Printing the optimizer_weights of each layer
                


# In[ ]:


# To load the DNN model saved in h5 file 

from tensorflow.keras.models import load_model

model = load_model("/folder/Deep_NN.h5")

predictions = model.predict(X_test).flatten()


# In[ ]:


# To load the Random Forest saved in pkl file

import pickle

with open("/folder/trained_model_RF.pkl", 'rb') as f:
    loaded_model = pickle.load(f)


prediction = loaded_model.predict(X_test).flatten()

