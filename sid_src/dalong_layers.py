import torch
import torch.nn as nn
from torch.autograd import Variable
import torch.nn.functional as F
import numpy as np
import NoiseEstimation as NE
import NoiseEstimation_KPN as NE_KPN
import collections
import config as cfg
CUDA_USE = cfg.CUDA_USE;
class simpleblock(nn.Module):
    def __init__(self,input_channel,output_channel,ksize,pad,batchnorm):
        super(simpleblock,self).__init__();
        if batchnorm:
            self.model = nn.Sequential(
                             nn.Conv2d(input_channel,output_channel,kernel_size = ksize,stride = 1,padding = pad),
                             nn.ReLU(),
                             nn.BatchNorm2d(input_channel)
                             );
        else :
            self.model = nn.Sequential(
                             nn.Conv2d(input_channel,output_channel,kernel_size = ksize,stride = 1,padding = pad),
                             nn.ReLU()
                             );
    def forward(self,inputs):
        outputs = self.model(inputs);
        return outputs;

class lowlevel_block(nn.Module):
    def __init__(self,depth,input_channel,output_channel,ksize,pad=0, batchnorm=True):
        super(lowlevel_block,self).__init__();
        modules = collections.OrderedDict();
        for index in range(depth):
            name = 'conv' + "_{}".format(index+1);
            modules[name] = simpleblock(input_channel,output_channel,ksize,pad,batchnorm);
        self.model = nn.Sequential(modules);

    def forward(self,inputs):
        outputs = self.model(inputs);
        return outputs;

class UnpackBayerMosaicLayer(nn.Module):
    def __init__(self):
        super(UnpackBayerMosaicLayer,self);

    def forward(self,inputs):
        top = Variable(torch.zeros(inputs.size(0),3,inputs.size(2),inputs.size(3)));
        if CUDA_USE:
            top = top.cuda();

        for channel in range(3):
            top[:,channel,::2,::2] = inputs[:,4*c,:,:];
            top[:,channel,::2,1::2] = inputs[:,4*c+1,:,:];
            top[:,channel,1::2,::2] = inputs[:,4*c+2,:,:];
            top[:,channel,1::2,1::2] = inputs[:,4*c+3,:,:];
        return top;
'''
supported bayer type
RGGB GRBG
defalut : GRBG
'''
class BayerMosaicLayer(nn.Module):
    def __init__(self,bayer_type = 'GRBG'):
        super(BayerMosaicLayer,self).__init__();
        self.bayer_type = bayer_type;
    def forward(self,inputs):
        outputs = Variable(torch.zeros(inputs.size(0),3,inputs.size(2),inputs.size(3)));
        if CUDA_USE:
            outputs = outputs.cuda();

        if self.bayer_type == 'GRBG':
            outputs[:,1,::2,::2] = inputs[:,1,::2,::2]; #G
            outputs[:,0,::2,1::2] = inputs[:,0,::2,1::2];# R
            outputs[:,2,1::2,::2] = inputs[:,2,1::2,::2];# B
            outputs[:,1,1::2,1::2] = inputs[:,1,1::2,1::2]; # G
        elif self.bayer_type == 'RGGB' :
            outputs[:,0,::2,::2] = inputs[:,0,::2,::2]; # R
            outputs[:,1,::2,1::2] = inputs[:,1,::2,1::2]; # G
            outputs[:,1,1::2,::2] = inputs[:,1,1::2,::2]; #G
            outputs[:,2,1::2,1::2] = inputs[:,2,1::2,1::2]; # B
        else :
            print('Dude, This bayer type is not supported for now ,sorry for that');
            exit();
        return outputs;
class CropLayer(nn.Module):
    def __init__(self):
        super(CropLayer,self).__init__();

    def forward(self,inputs,reference):
        src_sz = reference.size();
        dst_sz = inputs.size();
        offset = [(s-d) / 2 for s,d in zip(dst_sz,src_sz)];
        outputs = inputs[:,:,int(offset[2]):int(offset[2])+int(src_sz[2]),int(offset[3]):int(offset[3])+int(src_sz[3])].clone();
        return outputs;

