# -*- coding: utf-8 -*-
"""
Created on Tue Aug 15 23:58:30 2023

@author: asus
"""

from tensorflow.examples.tutorials.mnist import input_data
import cv2
import matplotlib.pyplot as plt
import numpy as np
#import os
from simple_deep_learning import SimpleNetWork

input_node_num=196
output_node_num=10
layers=[98,196,196,196,98]
iter_num=10000
lr=0.001
test_size=1000

mnist = input_data.read_data_sets('./datasets/MNIST_data/', one_hot=True)

train_X = mnist.train.images
train_Y = mnist.train.labels

def get_data_label(ind):
    data=train_X[ind]
    label=train_Y[ind]
    #data=np.reshape(data,[28,28])
    return data,label

def get_data_label_by_num(num):
    sjs=np.random.randint(0,len(train_X)-test_size)
    data=train_X[sjs]
    label=train_Y[sjs]
    while label[num]!=1:
        sjs=np.random.randint(0,len(train_X)-test_size)
        data=train_X[sjs]
        label=train_Y[sjs]
    return data,label

def im2bin(im):
    res=np.zeros_like(im)
    for i in range(len(res)):
        for j in range(len(res[i])):
            res[i][j]=1 if im[i][j]>0.5 else 0
    return res

snw=SimpleNetWork()
#if os.path.exists('./weights.npy') and os.path.exists('./bs.npy'):
    
#snw.construct_network(input_node_num,output_node_num,layers)
weights,bs=snw.load_network()
#print('weights',[i.shape for i in weights])
#print('bs',[i for i in bs])
for i in range(iter_num):
    sjs=np.random.randint(0,len(train_X)-test_size)
    #data_ori,label=get_data_label(sjs)
    data_ori,label=get_data_label_by_num(i%10)
    im=np.reshape(data_ori,[28,28])
    im_re=cv2.resize(im,(14,14))
    #im_re=im2bin(im_re)
    #plt.imshow(im_re)
    data=np.reshape(im_re,[-1])
    weights,bs,loss=snw.fit_data_step(data,label,lr,weights,bs)
    '''if loss>3:
        lr=0.01
    if loss>2 and loss<=3:
        lr=0.001
    if loss>1 and loss<=2:
        lr=0.0001
    if loss<=1:
        lr=0.00001'''
    print(i,loss)
print('ok')
snw.save_network(weights, bs)
