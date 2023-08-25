# -*- coding: utf-8 -*-
"""
Created on Thu Aug 17 00:38:44 2023

@author: asus
"""

from simple_deep_learning import SimpleNetWork
from tensorflow.examples.tutorials.mnist import input_data
import cv2
import matplotlib.pyplot as plt
import numpy as np

mnist = input_data.read_data_sets('./datasets/MNIST_data/', one_hot=True)

train_X = mnist.train.images
train_Y = mnist.train.labels

def get_data_label(ind):
    data=train_X[ind]
    label=train_Y[ind]
    #data=np.reshape(data,[28,28])
    return data,label

snw=SimpleNetWork()
weights,bs=snw.load_network()
data_ori,label=get_data_label(54960)
data=np.reshape(cv2.resize(np.reshape(data_ori,[28,28]),(14,14)),[-1])
plt.imshow(np.reshape(data,[14,14]))
pre=snw.predict(data,weights,bs)
print(pre)
print(np.argmax(pre))
print(label)