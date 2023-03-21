import numpy as np

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