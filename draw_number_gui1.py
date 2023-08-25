# -*- coding: utf-8 -*-
"""
Created on Sun Aug 20 21:32:46 2023

@author: asus
"""

import tkinter as tk
from simple_deep_learning import SimpleNetWork
import PIL.ImageGrab as ImageGrab
import numpy as np
import matplotlib.pyplot as plt
import cv2

def gaussian_blur(image, kernel_size=5, sigma=1.4):
    kernel = np.zeros((kernel_size, kernel_size), dtype=np.float32)
    center = kernel_size // 2
    sum_val = 0.0

    for i in range(kernel_size):
        for j in range(kernel_size):
            x = i - center
            y = j - center
            kernel[i, j] = np.exp(-0.5 * (x ** 2 + y ** 2) / (sigma ** 2))
            sum_val += kernel[i, j]

    kernel /= sum_val

    blurred_image = cv2.filter2D(image, -1, kernel)
    
    for i in range(len(blurred_image)):
        for j in range(len(blurred_image[i])):
            blurred_image[i][j]=sigmoid(blurred_image[i][j])
    return blurred_image

class Draw():
    def __init__(self):
 
        # Defining title and Size of the Tkinter Window GUI
        
        self.pointer = "white"
        self.background=None
        self.eraser_btn=None
        self.pen_btn=None
        self.pre_btn=None
        self.root=None
        self.GUI()
        
    def GUI(self):
        self.root=tk.Tk()
        self.root.title("画图工具Python")
        self.root.geometry("500x400")
        
        self.eraser_btn = tk.Button(self.root, text="Eraser", command=self.eraser, width=15)
        self.eraser_btn.place(x=10, y=50)
        
        self.pen_btn = tk.Button(self.root, text="Pen", command=self.pen, width=15)
        self.pen_btn.place(x=10, y=100)
        
        self.pre_btn=tk.Button(self.root, text="Predict", command=self.predict, width=15)
        self.pre_btn.place(x=10, y=150)
        
        self.background = tk.Canvas(self.root, bg='black', bd=5, relief=tk.GROOVE, height=300, width=300)
        self.background.place(x=140, y=50)
        self.background.bind("<B1-Motion>", self.paint)
        self.root.mainloop()
    
    def paint(self,event):
        x1, y1 = (event.x - 2), (event.y - 2)
        x2, y2 = (event.x + 2), (event.y + 2)
        self.background.create_oval(x1, y1, x2, y2, fill=self.pointer, outline=self.pointer,width=13)
        
    def eraser(self):
        self.pointer = 'black'
    
    def pen(self):
        self.pointer = 'white'
    
    def predict(self):
        x = self.root.winfo_rootx() + self.background.winfo_x()
        y = self.root.winfo_rooty() + self.background.winfo_y()
        x1 = x + self.background.winfo_width()
        y1 = y + self.background.winfo_height()
        tmp=ImageGrab.grab().crop((x, y, x1, y1))
        #print(tmp.load()[50,50])
        rgb=tmp.load()
        bin_im=np.zeros((self.background.winfo_height(),self.background.winfo_width()))
        for i in range(self.background.winfo_height()):
            for j in range(self.background.winfo_width()):
                bin_im[i][j]=1 if sum(rgb[j,i])>255 else 0
        #bin_im=im_filter(bin_im,10)
        data_ori=cv2.resize(bin_im,(14,14))
        #data_ori=im_filter(data_ori,2)
        data_ori=gaussian_blur(data_ori,2,1.4)
        #data_ori=im2bin(data_ori)
        plt.imshow(data_ori)
        data=np.reshape(data_ori,[-1])
        snw=SimpleNetWork()
        weights,bs=snw.load_network()
        pre=snw.predict(data,weights,bs)
        #print(pre,np.argmax(pre))
        print(np.argmax(pre))
        pass

def sigmoid(x,k=8,b=-0.5):
    return 2*(1/(1+np.exp(-(x/2)*k))+b)

def im_filter(im,filter_size):
    tmp=np.zeros((len(im)+filter_size*2,len(im[0])+filter_size*2))
    tmp[filter_size:len(im)+filter_size,filter_size:filter_size+len(im[0])]=im
    res=np.zeros_like(im)
    kernel_center=filter_size//2
    for i in range(len(tmp)-filter_size*2):
        for j in range(len(tmp[i])-filter_size*2):

            tmp_tmp=tmp[i+filter_size:i+filter_size*2,j+filter_size:j+filter_size*2]
            tmp_count=0
            for k in range(len(tmp_tmp)):
                for l in range(len(tmp_tmp[k])):
                    r=((k-kernel_center)**2+(l-kernel_center)**2)**0.5
                    tmp_count+=(tmp_tmp[k][l]*(1/(8**r)))/(filter_size)
                    
            res[i][j]=sigmoid(tmp_count)
            #print(res[i][j])
    return res

def im2bin(im):
    res=np.zeros_like(im)
    for i in range(len(res)):
        for j in range(len(res[i])):
            res[i][j]=1 if im[i][j]>0.5 else 0
    return res
        
Draw()