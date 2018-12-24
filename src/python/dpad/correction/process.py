from .energygrain import energygrain
from .timedelay import timedelay
from .actual2theroy import Module_data,Single_event
from ..auxiliary import hadd_by_row


def module_correction(data:List[Module_data],num_module,relation_moduleid,relation_crystalid)->Single_event:
    corrected_energy_data = []
    for module_id in range(num_module):
        energy_data = np.hstack(((energygain(data[module_id].extract_effective_data()
                            .update_module_id(relation_moduleid[module_id])
                            .update_crystal_id(relation_crystalid))),module_id*np.ones(data[module_id].shape[0],1)))
        corrected_energy_data.append(energy_data)
    corrected_energy_data = hadd_by_row(corrected_energy_data)
    return Single_event(corrected_energy_data[:,2],corrected_energy_data[:,1],
                                 corrected_energy_data[:,0],corrected_energy_data[:,3])                                          

def single_correction(data:Single_event,num_module,const,search_range,block_grid):
    smoothed_data = data.sort_by_time().smooth_event_time(num_module,const)
    delay_time = timedelay(smoothed_data,search_range,num_module,block_grid)
    time = smoothed_data.time
    for module_id in range(num_module):
        index = np.where(smoothed_data.blockid==module_id)[0]
        time[index] = time[index] - delay_time[module_id]
    return smoothed_data.update_time(time)