#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 15 19:17:57 2022

@author: vivianzhang
"""
#imports

import numpy as np
import os
import pydicom
import pandas as pd
from pathlib import Path


#%%
# Insert parent directory's path
path = '/home/vivianzhang/Desktop/fastMRI/curated_dataset/training/sagittal/sagittal_nfs_total'

#assign labels
def label_folder(parent, label_dict):
    # iterate over all the files in directory 'parent'
    for file_name in os.listdir(parent):
        if file_name.endswith('.dcm'):
            #get file and file path
            file = pydicom.data.data_manager.get_files(parent,file_name)[0]
            file_path = "".join((parent, "/", file_name))
            
            if 'sagittal_nfs' in file_path:
                #split file path into specific names
                names = file_path.split('sagittal_nfs_total')
                #hospital = names[6]
                #patient = names[6]
                #study = names[7]
                synth_fpath = names[0] + 'sagittal_fs_total' + names[1]
                
                # if you need to actually read the dicom
                #ds = pydicom.dcmread(file)
                #description = ds.SeriesDescription.lower()
                #sex = ds.PatientSex
    
                #create list of things to put into dataframe
                #labels = [patient, hospital, study, description, sex, birthdate, acq_date]
                
                
                #add to dictionary
                if file_path not in label_dict:
                    label_dict[file_path] = synth_fpath
                else:
                    return
        else:
            #iterate on loop
            current_path = "".join((parent, "/", file_name))
            if os.path.isdir(current_path):
                # if we're checking a sub-directory, recursively call this method
                label_folder(current_path, label_dict)
                
    return label_dict

#%% execute code

#create empty dictionary
label_dict = dict()

#execute function
labels = label_folder(path, label_dict)


#%% export

#export to dataframe
df = pd.DataFrame.from_dict(data = label_dict, orient = 'index', columns = ['synth_path'])

#export to excel file
df.to_csv('/home/vivianzhang/Desktop/fastMRI/train_sag_registration.csv', sep = str(','), index = True, index_label = 'orig_path')
