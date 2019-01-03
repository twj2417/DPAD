from ..io import load_data,is_file_normal
from ..preprocess.process import get_effective_data
from ..correction.process import module_correction,single_correction
from ..coincidence.process import coincidence_with_time_window
from srf.io.listmode import save_h5
from ..auxiliary import hadd_by_row
from doufo import dataclass
from jfs.api import File
import numpy as np
import time

@dataclass
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
        coordinate = []
        t1 = time.time()
        for i in range(config.num_file):
            print(i)
            file_name = config.input_path+str(i)+'.dat'
            if File(file_name).exists and is_file_normal(file_name):
                input_data = np.array(load_data(file_name))
                module_data = get_effective_data(input_data,scanner.nb_blocks_per_ring)
                corrected_module_data = module_correction(module_data,scanner.nb_blocks_per_ring,np.load(config.relation_moduleid),np.load(config.relation_crystalid))
                corrected_single_data = single_correction(corrected_module_data,scanner.nb_blocks_per_ring,config.time_period,config.search_range,scanner.blocks[0].grid)
                coincidence_data = coincidence_with_time_window(corrected_single_data,config.time_window)
                coordinate.append(coincidence_data.filter_with_energy_window(config.energy_window).get_coordinate(scanner))
        coordinate = hadd_by_row(coordinate)
        t2 = time.time()
        print(t2-t1)
        output = {'fst':coordinate[:,:3],'snd':coordinate[:,3:6],
                  'weight':np.ones_like(coordinate[:,0]),
                  'tof':np.ones_like(coordinate[:,0])}
        save_h5(config.output_path,output)
                        