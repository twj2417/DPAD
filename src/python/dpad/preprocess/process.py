from ..data import Train_data,Carriage_data
from ..correction.actual2theory import Module_data
from ..auxiliary import hadd_by_row
import numpy as np
import rx

def get_effective_data(data)->List(Carriage_data):
    true_data = data[4001:].reshape(-1,4)
    complete_data = _rm_loss_data(true_data)
    return complete_data


def _rm_loss_data(data)->List(Carriage_data):
    index1 = np.where((data[:,0]==0)&(data[:,1]==0)&(data[:,2]==0)&
                    (data[:,3]==254))[0]-1
    index2 = np.where((data[:,0]==0)&(data[:,1]==0)&(data[:,2]==0)&
                    (data[:,3]==253))[0]
    data_without_head_and_tail = []
    for i in range(index1.size):
        data_without_head_and_tail.append(Carriage_data(data[index1[i]:index2,:]))
    return data_without_head_and_tail


def split_data_into_module(data,num_module)->List(Module_data):
    carriage_data = get_effective_data(data)
    module_data_list = []
    for module_id in range(num_module):
        module_data = (rx.Observable.from_(carriage_data)
                        .filter(lambda d:d.Carriage_id=module_id)
                        .map(lambda d:d.extract_effective_data()).to_list().to_blocking().first())
        module_data_list.append(Module_data(module_id,hadd_by_row(module_data)))
    return module_data