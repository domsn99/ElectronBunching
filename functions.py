import os
import numpy as np
import matplotlib.pyplot as plt
from tkinter import filedialog
from tkinter import *

from tqdm import tqdm
from matplotlib.widgets import Slider
import matplotlib.colors as colors
from matplotlib.widgets import RangeSlider

data = []

def data_read(dir, typ):
    data_extracted = []
    for file in tqdm(os.listdir(dir), desc="Fortschritt"):
        if file.endswith(typ+".txt"):
            file_path=os.path.join(dir, file)
            data_extracted.append(np.loadtxt(file_path))
    return np.array(data_extracted)
#ToDo Programm auf tkinter anpassen
def data_ascii(path, name, type):
    data_path = np.loadtxt(path+name+type,skiprows=1, dtype="uint")
    return data_path
def data_file_map (index, path, name, type):
    num="%04d"%index
    data_path = np.loadtxt(path+name+num+'_ToA'+type,dtype=float)
    data_reduced=np.sort(data_path[data_path != 0])
    data_diff=[]
    for i in range(len(data_reduced)-1):
        data_diff=np.append(data_diff,data_reduced[i+1]-data_reduced[i])

    return np.array(np.sort(data_diff[data_diff != 0.0])[:420])
def data_file_hist (index, path, name, type):
    num="%04d"%index
    data_path = np.loadtxt(path+name+num+'_ToA'+type,dtype=float)
    data_reduced=np.sort(data_path[data_path != 0])
    data_diff=[]
    for i in range(len(data_reduced)-1):
        data_diff=np.append(data_diff,data_reduced[i+1]-data_reduced[i])
    return np.array(data_diff)
def data_file_hist_clust (index, path, name, type):
    num="%04d"%index
    data_path = cluster(np.loadtxt(path+name+num+'_ToA'+type,dtype=float))
    data_reduced=np.sort(data_path[data_path != 0])
    data_diff=[]
    for i in range(len(data_reduced)-1):
        data_diff=np.append(data_diff,data_reduced[i+1]-data_reduced[i])
    return np.array(data_diff)
def cluster(data):
    for i in range(data.shape[1]-1):
            for k in range(data.shape[0]-1):
                if (data[i][k]!=0.0 and (data[i][k+1]!=0.0 or data[i+1][k+1]!=0.0 or data[i+1][k]!=0.0 or data[i+1][k-1]!=0.0)):
                    pos_x=i
                    pos_y=k
                    min=data[pos_x][pos_y]
                    data,pos_x,pos_y,min=clustering(data, i, k, pos_x, pos_y, min)
                    data[pos_x][pos_y]=min
    return data
def clustering(data, i, k, min_x, min_y, min):
    delay=10000

    if (data[i][k] < data[min_x][min_y] and data[i][k]!=0.0):
        min=data[i][k]
        min_x=i
        min_y=k

    #if (data[i-1][k+1]!=0.0 and np.abs(data[i-1][k+1]-data[min_x][min_y])<=delay):
    #    data,min_x,min_y,min=clustering(data, i-1, k+1, min_x, min_y, min)

    if (data[i][k+1]!=0.0 and np.abs(data[i][k+1]-data[min_x][min_y])<=delay):
        data,min_x,min_y,min=clustering(data, i, k+1, min_x, min_y, min)

    if (data[i+1][k+1]!=0.0 and np.abs(data[i+1][k+1]-data[min_x][min_y])<=delay):
        data,min_x,min_y,min=clustering(data, i+1, k+1, min_x, min_y, min)

    if (data[i+1][k]!=0.0 and np.abs(data[i+1][k]-data[min_x][min_y])<=delay):
        data,min_x,min_y,min=clustering(data, i+1, k, min_x, min_y, min)

    if (data[i+1][k-1]!=0.0 and np.abs(data[i+1][k-1]-data[min_x][min_y])<=delay):
        data,min_x,min_y,min=clustering(data, i+1, k-1, min_x, min_y, min)
    
    #if (data[i][k-1]!=0.0 and np.abs(data[i][k-1]-data[min_x][min_y])<=delay):
    #    data,min_x,min_y,min=clustering(data, i-1, k, min_x, min_y, min)

    #if (data[i-1][k+1]!=0.0 and np.abs(data[i-1][k+1]-data[min_x][min_y])<=delay):
    #    data,min_x,min_y,min=clustering(data, i-1, k, min_x, min_y, min)

    data[i][k]=0.0
    return data,min_x,min_y,min

def analysis(dir, opt, typ, plot, fig, slider):
    fig.clear()
    slider.set(0)
    global data
    data=data_read(dir, typ)

    if(opt=="roher Datenplot"):
        map = fig.add_subplot(111)
        map.imshow(data[0])
        def plot_update(index):
            fig.clear()
            map = fig.add_subplot(111)
            map.imshow(data[int(index)])
            plot.draw()
        slider.configure(to=len(data)-1, command=plot_update)

    if(opt=="Geclusterter Datenplot"):
        fig.add_subplot(111).plot(np.sin(range(60)))
    
    plot.draw()

def data_length():
    return len(data)