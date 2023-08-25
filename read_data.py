# -*- coding: utf-8 -*-
"""
Created on Sat Jul 15 12:07:45 2023

@author: asus
"""

from tensorflow.examples.tutorials.mnist import input_data

mnist = input_data.read_data_sets('./datasets/MNIST_data/', one_hot=True)

train_X = mnist.train.images
train_Y = mnist.train.labels
print(train_X.shape, train_Y.shape)

