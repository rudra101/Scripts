%This script is for preprocessing the fMRI data from ABIDE groups. It takes a defined list of subject IDs for preprocessing.

%subids = [50977,51011,50970,50965,50989,51035,50983,51034,50992,50991,50974,51007]; %for autistic children of ABIDE I NYU
%subids = [50964, 50998, 50990, 50976, 50994, 50995, 50973]; %for autistic adolescents of ABIDE I NYU
%subids = [51025, 51018, 51023, 51016, 51028, 51015]; %for autistic adults of ABIDE I NYU

%%below section marks the newly matched subjects
subids = [50286, 50288, 50312, 50295, 50317, 50303, 50306, 50283, 50310, 50281, 50316, 50305]; % ASD children from ABIDE I UniMichigan_Sample1
%subids = [50358, 50355, 50372, 50377, 50332, 50359, 50364, 50337, 50334, 50376, 50333]; % TD  children from ABIDE I UniMichigan_Sample1
%subids = [50298, 50315]; % ASD adolesc  from ABIDE I UniMichigan_Sample1
%subids = [50370, 50381]; % TD  adolesc  from ABIDE I UniMichigan_Sample1

%subids = [50404, 50406]; % ASD adolesc from ABIDE I UniMichigan_Sample2
%subids = [50416, 50383, 50418, 50423, 50422, 50426, 50421, 50419]; % TD  adolesc from ABIDE I UniMichigan_Sample2

%subids = [29068, 29065, 29060, 29058, 29067, 29070, 29057, 29059, 29066, 29062]; % ASD adults from ABIDE II ABIDEII-ETH_1
%subids = [29082, 29094, 29071, 29081, 29091, 29093, 29075, 29079, 29092, 29078]; % TD  adults from ABIDE II ABIDEII-ETH_1

%subids = [51024, 51028, 51015, 51016, 51021, 51018, 51017, 51029, 51025, 51023]; % ASD adults from ABIDE I phenotypic_NYU
%subids = [51146, 51148, 51155, 51153, 51113, 51149, 51119, 51154, 51117, 51116]; % TD  adults from ABIDE I phenotypic_NYU

%caution: the four filenames following this line are older. And kept for legacy.
%filename = 'conn_testproject.mat';
%filename = 'conn_project_ABIDEINYU_children.mat'; %for ABIDE I NYU ASD children
%filename = 'conn_project_ABIDEINYU_adolescents.mat'; %for ABIDE I NYU ASD adolescents
%filename = 'conn_project_ABIDEINYU_adults.mat'; %for ABIDE I NYU ASD adults

%% below section for newly matched final subjects
filename = 'conn_ABIDEI_UMich_Samp1_ASD_child.mat'; % ASD children from ABIDE I UniMichigan_Sample1
%filename = 'conn_ABIDEI_UMich_Samp1_TD_child.mat';  % TD children from ABIDE I UniMichigan_Sample1
%filename = 'conn_ABIDEI_UMich_Samp1_ASD_adolsc.mat'; % ASD adolesc  from ABIDE I UniMichigan_Sample1
%filename = 'conn_ABIDEI_UMich_Samp1_TD_adolsc.mat'; % TD  adolesc  from ABIDE I UniMichigan_Sample1
%filename = 'conn_ABIDEI_UMich_Samp2_ASD_adolsc.mat'; % ASD adolesc from ABIDE I UniMichigan_Sample2
%filename = 'conn_ABIDEI_UMich_Samp2_TD_adolsc.mat'; % TD  adolesc from ABIDE I UniMichigan_Sample2
%filename = 'conn_ABIDEII_ETH_ASD_adult.mat'; % ASD adults from ABIDE II ABIDEII-ETH_1
%filename = 'conn_ABIDEII_ETH_TD_adult.mat'; % TD  adults from ABIDE II ABIDEII-ETH_1
%filename = 'conn_ABIDEI_NYU_ASD_adult.mat'; % ASD adults from ABIDE I phenotypic_NYU
%filename = 'conn_ABIDEI_NYU_TD_adult.mat'; % TD  adults from ABIDE I phenotypic_NYU
TR=2; %repetition time
ISNEW = 1; %isnew
OVERWRITE = 0; %overwrite

nsubjects = length(subids);
%%see if extraction is necessary
%anat_file_gz = 'anat.nii.gz';
anat_file_gz = 'mprage.nii.gz';
func_file_gz = 'rest.nii.gz';
funcfiles_gz = cellstr(conn_dir(func_file_gz));
anatfiles_gz = cellstr(conn_dir(anat_file_gz));
FUNC_FILE_gz = getRelevantSubjectFiles(funcfiles_gz, subids);
ANAT_FILE_gz = getRelevantSubjectFiles(anatfiles_gz, subids);
extractfiles(FUNC_FILE_gz);
extractfiles(ANAT_FILE_gz);
%extraction is done
%%search for right number of extracted files
%anat_file = 'anat.nii';
anat_file = 'mprage.nii';
func_file = 'rest.nii';
funcfiles = cellstr(conn_dir(func_file));
anatfiles = cellstr(conn_dir(anat_file));
FUNC_FILE = getRelevantSubjectFiles(funcfiles, subids);
ANAT_FILE = getRelevantSubjectFiles(anatfiles, subids);

