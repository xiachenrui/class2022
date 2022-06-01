r'''
Data loader for the vegetable picture dataset.
'''

from cgi import test
import torch
import os
import os.path as op
import numpy as np
import pickle as pkl

from torchvision import models, transforms, datasets
from sklearn.model_selection import train_test_split, validation_curve


class VegetablePic(datasets.ImageFolder):
    r'''
    Special data loader for homework vegetable picture dataset,
    Directly inherit from torchvision.datasets.ImageFolder
    -------
    Paras
        mode: ['train','test', 'validation']
    -------
    Note: can not change the class name
    '''
    file_path = './data/vegetable_pic/'
    mean = [0.485, 0.456, 0.406]
    std = [0.229, 0.224, 0.225]
    
    def __init__(self, mode):
        r'''

        '''
        super().__init__()
        self.root = os.path.join(VegetablePic.file_path, mode)
        if mode == 'train':
            self.transform  = transforms.Compose([
                                transforms.RandomResizedCrop(size=224),
                                transforms.RandomHorizontalFlip(),
                                transforms.ToTensor(),
                                transforms.Normalize(VegetablePic.mean, VegetablePic.std)
                                ])
        elif mode == 'test' or mode == 'validation':
            self.transform = transforms.Compose([
                        transforms.Resize(size=256),
                        transforms.CenterCrop(size=224),
                        transforms.ToTensor(),
                        transforms.Normalize(VegetablePic.mean, VegetablePic.std)
                        ])
        