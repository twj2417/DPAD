import scipy.io as sio
from jfs.api import File
from scipy.fftpack import fft,ifft
import numpy as np
import os
import h5py
from ..data import Single_event

def timedelay(event:Single_event,T,num_module,block_grid)->Single_event:
    data = np.hstack((np.hstack((event.crystalid,event.energy)),np.hstack((event.time,event.blockid))))
    new_data = cut(data,150,800)
    time = np.zeros((num_module,1))
    time[1] = interval(new_data,0,T)
        for j in range(1,num_module):
            drop = interval(new_data,j,block_grid,T)
            time[j+1] =time[j]+drop
    return time

def left_edge(data,up):
    return data[np.where(data[:,0]<=up),2]
def right_edge(data,low):
    return data[np.where(data[:,0]>low),2]
def cut(data,low_energy,high_energy):
    index = np.where(data[:,1]>low_energy)
    temp = data[index[0],]
    index1 = np.where(temp[:,1]<high_energy)
    result = temp[index1[0],]
    return result
# def continous(data,cycle,constant,offset):
#     temp = data[:,2]
#     adjusted = np.array(temp)
#     temp1 = data[:,2]+cycle
#     for i in range(1,temp.size):
#         if temp1[i]<temp[i-1]:
#             offset = offset + constant
#         if temp1[i-1]<temp[i]:
#             offset = offset - constant    
#         adjusted[i] = temp[i]+offset
#     return adjusted
# def preprocessing(data,num_module,search_range):
#     start = []
#     interval = []
#     for i in range(num_module):
#         index = np.where(data[:,3]==i)
#         temp_data = data[index[0],]
#         con_result = continous(temp_data,2**23,search_range,0)
#         data[index[0],2] = con_result
#         start.append(con_result[0])
#         interval.append(round((con_result[con_result.size-1]-con_result[0])/(con_result.size-1)))
#     start_shift = start - start[0]
#     return start_shift,interval,data

def get_time_data(new_data,block_id,block_grid):
    up = block_grid[1]
    low = block_grid[1]*block_grid[2]-block_grid[1]
    return {block_id:np.array(right_edge(new_data[np.where(new_data[:,3]==block_id)],low)[0],dtype=np.int64), 
            block_id+1:np.array(left_edge(new_data[np.where(new_data[:,3]==(block_id+1))],up)[0],dtype=np.int64)} 

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

def interval(new_data,block_id,block_grid,period):
    events = get_time_data(new_data,block_id,block_grid)
    events_one_hot = {k: one_hot(v, period) for k, v in events.items()}
    infer_  = delay3(events_one_hot,block_id,period)
    return infer_
    