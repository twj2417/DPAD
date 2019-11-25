from ..io import load_data,is_file_normal
from ..preprocess.process import get_effective_data
from ..correction.process import module_correction,single_correction
from ..coincidence.process import coincidence_with_time_window
from ..auxiliary import hadd_by_row
from srfnef import nef_class
# from jfs.api import File
import fs
import pathlib
import numpy as np
import time
import srfnef as nef

@nef_class
class Config:
    num_file:int
    input_path:str
    relation_moduleid:str
    relation_crystalid:str
    period:float
    nb_period:float      
    energy_window:list
    time_window:float
    output_path:str

    @property
    def time_period(self):
        return 2**self.period

    @property
    def search_range(self):
        return self.time_period*self.nb_period
    
class DPAD():
    def __init__(self,task_config,scanner):
        self.task = self._make_task(task_config,scanner)

    def _make_task(self,config,scanner):
        if pathlib.Path('./energy_peak.npy').exists():
            energy_peak = np.load('./energy_peak.npy')
        else:
            energy_peak = None
        if pathlib.Path('./delay_time.npy').exists():
            # delay_time = None
            delay_time = np.load('./delay_time.npy')
        else:
            delay_time = None
        for i in range(config.num_file):           
            print(i)
            t1 = time.time()
            file_name = config.input_path+str(i)+'.dat'
            if pathlib.Path(file_name).exists() and pathlib.Path(file_name).is_file() and is_file_normal(file_name):
                coordinate = []
                input_data = np.fromfile(file_name,dtype = np.dtype('u1'))
                module_data = get_effective_data(input_data,scanner.nb_blocks_per_ring)
                corrected_module_data,energy_peak = module_correction(module_data,scanner.nb_blocks_per_ring,np.load(config.relation_moduleid),np.load(config.relation_crystalid),energy_peak)
                np.save('./energy_peak.npy',energy_peak)
                corrected_single_data,delay_time = single_correction(corrected_module_data,scanner.nb_blocks_per_ring,config.time_period,config.search_range,scanner.blocks.shape,delay_time)
                np.save(f'./delay_time.npy',delay_time)
                coincidence_data = coincidence_with_time_window(corrected_single_data,config.time_window,config.energy_window)
                coordinate.append(coincidence_data.get_coordinate(scanner))
                coordinate = hadd_by_row(coordinate)
                t2 = time.time()
                print(t2-t1)
                np.save(config.output_path+f'_{i}',coordinate)
                        