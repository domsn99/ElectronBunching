import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm
from matplotlib.widgets import Slider
import matplotlib.colors as colors
from matplotlib.widgets import RangeSlider

def data_ascii(path, name, type):
    data_path = np.loadtxt(path+name+type,skiprows=1, dtype="uint")
    return data_path
def data_raw(index, path, name, type):
    num="%04d"%index
    data_path = np.loadtxt(path+name+num+'_ToA'+type,dtype=float)
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

def analysis(mode, path, filename, setsize, type):

    logscale_min=0
    logscale_max=1

    if (mode==0):
        data_plot=data_raw(0, path, filename, type)
        fig = plt.imshow(data_plot, cmap="hot", norm=colors.SymLogNorm(linthresh=0.03, linscale=0.03,
                                              vmin=logscale_min, vmax=logscale_max, base=10))
        plt.colorbar()
        slider=Slider(ax=plt.axes([0.2, 0, 0.65, 0.03]), label="Data index", valmin=0, valmax=setsize-1, valinit=0, valstep=1)

        def update(index):
            data=data_raw(index, path, filename, type)
            fig.set_data(data)
        
        slider.on_changed(update)
    
    elif (mode == 1):
        data_map = []
        for i in tqdm (range(setsize), desc = "Files analyzed: "):
            data_map.append(data_file_map(i,path,filename, type)) 
        plt.imshow(data_map, cmap='hot', vmin=np.min(data_map), vmax=np.max(data_map))
        plt.colorbar()
        plt.ylabel("Frame [0.1s]")
        plt.xlabel("Recorded Time Delay (min: "+str(np.min(data_map))+" ns, max: "+str(np.max(data_map))+" ns)")
    
    elif (mode == 2):
        data_hist = []
        for i in tqdm (range(setsize), desc = "Files analyzed: "):
            data_hist.append(data_file_hist(i,path,filename, type))
        data_flattened=np.hstack(data_hist)
        plt.hist(data_flattened, bins='auto', range=(0.0,100.0))
        plt.ylabel("Ct/bin")
        plt.xlabel("Time bin ["+str(np.min(data_flattened[data_flattened != 0]))+" ns]")
    
    elif (mode == 3):
        data_clustered=data_raw(0,path,filename, type)
        data_clustered=cluster(data_clustered)
        fig = plt.imshow(data_clustered, cmap="hot", norm=colors.SymLogNorm(linthresh=0.03, linscale=0.03,
                                              vmin=logscale_min, vmax=logscale_max, base=10))
        plt.colorbar()
        slider=Slider(ax=plt.axes([0.2, 0, 0.65, 0.03]), label="Data index", valmin=0, valmax=setsize-1, valinit=0, valstep=1)

        def update(index):
            fig.set_data(cluster(data_raw(index, path, filename, type)))
        
        slider.on_changed(update)

    elif (mode == 4):
        data_histclust = []
        for i in tqdm (range(setsize), desc = "Files analyzed: "):
            data_histclust.append(data_file_hist_clust(i,path,filename, type))
        data_flattened=np.hstack(data_histclust)
        plt.hist(data_flattened, bins='auto', range=(0.0,100.0))
        plt.ylabel("Ct/bin")
        plt.xlabel("Time bin ["+str(np.min(data_flattened[data_flattened != 0]))+" ns]")

    elif (mode == 5):
        data_events=data_ascii(path,filename, type)
        print(data_events.shape)
        print(data_events)
        
        #slider = RangeSlider(ax=plt.axes([0.2, 0, 0.65, 0.03]), label="Data index")

    plt.show()