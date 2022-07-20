# AI MRI Synthesis


## Variability in MRI Knee Dataset Organization and Demographic Reporting: Barriers to Dataset Harmonization and Identification of Bias
**Introduction:** MRI datasets have anecdotally been challenging to harmonize and identify potential sources of bias due to inconsistent organization and reporting of metadata and demographics. We evaluated the reporting and organization of metadata and demographics in large, publicly-available MRI knee datasets to shed light on potential obstacles to dataset harmonization and identification of potential sources of bias.

**Methods:** We evaluated 5 large public datasets of knee MRIs identified through a search of medical imaging data hubs with further cross-referencing of published papers. We included datasets with >25 MRIs as a reasonable dataset size for training and/or testing DL models. For each dataset, we summarized reporting and organization of metadata, image files, and demographics. For missing MRI sequence and/or reconstruction plane, we evaluated the utility of using convolutional neural network (CNN) classifiers to accurately ‘recover’ this information. 

**Results:** Amongst the 5 datasets, metadata and file organization was inconsistent (Table 1). 

From a file organization/metadata standpoint, each dataset inconsistently reported the number of ‘exams’ vs. ‘patients.’ Dataset sizes ranged from 155 to 3,795 MRI exams (full studies). Image formats ranged from DICOM files (3 datasets), to .h5, .npy and .pck files (1 data set each) – the latter may irrevocably lose important pixel information through necessary image processing. Although MRI sequence names and reconstruction planes were reported for 5/6 datasets, they did not specify if the sequences were ‘anatomic’ or ‘fluid-sensitive’ (fat-suppressed) [the two functionally important distinctions for musculoskeletal MRI] and specific scan parameters were lacking in 3/6 datasets. For the single dataset that did not provide sequence or reconstruction plane information (Stanford MRNet) , we were able to ‘recover’ this information in 100% of scans by finetuning an ImageNet-pretrained Resnet34 CNN on 48 MRI studies from the NYU fastMRI dataset (Figure 1).

Demographics were missing from 2 datasets. Of those reporting demographics, 2 reported gender and age only; only 1 (NIH Osteoarthritis Initiative) reported race. The datasets were homogenous, with 5 originating from the USA (4 from CA or NY) and 1 from Croatia.



Table 1
![image](https://user-images.githubusercontent.com/59489753/179047768-b9327bba-d8a4-437e-bd38-c667795febd4.png)

Figure 1
![image](https://user-images.githubusercontent.com/59489753/179047834-0dfa9ee6-2fa7-40a6-a4b8-614bceced202.png)


**Getting Started:** Each classification model has a file named requirements.txt for reference to set up a virtual environment compatible with the model. 
Installation:
dill==0.3.5.1
fastai==2.7.6
fastbook==0.0.26
gdcm==1.1
matplotlib==3.5.1
numpy==1.21.5
pandas==1.4.3
Pillow==9.2.0
pydicom==2.3.0
scikit_image==0.19.2
seaborn==0.11.2
skimage==0.0
torch==1.10.2+cu113

**Usage:** Instructions on how to use your code?

**Contribute:** Instructions on how one can contribute to your work

**Cite:** Instructions on how to cite your work.
