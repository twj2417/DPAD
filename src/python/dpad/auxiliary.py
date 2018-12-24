import numpy as np
def hadd_by_row(data:list):
    hadd_data = data[0,:]
    for i in range(1,data.size):
        hadd_data = np.vstack((hadd_data,data[i]))
    return hadd_data