if rem(length(FUNC_FILE),nsubjects),error('mismatch number of functional files %n', length(FUNC_FILE));
end
if rem(length(ANAT_FILE),nsubjects),error('mismatch number of anatomical files %n', length(ANAT_FILE));
end
nsessions=length(FUNC_FILE)/nsubjects;
FUNC_FILE=reshape(FUNC_FILE,[nsubjects,nsessions]);
ANAT_FILE={ANAT_FILE{1:nsubjects}};
disp([num2str(size(FUNC_FILE,1)),' subjects']);
disp([num2str(size(FUNC_FILE,2)),' sessions']);
%we have the files now

%%TBD: check if parallel config(Background for Linux) is possible - https://web.conn-toolbox.org/resources/cluster-configuration
%%start with conn batch definitions
%Watanabe 2017 - realignment, unwarping, slice timing correction,normalization to the standard template (ICBM 152) and spatial smoothing
clear batch;
batch.filename=fullfile(pwd,filename);
batch.Setup.isnew=ISNEW;
batch.Setup.nsubjects=nsubjects;
batch.Setup.RT=TR;
batch.Setup.VOX=2; % 2mm voxel size for analyses
batch.Setup.functionals=repmat({{}},[nsubjects,1]);
% Point to functional volumes for each subject/session
for nsub=1:nsubjects,
for nses=1:nsessions,
batch.Setup.functionals{nsub}{nses}{1}=FUNC_FILE{nsub,nses};
end;
end
batch.Setup.structurals=ANAT_FILE;
% Point to anatomical volumes for each subject
batch.Setup.rois.names={'power2011'};
%the following was created by conn_createmniroi('PP264_all_ROIs_4mmSphere_2mmres.nii', 'PP264_template_coords.txt', 4, 2). The *coords.txt file was created using SevenROIsDefinition.py
batch.Setup.rois.files{1}=fullfile(fileparts(which('conn')),'rois','test.nii');
%batch.Setup.rois.files{1}=fullfile(fileparts(which('conn')),'rois','PP264_all_ROIs_4mmSphere_2mmres.nii'); %use same roi file for all subjects & sessions
%batch.Setup.conditions.names=cellstr([repmat('Session',[nconditions,1]),num2str((1:nconditions)')]);
%TBD: verify if preprocessing steps are needed.
batch.Setup.conditions.names = {'rest'};
for nsub=1:nsubjects;
	batch.Setup.conditions.onsets{1}{nsub}{1}=0;
        batch.Setup.conditions.durations{1}{nsub}{1}=inf;
end;
%batch.Setup.preprocessing.coregtomean = 1; %Coregistration to 0 for first. 1 for mean. 
%batch.Setup.preprocessing.boundingbox = [-90 -126 -72;90 90 108];
%batch.Setup.preprocessing.voxelsize_anat = ; %target anat voxel size
%batch.Setup.preprocessing.voxelsize_func = ; %target func voxel size
batch.Setup.preprocessing.fwhm=6; %6mm FWHM smoothing
batch.Setup.preprocessing.steps={}; % user-ask

batch.Setup.overwrite=OVERWRITE; % 1 or 0.
batch.Setup.done=1;
%% CONN Denoising
batch.Denoising.confounds = {}; %use default
batch.Denoising.filter=[0.01, 0.1]; %frequency filter (band-pass values, in Hz)
batch.Denoising.done=1;

conn_batch(batch);
%% Display using CONN GUI - launches conn gui to explore results
%conn
%conn('load',fullfile(pwd, filename));
%conn gui_results

function extractfiles(filearray);
	for index = 1:length(filearray);
		candidate = char(filearray(index));
		if isempty(candidate);
			continue
		end
		if exist(candidate(1:end-3)) == 0; %remove .gz and check if file doesn't exist
		  fprintf('Extracting %s\n', candidate)
		  gunzip(candidate);
		end
	end
end

%filters relevant paths containing the subject IDs mentioned in subids file.
function result = getRelevantSubjectFiles(filearray, subids);
	result = {};
	foundSubjects = [];
	for index = 1:length(filearray);
		candidate = filearray(index);
		for indsub = 1:length(subids);
			subid = subids(indsub);
			if contains(candidate, num2str(subid));
				fprintf('Found file for sub %d\n', subid)
				result{end + 1} = char(candidate);
				foundSubjects = [foundSubjects subid];
				break
			end
		end
		%result
	end
	differ = setdiff(subids, foundSubjects);
	if ~isempty(differ)
	    fprintf('Caution: no files found for %g\n', differ);
        end
end
 
