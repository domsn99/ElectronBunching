import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm
from functions import *

mode = 2
path="C:\\Users\\domin\\Desktop\\Dataset"
filename="first_try_"
setsize=1000

if (mode == 1):
    data_map = []
elif (mode == 2):
    data_hist = []

for i in tqdm (range(setsize), desc = "Files analyzed: "):
    if (mode == 1):
        data_map.append(data_file_map(i,path,filename))
    elif (mode == 2):
        data_hist.append(data_file_hist(i,path,filename))


if (mode == 1):
    plt.imshow(data_map, cmap='hot', vmin=np.min(data_map), vmax=np.max(data_map))
    plt.colorbar()
    plt.ylabel("Frame [0.1s]")
    plt.xlabel("Recorded Time Delay (min: "+str(np.min(data_map))+", max: "+str(np.max(data_map))+")")
elif (mode == 2):
    data_flattened=np.hstack(data_hist)
    plt.hist(data_flattened, bins='auto', range=(0.1,100.0))
    plt.ylabel("Ct/bin")
    plt.xlabel("Time bin [a.u]")
plt.show()