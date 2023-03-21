import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm

def data_file_map (index):
    num="%04d"%index
    data_path = np.loadtxt('C:\\Users\\domin\\OneDrive\\Desktop\\Dataset\\first_try_'+num+'_ToA.txt',dtype=float)
    data_reduced=np.sort(data_path[data_path != 0])
    data_diff=[]
    for i in range(len(data_reduced)-1):
        data_diff=np.append(data_diff,data_reduced[i+1]-data_reduced[i])

    return np.array(np.sort(data_diff[data_diff != 0.0])[:420])

def data_file_hist (index):
    num="%04d"%index
    data_path = np.loadtxt('C:\\Users\\domin\\OneDrive\\Desktop\\Dataset\\first_try_'+num+'_ToA.txt',dtype=float)
    data_reduced=np.sort(data_path[data_path != 0])
    data_diff=[]
    for i in range(len(data_reduced)-1):
        data_diff=np.append(data_diff,data_reduced[i+1]-data_reduced[i])

    return np.array(data_diff)

#data_map = []
data_hist = []
for i in tqdm (range(1000), desc = "Files analyzed: "):
    #data_map.append(data_file_map(i))
    data_hist.append(data_file_hist(i))


#plt.imshow(data_map, cmap='hot', vmin=np.min(data), vmax=np.max(data))
#plt.colorbar()
#plt.ylabel("Frame [0.1s]")
#plt.xlabel("Recorded Time Delay (min: "+str(np.min(data_map))+", max: "+str(np.max(data_map))+")")
data_flattened=np.hstack(data_hist)
plt.hist(data_flattened, bins='auto', range=(0.1,100.0))
plt.ylabel("Ct/bin")
plt.xlabel("Time bin [a.u]")
plt.show()