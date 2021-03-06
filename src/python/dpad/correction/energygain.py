import numpy as np
from scipy.optimize import curve_fit
import scipy.io as sio
import os
import h5py
from .actual2theory import Module_data

def energygain(event:Module_data,energy_peak=None):
    corrected_energy_data = np.zeros_like(event.energy)
    energy_data = event.energy
    if energy_peak is not None:
        peak = energy_peak
    else:
        max_eng = int(np.max(energy_data))+1
        x,hist = histogram(energy_data,max_eng,(0,max_eng))
        index = np.argmax(hist[np.where((x>350)&(x<1000))[0]])
        peak = index+350
    corrected_energy_data = gain(energy_data,peak)
    return np.hstack((np.hstack((event.time.reshape(-1,1),corrected_energy_data.reshape(-1,1))),event.channel_id.reshape(-1,1))),peak

# def energygain(event:Module_data,num_channel):
#     for channel_id in range(num_channel):
#         corrected_energy_data = np.zeros_like(event.energy)
#         index = find_channel(event.channel_id,channel_id)
#         energy_data = event.energy[index]
#         if energy_data.size==0:
#             continue
#         x,hist = histogram(energy_data,2049,(0,2049))
#         popt,pcov = curve_fit(gaussian,x,hist,p0=[3,511,5,6,511,2,3,511,5,6,511,8],maxfev=5000000)
#         peak = max(popt[1],popt[4],popt[7],popt[10])
#         corrected_energy_data[index] = gain(energy_data,peak)
#     return np.hstack((np.hstack((event.time,corrected_energy_data)),event.channel_id))

def find_channel(data, channel):
    index_channel = np.where((data==channel))[0]
    return index_channel

def histogram(data,num_bin,range):
    hist,_ = np.histogram(data,bins=num_bin,range=range)
    return np.arange(num_bin),hist

def gaussian(x,*param):
    return (param[0]*np.exp(-np.power(((x - param[1])/param[2]), 2.))+
            param[3]*np.exp(-np.power(((x - param[4])/param[5]), 2.))+
            param[6]*np.exp(-np.power(((x - param[7])/param[8]), 2.))+
            param[9]*np.exp(-np.power(((x - param[10])/param[11]), 2.)))

def gain(energy,peak):
    energy = energy*511/peak
    return energy

