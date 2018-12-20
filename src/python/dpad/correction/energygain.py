import numpy as np
from scipy.optimize import curve_fit
import scipy.io as sio
import os
import h5py
from ..data import Single_event

def energygain(event:Single_event)->Single_event:
    pass

def find_channel(data,module,channel):
    index_channel = np.where((data[:,3]==module)&(data[:,0]==channel))[0]
    return index_channel

def histogram(data,num_bin,range):
    hist,_ = np.histogram(data,bins=num_bin,range=range)
    return np.arange(num_bin),hist

def gaussian(x,*param):
    return (param[0]*np.exp(-np.power(((x - param[1])/param[2]), 2.))+
            param[3]*np.exp(-np.power(((x - param[4])/param[5]), 2.))+
            param[6]*np.exp(-np.power(((x - param[7])/param[8]), 2.))+
            param[9]*np.exp(-np.power(((x - param[10])/param[11]), 2.)))

def gain(data,peak):
    data[:,1] = data[:,1]*511/peak
    return data

def correction(data):
    for i in range(0,1):
        for j in range(1,101):
            index = find_channel(data,i,j)
            channel_data = data[index,:]
            if channel_data.shape[0]==0:
                continue
            x,hist = histogram(channel_data[:,1],2049,(0,2049))
            popt,pcov = curve_fit(gaussian,x,hist,p0=[3,511,5,6,511,2,3,511,5,6,511,8],maxfev=5000000)
            peak = max(popt[1],popt[4],popt[7],popt[10])
            p = gain(channel_data,peak)
            data[index,:] = p
    return data

import datetime
start = datetime.datetime.now()
%matplotlib inline
for i in range(0,1):
    filename = f"/home/twj2417/Desktop/16module_flood_d12__{i+436}"
    if os.path.exists(filename+'.mat'):
        data=sio.loadmat(filename+'.mat')['single_event_data']
#         data = h5py.File(filename+'.mat','r')['single_event_data'].value
#         data = np.transpose(data)
        result = correction(data)
        #compare_data = h5py.File(filename+'GainCorrectt.mat','r')['single_event_data'].value
end = datetime.datetime.now()
print(end-start)