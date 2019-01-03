from .base import Carriage_data
from ..correction.actual2theory import Module_data
from ..auxiliary import hadd_by_row
from doufo import List
import numpy as np
import rx

def get_effective_data(data,num_module):
    true_data = data[4000:].reshape(-1,4)
    complete_data = _rm_loss_data(true_data)
    return _split_data_into_module(complete_data,num_module)


def _rm_loss_data(data):
    train_length = 276
    start1 = np.where((data[:,0]==0)&(data[:,1]==0)&(data[:,2]==0)&(data[:,3]==254))[0]+1
    len_each_train = start1[1:]-start1[:start1.size-1]
    index_complete_train = np.where(len_each_train==train_length)[0]
    complete_start_in_data = start1[index_complete_train]-1
    complete_data = np.zeros((index_complete_train.size*train_length,4))
    complete_start = np.arange(index_complete_train.size)*train_length
    for i in range(train_length):
        complete_data[complete_start+i,:] = data[complete_start_in_data+i,:]
    index1 = np.where(complete_data[:,3]==254)[0]    
    data_without_head = np.delete(complete_data,index1,0)
    index2 = np.where(data_without_head[:,3]==253)[0]
    return np.delete(data_without_head,index2,0)


def _split_data_into_module(data,num_module):
    line_end = np.where((data[:,0]==0)&(data[:,3]==240))[0]
    id_module = data[line_end,2]
    id_modules = np.tile(id_module.reshape(-1,1),(1,17)).reshape(-1,1)
    data = np.hstack((data,id_modules))
    module_data_list = []
    for module_id in range(num_module):
        index = np.where(data[:,4]==module_id)[0]
        whole_module_data = data[index,:4]
        index_240 = np.where(whole_module_data[:,3]==240)[0]
        module_data_without_tail = np.delete(whole_module_data,index_240,0)
        index_128 = np.where(module_data_without_tail[:,3]==128)[0]
        module_data_list.append(Module_data(module_id,np.delete(module_data_without_tail,index_128,0)))
    return module_data_list