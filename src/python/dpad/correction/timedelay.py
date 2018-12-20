import scipy.io as sio
from jfs.api import File
from scipy.fftpack import fft,ifft
import numpy as np
import os
import h5py
from ..data import Single_event

def timedelay(event:Single_event)->Single_event:
    pass

T = 2**24
def load(filename):
    return sio.loadmat(filename)
def left_edge(data):
    return data[np.where(data[:,0]<=10),2]
def right_edge(data):
    return data[np.where(data[:,0]>90),2]
def cut(data,low_energy,high_energy):
    index = np.where(data[:,1]>low_energy)
    temp = data[index[0],]
    index1 = np.where(temp[:,1]<high_energy)
    result = temp[index1[0],]
    return result
def continous(data,cycle,constant,offset):
    temp = data[:,2]
    adjusted = np.array(temp)
    temp1 = data[:,2]+cycle
    for i in range(1,temp.size):
        if temp1[i]<temp[i-1]:
            offset = offset + constant
        if temp1[i-1]<temp[i]:
            offset = offset - constant    
        adjusted[i] = temp[i]+offset
    return adjusted
def preprocessing(data):
    start = []
    interval = []
    for i in range(0,16):
        index = np.where(data[:,3]==i)
        temp_data = data[index[0],]
        con_result = continous(temp_data,2**23,T,0)
        data[index[0],2] = con_result
        start.append(con_result[0])
        interval.append(round((con_result[con_result.size-1]-con_result[0])/(con_result.size-1)))
    start_shift = start - start[0]
    return start_shift,interval,data

    time=np.zeros((15,150),dtype=np.int64)
for i in range(0,150):
    path = "/home/twj2417/Desktop/pt3/16module_pt3_"+str(i+1)+"GainCorrectt.mat"
    if os.path.exists(path):
        print("file"+str(i+1)+" is running!")
        #data=load(path)['single_event_data']
        data = h5py.File(path,'r')['single_event_data'].value
        data = np.transpose(data)
        start,interval,new_data = preprocessing(data)
        new_data = cut(new_data,150,800)
        def get_time_data(new_data,block_id):
            return {block_id:np.array(right_edge(new_data[np.where(new_data[:,3]==block_id)])[0],dtype=np.int64), 
                block_id+1:np.array(left_edge(new_data[np.where(new_data[:,3]==(block_id+1))])[0],dtype=np.int64)} 
        def one_hot(xs, period):
            xs = np.array(xs, dtype=np.int64) % period
            result = np.zeros([2*period])
            for x in xs:
                result[x] += 1.0
            return result
        def fft_(xs):
            fft_result = fft(xs)
            return fft_result
        def delay3(evts,block_id,period):
            f0 = fft_(evts[block_id][::-1])
            f1 = fft_(evts[block_id+1])
            idx = np.argmax(ifft(f0*f1))+1
            if idx > period:
                idx = idx - 2*period
            return idx
        def interval(new_data,block_id,period):
            events = get_time_data(new_data,block_id)
            events_one_hot = {k: one_hot(v, period) for k, v in events.items()}
            infer_  = delay3(events_one_hot,block_id,period)
            return infer_    
        time[0,i] = interval(new_data,0,T)
        for j in range(1,15):
            drop = interval(new_data,j,T)
            time[j,i] =time[j-1,i]+drop