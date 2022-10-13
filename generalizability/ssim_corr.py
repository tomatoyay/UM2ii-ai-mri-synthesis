#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 13 00:42:36 2022

@author: vivianzhang
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep  9 14:36:06 2022

@author: vivianzhang
"""
#imports

import ants
import numpy as np
import pandas as pd
import pydicom
from skimage.metrics import structural_similarity as ssim
from skimage import data, img_as_float
from skimage.metrics import mean_squared_error
import cv2
import argparse
import matplotlib.pyplot as plt
from skimage.transform import resize
import os
from pydicom.uid import ExplicitVRLittleEndian


#get list of studies and create dataframe
excel = '/home/vivianzhang/Desktop/fastMRI/train_sag_registration.csv'
df = pd.read_csv(excel, index_col = None, header = 0)  
    
    
#%% image registration
#create empty dictionary
total_values = dict()

#run through files
for i in df.index:
    #original image
    orig_path = df.loc[i,'orig_path']
    orig_file = pydicom.dcmread(orig_path)
    orig_img = orig_file.pixel_array.astype(float)
    orig_img = np.uint16((np.maximum(orig_img,0)/orig_img.max())*65535.0)
    resized_img = resize(orig_img, (1024,1024), anti_aliasing=True)

    #synthetic image
    synth_path = df.loc[i,'synth_path']
    synth_file = pydicom.dcmread(synth_path)
    synth_img = synth_file.pixel_array.astype(float)
    synth_img = np.uint16((np.maximum(synth_img,0)/synth_img.max())*65535.0)
    resized_synth_img = resize(synth_img, (1024,1024), anti_aliasing=True)
    
    
    fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(10, 4),
                              sharex=True, sharey=True)
    ax = axes.ravel()
    
    #get scores
    ssim_score = ssim(orig_img, synth_img)
    corr = np.corrcoef(orig_img.flatten(), synth_img.flatten())[0,1]

    #gather file information and name
    files = orig_path.split('/')
    study = files[7]
    
    #create dictionary
    stats = [study, orig_path, synth_path, ssim_score, corr]
    total_values[i] = stats
    
    ax[0].imshow(orig_img, cmap = 'gray')
    ax[0].set_title('Original Image')
 
    ax[1].set_title('Synthetic Image')
    ax[1].imshow(synth_img, cmap = 'gray')
    
    plt.tight_layout()
    plt.show()
    #print(sdfs)

    
#%% export
#export to dataframe
df_total = pd.DataFrame.from_dict(data = total_values, orient = 'index', columns = ['Study','Original Path','Synthetic Path','SSIM','Correlation'])

ssim_dict = dict()
corr_dict = dict()

for i in df_total.index:
    study = df_total.loc[i,'Study']
    ssim = df_total.loc[i,'SSIM']
    corr = df_total.loc[i,'Correlation']
    if study not in ssim_dict:
        ssim_dict[study] = [ssim]
        corr_dict[study] = [corr]
    else:
        ssim_dict[study].append(ssim)
        corr_dict[study].append(corr)


#%% 
avg_ssim_dict = dict()

for study,ssim in ssim_dict.items():
    ssim_list = ssim
    avg_ssim = sum(ssim)/len(ssim)
    slices = len(ssim)
    max_ssim = max(ssim)
    min_ssim = min(ssim)
    std = np.std(ssim)
    stats = [avg_ssim, max_ssim, min_ssim, std, slices]
    avg_ssim_dict[study] = stats
    
    
    #%% 
avg_corr_dict = dict()

for study,ssim in corr_dict.items():
    ssim_list = ssim
    avg_ssim = sum(ssim)/len(ssim)
    slices = len(ssim)
    max_ssim = max(ssim)
    min_ssim = min(ssim)
    std = np.std(ssim)
    stats = [avg_ssim, max_ssim, min_ssim, std, slices]
    avg_corr_dict[study] = stats

#%%
coronal_ssim = pd.DataFrame.from_dict(data = avg_ssim_dict, orient = 'index', columns = ['average ssim','max','min','std dev','number of slices'])
coronal_corr = pd.DataFrame.from_dict(data = avg_corr_dict, orient = 'index', columns = ['average corr','max','min','std dev','number of slices'])

coronal_ssim.to_csv('/home/vivianzhang/Desktop/Gradient/model_analysis/val_cor_avg_ssim_gradient90.csv', sep=str(','), index = True)
coronal_corr.to_csv('/home/vivianzhang/Desktop/Gradient/model_analysis/val_cor_avg_corr_gradient90.csv', sep=str(','), index = True)

