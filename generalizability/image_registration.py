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
    
    
#%% get ssim and corr
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
    orig_img_ants = ants.from_numpy(resized_img)

    #synthetic image
    synth_path = df.loc[i,'synth_path']
    synth_file = pydicom.dcmread(synth_path)
    synth_img = synth_file.pixel_array.astype(float)
    synth_img = np.uint16((np.maximum(synth_img,0)/synth_img.max())*65535.0)
    resized_synth_img = resize(synth_img, (1024,1024), anti_aliasing=True)
    synth_img_ants = ants.from_numpy(resized_synth_img)
    
    print(synth_file.pixel_array.size)
    
    #resize images
    original = orig_img_ants.resample_image((1024,1024),1,0)
    synthetic = synth_img_ants.resample_image((1024,1024),1,0)
    #original.plot(overlay = synthetic, title = 'Before Registration')
    synth_before = synthetic.numpy()
    
    #transpose image
    mytx = ants.registration(fixed=original, moving=synthetic, type_of_transform='DenseRigid')
    warped_moving = mytx['warpedmovout']
    #original.plot(overlay = warped_moving, title='After Registration')
    mywarpedimage = ants.apply_transforms(fixed=original, moving=synthetic,transformlist=mytx['fwdtransforms'])
    #mywarpedimage.plot()
    orig_array = original.numpy()
    synth_array = mywarpedimage.numpy()
    
        # get the pixel information into a numpy array
    desc = synth_file.SeriesDescription
    
    # copy the data back to the original data set
    synth_array = np.uint16((np.maximum(synth_array,0)/synth_array.max())*65535.0)
    synth_file.PixelData = synth_array.tobytes()
    
    # update the information regarding the shape of the data array
    synth_file.Rows, synth_file.Columns = synth_array.shape
    synth_file.SeriesDescription = desc + ' REGISTERED'
    synth_file.file_meta.TransferSyntaxUID = ExplicitVRLittleEndian
    
    # print the image information given in the dataset
    #print(synth_file)
    #print(synth_file.pixel_array.size)
    #print(len(synth_file.PixelData))
    
    # fig, axes = plt.subplots(nrows=1, ncols=3, figsize=(10, 4),
    #                           sharex=True, sharey=True)
    # ax = axes.ravel()
    
    #get scores
    #ssim_score = ssim(orig_array, synth_array)
    #corr = np.corrcoef(orig_array.flatten(), synth_array.flatten())[0,1]

    #gather file information and name
    files = synth_path.split('coronal_fs_total')
    new_folder = files[0] + 'coronal_fs_reg'
    new_path = new_folder + files[1]
    
    names = files[1].split('/')
    new_study = new_folder + '/' + names[1]
    # print(new_study)
    # print(new_folder)
    # print(new_path)
    
    if not os.path.exists(new_folder):
        os.mkdir(new_folder)
    
    if not os.path.exists(new_study):
        os.mkdir(new_study)
        
    synth_file.save_as(new_path)
    
    #create dictionary
    #stats = [study, orig_path, synth_path, ssim_score, corr]
    #total_values[i] = stats
    
    # ax[0].imshow(orig_array, cmap = 'gray')
    # ax[0].set_title('Original Image')
 
    # ax[1].set_title('Synthetic Image')
    # ax[1].imshow(synth_before, cmap = 'gray')
    
    # ax[2].imshow(synth_array, cmap = 'gray')
    # ax[2].set_title('Synthetic Image Registered')

    # plt.tight_layout()
    # plt.show()
    #print(sdfs)

    
#%% export

#export to dataframe
df_total = pd.DataFrame.from_dict(data = total_values, orient = 'index', columns = ['Study','Original Path','Synthetic Path','SSIM','Correlation'])

#export to excel file
#df_total.to_csv('.csv', sep=str(','), index = True)

#%%
import matplotlib.pyplot as plt

import pydicom

from pydicom.data import get_testdata_files


ds = pydicom.dcmread(new_path)

plt.imshow(ds.pixel_array, cmap=plt.cm.bone) 


        
#%% get ssim and corr
#create empty dictionary
total_values = dict()

#run through files
for i in range(0,10):#df.index:
    #original image
    orig_path = df.loc[i,'nfs_path']
    orig_file = pydicom.dcmread(orig_path)
    orig_img = orig_file.pixel_array.astype(float)
    orig_img = np.uint16((np.maximum(orig_img,0)/orig_img.max())*255.0)
    resized_img = resize(orig_img, (256,256), anti_aliasing=True)
    orig_img_ants = ants.from_numpy(resized_img)

    #synthetic image
    synth_path = df.loc[i,'fs_path']
    synth_file = pydicom.dcmread(synth_path)
    synth_img = synth_file.pixel_array.astype(float)
    synth_img = np.uint16((np.maximum(synth_img,0)/synth_img.max())*255.0)
    resized_synth_img = resize(synth_img, (256,256), anti_aliasing=True)
    synth_img_ants = ants.from_numpy(resized_synth_img)
    
    #resize images
    original = orig_img_ants.resample_image((64,64),1,0)
    synthetic = synth_img_ants.resample_image((64,64),1,0)
    #original.plot(overlay = synthetic, title = 'Before Registration')
    synth_before = synthetic.numpy()
    
    #transpose image
    mytx = ants.registration(fixed=original, moving=synthetic, type_of_transform='DenseRigid')
    warped_moving = mytx['warpedmovout']
    #original.plot(overlay = warped_moving, title='After Registration')
    mywarpedimage = ants.apply_transforms(fixed=original, moving=synthetic,transformlist=mytx['fwdtransforms'])
    #mywarpedimage.plot()
    orig_array = original.numpy()
    synth_array = mywarpedimage.numpy()
    
    fig, axes = plt.subplots(nrows=1, ncols=3, figsize=(10, 4),
                             sharex=True, sharey=True)
    ax = axes.ravel()
    
    
    #gather file information and name
    files = orig_path.split('/')
    study = files[7]
    
    ax[0].imshow(orig_array, cmap = 'gray')
    ax[0].set_title('Original Image')

    ax[1].set_title('Synthetic Image')
    ax[1].imshow(synth_before, cmap = 'gray')
    
    ax[2].imshow(synth_array, cmap = 'gray')
    ax[2].set_title('Synthetic Image Registered')

    plt.tight_layout()
    plt.show()
    #print(sdfs)
    
#c = b.pixel_array.astype("uint16")
