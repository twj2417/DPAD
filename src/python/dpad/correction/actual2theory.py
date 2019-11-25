from ..preprocess.base import Carriage_data
import numpy as np


class Single_event:
    def __init__(self,time,energy,blockid,crystalid):
        self.time = time
        self.energy = energy
        self.blockid = blockid
        self.crystalid = crystalid

    def sort_by_time(self):
        sort_index = np.argsort(self.time)
        return Single_event(self.time[sort_index],self.energy[sort_index],
                            self.blockid[sort_index],self.crystalid[sort_index])

    def update_time(self,time):
        return Single_event(time,self.energy,self.blockid,self.crystalid)

    def update_energy(self,energy):
        return Single_event(self.time,energy,self.blockid,self.crystalid)

    def filter_energy(self,energy_window):
        index = np.where((self.energy>energy_window[0])&(self.energy<energy_window[1]))[0]
        return Single_event(self.time[index],self.energy[index],self.blockid[index],self.crystalid[index])

    def smooth_event_time(self,num_module,const):
        smoothed_time = self.time
        # start = []
        for module_id in range(num_module):
            nb_module = np.where(self.blockid==module_id)[0]
            smoothed_module_time = get_smooth_time(self.time[nb_module],const)
            smoothed_time[nb_module] = smoothed_module_time
            # start.append(smoothed_module_time[0])
        # start_shift = np.array(start)-start[0] 
        return self.update_time(smoothed_time)

def get_smooth_time(data,const):
    result = np.array(data)
    comparison_data = data+const/2
    offset = 0
    for i in range(1,data.size):
        if comparison_data[i]<data[i-1]:
            offset = offset+const
        if comparison_data[i-1]<data[i]:
            offset = offset-const
        result[i] = data[i]+offset
    return result

def shift_start_time(time,block,shift,const):
    abnormal_block = np.where(np.abs(shift)>const/2)[0]
    for ab_block in abnormal_block:
        if shift[ab_block]<0:
            ab_index = np.where(block==ab_block)[0]
            time[ab_index] = time[ab_index] + const
            shift[ab_block] = shift[ab_block] + const
        else:
            ab_index = np.where(block==ab_block)[0]
            time[ab_index] = time[ab_index] - const
            shift[ab_block] = shift[ab_block] - const
    return time


class Module_data:
    def __init__(self,module_id,data=None):
        self.module_id = module_id
        self.data = data

    @property
    def time(self):
        return self.reshaped_data[:,4]+2**8*self.reshaped_data[:,5]+2**16*self.reshaped_data[:,6]
           
    @property
    def energy(self):
        return self.reshaped_data[:,0]+2**8*self.reshaped_data[:,1]

    @property
    def channel_id(self):
        return self.reshaped_data[:,2].astype(np.int64)

    @property
    def num_events(self):
        return self.reshaped_data.shape[0]
    
    @property
    def reshaped_data(self):
        return self.data.reshape(-1,8)

    def update_module_id(self,new_moduleid):
        return Module_data(new_moduleid,self.data)

    def update_crystal_id(self,relation_crystalid):
        reshape_data = np.array(self.reshaped_data)
        crystal_id = self.channel_id
        index = np.where((crystal_id>-1)&(crystal_id<100))[0]
        new_data = reshape_data[index,:]
        crystal_id = relation_crystalid[new_data[:,2].astype(np.int64)]-1 
        if self.module_id%2==0:
            crystal_id = relation_crystalid.size-crystal_id-1
        new_data[:,2] = crystal_id
        return Module_data(self.module_id,new_data.reshape(-1,4))

    def extract_effective_data(self):
        check_bit = self.data[:,3]
        d_value = check_bit[1:]+check_bit[:check_bit.size-1]
        index1 = np.where(d_value==284)[0]
        index2 = np.where(d_value==286)[0]+1
        index = np.hstack((index1,index2))
        effective_data = np.delete(self.data,index,0)
        if check_bit[0]==143:
            effective_data = effective_data[1:,:]
        return Module_data(self.module_id,effective_data)

    
        
# def add_data_from_carriage(module_data:Module_data,data:Carriage_data):
#     added_data = np.vstack(module_data.data,data.extract_effective_data())
#     return Module_data(module_data.module_id,added_data)


