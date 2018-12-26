from .base import Carriage_data
from ..correction.actual2theory import Module_data
from ..auxiliary import hadd_by_row
from doufo import List
import numpy as np
import rx

def get_effective_data(data,num_module):
    true_data = data[4001:].reshape(-1,4)
    complete_data = _rm_loss_data(true_data)
    return split_data_into_module(complete_data,num_module)


def _rm_loss_data(data):
    index1 = np.where((data[:,0]==0)&(data[:,1]==0)&(data[:,2]==0)&
                    (data[:,3]==254))[0]+1
    index2 = np.where((data[:,0]==0)&(data[:,1]==0)&(data[:,2]==0)&
                    (data[:,3]==253))[0]-1
    if index2[0]<index1[0]:
        index2 = np.delete(index2,0)
    data_without_head_and_tail = []
    for i in range(index2.size):
        data_without_head_and_tail.append(Carriage_data(data[index1[i]:index2[i],:]))
    return data_without_head_and_tail


def split_data_into_module(data,num_module):
    module_data_list = []
    for module_id in range(num_module):
        module_data = (rx.Observable.from_(data)
                        .filter(lambda d:d.carriage_id==module_id)
                        .map(lambda d:d.extract_effective_data()).to_list().to_blocking().first())
        module_data_list.append(Module_data(module_id,hadd_by_row(module_data)))
    return module_data_list