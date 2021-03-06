import argparse

CUDA_USE = 1;
parser = argparse.ArgumentParser();
'''
These are all parameters for training and testing
'''

parser.add_argument('--lr',type = float,default = 1e-4,help = 'learning rate for training ');
parser.add_argument('--depth',type = int,default = 15,help = 'number of convolution layers');
parser.add_argument('--kernel_size',type = int,default = 3,help = 'size of kernel for each convolution layer ');
parser.add_argument('--width',type = int,default = 64,help = 'channels for each feature map per layer');
parser.add_argument('--batchnorm',type = bool,default = False,help = 'whether to use batchnorm');
parser.add_argument('--print_freq',type = int ,default = 10,help = 'log print freq when training ');
parser.add_argument('--save_freq',type= int,default =15,help = 'model save freq when training');
parser.add_argument('--workers',type = int,default = 8,help = 'number of workers for reading the data ');
parser.add_argument('--max_epoch',type = int,default = 9,help = 'max epoch for training ');
parser.add_argument('--checkpoint_folder',type = str,default = '../models/');
parser.add_argument('--size',type = int,default = 128,help = 'size for training image setting ');
parser.add_argument('--pad',type = int,default = 0,help = 'paddding size ');
parser.add_argument('--data_dir',type = str,default = '',help = 'dataset directory for training ');
parser.add_argument('--flist',type = str,default = '',help = 'dataset list file for training ');
parser.add_argument('--Center',type = bool,default = False,help = 'whether to crop from center of the image ');
parser.add_argument('--Random',type = int,default = 1,help ='whether to crop randomly from the image ');
parser.add_argument('--model_name',type = str,default = 'DemoisaicNet',help = 'set the model name prefix');
parser.add_argument('--bayer_type',type = str,default = 'GRBG',help = 'set the bayer type for all training data ');
parser.add_argument('--Evaluate',type = int,default =0,help = 'Whether to evaluate the dataset');
parser.add_argument('--input_white_point',type = float,default = 255,help  = 'white point for raw data ');
parser.add_argument('--input_black_point',type = float,default = 0,help = 'black point for raw data ');
parser.add_argument('--gt_white_point',type = float,default = 255,help  = 'white point for raw data ');
parser.add_argument('--gt_black_point',type = float,default = 0,help = 'black point for raw data ');
parser.add_argument('--gt_white_balance',type = str,default = '1 1 1',help = 'white_balance for gt ');
parser.add_argument('--input_white_balance',type = str,default = '1 1 1',help = 'white balance for inputs');

parser.add_argument('--pretrained',type = int,default = 0,help = 'whether init the model with pretrained models');
parser.add_argument('--predemosaic',type = int,default = 0);
parser.add_argument('--init_model',type =str,default = '',help = 'choose init model');
# if there is a sigma_info file for using ,it is like sigma_shot ,sigma_read
# if not ,we use our own NoiseEstimation module for noise estimation
parser.add_argument('--sigma_info',type = bool,default = False,help = 'if this dataset has sigma_info file to use ');
parser.add_argument('--model',type = str,default = 'DemosaicNet',help = 'choose to a Net arch to train ');
parser.add_argument('--loss',type = str,default = '',help = 'choose a loss ')
parser.add_argument('--TRAIN_BATCH',type = int,default = 4,help = 'train BATCH inputs');
parser.add_argument('--GET_BATCH',type = int,default = 64,help = 'Load GET_BATCH inputs')
parser.add_argument('--TRAIN_GAN',type = int,default = 0,help = 'Whether to train ')
parser.add_argument('--lr_change',type = int,default = 1);
parser.add_argument('--input_type',type =str,default = 'IMG',help = 'Choose input data type for data_reader');
parser.add_argument('--gt_type',type = str,default  = 'IMG',help = 'Choose gt data type for data reader');
parser.add_argument('--input_normalize',type = int,default = 16, help = 'bitdepth for input data');
parser.add_argument('--gt_normalize',type = int,default = 16,help = 'bitdepth for gt data');
parser.add_argument('--Resize',type=int,default = 0,help = 'whether to resize the input ');
parser.add_argument('--scale_factor',type = int, default = 0, help = 'resize parameter to use ');
parser.add_argument('--AddGaussianNoise',type = int ,default = 0, help = 'whether to add Gaussian Noise');
parser.add_argument('--pack_depth',type = int,default = 3 ,help = 'choose pack depth for pack layer ');


# This is for submodels for pipelines

parser.add_argument('--init_submodel',type = str,default = '',help = '<REQUIRE> set model init path for submodels ');
parser.add_argument('--submodel_num',type = int , default = 16,help = 'decide how many models to use in the submodels');
parser.add_argument('--init_router',type = str,default = '',help = 'decide which model to use in router model');
parser.add_argument('--Crop',type=int,default = 0,help = 'decide if crop will be done to train images');
parser.add_argument('--submodel_depth',type = str,default = '',help = '<REQUIRE> set depth for for submodels ');
parser.add_argument('--encoder_div',type=int,default=1,help ='decide the channels used by encoder');
parser.add_argument('--submodel_div',type =int,default = 1,help =  'decide the channel used by submodels');
parser.add_argument('--real_patchsize',type = int ,default = 120,help = 'decide real patch  size ');
parser.add_argument('--test_patchsize',type = int,default = 128 , help = 'decide test patch size ');
parser.add_argument('--demosaicnet_div',type =int,default = 1,help =  'decide the channel used by demosaicnet');
parser.add_argument('--add_noise',type = int,default = 0,help = 'decide if add Gaussian noise to input image');
parser.add_argument('--max_noise',type = float,default = 0.1,help = 'decide the max noise level added to image');
parser.add_argument('--init_folder',type = str,default = '',help = 'decide model folder tested in pipeline');
parser.add_argument('--init_depth',type = str,default = '',help = 'decide model depth tested in pipeline');
