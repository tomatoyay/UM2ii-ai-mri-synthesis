%% Load your deepnet model
% Change your model between AX (for axial), Sag (for Sagittal), COR (for
% coronal)
deepnet = 'deepnet_unet_noNorm_98Pats_batch30_learn_05_SAG.mat';
load(deepnet);

%% Load directory of images
cd '/home/vivianzhang/Desktop/Gradient/curated_dataset/validation' %replace with folder of images
myFiles = dir('**/*.dcm');
myFiles = struct2table(myFiles);

%% Load list of studies
studies = readtable('/home/vivianzhang/Desktop/Gradient/validation_study.csv');

%parse through files
for k = 1:height(studies)
    study = studies.study{k};
    %new dicomuid for new image series to match each study
    ySeriesInstanceUID = dicomuid;
    
    study_list = contains(myFiles.folder,study);
    seq_list = contains(myFiles.folder,'coronal_nfs');
    [img_list, logical] = find((study_list & seq_list) == 1);

    for j = 1:height(img_list)
        index = img_list(j);
        path = myFiles.folder{index};
        image = myFiles.name{index};
        file_path = strcat(path,'/',image);
        files = split(path,"/");
        seq_idx = length(files);
        old_sequence = files{seq_idx};
        old_path = extractBefore(file_path,old_sequence);
        new_sequence = 'coronal_synthfs_gradient9'; %change this to sagittal or coronal when using

        % Use dicomread to read in the image and convert to square using padding
        PD_Img1 = dicomread(file_path);
        info = dicominfo(file_path,UseDictionaryVR = true);
        PD_Img = double(PD_Img1);
        PD_Img = 5 * PD_Img;
        %PD_Img = 2000 * normalize(PD_Img,'range');
        PD_Img = imresize(PD_Img,[256 256]);
        PD_Img = reshape(PD_Img,[256 256 1]);

        % Make your prediction
        testY = predict(deepnet9_gradient_cor,PD_Img);
        % Sharpen the resultant image to improve diagnostic quality
        testY = imsharpen(testY);%,'Radius',2.5,'Amount',1.5);
        testY = uint16(testY);

        % Change new DICOM image information
        info.SeriesDescription = 'CORONAL FS SYNTHETIC';
        info.ProtocolName = 'COR FS ORIG JHU MODEL GRADIENT 90'; %change to correct orientation
        info.SeriesNumber = 90;
        info.NumberOfPhaseEncodingSteps = 256;
        fprintf('%s\n%s\n', info.SeriesInstanceUID,ySeriesInstanceUID);
        info.SeriesInstanceUID = ySeriesInstanceUID;

        %Generate testY and save image
        new_folder = strcat(old_path,new_sequence);
        new_fname = strcat(old_path,new_sequence,'/',image);

        if ~exist(new_folder,'dir')
            mkdir(new_folder)
        end

        dicomwrite(testY, new_fname, info)
        fprintf('%s\n\n', new_fname);

    end
end

disp('done')
