import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm
from matplotlib.widgets import Slider

def data_raw(index, path, name):
    num="%04d"%index
    data_path = np.loadtxt(path+'\\'+name+num+'_ToA.txt',dtype=float)
    return data_path

def data_file_map (index, path, name):
    num="%04d"%index
    data_path = np.loadtxt(path+'\\'+name+num+'_ToA.txt',dtype=float)
    data_reduced=np.sort(data_path[data_path != 0])
    data_diff=[]
    for i in range(len(data_reduced)-1):
        data_diff=np.append(data_diff,data_reduced[i+1]-data_reduced[i])

    return np.array(np.sort(data_diff[data_diff != 0.0])[:420])

def data_file_hist (index, path, name):
    num="%04d"%index
    data_path = np.loadtxt(path+'\\'+name+num+'_ToA.txt',dtype=float)
    data_reduced=np.sort(data_path[data_path != 0])
    data_diff=[]
    for i in range(len(data_reduced)-1):
        data_diff=np.append(data_diff,data_reduced[i+1]-data_reduced[i])

    return np.array(data_diff)

def analysis(mode, path, filename, setsize):
    if (mode==0):
        data=data_raw(0, path, filename)
        fig = plt.imshow(data, cmap='hot', vmin=np.min(data), vmax=np.max(data))
        plt.colorbar()
        data_slider=Slider(ax=plt.axes([0.25, 0.1, 0.65, 0.03]), label="Data index", valmin=0, valmax=setsize-1, valinit=0, valstep=1)

        def data_update(index):
            fig.set_data(data_raw(index, path, filename))
        
        data_slider.on_changed(data_update)
    elif (mode == 1):
        data_map = []
        for i in tqdm (range(setsize), desc = "Files analyzed: "):
            data_map.append(data_file_map(i,path,filename)) 
        plt.imshow(data_map, cmap='hot', vmin=np.min(data_map), vmax=np.max(data_map))
        plt.colorbar()
        plt.ylabel("Frame [0.1s]")
        plt.xlabel("Recorded Time Delay (min: "+str(np.min(data_map))+" ns, max: "+str(np.max(data_map))+" ns)")
    elif (mode == 2):
        data_hist = []
        for i in tqdm (range(setsize), desc = "Files analyzed: "):
            data_hist.append(data_file_hist(i,path,filename))
        data_flattened=np.hstack(data_hist)
        plt.hist(data_flattened, bins='auto', range=(0.0,100.0), density=True)
        plt.ylabel("Normalized probability")
        plt.xlabel("Time bin ["+str(np.min(data_flattened[data_flattened != 0]))+" ns]")
    elif (mode == 3):
        data_clustered=[]
    plt.show()