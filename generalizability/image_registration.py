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


#get list of studies and create dataframe
excel = '...file/test_study_list.xlsx'
df = pd.read_excel(excel, index_col = None, header = 1)  
    
    
#%% get ssim and corr
#create empty dictionary
total_values = dict()

#run through files
for i in df.index:
    #original image
    orig_path = df.loc[i,'Original Image']
    orig_file = pydicom.dcmread(orig_path)
    orig_img = orig_file.pixel_array.astype(float)
    orig_img = np.uint8((np.maximum(orig_img,0)/orig_img.max())*255.0)
    resized_img = resize(orig_img, (256,256), anti_aliasing=True)
    orig_img_ants = ants.from_numpy(resized_img)

    #synthetic image
    synth_path = df.loc[i,'Synthetic Image']
    synth_file = pydicom.dcmread(synth_path)
    synth_img = synth_file.pixel_array.astype(float)
    synth_img = np.uint8((np.maximum(synth_img,0)/synth_img.max())*255.0)
    resized_synth_img = resize(synth_img, (256,256), anti_aliasing=True)
    synth_img_ants = ants.from_numpy(resized_synth_img)
    
    #resize images
    original = orig_img_ants.resample_image((64,64),1,0)
    synthetic = synth_img_ants.resample_image((64,64),1,0)
    #original.plot(overlay = synthetic, title = 'Before Registration')
    synth_before = synthetic.numpy()
    
    #transpose image
    mytx = ants.registration(fixed=original, moving=synthetic, type_of_transform='SyN')
    warped_moving = mytx['warpedmovout']
    #original.plot(overlay = warped_moving, title='After Registration')
    mywarpedimage = ants.apply_transforms(fixed=original, moving=synthetic,transformlist=mytx['fwdtransforms'])
    #mywarpedimage.plot()
    orig_array = original.numpy()
    synth_array = mywarpedimage.numpy()
    
    #fig, axes = plt.subplots(nrows=1, ncols=3, figsize=(10, 4),
    #                         sharex=True, sharey=True)
    #ax = axes.ravel()
    
    #get scores
    ssim_score = ssim(orig_array, synth_array)
    corr = np.corrcoef(orig_array.flatten(), synth_array.flatten())[0,1]
    
    #gather file information and name
    study = df.loc[i,'Study']
    orig_mri = df.loc[i,'Original MRI']
    synth_mri = df.loc[i,'Synthetic MRI']
    orig_seq = df.loc[i,'Original Sequence']
    synth_seq = df.loc[i,'Synthetic Sequence']
    
    #create dictionary
    stats = [study, orig_path, orig_mri, orig_seq, synth_path, synth_seq, synth_mri, ssim_score, corr]
    total_values[i] = stats
    #ax[0].imshow(orig_array, cmap = 'gray')
    #ax[0].set_title('Original Image')
    
    #ax[1].imshow(synth_before, cmap = 'gray')
    #ax[1].set_title('Synthetic Image')
    
    #ax[2].imshow(synth_array, cmap = 'gray')
    #ax[2].set_title('Synthetic Image Registered')

    #plt.tight_layout()
    #plt.show()
    
#%% export

#export to dataframe
df_total = pd.DataFrame.from_dict(data = total_values, orient = 'index', columns = ['Study','Original Path','Original MRI','Original Sequence','Synthetic Path','Synthetic MRI','Synthetic Sequence','SSIM','Correlation'])

#export to excel file
#df_total.to_csv('name.csv', sep=str(','), index = True)

    
    

