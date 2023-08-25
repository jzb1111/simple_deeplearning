# -*- coding: utf-8 -*-
"""
Created on Sat Jul 15 12:05:42 2023

@author: asus
"""

import numpy as np
import os

def sigmoid(x):
    return 1/(1+np.exp(-x))

def d_sigmoid(x):
    #S′(x)=S(x)(1−S(x))
    return sigmoid(x)*(1-sigmoid(x))

class SimpleNetWork:
    #1.构建网络
    #1.1 construct_network
    #2.训练网络
    #2.1 fit_data(循环的调用)
    #2.2 save_network
    #3.使用网络
    #3.1 load_network
    #3.2 predict
    def __init__(self):
        #self.input_node_num=0
        #self.output_node_num=0
        #self.layers=[]
        self.activate_function=sigmoid
        self.d_activate_function=d_sigmoid
        
    def construct_network(self,input_node_num,output_node_num,layers):
        input_node_num=input_node_num
        output_node_num=output_node_num
        layers=layers

        weights=[np.random.uniform(-1,1,[input_node_num,layers[0]])]#uniform
        bs=[np.random.uniform(-1,1)]
        for i in range(len(layers)-1):
            weights.append(np.random.uniform(-1,1,[layers[i],layers[i+1]]))
            bs.append(np.random.uniform(-1,1))
        weights.append(np.random.uniform(-1,1,[layers[-1],output_node_num]))
        bs.append(np.random.uniform(-1,1))
        self.save_network(weights, bs)
        
    def save_network(self,weights,bs):
        np.save('weights_bs.npy',[weights,bs])
        
    def load_network(self):
        return np.load('./weights_bs.npy',allow_pickle=True)
        
    def fit_data_step(self,xs,label,lr,weights,bs):

        siglis=[]
        nodelis=[]
        out=xs
        for i in range(len(weights)):
            sig=np.dot(out,weights[i])+bs[i]
            out=self.activate_function(sig)
            siglis.append(sig)
            nodelis.append(out)
        loss=np.sum((out-label)**2)
        d_loss_d_weights=[np.zeros_like(i) for i in weights]
        d_loss_d_bs=[np.zeros_like(i) for i in bs]
        d_loss_d_nodes=[np.zeros_like(i) for i in nodelis]
        d_loss_d_sigs=[np.zeros_like(i) for i in siglis]
        
        for i in range(len(weights)):
            ind=-i-1
            weight_tmp=weights[ind]
            b_tmp=bs[ind]
            node_tmp=nodelis[ind]
            sig_tmp=siglis[ind]
            #################
            ##d_loss_d_node##
            #################
            if ind==-1:
                for j in range(len(node_tmp)):
                    d_loss_d_node=2*(node_tmp[j]-label[j])
                    d_loss_d_nodes[ind][j]=d_loss_d_node
            else:
                for j in range(len(nodelis[ind])):
                    d_loss_d_node=0
                    for k in range(len(d_loss_d_sigs[ind+1])):
                        #print(ind,j,k)
                        d_loss_d_node+=d_loss_d_sigs[ind+1][k]*weights[ind+1][j][k]
                    d_loss_d_nodes[ind][j]=d_loss_d_node
            ################
            ##d_loss_d_sig##
            ################        
            for j in range(len(sig_tmp)):
                d_loss_d_sig=d_loss_d_nodes[ind][j]*d_sigmoid(sig_tmp[j])
                #print('d_loss_d_sig',j,d_loss_d_sigs.shape)
                d_loss_d_sigs[ind][j]=d_loss_d_sig
            ###################
            ##d_loss_d_weight##
            ###################
            if ind!=-len(weights):
                for j in range(len(nodelis[ind-1])):#d_loss_d_sigs[ind])):
                    for k in range(len(d_loss_d_sigs[ind])):#nodelis[ind-1])):
                        #print('d_loss_d_sigs',len(d_loss_d_sigs),d_loss_d_sigs[ind+1].shape,ind+1,j)
                        d_loss_d_weight=d_loss_d_sigs[ind][k]*nodelis[ind-1][j]
                        d_loss_d_weights[ind][j][k]=d_loss_d_weight
            else:
                for j in range(len(xs)):#d_loss_d_sigs[ind])):
                    for k in range(len(d_loss_d_sigs[ind])):#nodelis[ind-1])):
                        #print('d_loss_d_sigs',len(d_loss_d_sigs),d_loss_d_sigs[ind+1].shape,ind+1,j)
                        d_loss_d_weight=d_loss_d_sigs[ind][k]*xs[j]
                        d_loss_d_weights[ind][j][k]=d_loss_d_weight
            ##############
            ##d_loss_d_b##
            ##############
            d_loss_d_b=0
            for j in range(len(sig_tmp)):
                d_loss_d_b+=d_loss_d_sigs[ind][j]
            d_loss_d_bs[ind]=d_loss_d_b
        weights=[weights[i]-d_loss_d_weights[i]*lr for i in range(len(weights))]
        bs=[bs[i]-d_loss_d_bs[i]*lr for i in range(len(bs))]
        return weights,bs,loss
        
    def predict(self,xs,weights,bs):
        out=xs
        for i in range(len(weights)):
            sig=np.dot(out,weights[i])+bs[i]
            out=self.activate_function(sig)
        return out