class PackBayerMosaicLayer(nn.Module):
    def __init__(self,bayer_type='GRBG' ):
        super(PackBayerMosaicLayer,self).__init__();
        self.bayer_type = bayer_type;
    # receive a raw data
    def forward(self,inputs):
        top = Variable(torch.zeros(inputs.size(0),4,inputs.size(2) / 2,inputs.size(3) / 2));
        if CUDA_USE:
            top = top.cuda();

        if self.bayer_type == 'GRBG':
            '''
            G R G R G
            B G B G B
            G R G R B
            '''
            top[:,0,:,:] = inputs[:,1,::2,::2]; # G
            top[:,1,:,:] = inputs[:,0,::2,1::2]; # R
            top[:,2,:,:] = inputs[:,2,1::2,::2]; # B
            top[:,3,:,:] = inputs[:,1,1::2,1::2]; # G
        if self.bayer_type == 'RGGB':
            '''
            R G R G R
            G B G B G
            R G R G R
            G B G B G
            '''
            top[:,0,:,:] = inputs[:,1,::2,1::2]; # G
            top[:,1,:,:] = inputs[:,0,::2,::2]; # R
            top[:,2,:,:] = inputs[:,2,1::2,1::2]; # B
            top[:,3,:,:] = inputs[:,1,1::2,::2]; # G

        return top;
class UnpackBayerMosaicLayer(nn.Module):
    def __init__(self):
        super(UnpackBayerMosaicLayer,self).__init__();
    def forward(self,inputs):
        outputs = Variable(torch.zeros(inputs.size(0),3,inputs.size(2)*2,inputs.size(3)*2));
        if CUDA_USE:
            outputs = outputs.cuda();

        for channel in range(3):
            outputs[:,channel,::2,::2] = inputs[:,4*channel,:,:];
            outputs[:,channel,::2,1::2] = inputs[:,4*channel+1,:,:];
            outputs[:,channel,1::2,::2] = inputs[:,4*channel+2,:,:];
            outputs[:,channel,1::2,1::2] = inputs[:,4*channel+3,:,:];
        return outputs;
# implement noise estimation and add an noise layer to the inputs
# receive CFA array which has been splited into 4 channels
class AddNoiseEstimationLayer(nn.Module):
    def __init__(self):
        super(AddNoiseEstimationLayer,self).__init__();

    def forward(self,inputs,sigma_info = None):
        if sigma_info is not None :
            outputs = NE_KPN.NoiseEstimation(inputs,sigma_info[:,:,0,0],sigma_info[:,:,0,1]);
            return outputs ;
        else :
            outputs = Variable(torch.rand(inputs.size(0),1,inputs.size(2),inputs.size(3)));
            if CUDA_USE:
                outputs = outputs.cuda();

            for index in range(inputs.size(0)):
                outputs[index,:,:,:] = NE.NoiseEstimation(inputs[index,:,:,:]);
            return outputs;

class SliceHalfLayer(nn.Module):
    def __init__(self):
        super(SliceHalfLayer,self).__init__();

    def forward(self,inputs):
        n = inputs.size(1) / 2;
        A_Half = inputs[:,:n,:,:].clone();
        B_Half = inputs[:,n:,:,:].clone();

        return A_Half*B_Half;

class Upsample_Concat(nn.Module):
    def __init__(self,in_channels,out_channels):
        super(Upsample_Concat,self).__init__();
        self.deconv = nn.ConvTranspose2d(in_channels,out_channels,kernel_size =2,stride = 2);
        self.crop = CropLayer();
    def forward(self,inputs1,inputs2):

        outputs1 = self.deconv(inputs1);
        print('dalong log : check inputs and outputs size = {}  {}'.format(inputs1.size(),outputs1.size()));
        inputs2 = self.crop(inputs2,outputs1);
        return torch.cat([outputs1,inputs2],1);

