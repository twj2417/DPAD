import numpy as np
def hadd_by_row(data:list):
    if len(data)>0:
        hadd_data = data[0]    
        for i in range(1,len(data)):
            hadd_data = np.vstack((hadd_data,data[i]))
    else:
        hadd_data = np.empty(1)
    return hadd_data